import click
import asyncio
from bluetooth_manager import BluetoothManager
from colorama import Fore, Style, init
from functools import wraps
from typing import Dict, Any

# Initialize colorama for Windows color support
init()

def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

def format_signal_strength(rssi: int) -> str:
    """Format signal strength with a visual indicator"""
    if rssi >= -60:
        return f"{Fore.GREEN}Excellent ({rssi} dBm)●●●●{Style.RESET_ALL}"
    elif rssi >= -70:
        return f"{Fore.LIGHTGREEN_EX}Good ({rssi} dBm)●●●○{Style.RESET_ALL}"
    elif rssi >= -80:
        return f"{Fore.YELLOW}Fair ({rssi} dBm)●●○○{Style.RESET_ALL}"
    elif rssi >= -90:
        return f"{Fore.RED}Poor ({rssi} dBm)●○○○{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Very Poor ({rssi} dBm)○○○○{Style.RESET_ALL}"

@click.group()
def cli():
    """Bluetooth Terminal Manager"""
    pass

@cli.command()
@click.option('--duration', '-d', default=8, type=click.IntRange(1, 300),
              help='Scan duration in seconds (1-300)')
@click.option('--mode', '-m', type=click.Choice(['quick', 'normal', 'deep']), 
              default='normal', help='Scan mode: quick (3s), normal (8s), or deep (30s)')
@click.option('--continuous', '-c', is_flag=True, 
              help='Continuous scanning mode - keeps scanning until interrupted')
@click.option('--verbose', '-v', count=True,
              help='Verbosity level: -v for basic details, -vv for full details including raw data')
@async_command
async def scan(duration, mode, continuous, verbose):
    """Scan for nearby Bluetooth devices with flexible duration options"""
    manager = BluetoothManager()
    
    # Determine scan duration based on mode if duration wasn't explicitly set
    if mode == 'quick' and duration == 8:
        duration = 3
    elif mode == 'deep' and duration == 8:
        duration = 30
        
    try:
        while True:
            click.echo(f"{Fore.CYAN}Starting {mode} scan for {duration} seconds...{Style.RESET_ALL}")
            devices = await manager.scan_devices(duration)
            
            if not devices:
                click.echo(f"{Fore.YELLOW}No devices found!{Style.RESET_ALL}")
                if not continuous:
                    return
                continue
            
            click.echo(f"\n{Fore.GREEN}Found {len(devices)} devices (sorted by signal strength):{Style.RESET_ALL}")
            
            for addr, info in devices.items():
                click.echo(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
                name = info['name']
                click.echo(f"{Fore.CYAN}Address: {Style.RESET_ALL}{addr}")
                click.echo(f"{Fore.CYAN}Name: {Style.RESET_ALL}{name}")
                click.echo(f"{Fore.CYAN}Signal: {Style.RESET_ALL}{format_signal_strength(info['rssi'])}")
                
                # Show manufacturer data based on verbosity
                if info['manufacturer_data']:
                    click.echo(f"{Fore.CYAN}Device Type:{Style.RESET_ALL}")
                    for mfg_data in info['manufacturer_data']:
                        click.echo(f"  • {mfg_data['manufacturer']}")
                        if 'type' in mfg_data:
                            click.echo(f"    Type: {mfg_data['type']}")
                        # Show raw data only with -vv
                        if verbose >= 2:
                            click.echo(f"    Raw: {mfg_data['raw_data']}")
                
                # Show services with -v or -vv
                if verbose >= 1 and info['service_uuids']:
                    click.echo(f"{Fore.CYAN}Services:{Style.RESET_ALL}")
                    for uuid in info['service_uuids']:
                        click.echo(f"  • {uuid}")
            
            if not continuous:
                break
                
            click.echo(f"\n{Fore.YELLOW}Press Ctrl+C to stop continuous scanning...{Style.RESET_ALL}")
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}Scanning stopped by user{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"\n{Fore.RED}Error during scanning: {e}{Style.RESET_ALL}")

@cli.command()
@click.argument('address')
@async_command
async def info(address):
    """Get detailed information about a specific device"""
    manager = BluetoothManager()
    info = await manager.get_device_info(address)
    
    if info:
        click.echo(f"\n{Fore.GREEN}Device Information:{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Address: {Style.RESET_ALL}{info['address']}")
        click.echo(f"{Fore.CYAN}Name: {Style.RESET_ALL}{info['name']}")
        if info['services']:
            click.echo(f"\n{Fore.CYAN}Available Services:{Style.RESET_ALL}")
            for service in info['services']:
                click.echo(f"  • {service}")
    else:
        click.echo(f"{Fore.RED}Could not get device information{Style.RESET_ALL}")

@cli.command()
@click.argument('address')
@async_command
async def connect(address):
    """Connect to a specific Bluetooth device"""
    manager = BluetoothManager()
    success = await manager.connect_device(address)
    
    if success:
        click.echo(f"{Fore.GREEN}Successfully connected to device!{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}Failed to connect to device{Style.RESET_ALL}")

@cli.command()
@click.argument('address')
@async_command
async def disconnect(address):
    """Disconnect from a specific Bluetooth device"""
    manager = BluetoothManager()
    success = await manager.disconnect_device(address)
    
    if success:
        click.echo(f"{Fore.GREEN}Successfully disconnected from device{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}Failed to disconnect from device{Style.RESET_ALL}")

@cli.command()
@click.argument('address')
@async_command
async def forget(address):
    """Forget a paired Bluetooth device"""
    manager = BluetoothManager()
    success = manager.forget_device(address)
    
    if success:
        click.echo(f"{Fore.GREEN}Device has been forgotten{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}Could not forget device - it may not be in the known devices list{Style.RESET_ALL}")

@cli.command(name='known-devices')
@async_command
async def known_devices():
    """List all known/paired devices"""
    manager = BluetoothManager()
    devices = manager.get_known_devices()
    
    if not devices:
        click.echo(f"{Fore.YELLOW}No known devices{Style.RESET_ALL}")
        return
        
    click.echo(f"\n{Fore.GREEN}Known devices:{Style.RESET_ALL}")
    for addr, info in devices.items():
        click.echo(f"\n{Fore.CYAN}Address: {Style.RESET_ALL}{addr}")
        click.echo(f"{Fore.CYAN}Name: {Style.RESET_ALL}{info['name']}")
        if 'last_connected' in info:
            click.echo(f"{Fore.CYAN}Last Connected: {Style.RESET_ALL}{info['last_connected']}")

if __name__ == '__main__':
    cli()