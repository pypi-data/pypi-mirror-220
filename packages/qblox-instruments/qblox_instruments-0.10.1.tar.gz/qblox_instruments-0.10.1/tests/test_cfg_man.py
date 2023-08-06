# ----------------------------------------------------------------------------
# Description    : Configuration manager test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import pytest
import sys

from io import StringIO
from qblox_instruments import ConfigurationManager


# -- fixtures ----------------------------------------------------------------


@pytest.fixture(name="stdout")
def make_stdout():
    new_stdout = StringIO()
    sys.stdout = new_stdout
    yield new_stdout
    sys.stdout = sys.__stdout__


@pytest.fixture(name="cfg_man")
def make_cfg_man():
    with ConfigurationManager("test") as cfg_man:
        yield cfg_man


# -- functions ---------------------------------------------------------------


def test_help(stdout):
    """
    Test getting help using commandline interface

    Parameters
    ----------
    stdout
        StringIO connected to sys.stdout

    Returns
    ----------

    Raises
    ----------
    """

    try:
        ConfigurationManager.cmd_line("")
        raise AssertionError("Should have failed.")
    except RuntimeError:
        pass


# ----------------------------------------------------------------------------
def test_version(stdout):
    """
    Test getting the configuration manager version using commandline interface

    Parameters
    ----------
    stdout
        StringIO connected to sys.stdout

    Returns
    ----------

    Raises
    ----------
    """

    ConfigurationManager.cmd_line(["-V"])
