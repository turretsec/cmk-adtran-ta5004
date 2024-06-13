from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    startswith,
    SNMPTree,
    State,
    any_of,
    Metric,
)

# Parse Function
def parse_adtran(string_table):
    # All interfaces found in SNMP
    adtranInterfaces = {}
    # Only for selected interfaces
    adtranONTInterfaces = {}
    column_names=[
        "interface",
        "ifDesc",
        "ifType",
        "ifMTU",
        "ifSpeed",
        "ifMAC",
        "ifAdminStatus",
        "ifOpStatus",
        "ifLastChange",
        "if_in_bytes_agg",
        "if_in_unicast",
        "if_in_non_unicast",
        "if_in_discards",
        "if_in_errors",
        "if_out_bytes_agg",
        "if_out_unicast",
        "if_out_non_unicast",
        "if_out_discards",
        "if_out_errors"
    ]

    # Map string_table to column_names and store in adtranInterfaces
    for line in string_table:
        adtranInterfaces[line[0]] = {}
        for n in range(0, len(column_names)):
            adtranInterfaces[line[0]][column_names[n]]=line[n]
    
    # Filter to only selected interfaces and store in adtranONTInterfaces
    for interface in adtranInterfaces:
        if "ONT Port" in adtranInterfaces[interface]['ifDesc']:
            description = (adtranInterfaces[interface]['ifDesc']).split(',')
            shelf = (description[0]).replace('Shelf: ', '', 1)
            slot = (description[1]).replace(' Slot: ', '', 1)
            pon = (description[2]).replace(' Pon: ', '', 1)
            ont = (description[3]).replace(' ONT: ', '', 1)
            if int(ont) < 10:
                ont = f"0{ont}"
            port = (description[4]).replace(' ONT Port: ', '', 1)
            serviceName = f"ONT {shelf}:{slot}:{pon}:{ont} Port {port}"
            adtranONTInterfaces[serviceName]=adtranInterfaces[interface]
        if "Serial" in adtranInterfaces[interface]['ifDesc']:
            description = (adtranInterfaces[interface]['ifDesc']).split(',')
            shelf = (description[0]).replace('Shelf: ', '', 1)
            slot = (description[1]).replace(' Slot: ', '', 1)
            pon = (description[2]).replace(' Pon: ', '', 1)
            ont = (description[3]).replace(' ONT: ', '', 1)
            if int(ont) < 10:
                ont = f"0{ont}"
            serviceName = f"ONT {shelf}:{slot}:{pon}:{ont}"
            adtranONTInterfaces[serviceName]=adtranInterfaces[interface]
        if adtranInterfaces[interface]['ifType'] == "208":
            description = (adtranInterfaces[interface]['ifDesc']).split(',')
            shelf = (description[0]).replace('Shelf: ', '', 1)
            slot = (description[1]).replace(' Slot: ', '', 1)
            pon = (description[2]).replace(' Pon: ', '', 1)
            serviceName = f"Pon {shelf}:{slot}:{pon}"
            adtranONTInterfaces[serviceName]=adtranInterfaces[interface]

    # Return Adtran ONT Interfaces        
    return adtranONTInterfaces

# Discovery Function
def discover_adtran(section):
    for group in section:
        yield Service(item=group)

