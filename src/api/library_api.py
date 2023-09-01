from inspect import Attribute
from flask_restful import Resource, reqparse, request  
from db.swen344_db_utils import *
from requests import request
import hashlib
import secrets

class user(Resource):
    def get(self):  
        """
            GET all users within the user_table 
        """
      
        sql = """
            SELECT * FROM user_table
        """
        
        return "GET sucessful User data retrieved: " + str(exec_get_all(sql))
    

    def post(self): 
        """
            POST all users within the user_table 
        """
        #parse request body
        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('user_password', type=str)
        args = parser.parse_args()
        #store post request body
        p_num = args['phone_number']
        email = args['email']
        f_name = args['firstname']
        l_name = args['lastname']
        u_name = args['username']
        u_password = args['user_password']
       
        #Check if user exist
        #check_status="SELECT * FROM user_table WHERE user_table.username = %s " % (u_name)
        check_status="""
        SELECT CASE
         WHEN NOT EXISTS (SELECT * FROM user_table WHERE user_table.username = '%s') 
         THEN 1
         ELSE 2
        END 
        """% (u_name)
        #SELECT * FROM user_table WHERE user_table.username = %s 
        
        status = exec_get_all(check_status)
        if(int(status[0][0]) ==  2):
            return "POST unsucessful new user not created"
        
        #create a hash version of the password
        hashed_password = self.hashingAlgo(str(u_password))
        print(u_password)
        print(u_name)
        print(hashed_password)
        #place into SQL database
        sql = """
            INSERT INTO user_table(phone_number,email,firstname,lastname,username,user_password,session_key) 
            VALUES ('%s','%s', '%s', '%s','%s','%s','%d')
        """ % (p_num,email,f_name,l_name,u_name,hashed_password,0)
        
        exec_commit(sql)
        
        return "POST sucessful new user created"
    
    def hashingAlgo(self,str):
        result = hashlib.sha512(str.encode())
        return result.hexdigest()
        
class userDelete(Resource): 
    """
        DELETE users within the user_table 
    """
    def delete(self,username,session_key):
       
        #Check if user can be deleted
        Authenticate_user="""
        SELECT CASE
            WHEN NOT EXISTS (SELECT * FROM user_table WHERE user_table.username = '%s' AND user_table.session_key = '%s' ) 
            THEN 1
            ELSE 2
        END 
        """% (username,session_key)
        status = exec_get_all(Authenticate_user)
        if(int(status[0][0]) ==  1):
            return "DELETE unsucessful user deletion failed"
        
        delete_user = """
            DELETE FROM user_table WHERE user_table.username = '%s';
        """% (username)
        
        exec_commit(delete_user)
        
        
        return "DELETE sucessful user deletion succeed"
class userLogin(Resource): 
     
    def post(self): 
        """
           Login user within the user_table 
        """
        u = user()
        #send a POST request to your login endpoint with a username and password 
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        user_name = args['username']
        pass_word = args['password']

        #retrieve a hash version of the password
        hashed_password = u.hashingAlgo(str(pass_word))
   
        #check if user can login 
        Authenticate_user="""
        SELECT CASE
            WHEN NOT EXISTS (SELECT * FROM user_table WHERE user_table.username = '%s' AND user_table.user_password = '%s' ) 
            THEN 1
            ELSE 2
        END 
        """% (str(user_name),str(hashed_password))
        status = exec_get_all(Authenticate_user)
        
        if(int(status[0][0]) ==  1):
            return "POST unsucessful login failed"
        
        #create session key 
        session_key = secrets.token_hex(16)

        #input the session key
        update_sql = """
        UPDATE user_table
        SET session_key = '%s'
        WHERE username = '%s';
        """ % (str(session_key),str(user_name))
        exec_commit(update_sql)
        return "POST sucessful login succeed"
        
