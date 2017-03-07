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
    def __init__(self, min_val=None, max_val=None, avg_val=None, percentile_50=None,
                 percentile_10=None, percentile_90=None, var_val=None, num_samples=None,
                 **kwargs):
        self.min_val = min_val
        self.max_val = max_val
        self.avg_val = avg_val
        self.var_val = var_val
        self.percentile_50 = percentile_50
        self.percentile_10 = percentile_10
        self.percentile_90 = percentile_90
        self.num_samples = num_samples
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Metrics(object):
    """ Class representing network metrics
    Metrics {
        Stats loss, latency, rtt, size, pkt_tx_time, rate
        int totals_*
    }
    """
    def __init__(self, start_ts=None, end_ts=None, total_pkts=None, total_bytes=None, **kwargs):
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.total_pkts = total_pkts
        self.total_bytes = total_bytes

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class WirelessMetrics(Metrics):
    """ Class representing wireless metrics
    WirelessMetrics {
        Stats loss, latency, rtt, size, pkt_tx_time, rate
        int totals_*
    }
    """
    def __init__(self, start_ts=None, end_ts=None, total_pkts=None, total_bytes=None,
                 total_data_pkts=None, total_data_bytes=None, total_retx=None,
                 noise_stats=None, snr_stats=None, rate_stats=None, size_stats=None,
                 total_trans_time_usec=None, avg_data_pkt_duration_usec=None, **kwargs):
        Metrics.__init__(self, start_ts=start_ts, end_ts=end_ts,
                         total_pkts=total_pkts, total_bytes=total_bytes)
        self.total_data_pkts = total_data_pkts
        self.total_data_bytes = total_data_bytes
        self.total_retx = total_retx
        self.noise_stats = noise_stats
        self.snr_stats = snr_stats
        self.rate_stats = rate_stats
        self.size_stats = size_stats
        self.total_trans_time_usec = total_trans_time_usec
        self.avg_data_pkt_duration_usec = avg_data_pkt_duration_usec
        self.__dict__.update(kwargs)

    def update_stats(self, **updated_stats):
        self.__dict__.update(updated_stats)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return Metrics.__eq__(self, other) and \
                   self.total_data_pkts == other.total_data_pkts and \
                   self.total_data_bytes == other.total_data_bytes and \
                   self.total_retx == other.total_retx and \
                   self.total_trans_time_usec == other.total_trans_time_usec and \
                   self.avg_data_pkt_duration_usec == other.avg_data_pkt_duration_usec and \
                   self.noise_stats == other.noise_stats and \
                   self.snr_stats == other.snr_stats and \
                   self.size_stats == other.size_stats and \
                   self.rate_stats == other.rate_stats

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class TCPMetrics(Metrics):
    """ Class representing TCP metrics
    TCPMetrics {
        Stats loss, latency, rtt, size, pkt_tx_time, rate
        int totals_*
    }
    """
    def __init__(self, start_ts=None, end_ts=None, total_pkts=None, total_bytes=None,
                 duration=None, rtt_stats=None, mtu=None, total_loss=None,
                 total_acks=None, **kwargs):
        Metrics.__init__(self, start_ts=start_ts, end_ts=end_ts,
                         total_pkts=total_pkts, total_bytes=total_bytes)
        self.duration = duration
        self.rtt_stats = rtt_stats
        self.mtu = mtu
        self.total_loss = total_loss
        self.total_acks = total_acks

    def update_stats(self, **updated_stats):
        self.__dict__.update(updated_stats)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return Metrics.__eq__(self, other) and \
                   self.duration == other.duration and \
                   self.total_acks == other.total_acks and \
                   self.total_loss == other.total_loss and \
                   self.rtt_stats == other.rtt_stats
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
