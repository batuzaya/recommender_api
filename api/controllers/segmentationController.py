from flask_restful import Resource
from api.library.rfm_segmentation import get_rfm_class_by_id, get_rfm_class

class SegmentationController(Resource):

    def get(self, user_id=None):
        if user_id is not None:
            result = get_rfm_class_by_id(user_id)
        else:
            result = get_rfm_class()

        return result
