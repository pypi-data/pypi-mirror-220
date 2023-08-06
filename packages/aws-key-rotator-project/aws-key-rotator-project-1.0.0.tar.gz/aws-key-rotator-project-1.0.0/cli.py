'''CLI wrapper for AWS key rotator.'''
# TODO: Change help message, remove print statement, and fix switch case when
# full rotation is added.
import sys
import argparse
from key_rotator import KeyRotator


def main():
    parser = argparse.ArgumentParser(description='CLI Wrapper for KeyRotator')

    parser.add_argument(
        '--usernames',
        nargs='*',
        help=('Specify usernames for which to rotate. If not provided, keys '
              'for all users will be rotated.'),
    )
    parser.add_argument(
        '--key-age',
        type=int,
        default=7,
        help=('Specify the age (in days) of keys to consider for rotation '
              '(default is 7).'),
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='WARNING',
        help='Set the log level (default is WARNING).',
    )
    parser.add_argument(
        '--rotation-type',
        choices=['ROTATE-KEYS', 'DELETE-KEYS'],
        default='ROTATE-KEYS',
        help=('Choose whether to delete all keys or rotate them. NOTE: Only '
              'deletion implemented.')
    )
    args = parser.parse_args()

    if args.rotation_type == 'ROTATE_KEYS':
        print('Full rotation not implemented (only deletion), exiting.')
        sys.exit(0)

    print(f'Preparing to start rotation using: {args.rotation_type}. Getting '
          'key information.')
    if not args.usernames:
        confirmation = input('Caution: All users selected. Continue? y/n:').lower()
        if confirmation != 'y':
            sys.exit(0)
    key_rotator = KeyRotator(
        usernames=args.usernames,
        key_age=args.key_age,
        log_level=args.log_level,
    )
    match args.rotation_type:
        case 'DELETE-KEYS':
            confirmation = input('Going to delete all keys for marked users. '
                                 'Continue? y/n: ').lower()
            if confirmation != 'y':
                sys.exit(0)
            key_rotator.delete_keys()
        case 'ROTATE':
            pass
            
    print('Rotation complete.')


if __name__ == '__main__':
    main()
