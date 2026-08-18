<div align="center">
  <img src="https://raw.githubusercontent.com/Devopstrio/.github/main/assets/Browser_logo.png" alt="Devopstrio Logo" height="60">
</div>

<h1 align="center">Edge Autonomous Agent</h1>

<p align="center">
  <strong>Intelligent ReAct Daemon for IoT Environments</strong>
</p>

---

## 1. Executive Summary

The **Edge Autonomous Agent** is the 'Brain' of the DevopsTrio local edge node. While `edge-runtime` provides the raw LLM capability, this repository acts as the continuous LangChain daemon that listens to physical world events (via MQTT), reasons about anomalies using the local model, and executes physical tools.

It operates 100% offline, ensuring critical industrial control systems (ICS) remain safe and responsive even if internet connectivity drops.

---

## 2. High-Level Architecture

<div align="center">
  <img src="docs/architecture.jpg" alt="Edge Agent Architecture" width="800">
</div>

### System Flow Diagram
```mermaid
graph TD
    subgraph FactoryFloor["Factory Floor"]
        Sensors["IoT Sensors"]
        Machines["Physical Infrastructure"]
        Alarms["Siren / Alarm System"]
    end
    
    subgraph AgentNode["Edge Agent Node"]
        MQTT{"MQTT Broker (Local)"}
        EventLoop["Sensor Event Loop"]
        ReAct["LangChain ReAct Agent"]
        Tools["Physical Tools"]
    end
    
    subgraph LLMNode["Edge Runtime Node"]
        LocalLLM["Local LLM (GGUF)"]
    end
    
    Sensors -->|Publish| MQTT
    MQTT -->|Consume| EventLoop
    EventLoop -->|Anomaly Detected!| ReAct
    
    ReAct <-->|HTTP POST| LocalLLM
    ReAct -->|Invoke| Tools
    
    Tools -->|Send Control Signal| Machines
    Tools -->|Trigger Alert| Alarms
    
    classDef floor fill:#f0fdf4,stroke:#166534,stroke-width:2px,color:#000000;
    classDef agent fill:#f9f0ff,stroke:#6b21a8,stroke-width:2px,color:#000000;
    classDef llm fill:#fef3c7,stroke:#b45309,stroke-width:2px,color:#000000;
    
    class Sensors,Machines,Alarms floor;
    class EventLoop,ReAct,Tools,MQTT agent;
    class LocalLLM llm;
```

* **Sensor Event Loop**: Uses `aiomqtt` to actively monitor high-throughput sensor telemetry.
* **LangChain Integration**: Connects to an OpenAI-compatible endpoint pointed at `http://edge-runtime:8080/v1` to utilize a local quantized LLM for zero-shot ReAct reasoning.
* **Physical Tools**: Pre-configured LangChain tools like `ShutdownMachineTool` and `TriggerAlarmTool` allow the LLM to impact the real world.

---

## 3. Deployment

Start the agent loop and mock MQTT services locally:

```bash
docker-compose up -d --build
```

### Simulating an Anomaly
Publish a high temperature to the MQTT broker to wake the agent:
```bash
docker exec -it edge-agent_mosquitto_1 mosquitto_pub -t "sensors/motor_A/telemetry" -m '{"temperature": 110.5}'
```
*Watch the docker logs to see the Agent wake up, reason, and trigger the shutdown sequence!*

<hr>
<p align="center">
  <br>
  <i>Autonomous Edge Intelligence.</i>
  <br>
  <b><a href="https://devopstrio.com">© 2026 DevopsTrio Consulting. All rights reserved.</a></b>
</p>