# Check Function
def check_adtran(item, section):
    if item not in section:
        return

    attr = section.get(item)

    if attr['ifDesc']:
        interface_description = attr['ifDesc']
    else:
        interface_description = ''
    if attr['ifType']:
        interface_type = attr['ifType']
    else:
        interface_type = ''
    if attr['ifOpStatus']:
        interface_op_status = attr['ifOpStatus']
    else:
        interface_op_status = ''


    yield Result(
        state=State.OK,
        summary=f"OK, Description: {interface_description}, Type: {interface_type}, Status: {interface_op_status}"
        )

    # Integer Conversion and Validation for Metrics
    # Using a loop was causing a large performance hit?
    if attr['if_in_bytes_agg']:
        metric_if_in_bytes_agg = int(attr['if_in_bytes_agg'])
    else:
        metric_if_in_bytes_agg = 0
    if attr['if_in_unicast']:
        metric_if_in_unicast = int(attr['if_in_unicast'])
    else:
        metric_if_in_unicast = 0
    if attr['if_in_non_unicast']:
        metric_if_in_non_unicast = int(attr['if_in_non_unicast'])
    else:
        metric_if_in_non_unicast = 0
    if attr['if_in_discards']:
        metric_if_in_discards = int(attr['if_in_discards'])
    else:
        metric_if_in_discards = 0
    if attr['if_in_errors']:
        metric_if_in_errors = int(attr['if_in_errors'])
    else:
        metric_if_in_errors = 0
    if attr['if_out_bytes_agg']:
        metric_if_out_bytes_agg = int(attr['if_out_bytes_agg'])
    else:
        metric_if_out_bytes_agg = 0
    if attr['if_out_unicast']:
        metric_if_out_unicast = int(attr['if_out_unicast'])
    else:
        metric_if_out_unicast = 0
    if attr['if_out_non_unicast']:
        metric_if_out_non_unicast = int(attr['if_out_non_unicast'])
    else:
        metric_if_out_non_unicast = 0
    if attr['if_out_discards']:
        metric_if_out_discards = int(attr['if_out_discards'])
    else:
        metric_if_out_discards = 0
    if attr['if_out_errors']:
        metric_if_out_errors = int(attr['if_out_errors'])
    else:
        metric_if_out_errors = 0

    # Interface Metrics
    if "(Eth)" in interface_description:
        yield Metric(
            name="if_in_bytes_agg",
            value=metric_if_in_bytes_agg,
        )
        yield Metric(
            name="if_out_bytes_agg",
            value=metric_if_out_bytes_agg,
        )
        yield Metric(
            name="if_in_errors",
            value=metric_if_in_errors,
        )
        yield Metric(
            name="if_in_discards",
            value=metric_if_in_discards,
        )
        yield Metric(
            name="if_out_errors",
            value=metric_if_out_errors,
        )
        yield Metric(
            name="if_out_discards",
            value=metric_if_out_discards,
        )
        yield Metric(
            name="if_in_unicast",
            value=metric_if_in_unicast,
        )
        yield Metric(
            name="if_out_unicast",
            value=metric_if_out_unicast,
        )
        yield Metric(
            name="if_in_non_unicast",
            value=metric_if_in_non_unicast,
        )
        yield Metric(
            name="if_out_non_unicast",
            value=metric_if_out_non_unicast,
        )

# OIDs corresponding to the Adtran TA5004
detectAdtran = any_of(
    startswith(".1.3.6.1.2.1.1.1.0", "TA5004"),
    startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.664.1.1351"),
)

register.snmp_section(
    name = "adtran_base_config",
    parse_function = parse_adtran,
    detect = detectAdtran,
    fetch = SNMPTree(
        base = ".1.3.6.1.2.1.2.2.1",
        oids = [
            '1', # interface
            '2', # ifDesc
            '3', # ifType
            '4', # ifMTU
            '5', # ifSpeed
            '6', # ifMAC
            '7', # ifAdminStatus
            '8', # ifOpStatus
            '9', # ifLastChange
            '10', # ifInOctets
            '11', # ifInUcastPkts
            '12', # ifInNUcastPkts
            '13', # ifInDiscards
            '14', # ifInErrors
            '16', # ifOutOctets
            '17', # ifOutUcastPkts
            '18', # ifOutNUcastPkits
            '19', # ifOutDiscards
            '20', # ifOutErrors
            ],
    ),
)

register.check_plugin(
    name = "adtran_check",
    sections = ["adtran_base_config"],
    service_name = "Adtran %s",
    discovery_function = discover_adtran,
    check_function = check_adtran,
)