#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# moabdb - Online finance database
# https://github.com/MoabDB
# https://moabdb.com
# Copyright 2022-2023
#

"""
The get_treasuries() function retrieves historical treasury data from the MoabDB API.
"""

from . import constants
from . import errors
from . import timewindows
from .lib import _check_access, _server_req


def get_treasuries(sample: str = "1y",
                   start: str = None, end: str = None):
    """
    Gets equity data from the MoabDB API

    Args:
        sample (:obj:`str`, optional): Sample length, required if "start" or "end" is missing
        start (:obj:`str`, optional): Beginning date of sample,
            required if "end" or "sample" is missing
        end (:obj:`str`, optional): Ending date of sample,
            required if "start" or "sample" is missing

    Raises:
        errors.MoabResponseError: If there's a problem interpreting the response
        errors.MoabRequestError: If the server has a problem interpreting the request,
            or if an invalid parameter is passed
        errors.MoabInternalError: If the server runs into an unrecoverable error internally
        errors.MoabHttpError: If there's a problem transporting the payload or receiving a response
        errors.MoabUnauthorizedError: If the user is not authorized to request the datatype
        errors.MoabNotFoundError: If the data requested wasn't found
        errors.MoabUnknownError: If the error code couldn't be parsed

    Returns:
        DataFrame: A Pandas DataFrame of the returned data

    Examples:

        Request the last year of treasuries data::

            import moabdb as mdb
            mdb.login("your_email@mail.com", "secret_key")
            df = mdb.get_treasuries("1y")

        Request a specific month of data::

            import moabdb as mdb
            mdb.login("your_email@mail.com", "secret_key")
            df = mdb.get_treasuries(start="2022-04-01", sample="1m")

    """

    # Check authorization
    if not _check_access():
        raise errors.MoabRequestError(
            "Premium datasets needs API credentials, see moabdb.com")

    # String time to integer time
    start_tm, end_tm = timewindows.get_unix_dates(sample, start, end)

    # Request treasury data
    columns = constants.TREASURY_COLUMNS
    return_db = _server_req("INTERNAL_TREASURY",
                            start_tm, end_tm, "treasuries")
    return return_db[columns]
