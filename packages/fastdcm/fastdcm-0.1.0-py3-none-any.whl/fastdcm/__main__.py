"""
pypi-AgEIcHlwaS5vcmcCJGE4NjcyNGM2LTg4OWUtNDNmNC1hM2JiLWY4YWU0MzkyYTU2ZgACKlszLCJkNDMxMjU4Zi03NzU3LTQ0MzAtOTkyYi04ZDE2YjJiOTA1MDYiXQAABiAU932C6WCN1q-T2dyhvgJiJrb0cI-MPFk9LWXEdi7-xA
"""
import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")