"""
Pydantic модели для API запросов и ответов
"""

from pydantic import BaseModel


class LikeRequest(BaseModel):
    """Запрос для лайка анкеты"""

    user_id: int
    target_id: int
    message: str | None = None


class ComplaintRequest(BaseModel):
    """Запрос для жалобы на анкету"""

    user_id: int
    target_id: int
    reason: str


class ProfileResponse(BaseModel):
    """Ответ с данными профиля"""

    id: int
    username: str | None
    name: str
    age: int
    gender: str
    city: str
    description: str | None
    instagram: str | None
    photos: list[str]


class SearchProfileResponse(BaseModel):
    """Профиль в результатах поиска"""

    id: int
    user_id: int
    username: str | None
    name: str
    age: int
    gender: str
    city: str
    description: str | None
    instagram: str | None
    photos: list[str]


class SearchResponse(BaseModel):
    """Ответ со списком анкет"""

    profiles: list[SearchProfileResponse]
    total: int


class ActionResponse(BaseModel):
    """Стандартный ответ на действие"""

    status: str
    message: str
    is_new: bool | None = None
