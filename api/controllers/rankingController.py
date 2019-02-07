from flask_restful import Resource
from api.models.ranking import Ranking

class RankingController(Resource):

    def get(self, user_id):
        result = Ranking.find_by_user_id(user_id)

        if result is None or len(result.all()) == 0:
            return {"success" : 0}
        else:
            json_list = [i.serialize for i in result.all()]
            return {"success" : 1, "items": json_list}