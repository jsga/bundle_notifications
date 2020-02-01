.. highlight:: shell

====================
A simple tool to bundle notification
====================


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

This package contains a tool for bundling notifications in event streams. The goal is to minimize the number of notifications sent to users.

As an example, here it is the first couple of rows for a sample user_id::

	===================  ==============================  ==============================  =============
	timestamp            user_id                         friend_id                       friend_name
	===================  ==============================  ==============================  =============
	2017-08-08 11:04:36  0005BDD51B0185DCF1A4932CEB8437  0B56C34B2BB9B80100D1D5B5AB74EA  Rameshwor
	2017-08-10 12:29:47  0005BDD51B0185DCF1A4932CEB8437  266C5C5239255DF65ECFFDCEAF7048  Iustinian
	2017-08-11 11:53:12  0005BDD51B0185DCF1A4932CEB8437  0B56C34B2BB9B80100D1D5B5AB74EA  Rameshwor
	2017-08-12 23:42:11  0005BDD51B0185DCF1A4932CEB8437  FB63F29610B1EF67AD75C4BABDFCE1  Sara
	2017-08-24 14:49:06  0005BDD51B0185DCF1A4932CEB8437  0B56C34B2BB9B80100D1D5B5AB74EA  Rameshwor
	2017-08-31 14:30:48  0005BDD51B0185DCF1A4932CEB8437  FB63F29610B1EF67AD75C4BABDFCE1  Sara
	2017-09-01 13:21:59  0005BDD51B0185DCF1A4932CEB8437  DACE6D3C78D9B20B1F70A271BA98D5  Julie
	2017-09-01 13:29:40  0005BDD51B0185DCF1A4932CEB8437  DACE6D3C78D9B20B1F70A271BA98D5  Julie
	2017-09-01 17:13:37  0005BDD51B0185DCF1A4932CEB8437  DACE6D3C78D9B20B1F70A271BA98D5  Julie
	2017-09-26 13:02:32  0005BDD51B0185DCF1A4932CEB8437  FB63F29610B1EF67AD75C4BABDFCE1  Sara
	===================  ==============================  ==============================  =============

Using bundle_notifications tool, we can easily compute the following DataFrame with 3 new columns:

1. **tours**: number of friends that have gone on a tour since the beginning of the stream of data
2. **timestamp_first_tour**: timestamp for the first tour amongst his/her friends
3. **message**: notification message

Here it is the outcome::

	===================  ==============================  ==============================  =============  =======  ======================  =====================================
	timestamp            user_id                         friend_id                       friend_name      tours  timestamp_first_tour    message
	===================  ==============================  ==============================  =============  =======  ======================  =====================================
	2017-08-08 11:04:36  0005BDD51B0185DCF1A4932CEB8437  0B56C34B2BB9B80100D1D5B5AB74EA  Rameshwor            1  2017-08-08 11:04:36     Rameshwor went on a tour
	2017-08-10 12:29:47  0005BDD51B0185DCF1A4932CEB8437  266C5C5239255DF65ECFFDCEAF7048  Iustinian            2  2017-08-08 11:04:36     Rameshwor and 1 other went on a tour
	2017-08-11 11:53:12  0005BDD51B0185DCF1A4932CEB8437  0B56C34B2BB9B80100D1D5B5AB74EA  Rameshwor            2  2017-08-08 11:04:36     Rameshwor and 1 other went on a tour
	2017-08-12 23:42:11  0005BDD51B0185DCF1A4932CEB8437  FB63F29610B1EF67AD75C4BABDFCE1  Sara                 3  2017-08-08 11:04:36     Rameshwor and 2 others went on a tour
	2017-08-24 14:49:06  0005BDD51B0185DCF1A4932CEB8437  0B56C34B2BB9B80100D1D5B5AB74EA  Rameshwor            3  2017-08-08 11:04:36     Rameshwor and 2 others went on a tour
	2017-08-31 14:30:48  0005BDD51B0185DCF1A4932CEB8437  FB63F29610B1EF67AD75C4BABDFCE1  Sara                 3  2017-08-08 11:04:36     Rameshwor and 2 others went on a tour
	2017-09-01 13:21:59  0005BDD51B0185DCF1A4932CEB8437  DACE6D3C78D9B20B1F70A271BA98D5  Julie                4  2017-08-08 11:04:36     Rameshwor and 3 others went on a tour
	2017-09-01 13:29:40  0005BDD51B0185DCF1A4932CEB8437  DACE6D3C78D9B20B1F70A271BA98D5  Julie                4  2017-08-08 11:04:36     Rameshwor and 3 others went on a tour
	2017-09-01 17:13:37  0005BDD51B0185DCF1A4932CEB8437  DACE6D3C78D9B20B1F70A271BA98D5  Julie                4  2017-08-08 11:04:36     Rameshwor and 3 others went on a tour
	2017-09-26 13:02:32  0005BDD51B0185DCF1A4932CEB8437  FB63F29610B1EF67AD75C4BABDFCE1  Sara                 4  2017-08-08 11:04:36     Rameshwor and 3 others went on a tour
	===================  ==============================  ==============================  =============  =======  ======================  =====================================

