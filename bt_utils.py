from typing import Dict, Any, Optional

# Common Bluetooth manufacturer IDs
MANUFACTURERS = {
    0: "Ericsson Technology Licensing",
    1: "Nokia Mobile Phones",
    2: "Intel Corp.",
    3: "IBM Corp.",
    4: "Toshiba Corp.",
    5: "3Com",
    6: "Microsoft",
    7: "Lucent",
    8: "Motorola",
    9: "Infineon Technologies AG",
    10: "Cambridge Silicon Radio",
    11: "Silicon Wave",
    12: "Digianswer A/S",
    13: "Texas Instruments Inc.",
    14: "Parthus Technologies Inc.",
    15: "Broadcom Corporation",
    16: "Mitel Semiconductor",
    17: "Widcomm, Inc.",
    18: "Zeevo, Inc.",
    19: "Atmel Corporation",
    20: "Mitsubishi Electric Corporation",
    21: "RTX Telecom A/S",
    22: "KC Technology Inc.",
    23: "Newlogic",
    24: "Transilica, Inc.",
    25: "Rohde & Schwarz GmbH & Co. KG",
    26: "TTPCom Limited",
    27: "Signia Technologies, Inc.",
    28: "Conexant Systems Inc.",
    29: "Qualcomm",
    30: "Inventel",
    31: "AVM Berlin",
    32: "BandSpeed, Inc.",
    33: "Mansella Ltd",
    34: "NEC Corporation",
    35: "WavePlus Technology Co., Ltd.",
    36: "Alcatel",
    37: "NXP Semiconductors (formerly Philips Semiconductors)",
    38: "C Technologies",
    39: "Open Interface",
    40: "R F Micro Devices",
    41: "Hitachi Ltd",
    42: "Symbol Technologies, Inc.",
    43: "Tenovis",
    44: "Macronix International Co. Ltd.",
    45: "GCT Semiconductor",
    46: "Norwood Systems",
    47: "MewTel Technology Inc.",
    48: "ST Microelectronics",
    49: "Synopsys, Inc.",
    50: "Red-M (Communications) Ltd",
    51: "Commil Ltd",
    52: "Computer Access Technology Corporation (CATC)",
    53: "Eclipse (HQ Espana) S.L.",
    54: "Renesas Electronics Corporation",
    55: "Mobilian Corporation",
    384: "Plantronics/Poly (Including Altec Lansing)",
    224: "Google Inc.",
    76: "Apple, Inc.",
    # Add more as needed
}

def get_manufacturer_name(manufacturer_id: int) -> str:
    """Get manufacturer name from ID"""
    return MANUFACTURERS.get(manufacturer_id, f"Unknown Manufacturer ({manufacturer_id})")

def decode_manufacturer_data(manufacturer_id: int, data: bytes) -> Dict[str, Any]:
    """Decode manufacturer-specific data"""
    result = {
        "manufacturer": get_manufacturer_name(manufacturer_id),
        "raw_data": data.hex()
    }
    
    # Apple-specific decoding
    if manufacturer_id == 76:  # Apple
        if len(data) > 0:
            type_code = data[0] if len(data) > 0 else None
            result["type"] = {
                0x01: "iBeacon",
                0x07: "AirDrop",
                0x09: "AirPods",
                0x0A: "AirPlay",
                0x0C: "Find My",
                0x10: "Nearby",
                0x12: "HomeKit"
            }.get(type_code, f"Unknown Apple Type (0x{type_code:02x})" if type_code else "Unknown")
            
    # Microsoft-specific decoding
    elif manufacturer_id == 6:  # Microsoft
        result["type"] = "Microsoft Device"
        
    # Google-specific decoding
    elif manufacturer_id == 224:  # Google
        result["type"] = "Google Fast Pair Device"
        
    return result

def sort_devices_by_rssi(devices: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Sort devices by signal strength (RSSI)"""
    sorted_items = sorted(
        devices.items(),
        key=lambda x: x[1].get('rssi', -100),  # Default to -100 if no RSSI
        reverse=True  # Highest (least negative) first
    )
    return dict(sorted_items)