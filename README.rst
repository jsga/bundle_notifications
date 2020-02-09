.. highlight:: shell

=====================================
A simple tool to bundle notifications
=====================================


.. image:: https://img.shields.io/travis/jsga/bundle_notifications.svg
        :target: https://travis-ci.org/jsga/bundle_notifications

.. image:: https://readthedocs.org/projects/bundle-notifications/badge/?version=latest
        :target: https://bundle-notifications.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/codecov/c/gh/jsga/bundle_notifications
        :target: https://img.shields.io/codecov/c/gh/jsga/bundle_notifications
        :alt: codecov.io


`Read the docs`_ here

About
---------

This package contains a tool for bundling notifications in event streams. The goal is to minimize the number of notifications sent to users and to not send more than 4 notifications per day.

As an example, here it is the first couple of rows for a sample user_id::

    ===================  ==============================  ==============================  =============
    timestamp            user_id                         friend_id                       friend_name
    ===================  ==============================  ==============================  =============
    2017-08-01 01:20:47  CFFEC5978B0A4A05FA6DCEFB2C82CC  2BB0471CAA78ED0FCEE143E175F034  Mona
    2017-08-01 02:28:27  CFFEC5978B0A4A05FA6DCEFB2C82CC  2BB0471CAA78ED0FCEE143E175F034  Mona
    2017-08-01 03:00:42  CFFEC5978B0A4A05FA6DCEFB2C82CC  74C09338D7CA031859AE26A1586692  Toomas
    2017-08-01 03:51:05  CFFEC5978B0A4A05FA6DCEFB2C82CC  F039A0F7A3245F7B2D7BD0942F3680  Sean
    2017-08-01 05:03:44  CFFEC5978B0A4A05FA6DCEFB2C82CC  DF6A386FE701217C2A12292DB8D142  Buse
    2017-08-01 05:08:29  CFFEC5978B0A4A05FA6DCEFB2C82CC  385308FE41CA0484E84B01D5EED659  Σωτήριος
    2017-08-01 05:59:33  CFFEC5978B0A4A05FA6DCEFB2C82CC  00A0ED2A6F99DE0E577C51FAEBF302  三浦
    2017-08-01 06:31:08  CFFEC5978B0A4A05FA6DCEFB2C82CC  72C688FB41B4EDE06DBC790020FBE7  Victoria
    2017-08-01 06:45:44  CFFEC5978B0A4A05FA6DCEFB2C82CC  159854120B568D6449798289D97D64  Franciso
    2017-08-01 06:53:51  CFFEC5978B0A4A05FA6DCEFB2C82CC  B5BA8FA5CF5342CBCC9CDAA427E058  Λυκάων
    2017-08-01 07:01:17  CFFEC5978B0A4A05FA6DCEFB2C82CC  9AB43D430EF8C4443FB8698EFD5092  Δαμιανός
    2017-08-01 07:04:32  CFFEC5978B0A4A05FA6DCEFB2C82CC  B34CFFB5CA3C6EAA95991E35FA5066  Bakos
    2017-08-01 07:19:44  CFFEC5978B0A4A05FA6DCEFB2C82CC  16CC2AA801B1F29D4991C947B8705A  Rozalia
    2017-08-01 07:51:01  CFFEC5978B0A4A05FA6DCEFB2C82CC  268045C1DDB279D56F9873FCC5D2AA  Marcu
    2017-08-01 08:38:00  CFFEC5978B0A4A05FA6DCEFB2C82CC  57AA5706AD9E5D051463DCEA8FD9BF  Blanduzia

Using bundle_notifications tool, we can easily compute a solution table with the following columns:

1. **notification_sent**: timestamp of the timestamp when the notification should have been sent
2. **timestamp_first_tour**: timestamp for the first tour amongst his/her friends
3. **tours**: number of friends that have gone on a tour since the last notification was sent
4. **receiver_id**: id of the receiver
5. **message**: custom notification message


