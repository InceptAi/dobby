"""Base class for storing parsed summaries.
"""
from __future__ import division
from copy import deepcopy

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

class NetworkSummary(object):
    """Info parsed so far
    """
    def __init__(self, start_ts=None, end_ts=None,
                 mac_to_endpoints=None, ip_to_endpoints=None,
                 nodes=None, edges=None, ip_flows=None,
                 phy_models=None, apps=None):
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.mac_to_endpoints = mac_to_endpoints if mac_to_endpoints else {}
        self.ip_to_endpoints = ip_to_endpoints if ip_to_endpoints else {}
        self.nodes = nodes if nodes else {}
        self.edges = edges if edges else {}
        self.ip_flows = ip_flows if ip_flows else {}
        self.apps = apps if apps else {}
        self.phy_models = phy_models if phy_models else {}

