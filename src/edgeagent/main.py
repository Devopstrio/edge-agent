import asyncio

import structlog

from edgeagent.events.sensor_event_loop import run_sensor_loop

logger = structlog.get_logger()

if __name__ == "__main__":
    logger.info("Initializing DevopsTrio Edge Autonomous Agent")
    try:
        asyncio.run(run_sensor_loop())
    except KeyboardInterrupt:
        logger.info("Agent shutdown requested by user.")
