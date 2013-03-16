import os
import sys


# Add current directory to path so we can import settings.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import settings

__version__ = '0.1'
