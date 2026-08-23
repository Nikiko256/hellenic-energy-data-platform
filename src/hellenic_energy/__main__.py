"""Command-line entry point for the Hellenic Energy Data Platform."""

import typer

app = typer.Typer(
    help="Build and operate the Hellenic Energy Data Platform.",
)


@app.callback()
def main() -> None:
    """Run data-platform commands."""


@app.command()
def doctor() -> None:
    """Verify that the project command-line application works."""
    typer.echo("Hellenic Energy Data Platform environment is ready.")


if __name__ == "__main__":
    app()