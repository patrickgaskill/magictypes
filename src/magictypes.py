from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from effects import after_effects
from mtgjsondata import MtgjsonData
from stores import MaximalStore, UniqueStore
from utils import make_output_dir


def generate_table(stores):
    table = Table(box=box.SIMPLE)
    table.add_column("Store")
    table.add_column("Count", justify="right")

    for store in stores:
        table.add_row(store.name, f"{store.count}")
    return table


def main():
    console = Console()
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

    with Progress() as progress:
        progress.console.log("Starting to load objects")
        task = progress.add_task("Processing cards...", start=False)
        mtgjsondata = MtgjsonData()
        objects = list(mtgjsondata.load_objects())
        progress.console.log("Loading objects complete")
        progress.update(task, total=len(objects))
        progress.start_task(task)

        for card in objects:
            if card.is_token:
                unique_tokens.evaluate(card)
                maximal_tokens.evaluate(card)

                for affected_card in after_effects(card):
                    maximal_affected_tokens.evaluate(affected_card)
            else:
                unique.evaluate(card)
                maximal.evaluate(card)

                for affected_card in after_effects(card):
                    maximal_affected.evaluate(affected_card)

                if card.name == "Grist, the Hunger Tide":
                    grist_copy = card.get_copy()
                    grist_copy.types.add("Creature")
                    grist_copy.subtypes.add("Insect")
                    grist_copy.clear_cached_properties()
                    unique.evaluate(grist_copy)
                    maximal.evaluate(grist_copy)
                    for affected_grist in after_effects(grist_copy):
                        maximal_affected.evaluate(affected_grist)

            progress.advance(task)

    output_path = make_output_dir()
    console.log(f"Created directory {output_path}")
    for store in stores:
        csv_path = store.write_csv(output_path)
        console.log(f"Created CSV file {csv_path}")
        decklist_path = store.write_decklist(output_path)
        console.log(f"Created decklist file {decklist_path}")

    console.print(generate_table(stores))


if __name__ == "__main__":
    main()
