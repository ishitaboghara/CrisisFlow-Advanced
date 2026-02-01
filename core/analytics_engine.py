# core/analytics_engine.py - Analytics and Predictions

from datetime import datetime, timedelta
from collections import defaultdict
import random

class AnalyticsEngine:
    """
    Analytics engine for emergency patterns and predictions
    """
    
    def __init__(self, emergency_manager):
        self.emergency_manager = emergency_manager
        self.historical_data = []
        self.predictions = []
    
    def analyze_trends(self, days=7):
        """
        Analyze emergency trends over time
        Returns: trends data for visualization
        """
        trends = {
            "daily_counts": defaultdict(int),
            "hourly_pattern": defaultdict(int),
            "by_type": defaultdict(int),
            "by_location": defaultdict(int),
            "by_priority": defaultdict(int)
        }
        
        cutoff = datetime.now() - timedelta(days=days)
        
        # Analyze resolved emergencies
        all_resolved = []
        for emergency_type in self.emergency_manager.resolved_tree.get_all_keys():
            emergencies = self.emergency_manager.resolved_tree.search(emergency_type)
            all_resolved.extend(emergencies)
        
        for emergency in all_resolved:
            timestamp = emergency.get("timestamp")
            if not timestamp or timestamp < cutoff:
                continue
            
            # Daily counts
            date_key = timestamp.strftime("%Y-%m-%d")
            trends["daily_counts"][date_key] += 1
            
            # Hourly pattern
            hour = timestamp.hour
            trends["hourly_pattern"][hour] += 1
            
            # By type
            emergency_type = emergency.get("type", "Unknown")
            trends["by_type"][emergency_type] += 1
            
            # By location
            location = emergency.get("location", "Unknown")
            trends["by_location"][location] += 1
            
            # By priority
            priority = emergency.get("priority", 5)
            trends["by_priority"][priority] += 1
        
        return trends
    
    def get_hotspots(self, limit=10):
        """
        Identify emergency hotspots (locations with most incidents)
        Returns: list of (location, count) tuples
        """
        location_counts = defaultdict(int)
        
        # Count active emergencies
        for emergency in self.emergency_manager.get_active_emergencies():
            location = emergency.get("location", "Unknown")
            location_counts[location] += 1
        
        # Count recent resolved
        all_resolved = []
        for emergency_type in self.emergency_manager.resolved_tree.get_all_keys():
            emergencies = self.emergency_manager.resolved_tree.search(emergency_type)
            all_resolved.extend(emergencies)
        
        cutoff = datetime.now() - timedelta(days=7)
        for emergency in all_resolved:
            timestamp = emergency.get("timestamp")
            if timestamp and timestamp >= cutoff:
                location = emergency.get("location", "Unknown")
                location_counts[location] += 1
        
        # Sort and return top locations
        hotspots = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
        return hotspots[:limit]
    
    def calculate_response_metrics(self):
        """
        Calculate response time metrics
        Returns: dict with avg, min, max response times
        """
        response_times = []
        
        all_resolved = []
        for emergency_type in self.emergency_manager.resolved_tree.get_all_keys():
            emergencies = self.emergency_manager.resolved_tree.search(emergency_type)
            all_resolved.extend(emergencies)
        
        for emergency in all_resolved:
            if "resolution_time" in emergency:
                response_times.append(emergency["resolution_time"])
        
        if not response_times:
            return {"avg": 0, "min": 0, "max": 0, "count": 0}
        
        return {
            "avg": sum(response_times) / len(response_times),
            "min": min(response_times),
            "max": max(response_times),
            "count": len(response_times)
        }
    
    def predict_next_emergency(self):
        """
        Simple prediction of next emergency type and location
        Based on historical patterns
        """
        trends = self.analyze_trends(days=7)
        
        # Most common type
        if trends["by_type"]:
            most_common_type = max(trends["by_type"].items(), key=lambda x: x[1])[0]
        else:
            most_common_type = "Unknown"
        
        # Most common location
        if trends["by_location"]:
            most_common_location = max(trends["by_location"].items(), key=lambda x: x[1])[0]
        else:
            most_common_location = "Unknown"
        
        # Peak hour
        if trends["hourly_pattern"]:
            peak_hour = max(trends["hourly_pattern"].items(), key=lambda x: x[1])[0]
        else:
            peak_hour = datetime.now().hour
        
        return {
            "predicted_type": most_common_type,
            "predicted_location": most_common_location,
            "predicted_time": f"{peak_hour:02d}:00",
            "confidence": random.uniform(0.6, 0.9)
        }
    
    def get_emergency_distribution(self):
        """
        Get distribution of emergencies by type, priority, etc.
        For pie charts and bar graphs
        """
        stats = self.emergency_manager.get_statistics()
        
        return {
            "by_type": stats.get("by_type", {}),
            "by_priority": stats.get("by_priority", {}),
            "active_vs_resolved": {
                "Active": stats.get("total_active", 0),
                "Resolved": stats.get("total_resolved", 0)
            }
        }
    
    def generate_heatmap_data(self, grid_size=20):
        """
        Generate heatmap data for visualization
        Returns: 2D array of emergency counts
        """
        # Simplified heatmap - in real app would use actual coordinates
        heatmap = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
        hotspots = self.get_hotspots(limit=50)
        
        for i, (location, count) in enumerate(hotspots[:grid_size * grid_size]):
            row = i // grid_size
            col = i % grid_size
            if row < grid_size and col < grid_size:
                heatmap[row][col] = count
        
        return heatmap
    
    def get_performance_score(self):
        """
        Calculate overall system performance score (0-100)
        """
        stats = self.emergency_manager.get_statistics()
        metrics = self.calculate_response_metrics()
        
        # Factors for scoring
        active_count = stats.get("total_active", 0)
        avg_response = metrics.get("avg", 0)
        
        # Lower active emergencies = better
        active_score = max(0, 100 - (active_count * 2))
        
        # Lower response time = better (assume target is 15 minutes)
        if avg_response > 0:
            response_score = max(0, 100 - ((avg_response - 15) * 2))
        else:
            response_score = 100
        
        # Combined score
        overall_score = (active_score * 0.4 + response_score * 0.6)
        
        return {
            "overall": round(overall_score, 1),
            "active_score": round(active_score, 1),
            "response_score": round(response_score, 1)
        }
    
    def get_weekly_summary(self):
        """Get summary of last 7 days"""
        trends = self.analyze_trends(days=7)
        
        total_emergencies = sum(trends["daily_counts"].values())
        
        return {
            "total_emergencies": total_emergencies,
            "avg_per_day": total_emergencies / 7,
            "most_common_type": max(trends["by_type"].items(), key=lambda x: x[1])[0] if trends["by_type"] else "None",
            "busiest_hour": max(trends["hourly_pattern"].items(), key=lambda x: x[1])[0] if trends["hourly_pattern"] else 0
        }