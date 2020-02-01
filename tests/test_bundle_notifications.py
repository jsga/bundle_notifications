#!/usr/bin/env python

"""Tests for `bundle_notifications` package."""

import pytest
from click.testing import CliRunner
import pandas as pd
import numpy as np
from bundle_notifications import cli
from bundle_notifications import bundle_notifications #import load_data, bundle_func,add_message


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    # Test with no parameters
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Great! Here there are the bundled notifications' in result.output

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



def test_bundle_func():
    """Test for bundling function"""

    # Create fake data
    d_fake = {'timestamp': {0: Timestamp('2017-08-01 00:06:47'),
  1: Timestamp('2017-08-01 00:31:05'),
  2: Timestamp('2017-08-01 00:35:24'),
  3: Timestamp('2017-08-01 01:20:47'),
  4: Timestamp('2017-08-01 01:21:39')},
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
    df_test = bundle_notifications.bundle_func( pd.DataFrame(d_fake))
    
    assert isinstance(df_test,pd.core.frame.DataFrame), "Loaded data is not a pandas DataFrame"
    assert df_test.shape == (5,7), "Output dimensions mismatch."
    assert np.all(df_test.columns == ['timestamp', 'user_id', 'friend_id', 'friend_name', 'tours',
       'timestamp_first_tour', 'message']), "Wrong output names"




def test_add_message():
    """Test for the message of the notification"""

    x = pd.DataFrame({'message':['Javi','Javier', 'Saez'], 'tours':[1,2,3]})

    assert bundle_notifications.add_message(x.iloc[0,]) == 'Javi went on a tour'
    assert bundle_notifications.add_message(x.iloc[1,]) == 'Javier and 1 other went on a tour'
    assert bundle_notifications.add_message(x.iloc[2,]) == 'Saez and 2 others went on a tour'
