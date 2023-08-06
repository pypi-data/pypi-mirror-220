# AWS Key Rotator

A simple and extensible AWS key rotation tool. Checks a given list of IAM usernames (or all under account if not passed) and rotates or deletes their associated access keys.

## Limitations

Currently can only delete access keys, not make new ones and rotate them. However, this may be fine if you just do not want users to keep their access keys around (just be careful with using all users under your account, as you could delete critical application keys). I only include a CLI wrapper, but should be straightforward to run as a cronjob (except that input() cannot currently be disabled).

Tested live with AWS on Arch running Python 3.11.

## Installation

Install aws-key-rotator from PyPI with pip.

`pip install aws-key-rotator-project`

## Usage

Run the tool with `aws-key-rotator`. `--help` shows parameters. Main ones are `--usernames` to specify usernames to rotate keys for, `--key-age` to set age of keys to rotate (7 days by default), and `--rotation-type` (only `DELETE-KEYS` works right now). If no usernames are passed, access keys for all IAM accounts under the one that is running the tool. Note that credentials are set using boto3, see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html for info. 

```
aws-key-rotator --rotation-type=DELETE_KEYS
Preparing to start rotation using: DELETE_KEYS. Getting key information.
Caution: All users selected. Continue? y/n:y
Going to delete all keys for marked users. Continue? y/n: y
Rotation complete.
```

## Future work
- Implement full rotation capabilities. Another tool should probably be used to verify application functionality as it could be intricate. If we decide to keep this as deletion only, then remove incomplete methods, notes, etc.
- Improve exception handling. If bad usernames are passed an exception might be thrown.
- Ability to disable input() calls so that it can be forcibly ran via cron job, etc.
- Perhaps use moto testing library (https://github.com/getmoto/moto)