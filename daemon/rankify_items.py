import argparse
import tensorflow as tf
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from daemon.models.item_ranking.cdae import ICDAE
from daemon.utils.load_data.load_data_ranking import load_data_db, load_data_only

from api import db
from api.models.ranking import Ranking


def parse_args():
    parser = argparse.ArgumentParser(description='DeepRec')
    parser.add_argument('--epochs', type=int, default=40)
    parser.add_argument('--num_factors', type=int, default=10)
    parser.add_argument('--display_step', type=int, default=1000)
    parser.add_argument('--batch_size', type=int, default=1024)  # 128 for unlimpair
    parser.add_argument('--learning_rate', type=float, default=1e-3)  # 1e-4 for unlimpair
    parser.add_argument('--reg_rate', type=float, default=0.1)  # 0.01 for unlimpair
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    epochs = args.epochs
    learning_rate = args.learning_rate
    reg_rate = args.reg_rate
    num_factors = args.num_factors
    display_step = args.display_step
    batch_size = args.batch_size

    config = tf.ConfigProto(log_device_placement=True)
    config.gpu_options.allow_growth = True
    user_array = []
    item_array = []

    with tf.Session(config=config) as sess:
        model = None
        # Model selection
        print ('===============================Data loading start===================================')
        # n_user, n_item, user_array, item_array, agent_user_dict = load_data_only()
        train_data, test_data, n_user, n_item, user_array, item_array, agent_user_dict = load_data_db(test_size=0.2)
        print ('===============================Data loading finished================================')
        model = ICDAE(sess, n_user, n_item, epoch=epochs)

        # build and execute the model
        if model is not None:

            model.build_network()
            model.execute(train_data, test_data)

            print ('===============================Ranking items================================')
            Ranking.clear()

            for u in range(len(user_array)):
                temp_list = []
                for i in range(len(item_array)):
                    value = {
                        'item_id': item_array[i],
                        'rating': model.predict(u, i).item()
                    }
                    temp_list.append(value)

                sorted_list = sorted(temp_list, key=lambda k: k['rating'], reverse=True)

                for i in range(min(15, len(sorted_list))):
                    item = Ranking(
                        user_id=agent_user_dict[user_array[u]],
                        agent_id=user_array[u],
                        item_id=sorted_list[i]['item_id'],
                        rating=sorted_list[i]['rating']
                    )
                    db.session.add(item)

                db.session.commit()