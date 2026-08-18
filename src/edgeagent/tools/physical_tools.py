from typing import Any

import structlog
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

logger = structlog.get_logger()

class ShutdownMachineInput(BaseModel):
    machine_id: str = Field(description="The ID of the physical machine to shutdown")
    reason: str = Field(description="The reason for the emergency shutdown")

class ShutdownMachineTool(BaseTool): # type: ignore[override, misc]
    name: str = "shutdown_machine"
    description: str = (
        "Use this tool to issue an emergency shutdown command to a "
        "physical machine when dangerous anomalies are detected."
    )
    args_schema: Type[BaseModel] = ShutdownMachineInput

    def _run(self, machine_id: str, reason: str, run_manager: Any | None = None) -> str:
        logger.warning("EXECUTING PHYSICAL TOOL: SHUTDOWN_MACHINE", machine_id=machine_id, reason=reason)
        # In a real environment, this sends an MQTT control signal or Modbus TCP packet to a PLC
        return f"Successfully issued emergency shutdown signal to machine {machine_id}."

class TriggerAlarmInput(BaseModel):
    zone: str = Field(description="The factory zone where the alarm should sound")
    severity: str = Field(description="Severity level of the alarm (LOW, MEDIUM, HIGH, CRITICAL)")

class TriggerAlarmTool(BaseTool): # type: ignore[override, misc]
    name: str = "trigger_alarm"
    description: str = (
        "Use this tool to sound physical sirens and flashing lights "
        "in a specific factory zone to alert human operators."
    )
    args_schema: Type[BaseModel] = TriggerAlarmInput

    def _run(self, zone: str, severity: str, run_manager: Any | None = None) -> str:
        logger.warning("EXECUTING PHYSICAL TOOL: TRIGGER_ALARM", zone=zone, severity=severity)
        return f"Alarm triggered in zone {zone} with severity {severity}."

class QuerySensorDatabaseInput(BaseModel):
    sensor_id: str = Field(description="The ID of the sensor to query")

class QuerySensorDatabaseTool(BaseTool): # type: ignore[override, misc]
    name: str = "query_sensor_database"
    description: str = "Use this tool to lookup the last 5 minutes of historical context for a specific sensor."
    args_schema: type[BaseModel] = QuerySensorDatabaseInput

    def _run(self, sensor_id: str, run_manager: Any | None = None) -> str:
        logger.info("EXECUTING PHYSICAL TOOL: QUERY_SENSOR_DB", sensor_id=sensor_id)
        # Mock database query
        return f"Historical context for {sensor_id}: Normal range [40C-60C]. Current trend is spiking rapidly."

def get_edge_tools() -> list[BaseTool]:
    return [ShutdownMachineTool(), TriggerAlarmTool(), QuerySensorDatabaseTool()]
