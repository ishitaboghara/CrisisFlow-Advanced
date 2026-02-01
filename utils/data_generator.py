# utils/data_generator.py - Real-world Data Simulation

import random
from datetime import datetime, timedelta
from config import EMERGENCY_TYPES, MAJOR_CITIES, MUMBAI_AREAS, RESOURCE_TYPES

class DataGenerator:
    """Generate realistic emergency and resource data"""
    
    def __init__(self):
        self.emergency_counter = 1000
        self.resource_counter = 500
        
    def generate_emergency(self, location=None):
        """Generate a realistic emergency report"""
        emergency_type = random.choice(list(EMERGENCY_TYPES.keys()))
        
        if location is None:
            city = random.choice(MAJOR_CITIES)
            if city == "Mumbai":
                area = random.choice(MUMBAI_AREAS)
                location = f"{city} - {area}"
            else:
                location = city
        
        descriptions = self._get_descriptions(emergency_type)
        
        self.emergency_counter += 1
        
        return {
            "id": f"EMG{self.emergency_counter}",
            "type": emergency_type,
            "location": location,
            "description": random.choice(descriptions),
            "priority": EMERGENCY_TYPES[emergency_type]["priority"],
            "timestamp": datetime.now(),
            "status": "active",
            "assigned_resources": [],
            "severity": random.choice(["Low", "Medium", "High", "Critical"]),
            "affected_people": random.randint(1, 100),
            "estimated_response_time": random.randint(5, 45),  # minutes
        }
    
    def _get_descriptions(self, emergency_type):
        """Get realistic descriptions based on emergency type"""
        descriptions = {
            "Earthquake": [
                "Major tremors felt, buildings shaking violently",
                "Earthquake of magnitude 5.2 reported, structural damage observed",
                "Ground shaking severely, people evacuating buildings",
            ],
            "Fire": [
                "Building fire reported, flames visible from distance",
                "Residential building on fire, residents trapped inside",
                "Commercial complex fire, smoke spreading rapidly",
                "Vehicle fire blocking main road",
            ],
            "Flood": [
                "Heavy rainfall causing waterlogging, roads submerged",
                "Flash floods reported, water levels rising rapidly",
                "River overflowing, nearby areas getting flooded",
            ],
            "Accident": [
                "Multi-vehicle collision on highway, injuries reported",
                "Bus accident near junction, casualties reported",
                "Two-wheeler accident, rider seriously injured",
                "Pedestrian hit by vehicle, immediate medical attention needed",
            ],
            "Medical Emergency": [
                "Cardiac arrest patient, CPR in progress",
                "Severe allergic reaction, patient unconscious",
                "Multiple casualties in public gathering",
                "Elderly person fell, suspected fracture",
            ],
            "Crime": [
                "Armed robbery in progress at commercial establishment",
                "Assault reported, victim needs immediate help",
                "Suspicious activity reported, possible threat",
            ],
            "Tornado/Cyclone": [
                "Cyclonic winds causing severe damage to structures",
                "Tornado spotted, immediate evacuation required",
                "Severe storm causing widespread destruction",
            ],
            "Building Collapse": [
                "Partial building collapse, people trapped under debris",
                "Old structure collapsed, rescue operations needed",
                "Construction site accident, workers trapped",
            ],
            "Gas Leak": [
                "Gas pipeline leak detected, area needs evacuation",
                "Strong gas smell reported, potential explosion risk",
                "LPG cylinder leakage in residential area",
            ],
        }
        
        return descriptions.get(
            emergency_type,
            ["Emergency situation requires immediate attention"]
        )
    
    def generate_resource(self, resource_type=None):
        """Generate a resource unit"""
        if resource_type is None:
            resource_type = random.choice(list(RESOURCE_TYPES.keys()))
        
        self.resource_counter += 1
        
        location = random.choice(MAJOR_CITIES)
        if location == "Mumbai":
            area = random.choice(MUMBAI_AREAS)
            location = f"{location} - {area}"
        
        return {
            "id": f"RES{self.resource_counter}",
            "type": resource_type,
            "location": location,
            "status": random.choice(["available", "deployed", "maintenance"]),
            "capacity": RESOURCE_TYPES[resource_type]["capacity"],
            "assigned_to": None,
        }
    
    def generate_historical_data(self, days=30, count_per_day=20):
        """Generate historical emergency data for analytics"""
        history = []
        
        for day in range(days):
            date = datetime.now() - timedelta(days=day)
            
            for _ in range(random.randint(count_per_day - 5, count_per_day + 5)):
                emergency = self.generate_emergency()
                emergency["timestamp"] = date - timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                emergency["status"] = "resolved"
                emergency["resolution_time"] = random.randint(10, 120)  # minutes
                
                history.append(emergency)
        
        return history
    
    def generate_graph_data(self, num_nodes=30, num_edges=60):
        """Generate realistic route graph data"""
        nodes = []
        edges = []
        
        # Generate nodes (locations)
        for city in MAJOR_CITIES[:10]:
            nodes.append(city)
        
        for area in MUMBAI_AREAS[:num_nodes - 10]:
            nodes.append(f"Mumbai - {area}")
        
        # Generate edges (routes) - ensure connected graph
        for i in range(len(nodes) - 1):
            # Connect each node to next (backbone)
            edges.append({
                "from": nodes[i],
                "to": nodes[i + 1],
                "distance": random.randint(5, 30)
            })
        
        # Add random edges for better connectivity
        for _ in range(num_edges - len(edges)):
            node1 = random.choice(nodes)
            node2 = random.choice(nodes)
            
            if node1 != node2:
                edges.append({
                    "from": node1,
                    "to": node2,
                    "distance": random.randint(10, 50)
                })
        
        return nodes, edges


# Singleton instance
data_generator = DataGenerator()