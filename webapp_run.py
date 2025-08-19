#!/usr/bin/env python3
"""
Launch web admin panel for Dating Bot
"""

import os
import sys

from data.config import webapp
from utils.logging import logger

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    import uvicorn

    logger.log("WEBAPP", "🚀 Starting Dating Bot web admin panel...")

    uvicorn.run(
        "web.app:app",  # Pass as string for reload
        host=webapp.HOST,
        port=webapp.PORT,
        reload=True,
        log_level="info",
    )
