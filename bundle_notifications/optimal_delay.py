"""This module compiles a few functions used to compute the optimal notification times.
"""
import numpy as np
from numba import jit


@jit(nopython=True)
def delay(t, x): # pragma: no cover
    """Calculates delay if notifications are sent at indexes indicated by notification_idx

    Parameters
    ----------
    t : np.array
        Array containing the timestamps of the events

    Returns
    --------
    datetime[ns]
        Sum of total delay
    """

    p1 = t[x[0]]- t[:x[0]]
    p2 = t[x[1]]- t[x[0]+1:x[1]]
    p3 = t[x[2]]- t[x[1]+1:x[2]]
    p4 = t[-1] - t[(x[2]+1):]
    
    return  p1.sum() + p2.sum() + p3.sum() + p4.sum()
    

def total_delay_brute(timestamp): # pragma: no cover
    """ Given a Series of Timestamps, calculate total delay using brute force: try out all possible combinations

    This function is kept here for reference and possible future implementations.

    Parameters
    ----------
    t : np.array
        Array containing the timestamps of the events

    Returns
    --------
    np.array
        array of length 4. Each element indicates an index where the optimal notification should be sent.

    """

    import itertools as it

    # Calculate possible combinations
    N = len(timestamp)
    list_possible = list(it.combinations( list(range(0,N-1)), 3))

    # Add last element to all
    list_possible = [list(tup)+[N-1] for tup in list_possible]

    # Allocate array of times
    tot_delay = np.array( [0]* len(list_possible))

    # Compute total delay. Loop for all combinations
    for i,l in enumerate(list_possible):
        tot_delay[i] = delay(timestamp, np.array(l))
    
    # END
    return np.array(list_possible[np.argmin(tot_delay)])
    

# Heuristic: distribute equally along the day
@jit(nopython=True)
def total_delay_initial(timestamp): # pragma: no cover
    """ Given a Series of Timestamps, sample 4 points equally distributed index-wise

    Parameters
    ----------
    t : np.array
        Array containing the timestamps of the events

    Returns
    --------
    np.array
        array of length 4. Each element indicates an index where the initial optimal notification should be sent.

    """
    # Calculate possible combinations
    N = len(timestamp)
    
    # Compute total delay.
    x = [int(N/4), int(N/2), int(0.75*N), N-1]
    
    # END
    return np.array(x)

@jit(nopython=True) 
def local_search_negative(timestamp,x, max_iter = 20): # pragma: no cover
    """Local search negative step
    
    Parameters
    ----------
    t : np.array (DateTime)
        array of timestamps 
    x : list of int
        Indicate indexes where the notification is sent
    max_iter : int
        Maximum number of local search steps to be performed 
        
    Returns
    --------

    np.array
        optimized notification schedule. Each item corresponds to an index of t
    """

    #print(f'Negative local search. Starting solution: {x}')

    i = 0

    while i < max_iter:
        # Calculate initial delay
        f = delay(timestamp, x)
        i += 1
        max_improve = -9999999999#-pd.Timedelta('10000d')

        # Now try to decrease the notification indexes one by one. Keep solution if improves.
        for k in range(0,3):

            if x[k] == 0:
                continue
            
            x_aux = x.copy()
            x_aux[k] -= 1
            f1 = delay(timestamp,x_aux)
            improve = f - f1
            #print(f"{k} Total delay swap: {f1} x_aux: {x_aux}")

            if improve > max_improve:
                max_improve = improve
                k_improve = k

        # Now we've got the most improving index. If no improvement: stop
        if max_improve < 0:
            i = max_iter + 100

            #print('BREAK')
            return x
            

        # If there is improvement then swap and repeat
        else:
            x[k_improve] -= 1
            i += 1

            #print(f"****Total delay: {delay(df,x)} x: {x} k_improve:{k_improve}")

    return x

@jit(nopython=True)
def local_search_positive(timestamp,x, max_iter = 20): # pragma: no cover
    """Local search negative step
    
    Parameters
    ----------
    t : np.array (DateTime)
        array of timestamps 
    x : list of int
        Indicate indexes where the notification is sent
    max_iter : int
        Maximum number of local search steps to be performed 
        
    Returns
    --------
    np.array
        optimized notification schedule. Each item corresponds to an index of t

    """

    #print(f'Positive local search. Starting solution: {x}')

    i = 0
    while i < max_iter:
        
        # Calculate initial delay
        f = delay(timestamp,x)
        i += 1
        max_improve = -9999999999

        # Now try to decrease the notification indexes one by one. Keep solution if improves.
        for k in range(0,3):
            if x[k] == 0:
                continue

            x_aux = x.copy()
            x_aux[k] += 1
            f1 = delay(timestamp,x_aux)
            improve = f - f1
            #print(f"{k} Total delay swap: {f1} x_aux: {x_aux}")

            if improve > max_improve:
                max_improve = improve
                k_improve = k

        # Now we've got the most improving index. If no improvement: stop
        if max_improve < 0:
            i = max_iter + 100
            return x
            
        # If there is improvement then swap and repeat
        else:
            x[k_improve] += 1
            i += 1

            #print(f"****Total delay: {delay(df,x)} x: {x} k_improve:{k_improve}")

    return x

def local_search(timestamp):
    """Heuristic optimization of the notification schedule

    Parameters
    ----------
    t : np.array (int)
        Array of integer values. These could correspond to datetime64[ns]. The inputs needs to be an integer as it is better supported by the JIT compiler (TODO: allow for datetime64 type)
        
    Returns
    --------
    np.array
        Optimized notification schedule. Each item corresponds to an index of t where the notification should have been sent.
    """

    # Initial solution
    x = total_delay_initial(timestamp)

    # Negative moves
    x = local_search_negative(timestamp, x)
    
    # Postive moves
    x = local_search_positive(timestamp,x)
    
    return np.array(x)