Here it is the outcome::

    ===================  ======================  =======  ==============================  ========================================
    notification_sent    timestamp_first_tour      tours  receiver_id                     message
    ===================  ======================  =======  ==============================  ========================================
    2017-08-01 07:51:01  2017-08-01 01:20:47          13  CFFEC5978B0A4A05FA6DCEFB2C82CC  Mona and 12 others went on a tour
    2017-08-01 17:44:37  2017-08-01 08:38:00           9  CFFEC5978B0A4A05FA6DCEFB2C82CC  Blanduzia and 8 others went on a tour
    2017-08-01 20:18:46  2017-08-01 17:56:46          14  CFFEC5978B0A4A05FA6DCEFB2C82CC  史 and 13 others went on a tour
    2017-08-01 21:59:55  2017-08-01 20:29:26          15  CFFEC5978B0A4A05FA6DCEFB2C82CC  Rozalia and 14 others went on a tour
    2017-08-02 06:49:19  2017-08-02 02:25:24          14  CFFEC5978B0A4A05FA6DCEFB2C82CC  Buse and 13 others went on a to

Note that Mona went on 2 tours in a row. The tool takes this into account this so that Mona's friend receive a single notification that Mona went on a tour.




Quickstart
-----------------


1. Option 1: using pip to directly install the package to a virtual enviroment::

    # Create a virtual enviroment
    $ python -m venv .venv_bundle_notifications

    # Activate it
    $ source .venv_bundle_notifications/bin/activate

    # Install using pip + git
    $ pip install git+https://github.com/jsga/bundle_notifications.git

2. Option 2: clone the repository from Github::

    $ git clone https://github.com/jsga/bundle_notifications.git

Alternatively, you can manually download the repository as a zip file.

Make sure the terminal is at the root of the package::

    $ cd bundle_notifications
    $ pwd
    >/Users/myuser/Documents/GitHub/bundle_notifications

You should see something like the above

In case you want to install this package in a virtual enviroment, create one and activate it::

    $ python -m venv .venv_bundle_notifications
    $ source .venv_bundle_notifications/bin/activate 

Install the package::

    $ python setup.py install

3. **Ready!** Bundle your first notifications! Using an example dataset_, printing only 10 rows::

    $ bundle_notifications -p "https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv" -n 10
 
 It takes about 5 or 6 minutes. The output is as follows:

::

    Downloading data...
    Bundling notifications... (Estimated time: 368.35 seconds for 337657 rows)
    Saving to csv: bundle_notifications.csv
    Great! Here there are the first 10 bundled notifications
    notification_sent    timestamp_first_tour      tours  receiver_id                     message
    -------------------  ----------------------  -------  ------------------------------  ------------------------
    2017-09-05 12:54:49  2017-09-05 12:54:49           1  00013DA3ABDE2F0771AB56A53A9AA3  Amelia went on a tour
    2017-09-05 13:28:31  2017-09-05 13:28:31           1  00013DA3ABDE2F0771AB56A53A9AA3  Amelia went on a tour
    2017-09-24 11:20:48  2017-09-24 11:20:48           1  000367CD43072A5C649AD27FAC6479  Magdaléna went on a tour
    2017-08-01 12:34:51  2017-08-01 12:09:25           1  0005BDD51B0185DCF1A4932CEB8437  Sara went on a tour
    2017-08-01 13:01:50  2017-08-01 12:55:33           1  0005BDD51B0185DCF1A4932CEB8437  Sara went on a tour
    2017-08-01 14:26:25  2017-08-01 13:45:58           1  0005BDD51B0185DCF1A4932CEB8437  Sara went on a tour
    2017-08-01 15:31:46  2017-08-01 14:58:13           1  0005BDD51B0185DCF1A4932CEB8437  Sara went on a tour
    2017-08-02 09:25:01  2017-08-02 09:25:01           1  0005BDD51B0185DCF1A4932CEB8437  Bonifác went on a tour
    2017-08-03 11:00:03  2017-08-03 11:00:03           1  0005BDD51B0185DCF1A4932CEB8437  Bonifác went on a tour
    2017-08-04 13:26:34  2017-08-04 13:26:34           1  0005BDD51B0185DCF1A4932CEB8437  Rameshwor went on a tour



Optimization problem & local search solution
--------------------------------------------


