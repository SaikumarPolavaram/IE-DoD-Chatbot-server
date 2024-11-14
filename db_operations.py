# import mysql.connector
# from mysql.connector import Error
# from datetime import datetime
# from dotenv import load_dotenv
# import os

# load_dotenv()

# class DatabaseManager:
#     def __init__(self):
#         self.connection = None
#         self.connect()

#     def connect(self):
#         try:
#             self.connection = mysql.connector.connect(
#                 host=os.getenv('MYSQL_HOST'),
#                 user=os.getenv('MYSQL_USER'),
#                 password=os.getenv('MYSQL_PASSWORD'),
#                 database=os.getenv('MYSQL_DATABASE')
#             )
#             if self.connection.is_connected():
#                 print("Connected to MySQL database")
#         except Error as e:
#             print(f"Error connecting to MySQL database: {e}")

#     def close_connection(self):
#         if self.connection and self.connection.is_connected():
#             self.connection.close()
#             print("MySQL connection closed")

#     def save_chat_history(self, user_id, query, response):
#         try:
#             cursor = self.connection.cursor()
#             sql = """INSERT INTO chat_history (user_id, query, response, timestamp) 
#                      VALUES (%s, %s, %s, %s)"""
#             timestamp = datetime.now()
#             values = (user_id, query, response, timestamp)
#             cursor.execute(sql, values)
#             self.connection.commit()
#             cursor.close()
#             print("Chat history saved successfully")
#         except Error as e:
#             print(f"Error saving chat history: {e}")

#     def get_chat_history(self, user_id):
#         try:
#             cursor = self.connection.cursor(dictionary=True)
#             sql = """SELECT query, response, timestamp FROM chat_history 
#                      WHERE user_id = %s ORDER BY timestamp DESC"""
#             cursor.execute(sql, (user_id,))
#             history = cursor.fetchall()
#             cursor.close()
#             return history
#         except Error as e:
#             print(f"Error retrieving chat history: {e}")
#             return []

#     def update_faq_count(self, query):
#         try:
#             cursor = self.connection.cursor()
#             sql = """INSERT INTO faq_counts (query, count) 
#                      VALUES (%s, 1) 
#                      ON DUPLICATE KEY UPDATE count = count + 1"""
#             cursor.execute(sql, (query,))
#             self.connection.commit()
#             cursor.close()
#             print("FAQ count updated successfully")
#         except Error as e:
#             print(f"Error updating FAQ count: {e}")

#     def get_top_faqs(self, limit=10):
#         try:
#             cursor = self.connection.cursor(dictionary=True)
#             sql = """SELECT query, count FROM faq_counts 
#                      ORDER BY count DESC LIMIT %s"""
#             cursor.execute(sql, (limit,))
#             top_faqs = cursor.fetchall()
#             cursor.close()
#             return top_faqs
#         except Error as e:
#             print(f"Error retrieving top FAQs: {e}")
#             return []

#     @staticmethod
#     def create_tables(connection):
#         try:
#             cursor = connection.cursor()
            
