from cmk.gui.plugins.metrics import perfometer_info

perfometer_info.append(
    {
        "type": "dual",
        "perfometers": [
            {
                "type": "logarithmic",
                "metric": "if_in_bytes_agg",
                "half_value": 5000000,
                "exponent": 5,
            },
            {
                "type": "logarithmic",
                "metric": "if_out_bytes_agg",
                "half_value": 5000000,
                "exponent": 5,
            },
        ],
    }
)
