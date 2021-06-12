from pathlib import Path
from rich.console import Console

console = Console()


def get_data_path(filename) -> Path:
    return Path(__file__).parent.joinpath("../data/", filename).resolve()