#             # Create chat_history table
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS chat_history (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     user_id VARCHAR(255) NOT NULL,
#                     query TEXT NOT NULL,
#                     response TEXT NOT NULL,
#                     timestamp DATETIME NOT NULL
#                 )
#             """)
            
#             # Create faq_counts table
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS faq_counts (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     query VARCHAR(255) UNIQUE NOT NULL,
#                     count INT DEFAULT 1
#                 )
#             """)
            
#             connection.commit()
#             cursor.close()
#             print("Tables created successfully")
#         except Error as e:
#             print(f"Error creating tables: {e}")



#-------sql server

# from dotenv import load_dotenv
# import os
# import pyodbc
# import logging
# from datetime import datetime

# # Load environment variables
# load_dotenv()

# class DatabaseManager:
#     def __init__(self):
#         self.connection = None
#         self.connect()  # Call the connect method here

#     def connect(self):  # Ensure correct indentation level for connect method
#         try:
#             # Use Windows Authentication
#             self.connection = pyodbc.connect(
#                 f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#                 f"SERVER={os.getenv('SQL_SERVER_HOST')};"
#                 f"DATABASE={os.getenv('SQL_SERVER_DATABASE')};"
#                 f"Trusted_Connection=yes;"
#             )
#             if self.connection:
#                 print("Connected to SQL Server database using Windows Authentication")
#         except Exception as e:
#             print(f"Error connecting to SQL Server database: {e}")

#     # Optional: SQL Server Authentication
#     # def connect(self):
#     #     try:
#     #         self.connection = pyodbc.connect(
#     #             f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#     #             f"SERVER={os.getenv('SQL_SERVER_HOST')};"
#     #             f"DATABASE={os.getenv('SQL_SERVER_DATABASE')};"
#     #             f"UID={os.getenv('SQL_SERVER_USERNAME')};"
#     #             f"PWD={os.getenv('SQL_SERVER_PASSWORD')};"
#     #         )
#     #         if self.connection:
#     #             print("Connected to SQL Server database")
#     #     except Exception as e:
#     #         print(f"Error connecting to SQL Server database: {e}")

#     def close_connection(self):
#         if self.connection:
#             self.connection.close()
#             print("SQL Server connection closed")
 
#     # Rest of the code remains unchanged
#     def save_chat_history(self, user_id, query, response):
#         try:
#             cursor = self.connection.cursor()
#             sql = """INSERT INTO chat_history (user_id, query, response, timestamp)
#                      VALUES (?, ?, ?, ?)"""
#             timestamp = datetime.now()
#             values = (user_id, query, response, timestamp)
#             logging.info(f"Saving chat history: user_id={user_id}, query={query}, response={response[:50]}...")
#             cursor.execute(sql, values)
#             self.connection.commit()
#             cursor.close()
#             logging.info("Chat history saved successfully")
#         except Exception as e:
#             logging.error(f"Error saving chat history: {e}")
#             raise
 
#     def get_chat_history(self, user_id):
#         try:
#             cursor = self.connection.cursor()
#             print(user_id)
#             sql = """SELECT query,id, response, timestamp FROM chat_history
#                      WHERE user_id = ? ORDER BY timestamp DESC"""
#             cursor.execute(sql, (user_id,))
#             history = cursor.fetchall()
#             cursor.close()
#             print(history)
#             result = []
#             for row in history:
#                 result.append({
#                     'id': row.id,
#                     'query': row.query,
#                     'response': row.response,
#                     'timestamp': str(row.timestamp)
#                 })
#             return result
#         except Exception as e:
#             print(f"Error retrieving chat history: {e}")
#             return []
 
#     def update_faq_count(self, query,response,user_id):
#         try:
#             cursor = self.connection.cursor()
#             # Check if the query exists first
#             cursor.execute("SELECT count FROM faq_counts WHERE query = ?", (query,))
#             result = cursor.fetchone()
#             if result:
#                 # If query exists, update the count
#                 cursor.execute("UPDATE faq_counts SET count = count + 1, response = ?, timestamp = ? WHERE query = ?", (response, datetime.now(), query))
#             else:
#                 # If query does not exist, insert a new record
#                 timestamp = datetime.now()
#                 cursor.execute("INSERT INTO faq_counts (query, response,timestamp,user_id, count) VALUES (?,?,?,?, 1)", (query,response,timestamp,user_id))
#             self.connection.commit()
#             cursor.close()
#             logging.info("FAQ count updated successfully")
#         except Exception as e:
#             logging.error(f"Error updating FAQ count: {e}")
#             raise
 
#     def get_top_faqs(self,user_id):
#         try:
#             cursor = self.connection.cursor()
#             sql = """SELECT query,id,response,timestamp,count FROM faq_counts Where user_id = ?
#                      ORDER BY timestamp DESC """
#             cursor.execute(sql,(user_id,))
#             top_faqs = cursor.fetchall()
#             cursor.close()
#             # return top_faqs
#             result = []
#             for row in top_faqs:
#                 result.append({
#                     'id': row.id,
#                     'query': row.query,
#                     'count': row.count,
#                     'response': row.response,
#                     'timestamp': str(row.timestamp)
#                 })
#             return result
#         except Exception as e:
#             logging.error(f"Error retrieving top FAQs: {e}")
#             return []
#         except Exception as e:
#             print(f"Error retrieving top FAQs: {e}")
#             return []
#     def get_knowledge_graphs(self):
#         try:
#             cursor = self.connection.cursor()
#             sql = """SELECT * from knowledge_graphs"""
#             cursor.execute(sql)
#             top_faqs = cursor.fetchall()
#             cursor.close()
#             result = []
#             for row in top_faqs:
#                 result.append({
#                     'id': row.id,
#                     'title': row.title,
#                     'modifiedon': row.modifiedon,
#                     'createdon': row.createdon,
#                     'createdby': row.createdby,
#                     'modifiedby': row.modifiedby,
#                     'path'     : row.path,
#                     'description' : row.description
#                 })
#             return result
#         except Exception as e:
#             print(f"Error retrieving top FAQs: {e}")
#             return []
#     @staticmethod
#     def update_knowledge_graphs(connection):
#         try:
#             cursor = connection.cursor()
#             sql = """MERGE INTO knowledge_graphs AS target
#     USING (VALUES
#     ('About University of North Dakota', 'submitter2', GETUTCDate(), 'submitter2', GETUTCDate(), 'https://und.edu/',
#     'The University of North Dakota (UND), founded in 1883, is a public research university located in Grand Forks, North Dakota. It is the state''s oldest and largest university, known for its strong programs in aerospace, engineering, health sciences, and law. UND is home to one of the nation''s best aviation schools and also offers a wide range of undergraduate, graduate, and professional programs'),
#     ('UND Academics', 'submitter1', GETUTCDate(), 'submitter3', GETUTCDate(), 'https://und.edu/academics/index.html',
#     'The University of North Dakota (UND) offers a wide range of academic programs, including over 225 fields of study, with strong programs in aviation, engineering, health sciences, business, and law'),
#     ('UND Admissions', 'submitter3', GETUTCDate(), 'submitter3', GETUTCDate(), 'https://und.edu/admissions/index.html',
#     'The University of North Dakota (UND) offers a straightforward admissions process, welcoming applicants with a range of undergraduate, graduate, and online programs, along with resources to support a successful application'),
#     ('UND Student-life', 'submitter5', GETUTCDate(), 'submitter5', GETUTCDate(), 'https://und.edu/student-life/index.html',
#     'The University of North Dakota (UND) offers a vibrant student life with over 250 student organizations, on-campus housing, recreational activities, and a strong sense of community to enhance the overall college experience'),
#     ('UND Research', 'submitter7', GETUTCDate(), 'submitter5', GETUTCDate(), 'https://und.edu/research/index.html',
#     'The University of North Dakota (UND) is a leader in research, focusing on areas like aerospace, energy, health sciences, and unmanned systems, with state-of-the-art facilities and innovative projects'),
#     ('UND Athletics', 'submitter8', GETUTCDate(), 'submitter7', GETUTCDate(), 'https://fightinghawks.com/',
#     'The University of North Dakota (UND) Athletics offers competitive NCAA Division I programs, excelling in ice hockey, basketball, football, and more, fostering school spirit and athletic excellence')
#     ) AS source (title, createdby, createdon, modifiedby, modifiedon, path, description)
#    ON target.title = source.title
#  WHEN MATCHED THEN
#     UPDATE SET
#         modifiedon = source.modifiedon,
#         createdon = source.createdon
#  WHEN NOT MATCHED THEN
#     INSERT (title, createdby, createdon, modifiedby, modifiedon, path, description)
#     VALUES (source.title, source.createdby, source.createdon, source.modifiedby, source.modifiedon, source.path, source.description);"""
#             cursor.execute(sql)
#             connection.commit()
#             cursor.close()
#             print("knowledge graph updated successfully")
#         except Exception as e:
#             print(f"Error updating FAQ count: {e}")
#     @staticmethod
#     def create_tables(connection):
#         try:
#             cursor = connection.cursor()
#             # Create chat_history table
#             cursor.execute("""
#                 IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='chat_history' AND xtype='U')
#                 CREATE TABLE chat_history (
#                     id INT IDENTITY(1,1) PRIMARY KEY,
#                     user_id NVARCHAR(255) NOT NULL,
#                     query NVARCHAR(MAX) NOT NULL,
#                     response NVARCHAR(MAX) NOT NULL,
#                     timestamp DATETIME NOT NULL
#                 )
#             """)
#             # Create faq_counts table
#             cursor.execute("""
#                 IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='faq_counts' AND xtype='U')
#                 CREATE TABLE faq_counts (
#                     id INT IDENTITY(1,1) PRIMARY KEY,
#                     user_id NVARCHAR(255) NOT NULL,
#                     query NVARCHAR(255) UNIQUE NOT NULL,
#                     response NVARCHAR(MAX) NOT NULL,
#                     timestamp DATETIME NOT NULL,
#                     count INT DEFAULT 1
#                 )
#             """)
 
#             # Create knowledge graph
#             cursor.execute("""
#                 IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='knowledge_graphs' AND xtype='U')
#                 CREATE TABLE knowledge_graphs (
#                     id INT IDENTITY(1,1) PRIMARY KEY,
#                     title NVARCHAR(700) UNIQUE NOT NULL,
#                     createdby nvarchar(36),
#                     createdon datetime,
#                     modifiedby nvarchar(36),
#                     modifiedon datetime,
#                     path NVARCHAR(700) UNIQUE NOT NULL,
#                     description NVARCHAR(700) UNIQUE NOT NULL
#                 )
#             """)
#             connection.commit()
#             cursor.close()
#             print("Tables created successfully")
#         except Exception as e:
#             print(f"Error creating tables: {e}")



#--------updated sql server -------
from dotenv import load_dotenv
import os
import pyodbc
import logging
from datetime import datetime
from uuid import uuid4

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    # def connect(self):  # Ensure correct indentation level for connect method
    #     try:
    #         # Use Windows Authentication
    #         self.connection = pyodbc.connect(
    #             f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    #             f"SERVER={os.getenv('SQL_SERVER_HOST')};"
    #             f"DATABASE={os.getenv('SQL_SERVER_DATABASE')};"
    #             f"Trusted_Connection=yes;"
    #         )
    #         if self.connection:
    #             print("Connected to SQL Server database using Windows Authentication")
    #     except Exception as e:
    #         print(f"Error connecting to SQL Server database: {e}")

    # Optional: SQL Server Authentication
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={os.getenv('SQL_SERVER_HOST')};"
                f"DATABASE={os.getenv('SQL_SERVER_DATABASE')};"
                f"UID={os.getenv('SQL_SERVER_USERNAME')};"
                f"PWD={os.getenv('SQL_SERVER_PASSWORD')};"
            )
            if self.connection:
                print("Connected to SQL Server database")
        except Exception as e:
            print(f"Error connecting to SQL Server database: {e}")


    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("SQL Server connection closed")

    def create_user(self, first_name, last_name, role, username, email, hashed_password, created_by):
        try:
            user_id = str(uuid4())
            cursor = self.connection.cursor()
            sql = """
                INSERT INTO users (user_id, first_name, last_name, role, username, email, password, created_at, created_by, modified_by, modified_on)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (user_id, first_name, last_name, role, username, email, hashed_password, datetime.now(), created_by, None, None)
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def check_user(self, username):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT user_id, user_email, user_name, role, createdby, createdon, password FROM userprofilelist 
                     WHERE user_email = ?"""
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    def save_chat_history(self, user_id, query, response,role,email):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO chat_history (user_id, query, response, timestamp,role,email)
                     VALUES (?, ?, ?, ?,?,?)"""
            timestamp = datetime.now()
            values = (user_id, query, response, timestamp,role,email)
            logging.info(f"Saving chat history: user_id={user_id}, query={query}, response={response[:50]}...")
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
            logging.info("Chat history saved successfully")
        except Exception as e:
            logging.error(f"Error saving chat history: {e}")
            raise

    def get_chat_history(self, user_id):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT id,query, response, timestamp,role,email FROM chat_history
                     WHERE user_id = ? ORDER BY timestamp DESC""" 
            cursor.execute(sql, (user_id,))
            history = cursor.fetchall()
            cursor.close()
            result = []
            for row in history:
                result.append({
                    'id': row.id,
                    'query': row.query,
                    'role'      : row.role,
                    'email'      : row.email,
                    'response': row.response,
                    'timestamp': str(row.timestamp) 
                })
            return result
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return []

    def update_faq_count(self, query,response,user_id,role,email):
        try:
            cursor = self.connection.cursor()
            # Check if the query exists first
            cursor.execute("SELECT count FROM faq_counts WHERE query = ? and user_id = ?", (query,user_id))
            result = cursor.fetchone()
            if result:
                # If query exists, update the count
                cursor.execute("UPDATE faq_counts SET count = count + 1, response = ?, timestamp = ?,role = ?,email = ? WHERE query = ?", (response, datetime.now(), role,email, query))
            else:
                # If query does not exist, insert a new record
                timestamp = datetime.now() 
                cursor.execute("INSERT INTO faq_counts (query, response,timestamp,user_id,role,email, count) VALUES (?,?,?,?,?,?, 1)", (query,response,timestamp,user_id,role,email))
            self.connection.commit()
            cursor.close()
            logging.info("FAQ count updated successfully")
        except Exception as e:
            logging.error(f"Error updating FAQ count: {e}")
            raise
    def get_top_faqs(self,user_id):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT id,query,response,timestamp,role,email,count FROM faq_counts Where user_id = ?
                     ORDER BY timestamp DESC """
            cursor.execute(sql,(user_id,))
            top_faqs = cursor.fetchall()
            cursor.close()
            # return top_faqs
            result = []
            for row in top_faqs:
                result.append({
                    'id': row.id,
                    'query': row.query,
                    'count': row.count,
                    'role'      : row.role,
                    'email'      : row.email,
                    'response': row.response,
                    'timestamp': str(row.timestamp)
                })
            return result
        except Exception as e:
            logging.error(f"Error retrieving top FAQs: {e}")
            return []

    def get_knowledge_graphs(self):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT * from knowledge_graphs"""
            cursor.execute(sql)
            top_faqs = cursor.fetchall()
            cursor.close()
            result = []
            for row in top_faqs:
                result.append({
                    'id': row.id,
                    'title': row.title,
                    'modifiedon': row.modifiedon,
                    'createdon': row.createdon,
                    'createdby': row.createdby,
                    'role'      : row.role,
                    'modifiedby': row.modifiedby,
                    'path'     : row.path,
                    'description' : row.description
                })
            return result
        except Exception as e:
            print(f"Error retrieving top FAQs: {e}")
            return []
    def get_userprofile_list(self):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT * from userprofilelist"""
            cursor.execute(sql)
            top_faqs = cursor.fetchall()
            cursor.close()
            result = []
            for row in top_faqs:
                result.append({
                    'id': row.id,
                    'user_id': row.user_id,
                    'user_name': row.user_name,
                    'user_email': row.user_email,
                    'first_name': row.first_name,
                    'last_name' : row.last_name,
                    'role'      : row.role,
                    'modifiedon': row.modifiedon,
                    'createdon': row.createdon,
                    'createdby': row.createdby,
                    'modifiedby': row.modifiedby
                })
            return result
        except Exception as e:
            print(f"Error retrieving top FAQs: {e}")
            return []

    @staticmethod
    def update_knowledge_graphs(connection):
        try:
            cursor = connection.cursor()
            sql = """MERGE INTO knowledge_graphs AS target
    USING (VALUES 
    ('About University of North Dakota', 'submitter2','Public', GETUTCDate(), 'submitter2', GETUTCDate(), 'https://und.edu/', 
    'The University of North Dakota (UND), founded in 1883, is a public research university located in Grand Forks, North Dakota. It is the state''s oldest and largest university, known for its strong programs in aerospace, engineering, health sciences, and law. UND is home to one of the nation''s best aviation schools and also offers a wide range of undergraduate, graduate, and professional programs'),
    ('UND Academics', 'submitter1','Public', GETUTCDate(), 'submitter3', GETUTCDate(), 'https://und.edu/academics/index.html', 
    'The University of North Dakota (UND) offers a wide range of academic programs, including over 225 fields of study, with strong programs in aviation, engineering, health sciences, business, and law'),
    ('UND Admissions', 'submitter3','Public', GETUTCDate(), 'submitter3', GETUTCDate(), 'https://und.edu/admissions/index.html', 
    'The University of North Dakota (UND) offers a straightforward admissions process, welcoming applicants with a range of undergraduate, graduate, and online programs, along with resources to support a successful application'),
    ('UND Student-life', 'submitter5','Public', GETUTCDate(), 'submitter5', GETUTCDate(), 'https://und.edu/student-life/index.html', 
    'The University of North Dakota (UND) offers a vibrant student life with over 250 student organizations, on-campus housing, recreational activities, and a strong sense of community to enhance the overall college experience'),
    ('UND Research', 'submitter7','Public', GETUTCDate(), 'submitter5', GETUTCDate(), 'https://und.edu/research/index.html', 
    'The University of North Dakota (UND) is a leader in research, focusing on areas like aerospace, energy, health sciences, and unmanned systems, with state-of-the-art facilities and innovative projects'),
    ('UND Athletics', 'submitter8','Public', GETUTCDate(), 'submitter7', GETUTCDate(), 'https://fightinghawks.com/', 
    'The University of North Dakota (UND) Athletics offers competitive NCAA Division I programs, excelling in ice hockey, basketball, football, and more, fostering school spirit and athletic excellence')
    ) AS source (title, createdby,role, createdon, modifiedby, modifiedon, path, description)
   ON target.title = source.title
 WHEN MATCHED THEN 
    UPDATE SET 
        modifiedon = source.modifiedon,
        createdon = source.createdon
 WHEN NOT MATCHED THEN
    INSERT (title, createdby,role, createdon, modifiedby, modifiedon, path, description)
    VALUES (source.title, source.createdby,source.role, source.createdon, source.modifiedby, source.modifiedon, source.path, source.description);"""
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            print("knowledge graph updated successfully")
        except Exception as e:
            print(f"Error updating FAQ count: {e}")        
            print(f"Error updating FAQ count: {e}")
      
    @staticmethod
    def userproflie_list(connection):
        try:
            cursor = connection.cursor()
            sql = """MERGE INTO userprofilelist AS target
        USING (VALUES 
            ('submitter1', 'submitter1@ideaentity.com', 'Submitter', '1', 'public', 'submitter2', GETUTCDATE(), 'submitter2', GETUTCDATE(),'Entity@123'),
            ('submitter2', 'submitter2@ideaentity.com', 'Submitter', '2', 'individual', 'submitter2', GETUTCDATE(), 'submitter2', GETUTCDATE(),'Entity@123'),
            ('submitter3', 'submitter3@ideaentity.com', 'Submitter', '3', 'private', 'submitter2', GETUTCDATE(), 'submitter2', GETUTCDATE(),'Entity@123')
        ) AS source (user_name, user_email, first_name, last_name, role, createdby, createdon, modifiedby, modifiedon,password)
        ON target.user_name = source.user_name
    WHEN MATCHED THEN 
            UPDATE SET 
                modifiedon = source.modifiedon,
                createdon = source.createdon
    WHEN NOT MATCHED THEN
            INSERT (user_id, user_name, user_email, first_name, last_name, role, createdby, createdon, modifiedby, modifiedon,password)
            VALUES (NEWID(), source.user_name, source.user_email, source.first_name, source.last_name, source.role, source.createdby, source.createdon, source.modifiedby, source.modifiedon,source.password);"""
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            print("userprofilelist updated successfully")
        except Exception as e:
            print(f"Error updating FAQ count: {e}")
    @staticmethod
    def create_tables(connection):
        try:
            cursor = connection.cursor()
            # Create chat_history table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='chat_history' AND xtype='U')
                CREATE TABLE chat_history (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id NVARCHAR(255) NOT NULL,
                    role NVARCHAR(36),
                    email NVARCHAR(MAX) NOT NULL,
                    query NVARCHAR(MAX) NOT NULL,
                    response NVARCHAR(MAX) NOT NULL,
                    timestamp DATETIME NOT NULL
                )
            """)
            # Create faq_counts table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='faq_counts' AND xtype='U')
                CREATE TABLE faq_counts (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id NVARCHAR(255) NOT NULL,
                    role NVARCHAR(36),
                    email NVARCHAR(MAX) NOT NULL,
                    query NVARCHAR(255) NOT NULL,
                    response NVARCHAR(MAX) NOT NULL,
                    count INT DEFAULT 1,
                    timestamp DATETIME NOT NULL
                )
            """)
            # Create users table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
                CREATE TABLE users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id NVARCHAR(255) NOT NULL,
                    first_name NVARCHAR(50) NOT NULL,
                    last_name NVARCHAR(50) NOT NULL,
                    username NVARCHAR(100) NOT NULL,
                    email NVARCHAR(100) UNIQUE NOT NULL,
                    role NVARCHAR(20) NOT NULL,
                    password NVARCHAR(255) NOT NULL,
                    created_at DATETIME NOT NULL,
                    created_by NVARCHAR(255),
                    modified_by NVARCHAR(255),
                    modified_on DATETIME
                )
            """)
            # Create knowledge_graphs table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='knowledge_graphs' AND xtype='U')
                CREATE TABLE knowledge_graphs (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    title NVARCHAR(700) UNIQUE NOT NULL,
                    createdby NVARCHAR(36),
                    role NVARCHAR(36),
                    createdon DATETIME,
                    modifiedby NVARCHAR(36),
                    modifiedon DATETIME,
                    path NVARCHAR(2000),
                    description NVARCHAR(MAX)
                )
            """)
            # create userprofilelist
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='userprofilelist' AND xtype='U')
              CREATE TABLE userprofilelist (
                 id INT IDENTITY(1,1) PRIMARY KEY,
                 user_id NVARCHAR(700) NOT NULL,       
                 user_name NVARCHAR(700) UNIQUE NOT NULL,
                 user_email NVARCHAR(700) UNIQUE NOT NULL,
                 first_name NVARCHAR(700) NOT NULL,
                 last_name NVARCHAR(700) NOT NULL, 
                 password NVARCHAR(700) NOT NULL,
                 role NVARCHAR(36),      
                 createdby NVARCHAR(36),
                 createdon DATETIME,
                 modifiedby NVARCHAR(36),
                 modifiedon DATETIME
            )
            """)
            connection.commit()
            cursor.close()
            print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")

# obj = DatabaseManager()
# obj.close_connection()
# obj.create_tables(obj.connection)