import logging
logger = logging.getLogger(__name__)

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dd8.utils.email_ import Gmail

if __name__ == '__main__':    
    key = os.getenv('GMAIL_SECRET')

