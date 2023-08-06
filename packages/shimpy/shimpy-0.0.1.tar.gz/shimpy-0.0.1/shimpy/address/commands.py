import click
from iota_sdk import Wallet
from dotenv import load_dotenv
import os

load_dotenv()

@click.group()
def address():
    pass

@address.command()
@click.argument('alias')
def new(alias):
    """Create New Address for Account"""
    wallet = Wallet(os.environ['WALLET_DB_PATH'])

    if 'STRONGHOLD_PASSWORD' not in os.environ:
        raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

    wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])

    account = wallet.get_account(alias)

    address = account.generate_ed25519_addresses(1)
    print(f'Generated address:', address[0].address)

@address.command()
@click.argument('alias')
def list(alias):
    """Create New Address for Account"""
    wallet = Wallet(os.environ['WALLET_DB_PATH'])

    if 'STRONGHOLD_PASSWORD' not in os.environ:
        raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

    wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])

    account = wallet.get_account(alias)

    addresses = account.addresses()

    a = 0
    for address in addresses:
        print("Address #", a, "::", address.address)
        a += 1
