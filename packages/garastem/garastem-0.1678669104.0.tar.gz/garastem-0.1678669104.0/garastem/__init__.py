import asyncio
import time
import bleak
import os
import signal
import sys
import threading
import traceback
import garastem.version as version

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from termcolor import colored

UART_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
killed = False

try:
    import requests
    req = requests.get('https://pypi.org/pypi/garastem/json')
    package_info = req.json()
    latest_version = package_info['info']['version']
    if latest_version != version.version:
        print("Warning: Please update to latest version of this library")
except Exception as err:
    # print(err)
    pass

print('Running versions', version.version)

class GRobot:
    DISCONNECTED = 0
    CONNECTED = 1
    READY = 2
    discovered_devices = {}
    
    
    def __init__(self, name):
        self.name = name
        self.buzzer = GRobot.Buzzer(self)
        self.motor = GRobot.Motor(self)
        self.led = GRobot.Pixel(self)
        
        self.state = GRobot.DISCONNECTED
        # ble
        self.device = None
        self.client = None 
        
        # lock
        self.lock = asyncio.Lock()
        
        # recv buffer
        self.recv = bytearray()
    def handle_filter(self, device: BLEDevice, adv: AdvertisementData):
        if device.name == self.name:
            # print('Device Found: ', self.name)
            return True
        if device.name is not None:
            if device.name not in GRobot.discovered_devices:
                GRobot.discovered_devices[device.name] = None
                print('Found: ', device.name)
        return False
    def handle_disconnect(self, _: BleakClient):
        self.state = GRobot.DISCONNECTED
        print(f'grobot/ device disconnected')
        
    async def wait(self, ms: int = 0):
        print('grobot/ wait for {} ms'.format(ms))
        await asyncio.sleep(ms/1000)
    
    async def ensure_ready(self):
        async with self.lock:
            await self.ensure_connect()
            if self.state == GRobot.READY:
                return
            
            while True:
                await asyncio.sleep(1)
                self.recv.clear()
                await self.client.write_gatt_char(UART_RX_CHAR_UUID, b'*G#')
                await asyncio.sleep(0.1)
                await self.client.write_gatt_char(UART_RX_CHAR_UUID, b'*ffffff#')
                future = time.time() + 1
                while time.time() < future:
                    await asyncio.sleep(0.01)
                    if b'|||||' in self.recv or b'ffffff' in self.recv:
                        break
                else:
                    print("grobot/ timed out, make sure this is in Yellow Mode")
                
                # print('Chek', self.recv)
                if b'|||||' in self.recv or b'ffffff' in self.recv:
                    self.recv.clear()
                    break
            print("Connected")
            self.state = GRobot.READY
            

            
    
    def handle_rx(self, _: BleakGATTCharacteristic, data: bytearray):
        print(f'grobot/ recv: {data}')
        self.recv += data
    
    async def ensure_connect(self):
        if self.state >= GRobot.CONNECTED:
            return
        # start discovery, make sure after this the device is conencted to bluetooth
        while True:
            await asyncio.sleep(1)
            try:
                device = await BleakScanner.find_device_by_filter(self.handle_filter)
                if device is None:
                    print(f'grobot/ still finding {self.name}')
                    continue
                self.device = device 
                self.client = BleakClient(
                    self.device,
                    disconnected_callback=self.handle_disconnect
                )
                print(f'grobot/ device {self.name} is found')
                await self.client.connect()
                print(f'grobot/ device {self.name} is CONNECTED')
                await self.client.start_notify(UART_RX_CHAR_UUID, self.handle_rx)
                self.state = GRobot.CONNECTED
                return
                
            except:
                print("grobot/ please turn on bluetooth")                            
    
        
    async def send(self, send, expect=None):
        if isinstance(send, str):
            send = send.encode('utf8')
        self.recv.clear()
        print(f'core/ write {send}, expect {expect}')
        await self.client.write_gatt_char(UART_RX_CHAR_UUID, send)
        if expect is None: 
            expect = send[1:-1]
        if isinstance(expect, str):
            expect = expect.encode('utf8')
        
        future = time.time() + 5
        while time.time() < future:
            if expect in self.recv:
                print('satisfyied')
                break
            await asyncio.sleep(0.1)
            
        else:
            raise RuntimeError("grobot/ device is not responding")
        await asyncio.sleep(0.5)
        
    class Buzzer:
        def __init__(self, parent):
            self.parent = parent
        async def turn(self, state):
            await self.parent.ensure_ready()
            print('grobot/ turn buzzer to {}'.format(state))
            await self.parent.send(f"*B{'1' if state else '0'}#", expect=b'B')

        
    class Motor:
        def __init__(self, parent):
            self.parent = parent
        async def move_forward(self, speed: float):
            await self.parent.ensure_ready()
            speed = int(speed)
            await self.parent.send(f"*M1|{'1' if speed < 0 else ''}{abs(speed)}#")
        
        async def move_backward(self, speed: float):
            await self.parent.ensure_ready()
            speed = int(speed)
            await self.parent.send(f"*M2|{'1' if speed < 0 else ''}{abs(speed)}#")
        
        async def rotate_left(self, speed: float):
            await self.parent.ensure_ready()
            speed = int(speed)
            await self.parent.send(f"*M3|{'1' if speed < 0 else ''}{abs(speed)}#")
        
        async def rotate_right(self, speed: float):
            await self.parent.ensure_ready()
            speed = int(speed)
            await self.parent.send(f"*M4|{'1' if speed < 0 else ''}{abs(speed)}#")

        async def set_motor(self, motor: int, speed: float):
            await self.parent.ensure_ready()
            speed = int(speed)
            await self.parent.send(f"*M{'5' if motor == 0 else '6'}|{'1' if speed < 0 else ''}{abs(speed)}#")

        async def stop(self):
            await self.parent.send('*M0#')
            
    class Pixel:
        def __init__(self, parent):
            self.parent = parent
        
        '''
        *D3|10|10|10#
        *G#*ffffff#*D2|1#
        *D2|2#
        *D0|1|1#
        *D1|1|100|10|10#
        *D3|100|10|10#
        *G#*ffffff#*M1|100#
        
        '''
        def ensure_color(self, h):
            if isinstance(h, str):
                h = h.replace('#', '')
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            else:
                return h
        async def set_colour(self, color, pixel=None):
            await self.parent.ensure_ready()
            color = self.ensure_color(color)
            print('grobot/ set color to {color}')
            pkg = '|'.join([
                'D3' if pixel is None else 'D1',
                str(color[0]),
                str(color[1]),
                str(color[2]),
            ])
            await self.parent.send(f'*{pkg}#', expect=pkg)
            await asyncio.sleep(2)
                
    