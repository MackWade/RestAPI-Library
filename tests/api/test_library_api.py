import json
import unittest
import zipapp
from src.db.swen344_db_utils import exec_get_one
from tests.test_utils import *
import platform


class TestLibrary(unittest.TestCase):


    def test_List_all_users(self):
        expected = "GET sucessful User data retrieved: [(1, '9035856787', 'Ada@gmail.com', 'ada', 'Lovelace', 'adaGirl', 'ada1', '0'), (2, '9033226786', 'Mary33@gmail.com', 'Mary', 'Shelley', 'ShelleyMaster', 'shelly1', '0'), (3, '9035558976', 'Jackie44@gmail.com', 'Jackie', 'Gleason', 'GleasonTown', 'Gleason1', '0'), (4, '3435879022', 'Art55@gmail.com', 'Art', 'Garfunkel', 'GarfunkelKing', 'Garfunkel1', '0')]"
        actual = get_rest_call(self, 'http://localhost:4999/user')
        print(actual)
        self.assertEqual(expected, actual)


    def test_all_rest_2(self):
    
        """
            Test Case 1:
                You can add a new user with a password and any other user information
        """ 
    
        p_num = "0000000000"
        _email = "TestUser@gmail.com"
        f_name = "Test"
        l_name = "User"
        u_name = "TestUser1"
        _u_password = "Password"
        data = dict(phone_number=p_num, email=_email, firstname=f_name,lastname=l_name,username=u_name,u_password =_u_password )
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        actual = post_rest_call(self,'http://localhost:4999/user', jdata, hdr )
        expected = "POST sucessful new user created"
        print(actual)
        self.assertEqual(expected, actual)
    
        """
            Test Case 2:
                If a user already exists, the add user fails
        """     
    
        p_num = "9035856787"
        _email = "Ada@gmail.com"
        f_name = "ada"
        l_name = "Lovelace"
        u_name = "adaGirl"
        _u_password = "ada1"
        data = dict(phone_number=p_num, email=_email, firstname=f_name,lastname=l_name,username=u_name,u_password =_u_password )
        jdata = json.dumps(data)
        actual = post_rest_call(self,'http://localhost:4999/user', jdata, hdr )
        expected = "POST unsucessful new user not created"
        print(actual)
        self.assertEqual(expected, actual)
        
        """
            Test Case 3:
                You can login successfully with the right userId and password; 
                hashing is performed as described, and incorrect passwords fail login
        """         
   
        u_name = "TestUser1"
        _u_password = "Password"
        
        #login success
        logindata = dict(username=u_name,u_password =_u_password )
        jdata = json.dumps(logindata)
        actual = post_rest_call(self,'http://localhost:4999/userLogin', jdata, hdr)
        expected = "POST sucessful login succeed"
        print(actual)
        self.assertEqual(expected, actual)

        #login Fails
        u_name = "TestUser2"
        _uf_password = "Password!"
        logindata2 = dict(username=u_name,u_password =_uf_password )
        jdata2 = json.dumps(logindata2)
        actual_failed = post_rest_call(self,'http://localhost:4999/userLogin', jdata2, hdr)
        expected_failed = "POST unsucessful login failed"
        print(actual_failed)
        self.assertEqual(expected_failed, actual_failed)
    
        """
        Test Case 4:
            You can edit a users information; if you try to edit a non-existent user, the API fails
        """      

        columns = "email"
        values = "ada3@hi.com"
        u_names = "adaGirl"
     
        #edit success
        editdata = dict(column=columns,value =values,username=u_names )
        jdata = json.dumps(editdata)
        actual = put_rest_call(self,'http://localhost:4999/userUpdate', jdata, hdr)
        expected = "PUT sucessful user edit succeed"
        print(actual)
        self.assertEqual(expected, actual)
        
        #edit fails
        u_names = "ada3Girl"
        editdata = dict(column=columns,value =values,username=u_names )
        jdata = json.dumps(editdata)
        actual = put_rest_call(self,'http://localhost:4999/userUpdate', jdata2, hdr)
        expected = "PUT unsucessful user edit failed"
        print(actual)
        self.assertEqual(expected, actual)
        
          
        """
            Test Case 5:
                You can remove a user; again, if the user doesn’t exist, the API fails
        """      
        #retrieve session key
        sql = """
            SELECT session_key FROM user_table WHERE username = 'TestUser1'
        """
        key = exec_get_one(sql)
        #delete success
        actual = delete_rest_call(self,"http://localhost:4999/user/TestUser1/%s" %(str(key[0])))
        expected = "DELETE sucessful user deletion succeed"
        print(actual)
        self.assertEqual(expected, actual)
        
        #delete fails
        actual = delete_rest_call(self,"http://localhost:4999/user/TestUser3/%s" %(str(key[0])))
        expected= "DELETE unsucessful user deletion failed"
        print(actual)
        self.assertEqual(actual, expected)
        
        """
            Test Case 6:
                If you try to remove a user (who exists), and don’t have the correct authentication session key, the API fails
        """    
       
        actual = delete_rest_call(self,"http://localhost:4999/user/TestUser3/342532525" )
        expected= "DELETE unsucessful user deletion failed"
        print(actual)
        self.assertEqual(actual, expected)
        
        """
            Test Case 7:
                You can list all books or books by title or type. 
                Make sure you have the correct data in the DB to test this properly. Anyone can do this.
        """       
       
        #get books by title
        actual = get_rest_call(self,'http://localhost:4999/books/title/The Maid')
        expected = "GET sucessful data retrieved: [(1, 'The Maid', 'Fiction', '2022-01-04', 'Nita Prose', 3, None)]"
        print(actual)
        self.assertEqual(expected, actual)
        
        
        #get books by type
        actual = get_rest_call(self,'http://localhost:4999/books/genre/Fiction')
        expected = "GET sucessful data retrieved: [(1, 'The Maid', 'Fiction', '2022-01-04', 'Nita Prose', 3, None), (2, 'Olga Dies Dreaming', 'Fiction', '2022-01-04', 'Xochitl Gonzalez', 3, None), (3, 'To Paradise', 'Fiction', '2022-01-11', 'Hanya Yanagihara', 4, None)]"
        print(actual)
        self.assertEqual(expected, actual)
        
        #get all books
        actual = get_rest_call(self,'http://localhost:4999/books')
        expected ="GET sucessful inventory data retrieved: [(1, 'The Maid', 'Fiction', '2022-01-04', 'Nita Prose', 3, None), (2, 'Olga Dies Dreaming', 'Fiction', '2022-01-04', 'Xochitl Gonzalez', 3, None), (3, 'To Paradise', 'Fiction', '2022-01-11', 'Hanya Yanagihara', 4, None), (4, 'Walking Gentry Home', 'Non-Fiction', '2022-08-02', 'Alora Young', 8, None)]"
        print(actual)
        self.assertEqual(expected, actual)
        
        """
            You can perform a new checkout of a book by title. 
            Only an authenticated user can do this. In no user is authenticated, an error is returned.
        """
        #create user 
        p_num = "0000000000"
        _email = "TestUser@gmail.com"
        f_name = "Test"
        l_name = "User"
        u_name = "TestUser1"
        _u_password = "Password"
        data = dict(phone_number=p_num, email=_email, firstname=f_name,lastname=l_name,username=u_name,user_password =_u_password )
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        actual = post_rest_call(self,'http://localhost:4999/user', jdata, hdr )
        
        #check out success
        usernames = "TestUser1"
        passwords = "Password"
        titles = "The Maid"
        logindata = dict(username=usernames,password =passwords,title=titles )
        jdata2 = json.dumps(logindata)
        hdr = {'content-type': 'application/json'}
        actual = put_rest_call(self,'http://localhost:4999/checkOutBook', jdata2, hdr)
        expected = "PUT sucessful checkout succeed"
        print(actual)
        self.assertEqual(expected, actual)
        
        #check out fail
        usernames = "adaGirl7"
        logindata = dict(username=usernames,password =passwords,title=titles )
        jdata2 = json.dumps(logindata)
        hdr = {'content-type': 'application/json'}
        actual = put_rest_call(self,'http://localhost:4999/checkOutBook', jdata2, hdr)
        expected = "PUT unsucessful checkout failed"
        print(actual)
        self.assertEqual(expected, actual)
        
        

            
        