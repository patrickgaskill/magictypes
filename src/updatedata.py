from io import BytesIO
from zipfile import ZipFile
import requests
from rich.console import Console
from rich.progress import Progress
from utils import get_data_path

console = Console()

MTGJSON_BASE_URL = "https://mtgjson.com/api/v5"

MTGJSON_FILES = [
    "AllPrintings",
    "AtomicCards",
    "AllIdentifiers",
    "EnumValues",
    "SetList",
    "CardTypes",
]

SCRYFALL_BASE_URL = "https://api.scryfall.com"


def fetch_mtgjson() -> None:
    mtgjson_path = get_data_path("mtgjson")
    mtgjson_path.mkdir(parents=True, exist_ok=True)

    with Progress(console=console, transient=True) as progress:
        task = progress.add_task(
            "Downloading MTGJSON files...", total=len(MTGJSON_FILES)
        )
        for filename in MTGJSON_FILES:
            response = requests.get(f"{MTGJSON_BASE_URL}/{filename}.json.zip")
            zipfile = ZipFile(BytesIO(response.content))
            zipfile.extractall(mtgjson_path)
            file_path = mtgjson_path / f"{filename}.json"
            progress.console.log(f"MTGJSON {filename} downloaded to {file_path}")
            progress.advance(task)
        progress.console.log("✅ [bold green]MTGJSON data updated!")


def fetch_scryfall() -> None:
    scryfall_path = get_data_path("scryfall")
    scryfall_path.mkdir(parents=True, exist_ok=True)

    with console.status("Fetching bulk data list from Scryfall...", spinner="dots"):
        response = requests.get(f"{SCRYFALL_BASE_URL}/bulk-data")
        bulk_data_items = response.json()["data"]

    with Progress(console=console, transient=True) as progress:
        task = progress.add_task(
            "Downloading Scryfall files...", total=len(bulk_data_items)
        )
        for bulk_data_item in bulk_data_items:
            data = requests.get(bulk_data_item["download_uri"])
            file_path = scryfall_path / (bulk_data_item["type"] + ".json")
            file_path.write_bytes(data.content)
            progress.console.log(
                f"Scryfall {bulk_data_item['name']} downloaded to {file_path}"
            )
            progress.advance(task)
        progress.console.log("✅ [bold green]Scryfall data updated!")


if __name__ == "__main__":
    fetch_mtgjson()
    fetch_scryfall()
