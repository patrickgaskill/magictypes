import time
from pathlib import Path
from rich.console import Console

console = Console()


def get_data_path(filename) -> Path:
    return Path(__file__).parent.joinpath("../data/", filename).resolve()


def make_output_dir() -> Path:
    run_time = time.strftime("%Y-%m-%d-%H%M%S")
    output_path = get_data_path(f"output/{run_time}")
    output_path.mkdir(parents=True, exist_ok=True)
    console.log(f"Created directory {output_path}")
    return output_path
