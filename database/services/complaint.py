
from database.services.base import BaseService

from ..models.complaint import ProfileCompleintsModel


class Compleint(BaseService):
    model = ProfileCompleintsModel
