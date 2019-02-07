import pandas as pd
from datetime import datetime

from daemon import remote_db


def input_from_db():
    cursor = remote_db.cursor()

    # Execute SQL select statement
    cursor.execute(
        "SELECT a.id, b.user_id, a.agent_id, a.amount, a.status, a.created_at FROM orders as a LEFT JOIN agents as b ON a.agent_id = b.id")

    # Get the number of rows in the resultset
    numrows = cursor.rowcount

    data = []

    # Get and display one row at a time
    for x in range(0, numrows):
        row = cursor.fetchone()
        item = {}
        item['order_id'] = row[0]
        item['user_id'] = row[1]
        item['agent_id'] = row[2]
        item['amount'] = row[3]
        item['status'] = row[4]
        item['order_date'] = pd.to_datetime(row[5], format='%yyyy-%mm-%dd %H:%M:%S')

        data.append(item)

    # Close the connection
    remote_db.close()

    return pd.DataFrame(data)


def rfm(orders):
    print "---------------------------------------------"
    print " Calculating RFM segmentation"
    print "---------------------------------------------"

    NOW = datetime.now()

    rfmTable = orders.groupby('agent_id').agg({'order_date': lambda x: (NOW - x.max()).days,  # Recency
                                               'order_id': lambda x: len(x),  # Frequency
                                               'amount': lambda x: x.sum(),  # Monetary Value
                                               'user_id': lambda x: x.max()})

    rfmTable['order_date'] = rfmTable['order_date'].astype(int)
    rfmTable.rename(columns={'order_date': 'recency',
                             'order_id': 'frequency',
                             'amount': 'monetary_value'}, inplace=True)

    quantiles = rfmTable.quantile(q=[0.25, 0.5, 0.75])
    quantiles = quantiles.to_dict()

    rfmSegmentation = rfmTable

    rfmSegmentation['R_Quartile'] = rfmSegmentation['recency'].apply(RClass, args=('recency', quantiles,))
    rfmSegmentation['F_Quartile'] = rfmSegmentation['frequency'].apply(FMClass, args=('frequency', quantiles,))
    rfmSegmentation['M_Quartile'] = rfmSegmentation['monetary_value'].apply(FMClass,
                                                                            args=('monetary_value', quantiles,))

    rfmSegmentation['RFMClass'] = rfmSegmentation.R_Quartile.map(str) \
                                  + rfmSegmentation.F_Quartile.map(str) \
                                  + rfmSegmentation.M_Quartile.map(str)

    return rfmSegmentation


# We create two classes for the RFM segmentation since, being high recency is bad, while high frequency and monetary value is good.
# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def RClass(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4


# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def FMClass(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1


def get_rfm_class_by_id(user_id):
    input_data = input_from_db()

    rfm_result = rfm(input_data)

    item = rfm_result.loc[rfm_result['user_id'] == user_id]

    return {
        'R_Quartile': item['R_Quartile'].iloc[0],
        'F_Quartile': item['F_Quartile'].iloc[0],
        'M_Quartile': item['M_Quartile'].iloc[0],
        'RFMClass': item['RFMClass'].iloc[0]
    }


def get_rfm_class():
    input_data = input_from_db()

    rfm_result = rfm(input_data)

    list = []

    for index, item in rfm_result.iterrows():
        list.append({
            'R_Quartile': item['R_Quartile'],
            'F_Quartile': item['F_Quartile'],
            'M_Quartile': item['M_Quartile'],
            'RFMClass': item['RFMClass'],
            'user_id': int(item['user_id']),
        })

    return list