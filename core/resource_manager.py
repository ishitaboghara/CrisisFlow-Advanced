# core/resource_manager.py - Resource and Route Management

from data_structures import Graph, HashTable
from utils.data_generator import data_generator
import random

class ResourceManager:
    """
    Manage emergency response resources and routing
    """
    
    def __init__(self):
        # Route graph
        self.route_graph = Graph()
        
        # Resources indexed by type and ID
        self.resources = HashTable(size=50)
        self.resources_by_type = {}
        
        # Assignment tracking
        self.assignments = {}  # emergency_id -> [resource_ids]
        
        self.resource_counter = 0
        
        # Initialize with some default data
        self._initialize_default_graph()
    
    def _initialize_default_graph(self):
        """Initialize graph with some default routes"""
        nodes, edges = data_generator.generate_graph_data(num_nodes=25, num_edges=50)
        
        for edge in edges:
            self.route_graph.add_edge(
                edge["from"],
                edge["to"],
                edge["distance"]
            )
    
    def add_resource(self, resource_type, location, capacity=None):
        """
        Add a new resource unit
        Returns: resource ID
        """
        self.resource_counter += 1
        resource_id = f"RES{self.resource_counter}"
        
        resource = {
            "id": resource_id,
            "type": resource_type,
            "location": location,
            "status": "available",
            "capacity": capacity or 5,
            "assigned_to": None
        }
        
        # Add to hash table
        self.resources.insert(resource_id, resource)
        
        # Index by type
        if resource_type not in self.resources_by_type:
            self.resources_by_type[resource_type] = []
        self.resources_by_type[resource_type].append(resource)
        
        # Ensure location is in graph
        self.route_graph.add_node(location)
        
        return resource_id
    
    def get_resource(self, resource_id):
        """Get resource by ID"""
        return self.resources.get(resource_id)
    
    def get_resources_by_type(self, resource_type):
        """Get all resources of a type"""
        return self.resources_by_type.get(resource_type, [])
    
    def get_available_resources(self, resource_type=None):
        """Get available resources, optionally filtered by type"""
        all_resources = self.resources.values()
        available = [r for r in all_resources if r["status"] == "available"]
        
        if resource_type:
            available = [r for r in available if r["type"] == resource_type]
        
        return available
    
    def assign_resource(self, resource_id, emergency_id):
        """Assign a resource to an emergency"""
        resource = self.resources.get(resource_id)
        if not resource:
            return False
        
        if resource["status"] != "available":
            return False
        
        resource["status"] = "deployed"
        resource["assigned_to"] = emergency_id
        
        # Track assignment
        if emergency_id not in self.assignments:
            self.assignments[emergency_id] = []
        self.assignments[emergency_id].append(resource_id)
        
        return True
    
    def release_resource(self, resource_id):
        """Release a resource back to available pool"""
        resource = self.resources.get(resource_id)
        if not resource:
            return False
        
        emergency_id = resource["assigned_to"]
        
        resource["status"] = "available"
        resource["assigned_to"] = None
        
        # Remove from assignments
        if emergency_id and emergency_id in self.assignments:
            self.assignments[emergency_id] = [
                r for r in self.assignments[emergency_id] if r != resource_id
            ]
        
        return True
    
    def find_nearest_resource(self, location, resource_type=None):
        """
        Find nearest available resource to a location
        Returns: (resource, distance, path)
        """
        available = self.get_available_resources(resource_type)
        
        if not available:
            return None, None, None
        
        best_resource = None
        best_distance = float('inf')
        best_path = None
        
        for resource in available:
            resource_location = resource["location"]
            
            distance, path = self.route_graph.dijkstra(resource_location, location)
            
            if distance is not None and distance < best_distance:
                best_resource = resource
                best_distance = distance
                best_path = path
        
        return best_resource, best_distance, best_path
    
    def auto_assign_resources(self, emergency):
        """
        Automatically assign best resources to an emergency
        Returns: list of assigned resource IDs
        """
        location = emergency["location"]
        emergency_type = emergency["type"]
        
        # Determine needed resource types based on emergency
        needed_types = self._get_needed_resources(emergency_type)
        
        assigned = []
        
        for resource_type in needed_types:
            resource, distance, path = self.find_nearest_resource(location, resource_type)
            
            if resource:
                if self.assign_resource(resource["id"], emergency["id"]):
                    assigned.append({
                        "resource": resource,
                        "distance": distance,
                        "path": path,
                        "eta": distance * 2 if distance else None  # Simple ETA calculation
                    })
        
        return assigned
    
    def _get_needed_resources(self, emergency_type):
        """Determine what resources are needed for emergency type"""
        resource_map = {
            "Fire": ["Fire Truck", "Ambulance"],
            "Medical Emergency": ["Ambulance", "Medical Team"],
            "Accident": ["Ambulance", "Police Vehicle"],
            "Crime": ["Police Vehicle"],
            "Flood": ["Rescue Team", "Ambulance"],
            "Earthquake": ["Rescue Team", "Ambulance", "Fire Truck"],
            "Building Collapse": ["Rescue Team", "Fire Truck", "Ambulance"],
            "Gas Leak": ["Fire Truck"],
        }
        
        return resource_map.get(emergency_type, ["Ambulance"])
    
    def add_route(self, from_location, to_location, distance):
        """Add a route between two locations"""
        self.route_graph.add_edge(from_location, to_location, distance)
    
    def find_shortest_path(self, from_location, to_location):
        """Find shortest path between two locations"""
        return self.route_graph.dijkstra(from_location, to_location)
    
    def get_route_info(self, start_location):
        """Get routing information from a location"""
        return {
            "bfs_order": self.route_graph.bfs(start_location),
            "dfs_order": self.route_graph.dfs(start_location),
            "neighbors": self.route_graph.get_neighbors(start_location)
        }
    
    def get_graph_stats(self):
        """Get graph statistics"""
        return self.route_graph.get_stats()
    
    def get_resource_stats(self):
        """Get resource statistics"""
        all_resources = self.resources.values()
        
        stats = {
            "total": len(all_resources),
            "available": len([r for r in all_resources if r["status"] == "available"]),
            "deployed": len([r for r in all_resources if r["status"] == "deployed"]),
            "maintenance": len([r for r in all_resources if r["status"] == "maintenance"]),
            "by_type": {}
        }
        
        for resource_type, resources in self.resources_by_type.items():
            stats["by_type"][resource_type] = {
                "total": len(resources),
                "available": len([r for r in resources if r["status"] == "available"])
            }
        
        return stats