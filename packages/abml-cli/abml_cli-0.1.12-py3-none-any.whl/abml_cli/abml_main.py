import click

@click.group()
@click.pass_context
def cli(ctx):
    pass

cli.add_command(bundle)
cli.add_command(file)
cli.add_command(directory)
