import pandas as pd


def load_data(path_csv = "data/raw/notifications.csv"):
    """Loads the notification csv file
    """

    df = pd.read_csv(path_csv, sep=",", header=None, names=['timestamp','user_id','friend_id','friend_name'])

    print(df.head())

    return df