There are two goals:

1. To not send more than 4 notifications a day to a user (should happen only a few times)
2. To keep sending delay minimal

These goals can be translated into an optimization problem, where the decision variable is **x** =  [x1, x2, x3, x4] representing indexes, each one corresponding to the timestamp when the notification should have been sent. The function to minimize is, therefore, the total delay incurred by sending the notifications at **x**.

Let's formulate an example. Say there are 11 events with timestamps **t** = [t0, t2, .., t10] and that we decide to send notification at indexes **x** = [0, 2, 7, 10]. The total delay **D** is then calculated as::

    D = (t2-t1) + (t7-t6) + (t7-t4) + (t7-t3) + (t7-t6) + (t10-t8) + (t10-t9)

Even though the intuition behind this problem is quite simple, this optimization problem is unfortunately not linear and not straight-forward to formulate. For this reason, in this tool, we use a heuristic optimization approach (local search), which, in practice, seems to work well. See `speed considerations`_ section for further information.


Implementation
^^^^^^^^^^^^^^
In short, the strategy is as follows.

First, we group the users by *user_id* and *day*. For each of those groups, do:

1. If the number of notifications for a user is lower or equal than 4, we simply decide to send all notifications.

2. If the number of notifications is greater than 4:

    1. Obtain an optimal notification schedule:

        1. We first obtain an initial solution, simply by distributing the notifications at indexes ``x = [int(N/4), int(N/2), int(0.75*N), N-1]`` where N is the number of events for that user and day.

        2. From the initial solution we do a negative local search, checking 1 step a time if the total delay decreases by subtracting one of the indexes in **x**. We repeat this until the total delay function stops decreasing, or until a maximum number of iterations is reached

        3. We do a positive local search (similar as above)

    2. We proceed to bundle the notifications:

        1. Count how many unique friends are active in between two notifications

		2. Discard rows that do not correspond to **x**

3. Create a custom message

4. Gather relevant columns and delete intermediate ones

Finally, we consolidate all the datasets into one.


Features: Current and future
--------------------------------

The tool relies on two main pandas functionalities: reading CSV files and group-apply functions. Applying a custom function to a pandas groupby element is known to be rather slow - it is even mentioned in the documentation_. However, it is flexible and easy to work with, so for this reason, this was my initial approach. 

The advantage of using pandas over custom-made tools is its simplicity. The initial version of the functions was quite simple and it was also quick to develop. However, the computing time was too high and the tool would become unusable: 1h30min for 330k rows of data. By iteratively analyzing the bottlenecks and coding equivalent custom functions, the time is now reduced to 5% of what it used to be. I am sure that with some more effort it could go down to 1%.

The tool is built as a Python package. Tests have been implemented and the coding style is PEP8 consistent, checked with *flake8*. I have based the project on this cookie-cutter_.

Here there are some possible future improvements:

1. Implement speed enhancements, focusing on translating the groupby step in function *bundle_func()* to Numpy and Numba_.

2. Implement a parameter to set the maximum number of notifications. Currently, 4 is hardcoded.

3. Encapsulating this tool in a Docker image would make it much easier to move from development to a production server.

4. Add an option to read the data directly from a database, so that this tool can be run periodically without human supervision

5. If data grows, we could parallelize the computation using Dask_. If the docker image is in place we could scale this up to many threads quite easily.


Note
^^^^^^

This tool could be used to analyze what *could* have been the optimal notification schedule. As of version V.01, it cannot be used to predict *when* is the best time to send a notification. 

This tool could be used as a basis for further analysis: once we know what was optimal in the past, we can create rules for future decisions. This functionality falls out of the scope of the assignment.


.. _`Read the docs`: https://bundle-notifications.readthedocs.io
.. _dataset: https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv
.. _documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.apply.html#pandas.core.groupby.GroupBy.apply
.. _Dask: https://dask.org/
.. _Numba: https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html#using-numba
.. _`speed considerations`: https://bundle-notifications.readthedocs.io/en/latest/notebooks.html
.. _`cookie-cutter`: https://github.com/audreyr/cookiecutter-pypackage