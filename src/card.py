import datetime
import re
from types import SimpleNamespace


class Card(SimpleNamespace):
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
        release_date = None

        if self.release_date:
            release_date = datetime.date.fromisoformat(self.release_date)

        parsed_number = int(re.sub(r"[^\d]+", "", self.number))
        return release_date, parsed_number, self.number

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

        if self.layout == "token":
            return False

        if not self.release_date:
            return False

        if getattr(self, "borderColor", "") in ("gold", "silver"):
            return False

        if hasattr(self, "set") and self.set.type in ("funny", "memorabilia", "promo"):
            return False

        return True