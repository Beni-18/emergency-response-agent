# Multi-Agent Emergency Response Coordinator

## 🚨 Project Overview

The **Emergency Response Coordinator** is an AI-powered multi-agent system built with Google's Agent Development Kit (ADK) that coordinates emergency responders, assesses critical situations, and optimizes resource allocation for healthcare and safety emergencies.

## 🎯 Problem Statement

Emergency response teams face critical challenges:
- **Information Overload**: Multiple incoming emergency calls with incomplete/conflicting information
- **Resource Misallocation**: Limited ambulances, fire trucks, and medical personnel deployed inefficiently
- **Response Delays**: Manual coordination between different emergency units causes treatment delays
- **Poor Triage**: Inconsistent prioritization of critical patients leads to preventable deaths

This project tackles these problems through an intelligent multi-agent system that automates coordination and decision-making.

## ✨ Solution Architecture

### Multi-Agent System Design

The system implements **4 specialized agents** working in parallel and sequentially:

1. **Incident Assessment Agent** (LLM-powered)
   - Analyzes emergency calls and extracts key information
   - Determines incident type (cardiac, trauma, fire, etc.)
   - Estimates severity on a scale of 1-10

2. **Resource Allocation Agent** (Sequential/Parallel)
   - Tracks available responders and equipment
   - Calculates optimal deployment routes
   - Recommends resource dispatch strategy

3. **Triage Coordination Agent** (Loop Agent)
   - Maintains patient queue and priority levels
   - Updates priorities as new information arrives
   - Coordinates with hospitals for bed availability

4. **Communication Relay Agent** (Tool-based)
   - Dispatches instructions to responders
   - Maintains session memory of ongoing operations
   - Provides real-time status updates

### Key Technologies Implemented

- **Multi-Agent Orchestration**: Sequential, parallel, and loop-based agent coordination
- **LLM Integration**: Google Gemini for intelligent decision-making
- **Tools & MCP**: Custom tools for resource lookup, route optimization
- **Sessions & Memory**: Long-term memory for case history and patterns
- **Context Engineering**: Adaptive prompt engineering for emergency scenarios
- **Observability**: Comprehensive logging and tracing of all agent interactions

## 📁 Project Structure

```
emergency-response-agent/
├── src/
│   ├── agents/
│   │   ├── incident_assessment.py      # Analyzes emergency incidents
│   │   ├── resource_allocator.py       # Optimizes resource deployment
│   │   ├── triage_coordinator.py       # Manages patient prioritization
│   │   └── communication_relay.py      # Dispatches information
│   ├── tools/
│   │   ├── resource_lookup.py          # Query available resources
│   │   ├── route_optimization.py       # Calculate optimal routes
│   │   ├── hospital_availability.py    # Check hospital bed availability
│   │   └── responder_status.py         # Get responder status updates
│   ├── memory/
│   │   ├── session_manager.py          # Session state management
│   │   └── memory_bank.py              # Long-term case memory
│   ├── config/
│   │   ├── agents_config.yaml          # Agent configuration
│   │   └── prompts.py                  # System prompts for agents
│   └── main.py                          # Main orchestrator
├── tests/
│   ├── test_incident_assessment.py
│   ├── test_resource_allocation.py
│   └── test_multi_agent_flow.py
├── examples/
│   ├── cardiac_emergency.json          # Example scenario 1
│   ├── mass_casualty.json              # Example scenario 2
│   └── fire_emergency.json             # Example scenario 3
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud SDK
- API key for Google Gemini

### Installation

```bash
# Clone the repository
git clone https://github.com/Beni-18/emergency-response-agent.git
cd emergency-response-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_API_KEY="your-gemini-api-key"
export PROJECT_ID="your-google-cloud-project-id"
```

### Running the System

```bash
# Run with a sample emergency scenario
python src/main.py --scenario examples/cardiac_emergency.json

# Run with interactive input
python src/main.py --interactive

# Run tests
pytest tests/
```

## 📊 Features Implemented

### Multi-Agent System
- ✅ Multi-agent architecture with 4+ specialized agents
- ✅ LLM-powered incident assessment
- ✅ Parallel agent execution for resource allocation
- ✅ Sequential agent workflows for prioritization
- ✅ Loop-based agents for continuous monitoring

### Tools & Integrations
- ✅ Custom tools for resource lookup and route optimization
- ✅ Google Search API integration for real-time data
- ✅ Code execution tools for complex calculations
- ✅ OpenAPI tools for hospital system integration

### Memory & Sessions
- ✅ InMemorySessionService for state management
- ✅ Memory Bank for long-term case history
- ✅ Context compaction for efficient token usage

### Observability
- ✅ Comprehensive logging of all agent decisions
- ✅ Distributed tracing of request flows
- ✅ Metrics collection for performance monitoring

### Advanced Concepts
- ✅ Long-running operations with pause/resume capability
- ✅ A2A Protocol for agent-to-agent communication
- ✅ Agent evaluation framework
- ✅ Deployment-ready architecture

## 💡 Example Usage

```python
from src.agents.incident_assessment import IncidentAssessmentAgent
from src.agents.resource_allocator import ResourceAllocatorAgent
from src.memory.session_manager import SessionManager

# Initialize session
session = SessionManager(session_id="emergency-001")

# Create incident
incident = {
    "call_id": "911-2024-001",
    "location": "123 Main St, Hospital District",
    "description": "Cardiac patient, unresponsive",
    "severity_indicators": ["chest pain", "shortness of breath"]
}

# Assess incident
assessment_agent = IncidentAssessmentAgent()
assessment = assessment_agent.assess(incident, session)
print(f"Incident Type: {assessment['type']}")
print(f"Severity Score: {assessment['severity']}/10")

# Allocate resources
resource_agent = ResourceAllocatorAgent()
resources = resource_agent.allocate(assessment, session)
print(f"Dispatching: {resources['dispatch_plan']}")
```

## 🎓 Learning Outcomes

This project demonstrates:
- Advanced multi-agent orchestration patterns
- Integration of LLMs with enterprise systems
- Real-world problem solving with AI agents
- Production-ready agent deployment
- State management and memory persistence
- Observable and traceable AI systems

## 📈 Impact

**Potential Benefits:**
- **30-40% reduction** in response times
- **50%+ improvement** in resource utilization
- **25-35% decrease** in patient wait times
- **Better triage** resulting in improved patient outcomes

## 🔐 Security Notes

⚠️ **Important**: No API keys or sensitive credentials are included in this code. Always use environment variables for authentication.

## 📝 License

MIT License - see LICENSE file for details

## 👥 Author

Built as part of the Kaggle Agents Intensive - Capstone Project (Dec 2025)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

---

**Track**: Agents for Good (Healthcare & Safety Emergency Response)
