from lark.exceptions import UnexpectedCharacters, UnexpectedEOF
from rich.progress import Progress

from mtgjsondata import MtgjsonData, legal_card_filter
from tokenextractor import TokenExtractor

with Progress() as progress:
    task = progress.add_task("Processing cards...", start=False)
    mtgjsondata = MtgjsonData()
    extractor = TokenExtractor()
    cards = list(mtgjsondata.load_objects(filterfunc=legal_card_filter))
    progress.update(task, total=len(cards))
    progress.start_task(task)
    test_cases = {}

    for card in cards:
        if card.name in test_cases:
            continue

        try:
            tokens = extractor.extract_from_card(card)
            test_cases[card.name] = tokens
        except (UnexpectedEOF, UnexpectedCharacters) as err:
            progress.console.print(f"[bold cyan]{card.name}")
            progress.console.print(f"{card.text}")
            progress.console.print(f"[red]{err}")
            quit()
        finally:
            progress.advance(task)
