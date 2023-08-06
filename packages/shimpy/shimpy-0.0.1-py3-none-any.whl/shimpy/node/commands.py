import click
from iota_sdk import Client

# Create a Client instance
client = Client(nodes=['https://api.testnet.shimmer.network'])

@click.command()
def info():
    """Display the node info."""
    node_info = client.get_info()
    print(f'{node_info}')
    click.echo(node_info)
