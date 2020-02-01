"""Main module."""
import pandas as pd


def load_data(path_csv = "https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv", nrows=None):
    """Loads the notification csv file

    Parameters
    ----------
    path_csv : str, optional
        Path to the csv file containing the data. It should have 4 comma-separated columns
    
    nrows : int, optional
        Number of rows of file to read. Useful for reading pieces of large files or for testing this function.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the stream of data. It has 4 columns:  'timestamp','user_id','friend_id','friend_name'
        The column named 'timestamp' is cast as a datetime64[ns] type.

    """

    df = pd.read_csv(path_csv, sep=",", header=None, names=['timestamp','user_id','friend_id','friend_name'],
    parse_dates = ['timestamp'], nrows=nrows)

    return df



def add_message(x):
    """Creates a notification message based on a row of a dataFrame. It should at least contain two fields: 'message' and 'tours'.
    This function is meant to be called from a pd.DataFrame.apply
    
    Parameters
    ----------
    x : pd.DataFrame
        should be a single row of a pandas DataFrame.

    Returns
    -------
    str
        Notification message

    """

    if x.tours == 1:
        return f"{x.message} went on a tour"
    elif x.tours == 2:
        return f"{x.message} and {x.tours-1} other went on a tour"
    elif x.tours >= 3:
        return f"{x.message} and {x.tours-1} others went on a tour"
    else:
        raise ValueError(f'NUmber of tours not recognized. {x}')


def bundle_func(df_g):
    """Bundles notifications for a user_id

    This function is meant to be used after a pandas groupping (or manual filtering) of user_ids. It creates three new columns: 'timestamp_first_tour', 'tours' and 'message'

    Parameters
    ----------
    df_g : pd.DataFrame
        DataFrame containing 3 columns: 'timestamp_first_tour','tours','message'

    Returns
    -------
    pd.DataFrame
        Contains 3 extra columns as explained above

    """
    
    # Create number of tours. 1 - df.duplicated() marks True on the first occurrence.
    # Cumsum adds a counter when a new ocurrence (aka. friend_id) comes up
    df_g['tours']  = (1-df_g.friend_id.duplicated()).cumsum()
    
    # Simply get the first value of the tour. Make sure it has been sorted!
    df_g['timestamp_first_tour'] = df_g.timestamp.values[0]
    
    # Add message.
    df_g['message'] = df_g.friend_name.values[0]
    df_g['message'] = df_g.apply(add_message, axis=1)
    
    return df_g