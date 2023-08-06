'''IAM access key rotator for AWS.'''
import sys
import logging
from datetime import datetime, timedelta, timezone
from typing import Union
import boto3
import botocore.exceptions as boto_ex


class KeyRotator:
    # TODO: Implement full key rotation and change class message.
    """Rotate or delete AWS IAM access keys. Only deletion implemented.

    Can take in user list or grab all users if user list is not passed. Gets
    the key IDs and then rotate or delete as requested. If rotating, it will:
    generate new keys, apply them to applications, check the last used
    time of old keys, disable old keys, verify application functionality,
    revert if needed, and finally, delete the marked keys.

    Args:
        usernames (list[str]): A list of usernames to rotate the keys for.
        key_age (int): Age of keys in days to rotate. Default is 7 days.
        log_level (str): Log level for the logging module. Default 'WARNING'.
    """
    def __init__(self, usernames: list[Union[None, str]],
                 key_age: int, log_level: str) -> None:
        logging.basicConfig(level=log_level)
        # Credential information: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
        self.iam_client = boto3.client('iam')
        self.usernames = usernames
        if not usernames:
            logging.info('List of users not passed, getting all users.')
            self.usernames = self._get_all_usernames()
        self.key_age = timedelta(days=key_age)
        self.key_ids = self._get_key_ids()

    def _get_all_usernames(self) -> list[str]:
        '''Gets all AWS IAM users and returns a list of their usernames.'''
        logging.info('trying_response')
        try:
            response = self.iam_client.list_users()
            usernames = [user['UserName'] for user in response['Users']]
            logging.debug('Got the following usernames: %s', usernames)
        except boto_ex.HTTPClientError as ex:
            logging.error('Response error getting users: %s. Exiting.', ex)
            sys.exit(1)
        return usernames

    def _get_key_ids(self) -> dict[str, str]:
        '''Get all keys older than given age.'''
        # Dict with users can be used to generate new key for respective user.
        usernames_to_keys = {}
        for username in self.usernames:
            response = self.iam_client.list_access_keys(UserName=username)
            for key in response['AccessKeyMetadata']:
                if datetime.now(timezone.utc) - key['CreateDate'] > self.key_age:
                    usernames_to_keys[username] = key['AccessKeyId']
                    logging.debug('Key ID: %s for %s older than %s, adding.',
                                  key['AccessKeyId'], username, self.key_age)
        return usernames_to_keys

    def _generate_new_keys(self):
        '''Generate new keys as part of rotation.'''
        # TODO: Create new keys before deleting old ones for full rotation.
        pass

    def _apply_keys(self):
        '''Migrate applications to use new keys.'''
        # TODO: Implement this.
        pass

    def _check_last_used(self):
        '''Verify keys aren't being used before disabling them.'''
        # TODO: Implement this.
        pass

    def _disable_keys(self):
        '''Disable keys before deleting.'''
        # TODO: Implement this.
        pass
    
    def _verify_apps(self):
        '''Verify application functionality before disabling keys.'''
        # TODO: Implement this.
        pass
    
    def _revert_disable(self):
        '''Re-enable key if application is not working properly.'''
        # TODO: Implement this.
        pass

    def delete_keys(self) -> None:
        '''Deletes all keys for marked users.'''
        for key_id in self.key_ids.values():
            logging.debug('Deleting key %s', key_id)
            self.iam_client.delete_access_key(AccessKeyId=key_id)

    def rotate_keys(self):
        '''Generate, apply, check old, disable, check status, delete keys.'''
        # TODO: Rotate keys fully. Could only set delete but I think it is best
        # for user to explicitly state they only want to delete.
        pass