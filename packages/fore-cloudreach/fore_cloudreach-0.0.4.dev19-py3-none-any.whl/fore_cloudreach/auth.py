
import ast
import sys
import fore_cloudreach as fc
from fore_cloudreach.errors import AuthenticationError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import boto3
from botocore.exceptions import ClientError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 
 
class Auth:
    """
    The Class `Auth` will authenticate the current user with its Google's account
    """

    def __init__(self, aws_session: object, aws_credentials: list):
        """
        This will instantiate an object from the class Auth.
        The main purpose of the object is to provide methods for authenticating with AWS Secret Manager
        and Google's Sheets API.

        Args:
            aws_session: None or already existing boto3 session to be used to get secrets from the AWS secret manager
            aws_credentials: access key id (idx 0), secret key (idx 1) and token (idx 2) to authenticate with AWS
        """
        
        # Reseting package level google credentials object and user's token
        fc.gcreds = None
        fc.token = None

        self.session = None

        if not aws_session and len(aws_credentials) < 1:
            raise AuthenticationError("Can not instantiate auth object without AWS credentials")

        # AWS session (boto3)
        if aws_session is None:
            self.session = boto3.session.Session(
                aws_access_key_id=aws_credentials[0],
                aws_secret_access_key=aws_credentials[1],
                aws_session_token=aws_credentials[2]
            )
        else:
            self.session = aws_session


    def get_ggl_creds(self, aws_secret_name: str, aws_region_name:str):
        """
        This method will use the instantiated object and its connection to AWS in
        order to utilize the returned as secret client_id for the Jupyter notebook 
        application that exports the customers' reports to Googles Sheets files.
        This method will only works for aws secrets' values stored as string, but 
        in the format of Google's credentials.json file. 

        Args:
            aws_secret_name: the name of the secret in the AWS Secret Manager
            aws_region_name: the AWS region name

        Returns:
            object: the required by Google's Sheets API credentials

        Raises:
              AuthenticationError: when the credentials are not acquired by any reason
              Exception: general exceptions
        
        """

        try:
            if fc.token:
                fc.gcreds = Credentials.from_authorized_user_info(fc.token, SCOPES)
            
            # If there are no (valid) credentials available, let the user log in.
            if not fc.gcreds or not fc.gcreds.valid:
                if fc.gcreds and fc.gcreds.expired and fc.gcreds.refresh_token:
                    fc.gcreds.refresh(Request())
                else:
                    try:

                        fc.gcreds = self._get_trans_creds(aws_secret_name, aws_region_name)

                    except Exception as err:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(f"[get_ggl_creds] Error: {err} raised at line {exc_tb.tb_lineno}")
                        raise err

                # Save the credentials for the next run
                fc.token = fc.gcreds.to_json()

            if fc.gcreds is None:
                raise AuthenticationError("User authentication failed!")
        
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"[get_ggl_creds] Error: {err} raised at line {exc_tb.tb_lineno}")


    def _get_trans_creds(self, aws_secret_name:str, aws_region_name:str) -> object:
        """
        Internal helper function to convert the aws secret value into expected Google format

        Args:
            aws_secret_name: the name of the secret in the AWS Secret Manager
            aws_region_name: the AWS region name

        Returns:
            object: the credentials to be used with Google Sheets API in expected Google format

        Raises:
            Exception: general exception

        """

        try:
            clientid_dict = self._get_secret_from_awssm(aws_secret_name, aws_region_name)
            client_config = ast.literal_eval(json.dumps(clientid_dict))

            flow = InstalledAppFlow.from_client_config(client_config=client_config, scopes=SCOPES)

            credentials = flow.run_local_server(open_browser=True)

        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"[get_trans_creds] Error: {err} raised at line {exc_tb.tb_lineno}")
            raise err
        
        return credentials 


    def _get_secret_from_awssm(self, secret_name: str, region_name: str) -> dict:
        """
        Using the AWS session provided to the object, connects to the AWS Secret manager and returns 
        a dictionary where: the key is the secret id and the value is the value of the secret.
        visit the AWS docs: https://aws.amazon.com/developer/language/python/
        
        Args:
            secret_name: the name of the secret 
            region_name: the name of the region

        Returns:
            dict: the key is the secret id and the value is the value of the secret.
        """
        
        secret_name = secret_name 
        region_name = region_name 

        # Create a Secrets Manager client
        client = self.session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        secret_group = secret_name.split("/")

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )

            # Decrypts secret using the associated KMS key.
            secret = get_secret_value_response['SecretString']
            secret_dict = ast.literal_eval(secret)

            # Extract the secret value only (w/o the key)
            secret_str_value = secret_dict.get(secret_group[0]) 
            secret_value_dict = ast.literal_eval(secret_str_value)

        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"[get_secret_from_awssm] Error: {err} raised at line {exc_tb.tb_lineno}")
            raise err
        
        return secret_value_dict 
