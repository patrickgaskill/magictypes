import time
from pathlib import Path

import orjson


def get_data_path(filename) -> Path:
    return Path(__file__).parent.joinpath("../data/", filename).resolve()


def get_data_json(filename) -> any:
    with get_data_path(filename).open() as f:
        return orjson.loads(f.read())


def make_output_dir() -> Path:
    run_time = time.strftime("%Y-%m-%d-%H%M%S")
    output_path = get_data_path(f"output/{run_time}")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


# https://marshmallow.readthedocs.io/en/latest/examples.html#inflection-camel-casing-keys
def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)
