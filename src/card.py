import re
from datetime import datetime
from types import SimpleNamespace


class Card(SimpleNamespace):
    object = "card"

    @property
    def release_date(self):
        if hasattr(self, "originalReleaseDate"):
            return self.originalReleaseDate

        if hasattr(self, "set"):
            return self.set.releaseDate

        return None

    @property
    def is_every_creature_type(self):
        if "Changeling" in getattr(self, "keywords", []):
            return True

        if self.name == "Mistform Ultimus":
            return True

        return False

    @property
    def sort_key(self):
        release_date = datetime.max

        if self.release_date:
            release_date = datetime.fromisoformat(self.release_date)

        parsed_number = int(re.sub(r"[^\d]+", "", self.number))
        return release_date, self.setCode, parsed_number, self.number

    @property
    def types_key(self):
        return (
            tuple(self.supertypes),
            tuple(self.types),
            tuple(self.subtypes),
            self.is_every_creature_type,
        )

    @property
    def is_valid(self):
        if "shandalar" in self.availability:
            return False

        if self.layout in ("token", "emblem"):
            return False

        if getattr(self, "borderColor", "") in ("gold", "silver"):
            return False

        if hasattr(self, "set") and self.set.type in ("funny", "memorabilia", "promo"):
            return False

        if self.setCode in ("THP1", "THP2", "THP3", "PSAL"):
            return False

        return True
