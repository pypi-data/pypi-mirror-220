import click
from iota_sdk import Wallet, utf8_to_hex, MintNftParams, SendNftParams
from dotenv import load_dotenv
import os

load_dotenv()

@click.group()
def nft():
    pass

@nft.command()
@click.argument('alias')
def mint(alias):
    """Mint New NFT"""
    wallet = Wallet(os.environ['WALLET_DB_PATH'])

    if 'STRONGHOLD_PASSWORD' not in os.environ:
        raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

    wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])

    account = wallet.get_account(alias)

    # Sync account with the node
    response = account.sync()

    outputs = [MintNftParams(
        immutableMetadata=utf8_to_hex("some immutable nft metadata"),
    )]

    transaction = account.prepare_mint_nfts(outputs).send()
    print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')

@nft.command()
@click.option('--to', help='receiver of NFT Transfer')
@click.argument('alias')
def send(to, alias):
    """Mint New NFT"""
    wallet = Wallet(os.environ['WALLET_DB_PATH'])

    if 'STRONGHOLD_PASSWORD' not in os.environ:
        raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

    wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])

    account = wallet.get_account(alias)

    # Sync account with the node
    balance = account.sync()

    outputs = [SendNftParams(
        address=to,
        nftId=balance.nfts[0],
    )]

    transaction = account.prepare_send_nft(outputs).send()
    print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')