Note that Julie went on 3 tours in a row. The tool takes this into account this, so that Julie's friend receive a single notification that Julie went on a tour.




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

3. **Ready!** Bundle your first notifications! Using an example dataset_, printing only 20 rows::

    $ bundle_notifications -p "https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv" -n 10
 
 It takes about a minute. The output is as follows:

::

	Downloading data...
	Bundling notifications...
	Great! Here there are the bundled notifications
		timestamp            user_id                         friend_id                       friend_name      tours  timestamp_first_tour    message
	-------------------  ------------------------------  ------------------------------  -------------  -------  ----------------------  ------------------------
	2017-08-01 00:06:47  F62712701E7AF6588B69A44235A6FC  06D188F4064E0D47BD760EEFEB7AAD  Geir                 1  2017-08-01 00:06:47     Geir went on a tour
	2017-08-01 00:31:05  DF5BB50FAD220C8D2A8FF9A0DBAA47  588C89FCADD0DBA0E722822513A267  Antim                1  2017-08-01 00:31:05     Antim went on a tour
	2017-08-01 00:35:24  8473CCCE79294CB494D1B42E2B1BAA  EDBB3D240ADBCF6CF175B192630ABB  Σωτήριος             1  2017-08-01 00:35:24     Σωτήριος went on a tour
	2017-08-01 01:20:47  CFFEC5978B0A4A05FA6DCEFB2C82CC  2BB0471CAA78ED0FCEE143E175F034  Mona                 1  2017-08-01 01:20:47     Mona went on a tour
	2017-08-01 01:21:39  0978C6F8C5093039165B5C571EACC8  45FE4C99C612BEEDE6A34B54C5369D  Laura                1  2017-08-01 01:21:39     Laura went on a tour
	2017-08-01 01:21:58  FBA67EFA2766854B885F25C06CC2FA  92DEF3A48927B1B2B0295936679D1C  Rameshwor            1  2017-08-01 01:21:58     Rameshwor went on a tour
	2017-08-01 01:44:16  BE6B4CBB422BBF114FB109921F2B9F  7BCD287DF0EBF5CAA86458737777BD  Noë                  1  2017-08-01 01:44:16     Noë went on a tour
	2017-08-01 02:09:58  391A4416FC0ADE8FD604B2F1A9BCCE  96593EE816FB4CE2AEBA5B754CFA38  Λεωνίδας             1  2017-08-01 02:09:58     Λεωνίδας went on a tour
	2017-08-01 02:20:32  D12E9E35AF8817E88F94F966B9C1F8  723515D5D083C9C15EC9A24AA624D7  Lina                 1  2017-08-01 02:20:32     Lina went on a tour
	2017-08-01 02:20:32  DDBA7653545B1BB68658838A22BAA5  723515D5D083C9C15EC9A24AA624D7  Lina                 1  2017-08-01 02:20:32     Lina went on a tour


Features: current and future
--------------------------------

The tool is mainly based on pandas. It relies on two main functionalities: reading csv files and group-apply function. With a 30 MB dataset it takes around 1 minute to compute the groupping and applying a function to each user_id. 

The advantage of using pandas over custom-made tools is its simplicity. Also, vectorizing the calculations makes them quite fast.

Here there are some possible future improvements:

1. Implement speed enhacements translating the apply function *bundle_func()* to Numba_. This could speed up by asignificantly the computations.
2. Encapsulating this tool in a Docker image would make it much easier to move from development to a productions server.
3. Option to read the data directly from a database, so that this tool can be run periodically without human supervision
4. If data grows, parallelize the computation using Dask_, for example. If the docker image is in place we could scale this up to many threads quite easily.

.. _`Read the docs`: https://bundle-notifications.readthedocs.io
.. _dataset: https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv
.. _Dask: https://dask.org/
.. _Numba: https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html#using-numba