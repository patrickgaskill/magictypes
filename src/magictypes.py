import argparse
from pathlib import Path
from typing import Iterable, Optional

from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from effects import apply_effects
from magicobjects import SortKey
from mtgjsondata import MtgjsonData, legal_card_filter
from stores import MaximalStore, Store, UniquePowerToughnessStore, UniqueStore
from tokenextractor import TokenExtractor
from utils import make_output_dir
from variations import activated_variations, global_variations


def generate_output(
    stores: Iterable[Store],
    console: Console,
    generate_decklists: Optional[bool] = False,
) -> None:
    output_path = make_output_dir()
    table = Table(box=box.SIMPLE)
    table.add_column("Store")
    table.add_column("Count", justify="right", style="cyan")
    table.add_column("CSV File", style="magenta")

    if generate_decklists:
        table.add_column("Decklist File", style="magenta")

    for store in stores:
        csv_path = store.write_csv(output_path)
        table_row = [store.name, f"{len(store)}", f"{Path(*csv_path.parts[-2:])}"]
        if generate_decklists:
            decklist_path = store.write_decklist(output_path)
            table_row.append(f"{Path(*decklist_path.parts[-2:])}")
        table.add_row(*table_row)

    console.print(table)


def main(
    include_tokens: Optional[bool] = False, generate_decklists: Optional[bool] = False
) -> None:
    console = Console()
    extractor = TokenExtractor()

    # card_stores = [
    #     UniqueStore("unique cards"),
    #     MaximalStore("maximal cards"),
    #     MaximalStore("maximal affected cards", after_effects),
    # ]

    # token_stores = [
    #     UniqueStore("unique tokens"),
    #     MaximalStore("maximal tokens"),
    #     MaximalStore("maximal affected tokens", after_effects),
    # ]

    unique_card_store = UniqueStore("unique cards")
    maximal_card_store = MaximalStore("maximal cards")
    maximal_affected_card_store = MaximalStore("maximal affected cards")
    unique_power_toughness_card_store = UniquePowerToughnessStore("unique PT cards")

    card_stores = [
        unique_card_store,
        maximal_card_store,
        maximal_affected_card_store,
        unique_power_toughness_card_store,
    ]

    unique_token_store = UniqueStore("unique tokens")
    maximal_token_store = MaximalStore("maximal tokens")
    maximal_affected_token_store = MaximalStore("maximal affected tokens")
    unique_power_toughness_token_store = UniquePowerToughnessStore("unique PT tokens")

    token_stores = [
        unique_token_store,
        maximal_token_store,
        maximal_affected_token_store,
        unique_power_toughness_token_store,
    ]

    cached_sort_keys: dict[str, SortKey] = {}

    with Progress(transient=True, console=console) as progress:
        task = progress.add_task("Processing cards...", start=False)
        mtgjsondata = MtgjsonData()
        cards = list(mtgjsondata.load_cards(filterfunc=legal_card_filter))
        progress.update(task, total=len(cards))
        progress.start_task(task)

        for card in cards:
            # If we've already seen an older version of the same card, bail out
            if (
                card.name in cached_sort_keys
                and card.sort_key > cached_sort_keys[card.name]
            ):
                progress.advance(task)
                continue

            cached_sort_keys[card.name] = card.sort_key

            cards_to_evaluate = (
                [card] + global_variations[card.name](card)
                if card.name in global_variations
                else [card]
            )

            for c in cards_to_evaluate:
                for store in card_stores:
                    store.evaluate(c)

                for affected_obj in apply_effects(c):
                    # apply_effects could return cards and tokens

                    if affected_obj.object_type == "token" and include_tokens:
                        maximal_affected_token_store.evaluate(affected_obj)

                    if affected_obj.object_type == "card":
                        maximal_affected_card_store.evaluate(affected_obj)

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

            progress.advance(task)

    generate_output(
        card_stores + token_stores if include_tokens else card_stores,
        console,
        generate_decklists,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a type analysis on Magic cards.")
    parser.add_argument(
        "--tokens",
        action=argparse.BooleanOptionalAction,
        help="include tokens parsed from card texts",
    )
    parser.add_argument(
        "--decklists",
        action=argparse.BooleanOptionalAction,
        help="generate decklist-formatted files",
    )
    args = parser.parse_args()
    main(args.tokens, args.decklists)
