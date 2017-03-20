"""
Dobby
========

    Dobby is a Python package for the creation, manipulation, and interpreting summaries from
    packet processing module click.

    https://www.inceptai.com

Using
-----

    Just write in Python

    >>> import dobby as db
    >>> PM=db.ParseManager()
    >>> PM.parse_summary(start_ts=st, end_ts=ed, wireless_stream=ws,
            node_stream=ns, tcploss_stream=ts, tcpmystery_stream=ts)
    >>> print(PM.get_summary(st))
"""
#    Copyright (C) 2017 by
#    Vivek Shrivastava (vivek@obiai.tech)
#    All rights reserved.
#
# Add platform dependent shared library path to sys.path
#

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for NetworkX (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# These are import orderwise
from dobby.nwinfo.networksummary import NetworkSummary
from dobby.nwparser.parsemanager import ParseManager
