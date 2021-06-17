import json
from functools import cached_property
from typing import Callable, ClassVar, Generator, Literal, Optional, Type, Union

from marshmallow import EXCLUDE, Schema, fields
from marshmallow_dataclass import dataclass
from marshmallow_polyfield import PolyField

from magicobjects import CardType, MagicObject, Subtype, Supertype
from utils import camelcase, get_data_path


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonForeignData:
    Schema: ClassVar[Type[Schema]] = Schema
    face_name: Optional[str]  # wrong
    flavor_text: Optional[str]
    language: str
    multiverse_id: Optional[int]
    name: str
    text: Optional[str]
    type: Optional[str]


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonIdentifiers:
    Schema: ClassVar[Type[Schema]] = Schema
    card_kingdom_foil_id: Optional[str]
    card_kingdom_id: Optional[str]
    mcm_id: Optional[str]
    mcm_meta_id: Optional[str]
    mtg_arena_id: Optional[str]
    mtgo_foil_id: Optional[str]
    mtgo_id: Optional[str]
    mtgjson_v4_id: Optional[str]
    multiverse_id: Optional[str]
    scryfall_id: Optional[str]  # wrong
    scryfall_oracle_id: str
    scryfall_illustration_id: Optional[str]
    tcgplayer_product_id: Optional[str]


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonLeadershipSkills:
    Schema: ClassVar[Type[Schema]] = Schema
    brawl: bool
    commander: bool
    oathbreaker: bool


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonLegalities:
    Schema: ClassVar[Type[Schema]] = Schema
    brawl: Optional[str]
    commander: Optional[str]
    duel: Optional[str]
    future: Optional[str]
    frontier: Optional[str]
    gladiator: Optional[str]  # missing
    historic: Optional[str]
    legacy: Optional[str]
    modern: Optional[str]
    oldschool: Optional[str]  # missing
    pauper: Optional[str]
    penny: Optional[str]
    pioneer: Optional[str]
    premodern: Optional[str]  # missing
    standard: Optional[str]
    vintage: Optional[str]


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonPurchaseUrls:
    Schema: ClassVar[Type[Schema]] = Schema
    card_kingdom: Optional[str]
    card_kingdom_foil: Optional[str]
    cardmarket: Optional[str]
    tcgplayer: Optional[str]


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonRulings:
    Schema: ClassVar[Type[Schema]] = Schema
    date: str
    text: str


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonCardAtomic:
    Schema: ClassVar[Type[Schema]] = Schema
    ascii_name: Optional[str]
    color_identity: list[str]
    color_indicator: Optional[list[str]]  # wrong
    colors: list[str]
    converted_mana_cost: float
    edhrec_rank: Optional[int]
    face_converted_mana_cost: Optional[float]
    face_name: Optional[str]
    foreign_data: list[MtgjsonForeignData]
    hand: Optional[str]
    has_alternative_deck_limit: Optional[bool]
    identifiers: MtgjsonIdentifiers
    is_reserved: Optional[bool]
    keywords: Optional[list[str]]
    layout: str
    leadership_skills: Optional[MtgjsonLeadershipSkills]
    legalities: Optional[MtgjsonLegalities]
    life: Optional[str]
    loyalty: Optional[str]
    mana_cost: Optional[str]
    name: str
    power: Optional[str]
    printings: Optional[list[str]]
    purchase_urls: MtgjsonPurchaseUrls
    rulings: list[MtgjsonRulings]
    side: Optional[str]
    subtypes: list[str]
    supertypes: list[str]
    text: Optional[str]
    toughness: Optional[str]
    type: str
    types: list[str]
    uuid: Optional[str]  # wrong


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonCardSet:
    class Meta:
        unknown = EXCLUDE

    Schema: ClassVar[Type[Schema]] = Schema
    availability: list[Literal["arena", "dreamcast", "mtgo", "paper", "shandalar"]]
    border_color: Literal["black", "borderless", "gold", "silver", "white"]
    keywords: Optional[list[str]]
    layout: Literal[
        "adventure",
        "aftermath",
        "art_series",
        "augment",
        "emblem",
        "flip",
        "host",
        "leveler",
        "meld",
        "modal_dfc",
        "normal",
        "planar",
        "saga",
        "scheme",
        "split",
        "transform",
        "vanguard",
    ]
    name: str
    number: str
    original_release_date: Optional[str]
    set_code: str
    subtypes: list[Subtype]
    supertypes: list[Supertype]
    types: list[CardType]


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonCardToken:
    class Meta:
        unknown = EXCLUDE

    Schema: ClassVar[Type[Schema]] = Schema
    availability: list[Literal["arena", "dreamcast", "mtgo", "paper", "shandalar"]]
    border_color: Literal["black", "borderless", "gold", "silver", "white"]
    keywords: Optional[list[str]]
    layout: Literal["token"]
    name: str
    number: str
    original_release_date: Optional[str]
    set_code: str
    subtypes: list[Subtype]
    supertypes: list[Supertype]
    types: list[CardType]


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonMeta:
    Schema: ClassVar[Type[Schema]] = Schema
    date: str
    version: str


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonCardAtomicFile:
    Schema: ClassVar[Type[Schema]] = Schema
    data: dict[str, list[MtgjsonCardAtomic]]
    meta: MtgjsonMeta


def card_set_serialization_disambiguation(base_object, _):
    class_to_schema = {
        MtgjsonCardSet.__name__: MtgjsonCardSet.Schema(),
        MtgjsonCardToken.__name__: MtgjsonCardToken.Schema(),
    }
    try:
        return class_to_schema[base_object.__class__.__name__]()
    except KeyError:
        pass


