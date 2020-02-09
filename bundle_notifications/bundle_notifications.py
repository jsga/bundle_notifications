"""Main module."""
import pandas as pd
import numpy as np

from .optimal_delay import local_search


def load_data(path_csv, nrows=None):
    """Loads the notification csv file

    Parameters
    ----------
    path_csv : str, optional
        Path or url to the csv file containing the data. It should have 4
        comma-separated columns without header.

    nrows : int, optional
        Number of rows of file to read. Useful for reading pieces of large
        files or for testing this function.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the stream of data. It has 4 columns:
        ``'timestamp','user_id','friend_id','friend_name'``.
        The column named 'timestamp' is cast as a datetime64[ns] type.
    """

    df = pd.read_csv(path_csv, sep=",", header=None, names=[
        'timestamp', 'user_id', 'friend_id', 'friend_name'],
        parse_dates=['timestamp'], nrows=nrows)

    return df


def create_message(tours, name_first):
    """Returns the notification message as a numpy array

    Parameters
    ----------
    tours : np.array of in
        array of integers representing the number of tours
    name_first : np.array
        array of names

    Returns
    -------
    np.array
        array with the message like "Mona and 12 others went on a tour"
    """
    # Allocate solution
    message_array = np.empty(len(tours), dtype='<U256')

    for i, (t, n) in enumerate(zip(tours, name_first)):
        message_array[i] = create_message_single(t, n)

    return message_array


def create_message_single(t, n):
    """Creates custom message based on the number of tours and the friend name

    Parameters
    ----------
    t : int
        Number of tours
    n : str
        Name of the friend

    Returns
    -------
    str
        Notification message
    """

    if t == 1:
        return str(n) + " went on a tour"
    elif t == 2:
        return str(n) + " and 1 other went on a tour"
    elif t >= 3:
        return str(n) + " and " + str(t-1) + " others went on a tour"
    else:
        raise ValueError(f'Number of tours not recognized.' + str(n))


def add_notif_counter(x):
    """Creates a counter given a solution x

    Equivalent function to::

        df_g['notification_bool'] = False
        df_g.notification_bool.iloc[x] = True

        # Now do a cumsum counter
        df_g['notification_counter'] =
            df_g.notification_bool.cumsum().shift()+1
        df_g.notification_counter.iloc[0] = 1

    Computationally it is 50x faster to do it this way::

        print('With @jit:')
        %time n1 = add_notif_counter_j(x,np.zeros(x[-1]+1,dtype='int'))
        print('Without @jit:')
        %time n2 = add_notif_counter(x)
        print('With pandas:')
        %time n3 = notif_counter_pandas(df_g)
        # Recall that 1ms = 1000 ms. So it is 95x faster

        np.allclose(n1,n2.astype("int") )
        np.allclose(n2,n3.astype("int") )

        >> With @jit:
        >> CPU times: user 22 µs, sys: 0 ns, total: 22 µs
        >> Wall time: 26.9 µs
        >> Without @jit:
        >> CPU times: user 25 µs, sys: 1 µs, total: 26 µs
        >> Wall time: 29.1 µs
        >> With pandas:
        >> CPU times: user 2.62 ms, sys: 705 µs, total: 3.33 ms
        >> Wall time: 2.73 ms

    Parameters
    ----------
    x : np.array of int
        Array of length 4 with. Each element is an index, indicating the
        timestamp when the notification should be sent.
        Example: ``x = np.array([0,1,2,5])``

    Returns
    -------
    np.array of int
        Numpy array containing a counter, starting from 1 up to 4
    """
    notification_counter = np.zeros(x[-1]+1, dtype='int')
    notification_counter[:x[0]+1] = 1
    notification_counter[x[0]+1:x[1]+1] = 2
    notification_counter[x[1]+1:x[2]+1] = 3
    notification_counter[(x[2]+1):] = 4

    return notification_counter


