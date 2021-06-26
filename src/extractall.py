import csv

from rich.progress import Progress

from mtgjsondata import MtgjsonData, legal_card_filter
from tokenextractor import TokenExtractor
from utils import make_output_dir

with Progress() as progress:
    task = progress.add_task("Processing cards...", start=False)
    mtgjsondata = MtgjsonData()
    extractor = TokenExtractor()
    cards = list(mtgjsondata.load_cards(filterfunc=legal_card_filter))
    progress.update(task, total=len(cards))
    progress.start_task(task)
    test_cases = {}
    exceptions = []

    for card in cards:
        if card.name in test_cases:
            progress.advance(task)
            continue

        try:
            tokens = extractor.extract_from_card(card)
            test_cases[card.name] = tokens
        except Exception as err:
            # progress.console.print(f"[bold cyan]{card.name}")
            # progress.console.print(f"{card.text}")
            # progress.console.print(f"[red]{err}")
            # quit()
            exceptions.append((card.name, type(err).__name__))

        progress.advance(task)

    output_path = make_output_dir()
    csv_path = output_path / "exceptions.csv"
    with csv_path.open("w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(exceptions)
