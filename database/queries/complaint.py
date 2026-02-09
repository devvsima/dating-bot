from database.queries.base import BaseService

from ..models.complaint import ProfileComplaintModel


class Complaint(BaseService):
    model = ProfileComplaintModel
