from flask import Flask, request, jsonify
from flask_cors import CORS
import markdown2  # Library for converting markdown to HTML
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from main import setup


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=int(os.getenv('TOKEN_EXPIRE_IN_DAYS')))
jwt = JWTManager(app)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Initialize query handler, responder, memory context, and database manager
public_query_handler, private_query_handler, individual_query_handler, responder, memory, db_manager = setup()


@app.route('/signin', methods=['POST'])
def signin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db_manager.check_user(username)

    if user and user[-1] == password:
        additional_claims = {
            "user_id": user[0], 
            "user_name": user[2],
            "role": user[3], 
            "createdby": user[4], 
            "createdon": user[5]
        }
        access_token = create_access_token(username, additional_claims=additional_claims)
        return jsonify({'access_token': access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "public")
    created_by = data.get("created_by", None)

    if not (first_name and last_name and username and email and password):
        return jsonify({"message": "Missing required fields"}), 400
    
    hashed_password = generate_password_hash(password)
    user = db_manager.create_user(first_name, last_name, role, username, email, hashed_password, created_by)    
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({"message": "User created successfully"}), 201


@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        claims = get_jwt()
        data = request.get_json()
        query = data.get('query', '').lower()
        user_id = claims.get('user_id')  # Get user_id from request, default to 'anonymous'
        role = claims.get('role', '')
        email = claims.get('sub', '')

        if query.lower() == 'quit':
            return jsonify({"error": "Session ended"}), 400

        # Get the previous interaction context
        memory_context = memory.get_context()

        # Restrict access based on role
        if role == 'public':
            context = public_query_handler.handle(query, role, memory)
        elif role == 'private':
            context = private_query_handler.handle(query, role, memory)
        elif role == 'individual':
            context = individual_query_handler.handle(query, role, memory)
        else:
            return jsonify({'message': 'Invalid role or access denied'}), 403

        # Check for restricted content in the response
        if any(term in context.lower() for term in ['no information', 'no mention', "can't access", 'not available', "doesn't exist", 'not provided', 'no specific information', 'unrelated']):
            return jsonify({'msg': 'Access Denied'}), 403

        # Prepare full context and get the answer
        full_context = f"{memory_context}\n\n{context}"
        answer = responder.respond(query, full_context, memory)

        # Convert the answer from Markdown to HTML
        formatted_answer = markdown2.markdown(answer, extras=["tables"])

        # Save the conversation history in memory and database
        if "technical difficulties" not in answer and "unable to provide an answer" not in answer:
            memory.add(query, answer)
            memory.set_current_context(f"{query} - {answer[:100]}...")  # Update memory context

            # Save chat history and update FAQ count in database
            db_manager.save_chat_history(user_id, query, formatted_answer, role, email)
            db_manager.update_faq_count(query, formatted_answer, user_id, role, email)

        # Send the HTML response
        return jsonify({"answer": formatted_answer}), 200
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500


@app.route('/token_details', methods=['GET'])
@jwt_required()
def get_token_details():
    claims = get_jwt()
    response = {
        "user_id": claims.get('user_id'),
        "email": claims.get('sub'),
        "role": claims.get('role'),
        "username": claims.get('user_name')
    }
    return jsonify({"message": response}), 200


@app.route('/chat_history', methods=['GET'])
@jwt_required()
def get_chat_history():
    claims = get_jwt()
    user_id = claims.get('user_id', 'anonymous')
    history = db_manager.get_chat_history(user_id)
    return jsonify({"history": history}), 200


@app.route('/top_faqs', methods=['GET'])
@jwt_required()
def get_top_faqs():
    claims = get_jwt()
    user_id = claims.get('user_id', 'anonymous')
    top_faqs = db_manager.get_top_faqs(user_id)
    return jsonify({"top_faqs": top_faqs}), 200


@app.route('/knowledge_graphs', methods=['GET'])
@jwt_required()
def get_knowledge_graphs():
    top_faqs = db_manager.get_knowledge_graphs()
    return jsonify({"top_faqs": top_faqs}), 200


@app.route('/userprofile_list', methods=['GET'])
@jwt_required()
def get_userprofile_list():
    data = db_manager.get_userprofile_list()
    return jsonify({"data": data}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=True)
