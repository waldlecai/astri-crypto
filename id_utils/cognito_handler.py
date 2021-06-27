import os
import json
from dotenv import load_dotenv, find_dotenv
import boto3


class CognitoHandler:
    def __init__(self):
        load_dotenv(find_dotenv())
        dotenv_path = os.path.join(os.path.dirname(os.path.abspath("__file__")), ".env")
        load_dotenv(dotenv_path)
        self.client = boto3.client("cognito-idp", region_name=os.getenv("REGION_NAME"))
        self.client_id = os.getenv("COGNITO_USER_CLIENT_ID")
        self.user_pool_id=os.getenv("COGNITO_USER_POOL_ID")

    def signupUser(self, username, password, email):
        response = self.client.sign_up(ClientId=self.client_id, \
                                        Username=username, \
                                        Password=password, \
                                        UserAttributes=[{"Name": "email", "Value": email}],
        )
        return response

    def confirmUser(self, username, confirmation_code):
        response = self.client.confirm_sign_up(ClientId=self.client_id, \
                                        Username=username, \
                                        ConfirmationCode=confirmation_code,
        )
        return response

    def listAllUsers(self):
        response = self.client.list_users(UserPoolId=self.user_pool_id, \
                                        AttributesToGet=["email"], \
                                        Filter=""
        )
        return response

    def searchByUserName(self, username):
        response = self.client.list_users(UserPoolId=self.user_pool_id, \
                                        AttributesToGet=["email"], \
                                        Filter="username=\"" + username + "\""
        )
        return response

    def logIn(self, username, password):
        response = self.client.initiate_auth(ClientId=self.client_id, \
                                        AuthFlow="USER_PASSWORD_AUTH", \
                                        AuthParameters={"USERNAME": username, "PASSWORD": password}, \
        )
        return response

    def deleteUser(self, access_token):
        response = self.client.delete_user(AccessToken=access_token)
        return response

    def updateUser(self, access_token, attributes):
        response = self.client.update_user_attributes(
            UserAttributes=attributes,
            AccessToken=access_token
        )
        return response
    
    def getEmailVerificationCode(self, access_token):
        response = self.client.get_user_attribute_verification_code(AccessToken=access_token, AttributeName="email")
        return response

    def verifyEmail(self, access_token, verification_code):
        response = self.client.verify_user_attribute(
                AccessToken=access_token,
                AttributeName='email',
                Code=verification_code
        )
        return response

    def getPhoneVerificationCode(self, access_token):
        response = self.client.get_user_attribute_verification_code(AccessToken=access_token, AttributeName="phone_number")
        return response

    def verifyPhoneNumber(self, access_token, verification_code):
        response = self.client.verify_user_attribute(
                AccessToken=access_token,
                AttributeName='phone_number',
                Code=verification_code
        )
        return response

    def forgetPassword(self, username):
        response = self.client.forgot_password(
                ClientId=self.client_id, \
                Username=username
        )
        return response

    def confirmForgetPassword(self, username, verification_code, new_pwd):
        response = self.client.confirm_forgot_password(
                ClientId=self.client_id, \
                Username=username, \
                ConfirmationCode=verification_code, \
                Password=new_pwd
        )
        return response

#handler = CognitoHandler()
#handler.signupUser(username="waldlecai", password="Mango$4waldle", email="waldlecai@hotmail.com")
#handler.confirmUser("waldlecai", "785508")
#handler.listAllUsers()
#handler.searchUsers("username", '^=', "\"waldlecai\"")
#token = handler.logIn("yuhengcai", "Mango$49764aa")
#handler.updateUser(token, [{'Name': 'email', 'Value': 'waldlecai@gmail.com'}])
#handler.verifyEmail(token, "649465")
#handler.getPhoneVerificationCode(token)
#handler.deleteUser(token)
#handler.forgetPassword('yuhengcai')
#handler.confirmForgetPassword('yuhengcai', '328666', 'Mango$49764aa')