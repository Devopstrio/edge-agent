import asyncio
import json
import os

import aiomqtt
import structlog

from edgeagent.core.agent_loop import EdgeAutonomousAgent

logger = structlog.get_logger()
MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL", "localhost")

async def run_sensor_loop() -> None:
    logger.info("Starting Autonomous Sensor Loop", broker=MQTT_BROKER_URL)
    agent = EdgeAutonomousAgent()

    while True:
        try:
            async with aiomqtt.Client(MQTT_BROKER_URL) as client:
                logger.info("Connected to local MQTT Message Bus")
                await client.subscribe("sensors/+/telemetry")
                
                async for message in client.messages:
                    topic = str(message.topic)
                    payload = message.payload.decode() if isinstance(message.payload, bytes) else message.payload
                    
                    try:
                        data = json.loads(payload)
                        temperature = data.get("temperature")
                        
                        if temperature and float(temperature) > 100.0:
                            logger.warning("Anomaly Detected. Waking up Agent.", topic=topic, temp=temperature)
                            sensor_id = topic.split("/")[1]
                            # Offload to the agent to reason about the event
                            response = await agent.handle_anomaly(sensor_id, float(temperature), 100.0)
                            logger.info("Agent finished reasoning", resolution=response)
                            
                    except json.JSONDecodeError:
                        logger.error("Invalid JSON payload", payload=payload)
                        
        except aiomqtt.MqttError as error:
            logger.warning("Lost connection to MQTT bus. Retrying...", error=str(error))
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.info("Sensor loop cancelled")
            break
        except Exception as e:
            logger.error("Unexpected error in event loop", error=str(e))
            await asyncio.sleep(5)
