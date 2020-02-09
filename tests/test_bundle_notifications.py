#!/usr/bin/env python

"""Tests for `bundle_notifications` package."""

import pytest
from click.testing import CliRunner
import pandas as pd
import numpy as np
from bundle_notifications import cli
from bundle_notifications import bundle_notifications
from bundle_notifications import optimal_delay

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    # Test with no parameters
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Great!' in result.output

    # Test with --help
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output


def test_load_data():
    """Test for loading data function"""

    # Donwload a single dataframe
    df = bundle_notifications.load_data(nrows=1)
    print(df.shape)
    
    assert isinstance(df,pd.core.frame.DataFrame), "Loaded data is not a pandas DataFrame"
    assert df.shape == (1,4), "Data is not loaded correctly."


def test_create_message_single():
    """Test single message creation"""


    assert bundle_notifications.create_message_single(1,'Javi') == 'Javi went on a tour'
    assert bundle_notifications.create_message_single(2,'Javi') == 'Javi and 1 other went on a tour'
    assert bundle_notifications.create_message_single(3,'Javi') == 'Javi and 2 others went on a tour'
    with pytest.raises(ValueError):
        bundle_notifications.create_message_single(-1,'error')


def test_create_message():
    """Test for the message of the notification"""

    tours = np.array([1,2,3,10])
    names = np.array(['Javi','Javier', 'Saez','Gallego'])
    message = bundle_notifications.create_message(tours, names)

    assert len(message) == 4
    assert isinstance(message,np.ndarray)


def test_bundle_func():
    """Test for bundling function"""

    # Create fake data
    d_fake = {'timestamp': {0: pd.Timestamp('2017-08-01 00:06:47'),
  1: pd.Timestamp('2017-08-01 00:31:05'),
  2: pd.Timestamp('2017-08-01 00:35:24'),
  3: pd.Timestamp('2017-08-01 01:20:47'),
  4: pd.Timestamp('2017-08-01 01:21:39')},
 'user_id': {0: 'F62712701E7AF6588B69A44235A6FC',
  1: 'DF5BB50FAD220C8D2A8FF9A0DBAA47',
  2: '8473CCCE79294CB494D1B42E2B1BAA',
  3: 'CFFEC5978B0A4A05FA6DCEFB2C82CC',
  4: '0978C6F8C5093039165B5C571EACC8'},
 'friend_id': {0: '06D188F4064E0D47BD760EEFEB7AAD',
  1: '588C89FCADD0DBA0E722822513A267',
  2: 'EDBB3D240ADBCF6CF175B192630ABB',
  3: '2BB0471CAA78ED0FCEE143E175F034',
  4: '45FE4C99C612BEEDE6A34B54C5369D'},
 'friend_name': {0: 'Geir', 1: 'Antim', 2: 'Σωτήριος', 3: 'Mona', 4: 'Laura'}}

    # Run bundle function
    df_test = bundle_notifications.bundle( pd.DataFrame(d_fake))
    
    assert isinstance(df_test,pd.core.frame.DataFrame), "Output element is not a pandas DataFrame"
    assert df_test.shape == (5,5), 'Output dimensions mismatch.'
    assert np.all(df_test.columns == ['notification_sent', 'timestamp_first_tour', 'tours', 'receiver_id', 'message']), "Wrong output column names"


def test_total_delay():
    """Test for the total delay of notifications"""

    t = np.array([0,1,2,3,4,10]) # timestamps
    x = np.array([0,1,2,5]) # notification indexes
    tot = optimal_delay.delay(t, x)
    # (10-3) + (10-4) = 13
    assert tot == 13, 'Unexpected delay calculation'