def count_tours_per_notif(notification_counter, friend_id, friend_name,
                          timestamp):
    """Count number of friends that went on a tour during a given time,
    indicated by a counter.

    Equivalent to::

        df_g['tours'] =
            df_g.groupby('notification_counter')['friend_id'].apply(
                    lambda x:(1- x.duplicated()).cumsum()
                    )

    In pseudo-code, this is equivalent to:

    - As an input, we have a dataset filtered by user_id and day of the year
    - Each of the inputs of this function are numpy arrays, corresponding to a
      column of the dataset. Doing basic in numpy is much faster, especially if
      we manage to use a @jit compilator (TODO)
    - Let us call the solution _tours_. For each element in friend_id we do:
        - Start tours = 1 at iteration i=0
        - We add tours += 1 if the friend_id is new.
        - We continue until i in notification_counter
            - Reset tours = 1
            - Keep track of the name and timestamp of the first element
                (name_first,timestamp_first_tour)

    Parameters
    ----------
    notification_counter : np.array
        notification counter. Could be the output of an optimal_delay method.
        For example, ``np.array([1,2,3,10])`` for a 10 element array
    friend_id : np.array of str
        array containing names of the friends
    friend_name : np.array of str
        array containing names of the friends
    timestamp: np.array of datetime64[ns]
        timestamps when the notifications are generated

    Returns
    -------
    tours : np.array of int
        Count of the number of tours done since the last notification was sent,
        for unique friends-id
    name_first : np.array of <U256
        Names of the friend who first did a tour since the last notification was
        sent.
        len(name_first) <=4
    timestamp_first_tour : np.array of datetime64[ns]
        Timestamp of the first tour done by a friend, since the last
        notification was sent.
        ``len(timestamp_first_tour) <=4``
    message : np.array of np.array of <U256
        Message to be sent.
        ``len(message) <= 4``
    """
    # Allocate solution
    N = len(notification_counter)
    tours = np.zeros(N, dtype='int')
    tours_counter = 1

    message = np.empty(4, dtype='<U256')

    # First name and timestamp is always kept
    name_first = np.empty(4, dtype='<U256')
    name_first[0] = friend_name[0]

    timestamp_first_tour = np.zeros(4, dtype='datetime64[ns]')
    timestamp_first_tour[0] = timestamp[0]

    # Aux counter and hash table
    prev_counter = notification_counter[0]  # == 1
    frend_id_hash = set({friend_id[0]})

    for i in range(0, N):

        if prev_counter == notification_counter[i]:
            # do the counting
            if friend_id[i] not in frend_id_hash:
                # New friend. Add one more tour
                tours_counter += 1
                # Add friend to set
                frend_id_hash.add(friend_id[i])
            tours[i] = tours_counter

        else:
            # Create message
            message[prev_counter-1] = create_message_single(
                tours_counter, name_first[prev_counter-1])

            # Keep name and timestamp of reset index (aka, first friend)
            name_first[prev_counter] = friend_name[i]
            timestamp_first_tour[prev_counter] = timestamp[i]

            # Reset
            prev_counter = notification_counter[i]
            frend_id_hash = set({friend_id[i]})
            tours_counter = 1
            tours[i] = 1

    # Final message
    message[prev_counter - 1] = \
        create_message_single(tours_counter, name_first[prev_counter-1])

    # END
    return tours, name_first, timestamp_first_tour, message


def bundle_func(df_g):
    """Bundles notifications for a user_id

    This function is meant to be used after a pandas grouping
    (or manual filtering) of user_ids.

    Parameters
    ----------
    df_g : pd.DataFrame
        DataFrame containing 4 columns: ``['timestamp', 'user_id', 'friend_id',
        'friend_name']``

    Returns
    -------
    pd.DataFrame
        DataFrame containing 5 extra columns:
        ``['notification_bool','tours','notification_counter',
        'message','timestamp_first_tour']``
    """

    # Always send if less than 4 notifications per day
    if df_g.shape[0] <= 4:

        df_g['notification_bool'] = True
        df_g['tours'] = 1
        df_g['notification_counter'] = list(
            range(1, df_g.shape[0]+1))  # [1,2,3,4]
        df_g['message'] = create_message(df_g.tours, df_g.friend_name)
        df_g['timestamp_first_tour'] = df_g.timestamp

    else:

        # Calculate best times to send notification
        x = local_search(df_g.timestamp_ns.to_numpy())

        # Add up an indicator whether the notification is sent at those times
        df_g['notification_counter'] = add_notif_counter(x)

        # Group by counter and add
        # We also get the names and timestamp of the
        # first element in the notification counter
        df_g['tours'], name_first, timestamp_first_tour, message = \
            count_tours_per_notif(df_g.notification_counter.to_numpy('int'),
                                  df_g.friend_id.to_numpy(),
                                  df_g.friend_name.to_numpy(),
                                  df_g.timestamp.to_numpy())

        # Filter: lets keep the rows with notifications
        df_g = df_g.iloc[x, ]

        # Add timestamp first tour
        df_g['timestamp_first_tour'] = timestamp_first_tour

        # Cutomize message.
        df_g['message'] = message

    return df_g


def bundle(df):
    """Bundles the motifications given a pd.dataFrame of events

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 4 columns:
        ``['timestamp', 'user_id', 'friend_id', 'friend_name']``

    Returns
    -------
    pd.DataFrame
        Contains 4 derived columns: ``['notification_sent',
        'timestamp_first_tour', 'tours', 'receiver_id', 'message']``
    """

    # Create auxiliary columns. Times as int are used for delay calculations.
    df['timestamp_ns'] = df.timestamp.copy().astype("int")
    df['dayofyear'] = df.timestamp.copy().dt.dayofyear

    # groypby-apply
    df = df.groupby(['user_id', 'dayofyear']).apply(bundle_func)

    # Keep interesting columns only
    df.rename(columns={'timestamp': 'notification_sent',
                       'user_id': 'receiver_id'}, inplace=True)

    # END
    return df[['notification_sent', 'timestamp_first_tour', 'tours',
               'receiver_id', 'message']]
