from io import BytesIO
from zipfile import ZipFile
import requests
from rich.console import Console
from utils import get_data_path

console = Console()

MTGJSON_BASE_URL = "https://mtgjson.com/api/v5"

MTGJSON_FILES = [
    "AllPrintings",
    "AtomicCards",
    "AllIdentifiers",
    "EnumValues",
    "SetList",
    "Vintage",
    "VintageAtomic",
    "CardTypes",
]

SCRYFALL_BASE_URL = "https://api.scryfall.com"


def fetch_mtgjson() -> None:
    mtgjson_path = get_data_path("mtgjson")
    mtgjson_path.mkdir(parents=True, exist_ok=True)

    for filename in MTGJSON_FILES:
        with console.status(f"Downloading {filename} from MTGJSON...", spinner="dots"):
            response = requests.get(f"{MTGJSON_BASE_URL}/{filename}.json.zip")
            zipfile = ZipFile(BytesIO(response.content))
            zipfile.extractall(mtgjson_path)
            console.log(f"MTGJSON {filename} downloaded")


def fetch_scryfall() -> None:
    scryfall_path = get_data_path("scryfall")
    scryfall_path.mkdir(parents=True, exist_ok=True)

    response = requests.get(f"{SCRYFALL_BASE_URL}/bulk-data")
    bulk_data_items = response.json()

    for bulk_data_item in bulk_data_items["data"]:
        with console.status(
            f"Downloading {bulk_data_item['name']} from Scryfall...", spinner="dots"
        ):
            data = requests.get(bulk_data_item["download_uri"])
            file_path = scryfall_path / (bulk_data_item["type"] + ".json")
            file_path.write_bytes(data.content)
            console.log(f"Scryfall {bulk_data_item['name']} downloaded")


if __name__ == "__main__":
    fetch_mtgjson()
    fetch_scryfall()
