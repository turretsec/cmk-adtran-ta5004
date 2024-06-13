from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import metric_info, graph_info

metric_info["if_in_bytes_agg"] = {
    "title": _("Input Bandwidth (Agg.)"),
    "unit": "bytes",
    "color": "31/a",
}

metric_info["if_out_bytes_agg"] = {
    "title": _("Output Bandwidth (Agg.)"),
    "unit": "bytes",
    "color": "36/a",
}

graph_info["bandwidth_agg"] = {
    "title": _("Total Bandwidth Usage"),
    "metrics": [
        ("if_in_bytes_agg", "area", _("Input bandwidth (Agg.)")),
        ("if_out_bytes_agg", "-area", _("Output bandwidth (Agg.)")),
    ],
}