import os

import structlog
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI

from edgeagent.tools.physical_tools import get_edge_tools

logger = structlog.get_logger()

# By default, point to the local edge-runtime server running on the same hardware
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://edge-runtime:8080/v1")

class EdgeAutonomousAgent:
    def __init__(self) -> None:
        self.tools = get_edge_tools()
        self.llm = ChatOpenAI(
            base_url=LOCAL_LLM_URL,
            api_key="local-edge-key",
            model="local-edge-model",
            temperature=0.1
        )
        
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )

    async def handle_anomaly(self, sensor_id: str, value: float, threshold: float) -> str:
        logger.info("Agent invoked to handle anomaly", sensor_id=sensor_id, value=value)
        prompt = (
            f"URGENT: Sensor {sensor_id} has breached critical thresholds. "
            f"Current value is {value}, which is above the safe limit of {threshold}. "
            "Use your tools to query historical context if needed, trigger alarms, "
            "or shutdown the machine to prevent a fire."
        )
        try:
            # Using synchronous invoke inside an async context for simplicity, 
            # ideally we'd use agent.ainvoke, but keeping it simple for the edge wrapper.
            response = await self.agent.ainvoke({"input": prompt})
            return str(response.get("output", "Action completed."))
        except Exception as e:
            logger.error("Agent execution failed", error=str(e))
            return "Failed to execute agent."
