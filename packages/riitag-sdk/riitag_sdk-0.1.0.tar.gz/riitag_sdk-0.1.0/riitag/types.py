from typing import TypedDict


class User(TypedDict):
    id: str
    name: str


class LastPlayed(TypedDict):
    game_id: str
    console: str
    region: str
    cover_url: str
    time: int


class TagUrl(TypedDict):
    normal: str
    max: str


class GameData(TypedDict):
    last_played: LastPlayed
    games: list[str]


class Tag(TypedDict):
    user: User
    tag_url: TagUrl
    game_data: GameData
