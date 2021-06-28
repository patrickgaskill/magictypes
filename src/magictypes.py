import argparse
from pathlib import Path
from typing import Iterable

from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from effects import after_effects
from mtgjsondata import MtgjsonData, legal_card_filter
from stores import MaximalStore, Store, UniqueStore
from tokenextractor import TokenExtractor
from utils import make_output_dir


def generate_output(stores: Iterable[Store], console: Console) -> None:
    output_path = make_output_dir()
    table = Table(box=box.SIMPLE)
    table.add_column("Store")
    table.add_column("Count", justify="right", style="cyan")
    table.add_column("File", style="magenta")

    for store in stores:
        csv_path = store.write_csv(output_path)
        # store.write_decklist(output_path)
        table.add_row(store.name, f"{len(store)}", f"{Path(*csv_path.parts[-2:])}")

    console.print(table)


def main(include_tokens: False) -> None:
    console = Console()
    extractor = TokenExtractor()

    card_stores = [
        UniqueStore("unique cards"),
        MaximalStore("maximal cards"),
        MaximalStore("maximal affected cards", after_effects),
    ]

    token_stores = [
        UniqueStore("unique tokens"),
        MaximalStore("maximal tokens"),
        MaximalStore("maximal affected tokens", after_effects),
    ]

    with Progress(transient=True, console=console) as progress:
        task = progress.add_task("Processing cards...", start=False)
        mtgjsondata = MtgjsonData()
        cards = list(mtgjsondata.load_cards(filterfunc=legal_card_filter))
        progress.update(task, total=len(cards))
        progress.start_task(task)

        for card in cards:
            for store in card_stores:
                store.evaluate(card)

            if include_tokens:
                try:
                    tokens = extractor.extract_from_card(card)
                except Exception as err:
                    progress.console.print(
                        f"Exception: [bold cyan]{card.name} [red]{err}"
                    )
                else:
                    for token in tokens:
                        for store in token_stores:
                            store.evaluate(token)

            if card.name == "Grist, the Hunger Tide":
                grist_copy = card.copy()
                grist_copy.types.add("Creature")
                grist_copy.subtypes.add("Insect")
                grist_copy.clear_cached_properties()
                for store in card_stores:
                    store.evaluate(grist_copy)

            progress.advance(task)

    generate_output(
        card_stores + token_stores if include_tokens else card_stores, console
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a type analysis on Magic cards.")
    parser.add_argument(
        "--tokens",
        action=argparse.BooleanOptionalAction,
        help="include tokens parsed from card texts",
    )
    args = parser.parse_args()
    main(args.tokens)
