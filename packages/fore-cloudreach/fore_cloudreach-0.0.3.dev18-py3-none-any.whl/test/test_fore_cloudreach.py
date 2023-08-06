import unittest
import boto3
import fore_cloudreach as fc

from fore_cloudreach import Auth
from fore_cloudreach import Ingester
from fore_cloudreach import Template
from fore_cloudreach import AuthenticationError, EmptyMapFileError, ReadingMapFileError, ReportCreationError


class TestAuth(unittest.TestCase):
    """
    Test suit for the class Auth
    
    Testing the object instantiation (__init__):
        - test_0.. - test_2..
    
    Testing `get_ggl_creds` method:
        - test_3.. -  

    Testing `_get_trans_creds` method:
        - ...

    Testing `_get_secret_from_awssm` method:
        - ...
    """

    def test_0_Auth_misses_aws_credentials(self):
        print("testing Auth class to raise an AuthenticationError ...")
        with self.assertRaises(AuthenticationError) as context:
            Auth(None, [])
    
    def test_1_Auth_resets_globals(self):
        print("testing Auth class to reset global vars at init time ...")
        dm1 = {"1":"A"}
        dm2 = {"2":"B"}
        dm3 = {"3":"C"}

        fc.gcreds = dm1
        fc.token = dm2

        auth = Auth(dm3, ["100", "101"])
        self.assertIsNone(fc.gcreds)
        self.assertIsNone(fc.token)

    def test_2_build_aws_session(self):
        print("testing Auth build aws boto3 session...")
        auth = Auth(None, ["1", "2", "3"])
        self.assertIsInstance(auth.session, boto3.Session)

    def test_3_assert_exception_on_empty_params(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
