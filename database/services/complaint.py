from database.services.base import BaseService

from ..models.complaint import ProfileComplaintsModel


class Complaint(BaseService):
    model = ProfileComplaintsModel
