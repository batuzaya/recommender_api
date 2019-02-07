from api import app, config
from flask_restful import Api
from api.controllers import rankingController, segmentationController

api = Api(app)

api.add_resource(rankingController.RankingController, '/api/ranking/<int:user_id>')
api.add_resource(segmentationController.SegmentationController, '/api/segmentation', '/api/segmentation/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)