def card_set_deserialization_disambiguation(object_dict, _):
    if object_dict.get("layout") == "token":
        return MtgjsonCardToken.Schema()

    return MtgjsonCardSet.Schema()


class MtgjsonAllIdentifiersFileSchema(CamelCaseSchema):
    data = fields.Dict(
        keys=fields.Str(),
        values=PolyField(
            serialization_schema_selector=card_set_serialization_disambiguation,
            deserialization_schema_selector=card_set_deserialization_disambiguation,
        ),
    )
    meta = fields.Nested(MtgjsonMeta.Schema())


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonSealedProduct:
    Schema: ClassVar[Type[Schema]] = Schema
    identifiers: dict[str, str]
    name: str
    purchase_urls: dict[str, str]
    release_date: Optional[str]
    uuid: str


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonSetList:
    Schema: ClassVar[Type[Schema]] = Schema
    base_set_size: int
    block: Optional[str]
    code: str
    code_v3: Optional[str]
    is_foreign_only: Optional[bool]
    is_foil_only: bool
    is_non_foil_only: Optional[bool]
    is_online_only: bool
    is_paper_only: Optional[bool]
    is_partial_preview: Optional[bool]
    keyrune_code: str
    mcm_id: Optional[int]
    mcm_id_extras: Optional[int]
    mcm_name: Optional[str]
    mtgo_code: Optional[str]
    name: str
    parent_code: Optional[str]
    release_date: str
    tcgplayer_group_id: Optional[int]
    total_set_size: int
    translations: dict[str, Optional[str]]  # not optional in docs
    type: str
    sealed_product: Optional[list[MtgjsonSealedProduct]]  # missing


@dataclass(base_schema=CamelCaseSchema)
class MtgjsonSetListFile:
    Schema: ClassVar[Type[Schema]] = Schema
    data: list[MtgjsonSetList]
    meta: MtgjsonMeta


def legal_card_filter(card):
    if "Card" in card.types:
        return False

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


class MtgjsonData:
    def __init__(self):
        self._all_identifiers: list[Union[MtgjsonCardSet, MtgjsonCardToken]] = None
        self._atomic_cards: list[MtgjsonCardAtomic] = None
        self._set_list: list[MtgjsonSetList] = None
        self._creature_types: list[Subtype] = None

    def get_card_by_name(self, name: str):
        objects = self.load_objects()
        card = next(
            (c for c in objects if c.name == name),
            None,
        )
        assert card is not None
        return card

    @cached_property
    def all_identifiers(self) -> list[Union[MtgjsonCardSet, MtgjsonCardToken]]:
        if self._all_identifiers is None:
            self._all_identifiers = self._load_all_identifiers()
        return self._all_identifiers

    def _load_all_identifiers(self) -> list[Union[MtgjsonCardSet, MtgjsonCardToken]]:
        with get_data_path("mtgjson/AllIdentifiers.json").open() as f:
            all_identifiers = MtgjsonAllIdentifiersFileSchema().loads(f.read())
            return all_identifiers["data"]

    @cached_property
    def atomic_cards(self) -> list[MtgjsonCardAtomic]:
        if self._atomic_cards is None:
            self._atomic_cards = self._load_atomic_cards()
        return self._atomic_cards

    def _load_atomic_cards(self) -> list[MtgjsonCardAtomic]:
        with get_data_path("mtgjson/AtomicCards.json").open() as f:
            atomic_cards = MtgjsonCardAtomicFile.Schema().loads(f.read())
            return atomic_cards.data

    @cached_property
    def set_list(self) -> list[MtgjsonSetList]:
        if self._set_list is None:
            self._set_list = self._load_set_list()
        return self._set_list

    def _load_set_list(self) -> list[MtgjsonSetList]:
        with get_data_path("mtgjson/SetList.json").open() as f:
            set_list = MtgjsonSetListFile.Schema().loads(f.read())
            return set_list.data

    @cached_property
    def creature_types(self) -> set[Subtype]:
        if self._creature_types is None:
            self._creature_types = self._load_creature_types()
        return self._creature_types

    def _load_creature_types(self) -> set[Subtype]:
        with get_data_path("mtgjson/CardTypes.json").open() as f:
            card_types_data = json.load(f)["data"]
        creature_types = card_types_data["creature"]["subTypes"]
        # mtgjson includes some illegal creature types
        unwanted_types = ("Chicken", "Head", "Hornet", "Reveler", "Rukh", "Wasp")
        return set(t for t in creature_types if t not in unwanted_types)

    def load_objects(
        self, filterfunc: Optional[Callable[[MagicObject], bool]] = legal_card_filter
    ) -> Generator[MagicObject, None, None]:
        MagicObject.all_creature_types = self.creature_types

        sets = {s.code: s for s in self.set_list}
        MagicObject.sets = sets

        for card in self.all_identifiers.values():
            magic_obj = MagicObject(
                name=card.name,
                types=set(card.types),
                subtypes=set(card.subtypes),
                supertypes=set(card.supertypes),
                keywords=set(card.keywords) if card.keywords is not None else set(),
                set_code=card.set_code,
                set_release_date=sets[card.set_code].release_date
                if card.set_code in sets
                else None,
                set_type=sets[card.set_code].type if card.set_code in sets else None,
                original_release_date=card.original_release_date,
                number=card.number,
                border_color=card.border_color,
                availability=set(card.availability),
                layout=card.layout,
                subtype_order={t: i for i, t in enumerate(card.subtypes)},
            )

            if filterfunc and not filterfunc(magic_obj):
                continue

            yield magic_obj


if __name__ == "__main__":
    mtgjsondata = MtgjsonData()
    print(len(mtgjsondata.all_identifiers))
