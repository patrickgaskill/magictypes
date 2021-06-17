from typing import ClassVar, Literal, Optional, Type

from marshmallow import Schema
from marshmallow_dataclass import dataclass

from utils import get_data_path

# from marshmallow_dataclass.typing import Url


Colors = list[Literal["W", "U", "B", "R", "G", "C"]]  # C is missing from docs
Layout = Literal[
    "normal",
    "split",
    "flip",
    "transform",
    "modal_dfc",
    "meld",
    "leveler",
    "saga",
    "adventure",
    "planar",
    "scheme",
    "vanguard",
    "token",
    "double_faced_token",
    "emblem",
    "augment",
    "host",
    "art_series",
    "double_sided",
]
Frame = Literal["1993", "1997", "2003", "2015", "future"]
FrameEffects = Literal[
    "legendary",
    "miracle",
    "nyxtouched",
    "draft",
    "devoid",
    "tombstone",
    "colorshifted",
    "inverted",
    "sunmoondfc",
    "compasslanddfc",
    "originpwdfc",
    "mooneldrazidfc",
    "waxingandwaningmoondfc",
    "showcase",
    "extendedart",
    "companion",
    "etched",
    "snow",
    "nyxborn",  # missing
    "fullart",  # missing
]
CardImagery = dict[
    Literal["png", "border_crop", "art_crop", "large", "normal", "small"], str
]


@dataclass
class ScryfallCardFace:
    Schema: ClassVar[Type[Schema]] = Schema
    artist: Optional[str]
    artist_id: Optional[str]  # UUID
    color_indicator: Optional[Colors]
    colors: Optional[Colors]
    flavor_text: Optional[str]
    illustration_id: Optional[str]  # UUID
    image_uris: Optional[CardImagery]
    loyalty: Optional[str]
    mana_cost: str
    name: str
    object: Literal["card_face"]
    oracle_text: Optional[str]
    power: Optional[str]
    printed_name: Optional[str]
    printed_text: Optional[str]
    printed_type_line: Optional[str]
    toughness: Optional[str]
    type_line: str
    watermark: Optional[str]


@dataclass
class ScryfallRelatedCardObject:
    id: str  # UUID
    object: Literal["related_card"]
    component: Literal["token", "meld_part", "meld_result", "combo_piece"]
    name: str
    type_line: str
    uri: str


@dataclass
class ScryfallCard:
    Schema: ClassVar[Type[Schema]] = Schema

    # Core card fields
    arena_id: Optional[int]
    id: str  # UUID
    lang: str
    mtgo_id: Optional[int]
    mtgo_foil_id: Optional[int]
    multiverse_ids: Optional[list[int]]
    tcgplayer_id: Optional[int]
    cardmarket_id: Optional[int]
    object: Literal["card"]
    oracle_id: str  # UUID
    prints_search_uri: str
    rulings_uri: str
    scryfall_uri: str
    uri: str

    # Gameplay fields
    all_parts: Optional[list[ScryfallRelatedCardObject]]
    card_faces: Optional[list[ScryfallCardFace]]
    cmc: float
    color_identity: Colors
    color_indicator: Optional[Colors]
    colors: Optional[Colors]
    edhrec_rank: Optional[int]
    foil: bool
    hand_modifier: Optional[str]
    keywords: list[str]
    layout: Layout
    legalities: dict[str, Literal["legal", "not_legal", "restricted", "banned"]]
    life_modifier: Optional[str]
    loyalty: Optional[str]
    mana_cost: Optional[str]
    name: str
    nonfoil: bool
    oracle_text: Optional[str]
    oversized: bool
    power: Optional[str]
    produced_mana: Optional[Colors]
    reserved: bool
    toughness: Optional[str]
    type_line: str

    # Print fields
    artist: Optional[str]
    artist_ids: Optional[list[str]]  # UUIDs, missing
    booster: bool
    border_color: Literal["black", "borderless", "gold", "silver", "white"]
    card_back_id: str  # UUID
    collector_number: str
    content_warning: Optional[bool]
    digital: bool
    flavor_name: Optional[str]
    flavor_text: Optional[str]
    frame_effects: Optional[list[FrameEffects]]
    frame: Frame
    full_art: bool
    games: list[
        Literal["paper", "arena", "mtgo", "astral", "sega"]
    ]  # astral, sega missing from docs
    highres_image: bool
    illustration_id: Optional[str]  # UUID
    image_status: Literal["missing", "placeholder", "lowres", "highres_scan"]
    image_uris: Optional[CardImagery]
    prices: dict[Literal["usd", "usd_foil", "eur", "eur_foil", "tix"], Optional[str]]
    printed_name: Optional[str]
    printed_text: Optional[str]
    printed_type_line: Optional[str]
    promo: bool
    promo_types: Optional[list[str]]
    purchase_uris: Optional[dict[str, str]]  # actually optional
    rarity: Literal["common", "uncommon", "rare", "special", "mythic", "bonus"]
    related_uris: dict[str, str]
    released_at: str
    reprint: bool
    scryfall_set_uri: str
    set_name: str
    set_search_uri: str
    set_type: str
    set_uri: str
    set: str
    story_spotlight: bool
    textless: bool
    variation: bool
    variation_of: Optional[str]  # UUID
    watermark: Optional[str]
    preview: Optional[dict[str, str]]


class ScryfallData:
    def __init__(self):
        self.default_cards = self.load_default_cards()

    def load_default_cards(self):
        with get_data_path("scryfall/default_cards.json").open() as default_cards_file:
            schema = ScryfallCard.Schema()
            return schema.loads(default_cards_file.read(), many=True)
