"""Shimpy"""

import time
import arrow
import click

from .node import commands as node
from .account import commands as account
from .address import commands as address
from .nft import commands as nft

@click.group()
def shimpy():
    pass

shimpy.add_command(node.info)
shimpy.add_command(account.account)
shimpy.add_command(address.address)
shimpy.add_command(nft.nft)
