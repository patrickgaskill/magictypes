import time
from pathlib import Path
from rich.table import Table
from rich.progress import Progress
from utils import console, get_data_path
from stores import UniqueStore, MaximalStore
from mtgjsondata import load_objects
from effects import after_effects


def legal_card_filter(card):
    if card.border_color in ("gold", "silver"):
        return False

    if "shandalar" in card.availability:
        return False

    if card.layout == "emblem":
        return False

    if card.set_type in ("funny", "memorabilia", "promo"):
        return False

    if card.set_code in (
        "THP1",
        "THP2",
        "THP3",
        "PSAL",
        "TDAG",
        "TBTH",
        "TFTH",
        "TUND",
    ):
        return False

    return True


def mk_output_dir() -> Path:
    run_time = time.strftime("%Y-%m-%d-%H%M%S")
    output_path = get_data_path(f"output/{run_time}")
    output_path.mkdir(parents=True, exist_ok=True)
    console.log(f"Created directory {output_path}")
    return output_path


def generate_table(stores):
    table = Table()
    table.add_column("Store")
    table.add_column("Count", justify="right")

    for store in stores:
        table.add_row(store.name, f"{store.count}")
    return table


def main():
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
        task = progress.add_task("Processing cards", start=False)
        objects = list(load_objects(legal_card_filter))
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
                    unique.evaluate(grist_copy)
                    maximal.evaluate(grist_copy)
                    for affected_grist in after_effects(grist_copy):
                        maximal_affected.evaluate(affected_grist)

            progress.advance(task)

    output_path = mk_output_dir()
    for store in stores:
        csv_path = store.write_csv(output_path)
        console.log(f"Created CSV file {csv_path}")

    console.print(generate_table(stores))


if __name__ == "__main__":
    main()
