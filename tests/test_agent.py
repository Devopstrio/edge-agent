from unittest.mock import AsyncMock, patch

import pytest

from edgeagent.core.agent_loop import EdgeAutonomousAgent


@pytest.mark.asyncio
async def test_agent_handle_anomaly() -> None:
    # Mock the LLM chain invoke to prevent needing a real LLM in CI
    with patch("langchain.agents.agent.AgentExecutor.ainvoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {"output": "I have triggered the alarm and shutdown the machine."}
        
        agent = EdgeAutonomousAgent()
        response = await agent.handle_anomaly("sensor_42", 105.5, 100.0)
        
        assert "triggered the alarm" in response
        mock_invoke.assert_called_once()
        
        call_args = mock_invoke.call_args[0][0]
        assert "sensor_42" in call_args["input"]
        assert "105.5" in call_args["input"]
