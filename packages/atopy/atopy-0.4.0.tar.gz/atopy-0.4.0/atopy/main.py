from loguru import logger

from atopy.typer import typer

app = typer()


@app.command()
def debug(msg: str) -> None:
    logger.debug(f"{msg}")


@app.command()
def info(msg: str) -> None:
    logger.info(f"{msg}")


@app.command()
def error(msg: str) -> None:
    logger.error(f"{msg}")


if __name__ == "__main__":
    app()