class userLogout(Resource):   
    def post(self): 
        """
           Logout user within the user_table 
        """
        u = user()
        #send a POST request to your login endpoint with a username and password 
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        user_name = args['username']
        pass_word = args['password']

        #retrieve a hash version of the password
        hashed_password = u.hashingAlgo(str(pass_word))
        print(user_name)
        print(hashed_password)
        
        #check if user can login 
        Authenticate_user="""
        SELECT CASE
            WHEN NOT EXISTS (SELECT * FROM user_table WHERE user_table.username = '%s' AND user_table.user_password = '%s' ) 
            THEN 1
            ELSE 2
        END 
        """% (str(user_name),str(hashed_password))
        status = exec_get_all(Authenticate_user)
        
        if(int(status[0][0]) ==  2):
            return "false"
        
        #input the session key
        update_sql = """
        UPDATE user_table
        SET user_table.session_key = 0
        WHERE user_table.username = '%s';
        """ % (user_name)
        exec_commit(update_sql)
        
        return "true"      
class userUpdate(Resource):   
    def put(self): 
        """
           UPDATE user within the user_table 
        """
        #send a POST request to your login endpoint with a username and password 
        parser = reqparse.RequestParser()
        parser.add_argument('column', type=str)
        parser.add_argument('value', type=str)
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        column = args['column']
        value = args['value']
        user_name = args['username']
        
        print(user_name)
        #check if user can login 
        Authenticate_user="""
        SELECT CASE
            WHEN NOT EXISTS (SELECT * FROM user_table WHERE user_table.username = '%s'  ) 
            THEN 1
            ELSE 2
        END 
        """% (str(user_name))
        status = exec_get_all(Authenticate_user)
        
        if(int(status[0][0]) ==  1):
            return "PUT unsucessful user edit failed"

        #input the session key
        update_sql = """
        UPDATE user_table
        SET %s = '%s'
        WHERE username = '%s';
        """ % (column,value,user_name)
        exec_commit(update_sql)
        return "PUT sucessful user edit succeed"

class inventory(Resource):
    def get(self):
        """
            GET all books within the inventory_table
        """   
        sql = """
            SELECT * FROM inventory_table
        """
        return "GET sucessful inventory data retrieved: " + str(exec_get_all(sql))
    
class inventoryAttribute(Resource):
    """
        GET select books within the inventory_table
    """   
    def get(self,attribute,username):   
        sql = """
            SELECT * FROM inventory_table WHERE inventory_table.%s = '%s'
        """% (attribute,username)
        return exec_get_all(sql)
    
class checkOutBook(Resource):
    def put(self): 
        """
            Checkout select books within the inventory_table
        """   
        u = user()
        #send a POST request to your login endpoint with a username and password 
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('title', type=str)
        args = parser.parse_args()
        user_name = args['username']
        pass_word = args['password']
        title = args['title']
        print(pass_word)
        #retrieve a hash version of the password
        hashed_password = u.hashingAlgo(str(pass_word))
   
        #check if user can login 
        print(user_name)
        print(hashed_password)
        Authenticate_user="""
        SELECT CASE
            WHEN NOT EXISTS (SELECT * FROM user_table WHERE user_table.username = '%s' AND user_table.user_password = '%s' ) 
            THEN 1
            ELSE 2
        END 
        """% (str(user_name),str(hashed_password))
        status = exec_get_all(Authenticate_user)
        
        if(int(status[0][0]) ==  1):
            return "PUT unsucessful checkout failed"
        

        get_User_ID = """
            SELECT user_table.user_id FROM user_table WHERE user_table.username ='%s';
        """% (str(user_name))
        
        status2 = exec_get_one(get_User_ID)
        
    
        #input the session key
        update_sql = """
        UPDATE inventory_table
        SET user_id= '%d'
        WHERE title = '%s';
        """ % (int(status2[0]),str(title))
        exec_commit(update_sql)
        return "PUT sucessful checkout succeed"
    
class checkOutBookID(Resource): 
    def get(self,username):   
        """
            GET select books checkout by user within the inventory_table
        """   
        get_User_ID = """
            SELECT user_table.user_id FROM user_table WHERE user_table.username ='%s';
        """% (username)
        
        status2 = exec_get_all(get_User_ID)
        sql = """
            SELECT * FROM inventory_table WHERE inventory_table.user_id= '%d'
        """% (status2)
        return "GET sucessful data retrieved: " + str(exec_get_all(sql))
        
        

    
class inventoryGenreTitle(Resource):
    
    def get(self,attribute,text):        
        sql = "SELECT * FROM inventory_table WHERE inventory_table.%s = '%s' " % (attribute,text)
        return "GET sucessful data retrieved: " + str(exec_get_all(sql))