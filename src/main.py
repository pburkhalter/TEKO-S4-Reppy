import logging
import os
import sys

from lib.thread import ThreadManager
from lib.limit import LimitSwitch

from settings import settings_dict
from print import PrintLoop
from api import APIController
from api.ws import WebSocketController

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(settings_dict['system']['paths']['logging'], "application.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize the ThreadManager
tm = ThreadManager()

# Register various threads
tm.register("limit", LimitSwitch)  # Registering the z-axis limit switch observer for safety
tm.register("printer", PrintLoop)  # Registering the print manager for handling print jobs

# Conditionally register API and WebSocket controllers based on settings
if settings_dict['system']['modules']['api'] == 'enabled':
    tm.register("api", APIController)  # Registering the Flask REST API for external control

if settings_dict['system']['modules']['wsc'] == 'enabled':
    tm.register("wsc", WebSocketController)  # Registering the WebSocket controller for real-time communication

# Main entry point
if __name__ == "__main__":
    # Start all registered threads
    tm.start()
