"""
This module provides a functions for starting and connecting to a Sense HAT service. This service is needed so that it can be run
as root to use the sense_hat module, while allowing clients that are not running as root to access Sense HAT data.
"""
from multiprocessing.managers import BaseManager, RemoteError
from myDevices.utils.logger import error, debug

SERVER_ADDRESS = ('127.0.0.1', 5600)
AUTH_KEY = b'sensehat'


class SenseHATManager(BaseManager):
    """Manager for sharing Sense HAT data between processes."""
    pass


def use_emulator(emulate=False):
    """Set the sensehat service to use an emulator. 
    
    Arguments:
    emulate: True if the Sense HAT Emulator should be used. This requires the Emulator to be installed and running on the desktop. 
    """
    if emulate:
        from sense_emu import SenseHat
    else:
        from sense_hat import SenseHat
    SenseHATManager.register('SenseHat', SenseHat)

def start_server(emulate=False):
    """Start the sensehat service. 
    
    Arguments:
    emulate: True if the Sense HAT Emulator should be used. This requires the Emulator to be installed and running on the desktop. 
    """
    use_emulator(emulate)
    SenseHATManager.register('use_emulator', use_emulator)
    manager = SenseHATManager(SERVER_ADDRESS, AUTH_KEY)
    manager.get_server().serve_forever()

def connect_client():
     """Connect a client to the sensehat service."""
    try:
        debug('Connecting to sensehat service')        
        SenseHATManager.register('SenseHat')
        SenseHATManager.register('use_emulator')
        manager = SenseHATManager(SERVER_ADDRESS, AUTH_KEY)
        manager.connect()
        return manager
    except RemoteError as e:
        error('Error connecting to sensehat service, if using the Sense HAT emulator make sure it is has been launched in the GUI')

