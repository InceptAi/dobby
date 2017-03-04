#!/usr/bin/env python3
"""Utility class for network metrics.
"""
from __future__ import division
from copy import deepcopy
import re
import time
from collections import Counter
from enum import Enum, unique

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

class Stats(object):
    """ Utility class for stats
     Stats {
        Float min, max, avg, variance;
        int num_pkts
    }
    """
    def __init__(self, min_val=None, max_val=None, avg_val=None, median_val=None,
                 percentile_10=None, percentile_10=None, var_val=None)
        self.min_val = min_val
        self.max_val = max_val
        self.avg_val = avg_val
        self.var_val = var_val
        self.median_val = median_val
        self.percentile_10 = percentile_10
        self.percentile_90 = percentile_90

class Metrics(object):
    """ Class representing network metrics
    Metrics {
        Stats loss, latency, rtt, size, pkt_tx_time, rate
        int totals_*
    }
    """
    def __init__(self, start_ts=None, end_ts=None, total_pkts=None, total_bytes=None):
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.total_pkts = total_pkts
        self.total_bytes = total_bytes

class WirelessMetrics(Metrics):
    """ Class representing wireless metrics
    WirelessMetrics {
        Stats loss, latency, rtt, size, pkt_tx_time, rate
        int totals_*
    }
    """
    def __init__(self, start_ts=None, end_ts=None, total_pkts=None, total_bytes=None,
                 total_data_pkts=None, total_data_bytes=None, total_retx=None,
                 noise_stats=None, snr_stats=None, rate_stats=None, size_stats=None):
        Metrics.__init__(self, start_ts=start_ts, end_ts=end_ts,
                         total_pkts=total_pkts, total_bytes=total_bytes)
        self.total_data_pkts = total_data_pkts
        self.total_data_bytes = total_data_bytes
        self.total_retx = total_retx
        self.noise_stats = noise_stats
        self.snr_stats = snr_stats
        self.rate_stats = rate_stats
        self.size_stats = size_stats

class TCPMetrics(Metrics):
    """ Class representing TCP metrics
    TCPMetrics {
        Stats loss, latency, rtt, size, pkt_tx_time, rate
        int totals_*
    }
    """
    def __init__(self, start_ts=None, end_ts=None, total_pkts=None, total_bytes=None,
                 duration=None, rtt_stats=None, mtu=None, total_loss=None, total_acks=None):
        Metrics.__init__(self, start_ts=start_ts, end_ts=end_ts,
                         total_pkts=total_pkts, total_bytes=total_bytes)
        self.duration = duration
        self.rtt_stats = rtt_stats
        self.mtu = mtu
        self.total_loss = total_loss
        self.total_acks = total_acks

    def update_stats(self, **updated_stats)
        self.update(updated_stats)
