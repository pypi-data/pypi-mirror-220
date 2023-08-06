"""
    lager.ssh.commands

    SSH commands
"""
import click
from ..context import get_default_gateway
import os
import time
import tempfile

@click.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
def ssh(ctx, dut):
    """
    SSH to the specified gateway
    """
    if dut is None:
        dut = get_default_gateway(ctx)

    session = ctx.obj.session
    resp = session.get_ssh_info(dut)
    data = resp.json()
    key_filename = None
    with tempfile.NamedTemporaryFile('wb', delete=False) as f:
        key_filename = f.name
        f.write(data['privkey'].encode())

    pid = os.fork()
    if pid > 0:
        """Parent process"""
        os.execlp(
            "ssh",
            "ssh",
            "-i",
            key_filename,
            "-p",
            str(data['port']),
            f"{data['username']}@{data['host']}",
        )

    else:
        """Child process"""
        time.sleep(2)
        os.remove(key_filename)
