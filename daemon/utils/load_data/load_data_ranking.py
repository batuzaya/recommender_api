import pandas as pd
import numpy as np
import collections

from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix

from daemon import remote_db

def load_data_only():
    cursor = remote_db.cursor()

    # Execute SQL select statement
    cursor.execute(
        "SELECT b.user_id, a.agent_id, a.package_id FROM orders as a LEFT JOIN agents as b ON a.agent_id = b.id WHERE a.amount != 0.00")

    # Get the number of rows in the resultset
    myresult = cursor.fetchall()

    user_array = []
    item_array = []
    agent_user_dict = collections.defaultdict(list)

    i = 0
    for row in myresult:
        if row[1] is None or row[2] is None:
            continue
        user_array.append(row[1])
        item_array.append(row[2])
        agent_user_dict[row[1]] = row[0]

    unique_users = np.unique(user_array)
    unique_items = np.unique(item_array)

    n_users = len(unique_users)
    n_items = len(unique_items)

    # Close the connection
    remote_db.close()

    return n_users, n_items, unique_users, unique_items, agent_user_dict

def load_data_db(test_size=0.2):
    cursor = remote_db.cursor()

    # Execute SQL select statement
    cursor.execute("SELECT b.user_id, a.agent_id, a.package_id FROM orders as a LEFT JOIN agents as b ON a.agent_id = b.id WHERE a.amount != 0.00")

    # Get the number of rows in the resultset
    myresult = cursor.fetchall()

    train_row = []
    train_col = []
    train_rating = []
    train_dict = {}

    test_data = []
    test_row = []
    test_col = []
    test_rating = []
    test_dict = {}

    user_array = []
    item_array = []
    new_result = []
    agent_user_dict = collections.defaultdict(list)

    i = 0
    for row in myresult:
        if row[1] is None or row[2] is None:
            continue
        new_result.append([row[1], row[2]])
        user_array.append(row[1])
        item_array.append(row[2])
        agent_user_dict[row[1]] = row[0]

    train_data, test_data = train_test_split(new_result, test_size=test_size)
    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)

    for row in train_data.itertuples():
        user = row[1]
        item = row[2]
        train_dict[(user, item)] = 1

    unique_users = np.unique(user_array)
    unique_items = np.unique(item_array)

    n_users = len(unique_users)
    n_items = len(unique_items)

    for u in range(n_users):
        for i in range(n_items):
            train_row.append(u)
            train_col.append(i)
            if (u, i) in train_dict.keys():
                train_rating.append(1)
            else:
                train_rating.append(0)

    train_matrix = csr_matrix((train_rating, (train_row, train_col)), shape=(n_users, n_items))
    all_items = set(np.arange(n_items))

    neg_items = {}
    train_interaction_matrix = []
    for u in range(n_users):
        neg_items[u] = list(all_items - set(train_matrix.getrow(u).nonzero()[1]))
        train_interaction_matrix.append(list(train_matrix.getrow(u).toarray()[0]))

    for line in test_data.itertuples():
        test_row.append(line[1])
        test_col.append(line[2])
        test_rating.append(1)

    # test_matrix = csr_matrix((test_rating, (test_row, test_col)), shape=(n_users, n_items))
    test_matrix = train_matrix

    for u in range(n_users):
        test_dict[u] = test_matrix.getrow(u).nonzero()[1]

    # Close the connection
    remote_db.close()

    return train_interaction_matrix, test_dict, n_users, n_items, unique_users, unique_items, agent_user_dict

if __name__ == '__main__':
    load_data_db(test_size=0.2)
