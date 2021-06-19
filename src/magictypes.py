from pathlib import Path
from typing import Iterable

from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from effects import after_effects
from mtgjsondata import MtgjsonData
from stores import MaximalStore, Store, UniqueStore
from utils import make_output_dir

console = Console()


def generate_output(stores: Iterable[Store]) -> None:
    output_path = make_output_dir()
    table = Table(box=box.SIMPLE)
    table.add_column("Store")
    table.add_column("Count", justify="right", style="cyan")
    table.add_column("File", style="magenta")

    for store in stores:
        csv_path = store.write_csv(output_path)
        store.write_decklist(output_path)
        table.add_row(store.name, str(len(store)), str(Path(*csv_path.parts[-2:])))

    console.print(table)


def main() -> None:
    unique = UniqueStore("unique cards")
    maximal = MaximalStore("maximal cards")
    maximal_affected = MaximalStore("maximal affected cards")
    unique_tokens = UniqueStore("unique tokens")
    maximal_tokens = MaximalStore("maximal tokens")
    maximal_affected_tokens = MaximalStore("maximal affected tokens")
    stores = (
        unique,
        maximal,
        maximal_affected,
        unique_tokens,
        maximal_tokens,
        maximal_affected_tokens,
    )

    with Progress(transient=True) as progress:
        task = progress.add_task("Processing cards...", start=False)
        mtgjsondata = MtgjsonData()
        objects = list(mtgjsondata.load_objects())
        progress.update(task, total=len(objects))
        progress.start_task(task)

        for card in objects:
            if card.is_token:
                unique_tokens.evaluate(card)
                maximal_tokens.evaluate(card)
                maximal_affected_tokens.evaluate(card, after_effects)
            else:
                unique.evaluate(card)
                maximal.evaluate(card)
                maximal_affected.evaluate(card, after_effects)

                if card.name == "Grist, the Hunger Tide":
                    grist_copy = card.copy()
                    grist_copy.types.add("Creature")
                    grist_copy.subtypes.add("Insect")
                    grist_copy.clear_cached_properties()
                    unique.evaluate(grist_copy)
                    maximal.evaluate(grist_copy)
                    maximal_affected.evaluate(grist_copy, after_effects)

            progress.advance(task)

    generate_output(stores)


if __name__ == "__main__":
    main()
