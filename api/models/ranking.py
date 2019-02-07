from api import db
from sqlalchemy.orm.exc import NoResultFound

class Ranking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    agent_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, agent_id, item_id, rating):
        """ Setup the class """
        self.user_id = user_id
        self.agent_id = agent_id
        self.item_id = item_id
        self.rating = rating

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            # 'user_id': self.user_id,
            'item_id': self.item_id
        }

    @staticmethod
    def clear():
        """ Remove all items """

        # try:
        #     db.session.query(Ranking).delete()
        #     db.session.commit()
        # except:
        #     db.session.rollback()

        db.engine.execute("TRUNCATE TABLE ranking;")

    @staticmethod
    def find_by_user_id(user_id, limit=5):
        """ Get items by user_id """
        try:
            return db.session.query(Ranking).\
                filter(Ranking.user_id == user_id).\
                limit(limit)
        except NoResultFound:
            return None

    @staticmethod
    def find_by_agent_id(agent_id, limit=5):
        """ Get items by agent_id """
        try:
            return db.session.query(Ranking).\
                filter(Ranking.agent_id == agent_id).\
                limit(limit)
        except NoResultFound:
            return None