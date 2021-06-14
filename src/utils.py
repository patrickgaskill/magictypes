import time
from pathlib import Path


def get_data_path(filename) -> Path:
    return Path(__file__).parent.joinpath("../data/", filename).resolve()


def make_output_dir() -> Path:
    run_time = time.strftime("%Y-%m-%d-%H%M%S")
    output_path = get_data_path(f"output/{run_time}")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
