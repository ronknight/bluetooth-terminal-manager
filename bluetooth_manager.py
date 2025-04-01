from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typing import Dict, Optional, Set, Any
import asyncio
from bt_utils import decode_manufacturer_data, sort_devices_by_rssi
import json
import os

class BluetoothManager:
    def __init__(self):
        self.nearby_devices = {}
        self._discovered_devices = set()
        self._known_devices_file = "known_devices.json"
        self._known_devices = self._load_known_devices()
        
    def _load_known_devices(self) -> Dict[str, Dict[str, Any]]:
        """Load known devices from storage"""
        if os.path.exists(self._known_devices_file):
            try:
                with open(self._known_devices_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_known_devices(self):
        """Save known devices to storage"""
        with open(self._known_devices_file, 'w') as f:
            json.dump(self._known_devices, f, indent=2)

    async def _detection_callback(self, device: BLEDevice, advertisement_data: AdvertisementData):
        """Callback for device detection to gather more detailed information"""
        if device.address not in self._discovered_devices:
            self._discovered_devices.add(device.address)
            name = None
            
            # Try multiple sources for the device name
            if advertisement_data.local_name:
                name = advertisement_data.local_name
            elif device.name:
                name = device.name
            
            name = name or "Unknown"
            addr = str(device.address)
            
            # Decode manufacturer data
            decoded_manufacturer_data = []
            for mfg_id, data in advertisement_data.manufacturer_data.items():
                decoded = decode_manufacturer_data(mfg_id, data)
                decoded_manufacturer_data.append(decoded)
            
            self.nearby_devices[addr] = {
                'name': name,
                'rssi': advertisement_data.rssi,
                'manufacturer_data': decoded_manufacturer_data,
                'service_data': advertisement_data.service_data,
                'service_uuids': advertisement_data.service_uuids
            }
            
    async def scan_devices(self, duration: int = 8) -> Dict[str, Dict[str, Any]]:
        """Scan for nearby Bluetooth devices"""
        print(f"Scanning for devices (this will take about {duration} seconds)...")
        self.nearby_devices = {}
        self._discovered_devices = set()
        
        scanner = BleakScanner(detection_callback=self._detection_callback)
        await scanner.start()
        await asyncio.sleep(duration)
        await scanner.stop()
        
        # Sort devices by signal strength
        self.nearby_devices = sort_devices_by_rssi(self.nearby_devices)
        return self.nearby_devices
    
    async def get_device_info(self, addr: str) -> Optional[dict]:
        """Get detailed information about a specific device"""
        try:
            device = await BleakScanner.find_device_by_address(addr)
            if device:
                async with BleakClient(device) as client:
                    services = await client.get_services()
                    return {
                        "address": addr,
                        "name": device.name or "Unknown",
                        "services": [service.description for service in services]
                    }
            return None
        except Exception as e:
            print(f"Error getting device info: {e}")
            return None
    
    async def connect_device(self, addr: str) -> bool:
        """Attempt to connect to a device"""
        try:
            device = await BleakScanner.find_device_by_address(addr)
            if not device:
                print("Device not found")
                return False
                
            async with BleakClient(device) as client:
                if client.is_connected:
                    # Load existing device info to preserve custom name
                    existing_device = self._known_devices.get(addr, {})
                    self._known_devices[addr] = {
                        "name": existing_device.get("name") or device.name or "Unknown",
                        "last_connected": asyncio.get_running_loop().time()
                    }
                    self._save_known_devices()
                    print(f"Successfully connected to {self._known_devices[addr]['name']}")
                    return True
            return False
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    async def disconnect_device(self, addr: str) -> bool:
        """Disconnect from a connected device"""
        try:
            device = await BleakScanner.find_device_by_address(addr)
            if not device:
                print("Device not found")
                return False
            
            # Attempt to disconnect by creating a new client and closing it
            async with BleakClient(device) as client:
                if client.is_connected:
                    await client.disconnect()
                    print(f"Successfully disconnected from {device.name or addr}")
                    return True
                else:
                    print("Device was not connected")
                    return False
        except Exception as e:
            print(f"Failed to disconnect: {e}")
            return False
    
    def forget_device(self, addr: str) -> bool:
        """Forget a known device"""
        if addr in self._known_devices:
            del self._known_devices[addr]
            self._save_known_devices()
            if addr in self._discovered_devices:
                self._discovered_devices.remove(addr)
            if addr in self.nearby_devices:
                del self.nearby_devices[addr]
            print(f"Device {addr} has been forgotten")
            return True
        else:
            print("Device was not in known devices list")
            return False
            
    def get_known_devices(self) -> Dict[str, Dict[str, Any]]:
        """Get list of known devices"""
        self._known_devices = self._load_known_devices()  # Reload before returning
        return self._known_devices