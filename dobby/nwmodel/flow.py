"""Base class for a Flow.
Flow: A flow is a transport or high layer connection from one
endpoint to another such as a HTTP connection, an RTP streaming connection, etc.
"""
from __future__ import division
from copy import deepcopy
from collections import Counter
from enum import Enum, unique
from dobby.classes.metrics import *

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

@unique
class FlowType(Enum):
  UNKNOWN = 0
  HTTP = 1
  STREAMING = 2
  EMAIL = 3
  TELNET = 4
  SSH = 5
  RTP = 6
  TCP = 7
  IP = 8
  DNS = 9
  DHCP = 10
  MISC = 11

class Flow(object):
    """
    Base class for a Flow.

    Flow {
        Vector edgeList[MAX_HOPS] // An ordered list of edges
        FlowType flowType[MAX_PROTOCOL_LAYERS] // A list of protocols like HTTP/TCP/IP
        Int Port
        FlowMetrics flowMetrics  // Captures network metrics for this flow.
    }

    """
    def __init__(self, edge_list=[], flow_type=FlowType.UNKNOWN,
                 src_endpoint=None, dst_endpoint=None, sport=None,
                 dport=None, flow_metrics=None, flow_metrics_src_to_dst=None,
                 flow_metrics_dst_to_src=None, **kwargs):
        self.src_endpoint = src_endpoint
        self.dst_endpoint = dst_endpoint
        self.edge_list = edge_list
        self.flow_type = flow_type
        self.sport = sport
        self.dport = dport
        self.flow_metrics = flow_metrics
        self.flow_metrics_src_to_dst = flow_metrics_src_to_dst
        self.flow_metrics_dst_to_src = flow_metrics_dst_to_src
        self.__dict__.update(kwargs)

class TCPFlow(object):
    """TCP Flow.
    """
    def __init__(self, edge_list=[], flow_type=FlowType.TCP,
                 src_endpoint=None, dst_endpoint=None, sport=None,
                 dport=None, flow_metrics=None, flow_metrics_src_to_dst=None,
                 flow_metrics_dst_to_src=None, **kwargs):
        Flow.__init__(self,
                      edge_list=edge_list,
                      flow_type=flow_type,
                      src_endpoint=src_endpoint,
                      dst_endpoint=dst_endpoint,
                      sport=sport,
                      dport=dport,
                      flow_metrics=flow_metrics,
                      flow_metrics_src_to_dst=flow_metrics_src_to_dst,
                      flow_metrics_dst_to_src=flow_metrics_dst_to_src)
        if not flow_metrics:
            self.flow_metrics = TCPMetrics()
        if not flow_metrics_src_to_dst:
            self.flow_metrics_src_to_dst = TCPMetrics()
        if not flow_metrics_dst_to_src:
            self.flow_metrics_dst_to_src = TCPMetrics()

    def update_flow_metrics(self, **metrics):
        self.flow_metrics.update_stats(**metrics)

    def update_flow_metrics_src_to_dst(self, **metrics):
        self.flow_metrics_src_to_dst.update_stats(**metrics)

    def update_flow_metrics_dst_to_src(self, **metrics):
        self.flow_metrics_dst_to_src.update_stats(**metrics)

