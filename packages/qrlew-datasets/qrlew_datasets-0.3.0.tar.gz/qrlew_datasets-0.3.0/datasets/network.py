import subprocess
import logging

NAME: str = 'qrlew-net'

class Network:
    """Create a network"""
    def __init__(self, name=NAME):
        self.name = name
        try:
            subprocess.run(['docker', 'network', 'create', self.name])
        except:
            logging.info("docker not installed")
