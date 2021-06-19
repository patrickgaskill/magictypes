from lark.exceptions import UnexpectedCharacters, UnexpectedEOF
from rich.progress import Progress

from mtgjsondata import MtgjsonData
from tokenextractor import TokenExtractor

with Progress() as progress:
    task = progress.add_task("Processing cards...", start=False)
    mtgjsondata = MtgjsonData()
    extractor = TokenExtractor()
    objects = list(mtgjsondata.load_objects())
    progress.update(task, total=len(objects))
    progress.start_task(task)

    for card in objects:
        try:
            tokens = extractor.extract_from_card(card)
        except (UnexpectedEOF, UnexpectedCharacters) as err:
            progress.console.print(f"[bold cyan]{card.name}")
            progress.console.print(f"{card.text}")
            progress.console.print(f"[red]{err}")
            quit()

        progress.advance(task)
