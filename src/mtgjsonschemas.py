from typing import ClassVar, Literal, Optional, Type

from marshmallow import EXCLUDE, Schema, fields
from marshmallow_dataclass import dataclass
from marshmallow_polyfield import PolyField
from rich.console import Console
from rich.pretty import pprint

from magicobjects import CardType, Subtype, Supertype
from utils import camelcase, get_data_json


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


@dataclass(base_schema=CamelCaseSchema)
class ForeignData:
    Schema: ClassVar[Type[Schema]] = Schema
    face_name: Optional[str]  # wrong
    flavor_text: Optional[str]
    language: str
    multiverse_id: Optional[int]
    name: str
    text: Optional[str]
    type: Optional[str]


@dataclass(base_schema=CamelCaseSchema)
class Identifiers:
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
class LeadershipSkills:
    Schema: ClassVar[Type[Schema]] = Schema
    brawl: bool
    commander: bool
    oathbreaker: bool


@dataclass(base_schema=CamelCaseSchema)
class Legalities:
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
class PurchaseUrls:
    Schema: ClassVar[Type[Schema]] = Schema
    card_kingdom: Optional[str]
    card_kingdom_foil: Optional[str]
    cardmarket: Optional[str]
    tcgplayer: Optional[str]


@dataclass(base_schema=CamelCaseSchema)
class Rulings:
    Schema: ClassVar[Type[Schema]] = Schema
    date: str
    text: str


@dataclass(base_schema=CamelCaseSchema)
class AtomicCard:
    Schema: ClassVar[Type[Schema]] = Schema
    ascii_name: Optional[str]
    color_identity: list[str]
    color_indicator: list[str]  # wrong
    colors: list[str]
    converted_mana_cost: float
    edhrec_rank: Optional[int]
    face_converted_mana_cost: Optional[float]
    face_name: Optional[str]
    foreign_data: list[ForeignData]
    hand: Optional[str]
    has_alternative_deck_limit: Optional[bool]
    identifiers: Identifiers
    is_reserved: Optional[bool]
    keywords: Optional[list[str]]
    layout: str
    leadership_skills: Optional[LeadershipSkills]
    legalities: Optional[Legalities]
    life: Optional[str]
    loyalty: Optional[str]
    mana_cost: Optional[str]
    name: str
    power: Optional[str]
    printings: Optional[list[str]]
    purchase_urls: PurchaseUrls
    rulings: list[Rulings]
    side: Optional[str]
    subtypes: list[str]
    supertypes: list[str]
    text: Optional[str]
    toughness: Optional[str]
    type: str
    types: list[str]
    uuid: Optional[str]  # wrong


@dataclass(base_schema=CamelCaseSchema)
class SetCard:
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
class TokenCard:
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
class Meta:
    Schema: ClassVar[Type[Schema]] = Schema
    date: str
    version: str


@dataclass(base_schema=CamelCaseSchema)
class AtomicCardsFile:
    Schema: ClassVar[Type[Schema]] = Schema
    data: dict[str, list[AtomicCard]]
    meta: Meta


def card_set_serialization_disambiguation(base_object, _):
    class_to_schema = {
        SetCard.__name__: SetCard.Schema(),
        TokenCard.__name__: TokenCard.Schema(),
    }
    try:
        return class_to_schema[base_object.__class__.__name__]()
    except KeyError:
        pass


def card_set_deserialization_disambiguation(object_dict, _):
    if object_dict.get("layout") == "token":
        return TokenCard.Schema()

    return SetCard.Schema()


class AllIdentifiersFileSchema(CamelCaseSchema):
    data = fields.Dict(
        keys=fields.Str(),
        values=PolyField(
            serialization_schema_selector=card_set_serialization_disambiguation,
            deserialization_schema_selector=card_set_deserialization_disambiguation,
        ),
    )
    meta = fields.Nested(Meta.Schema())


@dataclass(base_schema=CamelCaseSchema)
class SealedProduct:
    Schema: ClassVar[Type[Schema]] = Schema
    identifiers: dict[str, str]
    name: str
    purchase_urls: dict[str, str]
    release_date: Optional[str]
    uuid: str


@dataclass(base_schema=CamelCaseSchema)
class SetList:
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
    sealed_product: Optional[list[SealedProduct]]  # missing


@dataclass(base_schema=CamelCaseSchema)
class SetListFile:
    Schema: ClassVar[Type[Schema]] = Schema
    data: list[SetList]
    meta: Meta


console = Console()


def validate_file(name: str, schema: Schema):
    with console.status(f"Validating {name}...", spinner="dots"):
        errors = schema.validate(get_data_json(f"mtgjson/{name}.json"))

    if errors:
        pprint(errors["data"], max_length=10, console=console)
        console.print(f"❌ [bold red]{name} had {len(errors['data'])} errors")
    else:
        console.print(f"✅ [bold green]{name} validated")


def main():
    file_schemas = {
        "SetList": SetListFile.Schema(),
        "AtomicCards": AtomicCardsFile.Schema(),
        "AllIdentifiers": AllIdentifiersFileSchema(),
    }

    for name, schema in file_schemas.items():
        validate_file(name, schema)


if __name__ == "__main__":
    main()
