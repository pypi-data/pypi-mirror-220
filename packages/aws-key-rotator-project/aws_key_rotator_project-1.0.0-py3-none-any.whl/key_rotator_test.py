'''Tests for key_rotator.py.'''
import unittest
from unittest import mock
from datetime import datetime, timedelta
from key_rotator import KeyRotator

# Fake two users. 1st has an old key, second has a new key.
user1 = 'user1'
user2 = 'user2'
fake_user_resp = {
    'Users': [
        {'UserName': user1},
        {'UserName': user2}
    ]
}
current_date = datetime.now()
user1_create_date = current_date - timedelta(days=10)
user2_create_date = current_date - timedelta(days=1)
fake_key_resp_1 = {
    'AccessKeyMetadata': [
        {
            'AccessKeyId': '1',
            'CreateDate': user1_create_date,
            'Status': 'Active',
            'UserName': user1,
        }
    ]
}
fake_key_resp_2 = {
    'AccessKeyMetadata': [
        {
            'AccessKeyId': '2',
            'CreateDate': user2_create_date,
            'Status': 'Active',
            'UserName': user2,
        }
    ]
}


def list_access_keys_side_effect(UserName):
    '''Side effect for boto3.list_access_keys.'''
    match UserName:
        case 'user1':
            return fake_key_resp_1
        case 'user2':
            return fake_key_resp_2


class TestKeyRotator(unittest.TestCase):
    '''Tests for AWS key rotator class.'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
      
    def setUp(self):
        super().setUp()
        self.iam_client_mock = mock.MagicMock()
        self.iam_client_mock.list_users.return_value = fake_user_resp
        self.iam_client_mock.list_access_keys.side_effect = list_access_keys_side_effect
        self.boto3_client_patch = mock.patch('key_rotator.boto3.client', 
                                             return_value=self.iam_client_mock)
        self.boto3_client_patch.start()

    def tearDown(self) -> None:
        super().tearDown()
        mock.patch.stopall()

    def test_key_rotator_deletion(self):
        '''End-to-end test for KeyRotator.delete_keys.'''
        # Pass user1 and 2. Only 1 has an old key.
        KeyRotator(usernames=[user1, user2], key_age=7,
                   log_level='DEBUG').delete_keys()
        self.iam_client_mock.delete_access_key.assert_called_once_with(AccessKeyId='1')
        
    def test_get_all_usernames(self):
        '''Test _get_all_usernames and that it returns all usernames.'''
        users = KeyRotator(usernames=[], key_age=7,
                           log_level='DEBUG')._get_all_usernames()
        # We mock the response value for list_users to be our specified users.
        self.assertEqual(users, [user1, user2])
        
    def test_get_key_ids(self):
        '''Test _get_key_ids and that it returns only old keys.'''
        key_ids = KeyRotator(usernames=[], key_age=7,
                             log_level='DEBUG')._get_key_ids()
        # user1 has a key older than 7 days.
        self.assertEqual(key_ids, {user1: '1'})


if __name__ == '__main__':
    unittest.main()