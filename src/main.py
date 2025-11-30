"""Emergency Response Coordinator - Main Orchestrator

This module orchestrates the multi-agent system for emergency response coordination.
It coordinates between incident assessment, resource allocation, triage coordination,
and communication relay agents.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EmergencyIncident:
    """Data class representing an emergency incident."""
    call_id: str
    timestamp: str
    location: str
    description: str
    severity_indicators: List[str]
    caller_contact: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class IncidentAssessment:
    """Assessment result from the incident assessment agent."""
    incident_id: str
    incident_type: str
    severity_score: int  # 1-10 scale
    medical_priority: str  # Critical, High, Medium, Low
    recommended_response: str
    estimated_arrival_time: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ResourceAllocation:
    """Resource allocation plan from the resource allocator agent."""
    allocation_id: str
    ambulances_required: int
    fire_trucks_required: int
    personnel_required: int
    estimated_cost: float
    dispatch_order: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class EmergencyResponseCoordinator:
    """Main orchestrator for multi-agent emergency response system."""
    
    def __init__(self, project_id: str, api_key: Optional[str] = None):
        """Initialize the emergency response coordinator.
        
        Args:
            project_id: Google Cloud project ID
            api_key: Google Gemini API key (uses env var if not provided)
        """
        self.project_id = project_id
        self.api_key = api_key
        self.active_incidents: Dict[str, Dict] = {}
        self.session_memory = {}
        logger.info(f"Initialized Emergency Response Coordinator for project: {project_id}")
    
    def process_emergency_call(self, incident: EmergencyIncident) -> Dict:
        """Process an incoming emergency call using multi-agent system.
        
        This method orchestrates the flow:
        1. Assess the incident (parallel agents)
        2. Allocate resources (based on assessment)
        3. Coordinate triage (based on severity)
        4. Relay communication (continuous)
        
        Args:
            incident: EmergencyIncident object with call details
            
        Returns:
            Dictionary containing the complete response plan
        """
        logger.info(f"Processing emergency call: {incident.call_id}")
        
        # Step 1: Assessment (would call actual LLM-powered agent)
        assessment = self._assess_incident(incident)
        logger.info(f"Assessment complete - Type: {assessment.incident_type}, "
                   f"Severity: {assessment.severity_score}/10")
        
        # Step 2: Resource Allocation
        resources = self._allocate_resources(assessment)
        logger.info(f"Resources allocated - Ambulances: {resources.ambulances_required}, "
                   f"Fire trucks: {resources.fire_trucks_required}")
        
        # Step 3: Store in active incidents
        self.active_incidents[incident.call_id] = {
            'incident': incident.to_dict(),
            'assessment': assessment.to_dict(),
            'resources': resources.to_dict(),
            'status': 'DISPATCHED',
            'timestamp': datetime.now().isoformat()
        }
        
        # Step 4: Prepare response
        response = {
            'call_id': incident.call_id,
            'incident_type': assessment.incident_type,
            'severity': assessment.severity_score,
            'priority': assessment.medical_priority,
            'dispatch_plan': resources.dispatch_order,
            'estimated_arrival': assessment.estimated_arrival_time,
            'status': 'DISPATCHED'
        }
        
        logger.info(f"Response plan ready for {incident.call_id}")
        return response
    
    def _assess_incident(self, incident: EmergencyIncident) -> IncidentAssessment:
        """Assess incident severity and type.
        
        In production, this would call the LLM-powered assessment agent.
        For now, returns a mock assessment.
        """
        # Determine incident type from keywords
        description_lower = incident.description.lower()
        if any(word in description_lower for word in ['cardiac', 'heart', 'chest pain']):
            incident_type = 'CARDIAC'
            base_severity = 8
        elif any(word in description_lower for word in ['trauma', 'accident', 'hit', 'crash']):
            incident_type = 'TRAUMA'
            base_severity = 7
        elif any(word in description_lower for word in ['fire', 'smoke', 'burn']):
            incident_type = 'FIRE'
            base_severity = 8
        else:
            incident_type = 'MEDICAL'
            base_severity = 5
        
        # Adjust severity based on indicators
        severity = base_severity + len(incident.severity_indicators) * 0.5
        severity = min(10, max(1, severity))  # Clamp between 1-10
        
        # Determine priority
        if severity >= 8:
            priority = 'CRITICAL'
        elif severity >= 6:
            priority = 'HIGH'
        elif severity >= 4:
            priority = 'MEDIUM'
        else:
            priority = 'LOW'
        
        return IncidentAssessment(
            incident_id=incident.call_id,
            incident_type=incident_type,
            severity_score=int(severity),
            medical_priority=priority,
            recommended_response=f'Deploy specialized {incident_type} response team',
            estimated_arrival_time='5-8 minutes'
        )
    
    def _allocate_resources(self, assessment: IncidentAssessment) -> ResourceAllocation:
        """Allocate resources based on incident assessment.
        
        In production, this would call the resource allocator agent.
        """
        # Base allocation on incident type and severity
        if assessment.incident_type == 'CARDIAC':
            ambulances = 2
            fire_trucks = 0
            personnel = 6
        elif assessment.incident_type == 'TRAUMA':
            ambulances = 2 if assessment.severity_score >= 7 else 1
            fire_trucks = 1 if assessment.severity_score >= 8 else 0
            personnel = 8 if assessment.severity_score >= 8 else 4
        elif assessment.incident_type == 'FIRE':
            ambulances = 2
            fire_trucks = 3 if assessment.severity_score >= 8 else 2
            personnel = 12
        else:
            ambulances = 1
            fire_trucks = 0
            personnel = 2
        
        return ResourceAllocation(
            allocation_id=f"ALLOC-{assessment.incident_id}",
            ambulances_required=ambulances,
            fire_trucks_required=fire_trucks,
            personnel_required=personnel,
            estimated_cost=ambulances * 500 + fire_trucks * 1000 + personnel * 100,
            dispatch_order=[f'Unit-{i}' for i in range(ambulances + fire_trucks)]
        )
    
    def get_incident_status(self, call_id: str) -> Optional[Dict]:
        """Get status of an active incident."""
        return self.active_incidents.get(call_id)
    
    def update_incident_status(self, call_id: str, status: str) -> bool:
        """Update status of an active incident."""
        if call_id in self.active_incidents:
            self.active_incidents[call_id]['status'] = status
            logger.info(f"Updated {call_id} status to {status}")
            return True
        return False


def main():
    """Main entry point for the emergency response coordinator."""
    # Initialize coordinator
    coordinator = EmergencyResponseCoordinator(project_id='emergency-response')
    
    # Example: Process a cardiac emergency
    cardiac_incident = EmergencyIncident(
        call_id='911-2024-001',
        timestamp=datetime.now().isoformat(),
        location='123 Main St, Hospital District',
        description='Patient experiencing severe chest pain, unresponsive',
        severity_indicators=['chest pain', 'shortness of breath', 'unresponsive'],
        caller_contact='555-0123'
    )
    
    logger.info("=" * 60)
    logger.info("EMERGENCY RESPONSE COORDINATOR - DEMONSTRATION")
    logger.info("=" * 60)
    
    # Process the incident
    response = coordinator.process_emergency_call(cardiac_incident)
    
    # Print response
    logger.info("\nResponse Plan:")
    logger.info(json.dumps(response, indent=2))
    
    # Get status
    status = coordinator.get_incident_status('911-2024-001')
    logger.info("\nIncident Status:")
    logger.info(json.dumps(status, indent=2, default=str))


if __name__ == '__main__':
    main()
