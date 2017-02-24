from __future__ import division
from copy import deepcopy
from collections import Counter

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


 class Edge(object):
    """
    Base class for edges in our model.
    Edge : {
      Edge {
        Endpoint A   // Pointer or reference to Endpoint labelled "A"
        Endpoint B   // Pointer or reference to Endpoint labelled "B"
        EdgeType edgeType // Type of edge -- by default set to PHYSICAL
        LinkMetrics AtoB  // link metrics for the traffic from A to B
        LinkMetrics BtoA  // link metrics for the traffic from B to A
        Metrics avgRTT, avgLatency, avgLoss // direction-less link metrics.
        PhyModel phyModel = if (A.phyModel.type == B.phyModel.type) ? A.phyModel : BRIDGE 
        phyModel.mtu = min(A.phyModel.mtu, B.phyModel.mtu)
      }

    Parameters
    ----------
    See above
    attr : keyword arguments, optional (default= no attributes)
        Attributes to add to graph as key=value pairs.
    """
    def __init__(self, endpoint_a, endpoint_b, edge_type, **metrics, **metrics_ab, **metrics_ba)
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b
        self.edge_type = edge_type
        self.edge_metrics = Counter()
        self.edge_metrics_ab = Counter()
        self.edge_metrics_ba = Counter()
        self.edge_metrics.update(metrics)
        self.edge_metrics.update(metrics_ab)
        self.edge_metrics.update(metrics_ba)


    def update_metrics(self, **metrics, **metrics_ab, **metrics_ba):
        self.edge_metrics.update(metrics) 
        self.edge_metrics.update(metrics_ab)
        self.edge_metrics.update(metrics_ba)
