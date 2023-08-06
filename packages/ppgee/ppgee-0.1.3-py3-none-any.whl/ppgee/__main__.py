import argparse
import asyncio
from ppgee import PPGEE
import sys
from . import errors


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_args():
    parser = argparse.ArgumentParser(description="Confirm your montly PPGEE attendency")
    parser.add_argument("username", type=str, help="Your PPGEE's username")
    parser.add_argument("password", type=str, help="Your PPGEE's password")
    return parser.parse_args()


async def cli():
    args = get_args()
    user, password = args.username, args.password
    try:
        async with PPGEE(user=user, password=password) as ppgee:
            frequency_page = await ppgee.frequency()
            await asyncio.sleep(1)
            if frequency_page.is_available():
                print("Attendency confirmed.")
                await frequency_page.confirm()
            else:
                eprint("Attendency not available yet.")
            await asyncio.sleep(1)
    except errors.InvalidCredentialsException:
        eprint("Invalid credentials.")


def main():
    try:
        asyncio.run(cli())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting.")


if __name__ == "__main__":
    main()
