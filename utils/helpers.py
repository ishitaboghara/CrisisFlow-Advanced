# utils/helpers.py - Helper utility functions

from datetime import datetime
import json
import os

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return str(timestamp)

def format_duration(minutes):
    """Format duration in minutes to readable string"""
    if minutes < 60:
        return f"{int(minutes)} min"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f} hrs"
    days = hours / 24
    return f"{days:.1f} days"

def truncate_text(text, max_length=50):
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def calculate_eta(distance, avg_speed=40):
    """
    Calculate ETA based on distance
    distance: in km
    avg_speed: in km/h (default 40 for city traffic)
    Returns: minutes
    """
    if distance <= 0:
        return 0
    return (distance / avg_speed) * 60

def get_priority_color(priority):
    """Get color for priority level"""
    colors = {
        1: "#dc2626",  # Red
        2: "#ea580c",  # Orange
        3: "#f59e0b",  # Amber
        4: "#eab308",  # Yellow
        5: "#84cc16"   # Lime
    }
    return colors.get(priority, "#6b7280")

def get_severity_color(severity):
    """Get color for severity level"""
    colors = {
        "Critical": "#dc2626",
        "High": "#f97316",
        "Medium": "#f59e0b",
        "Low": "#84cc16"
    }
    return colors.get(severity, "#6b7280")

def validate_location(location):
    """Basic location validation"""
    if not location or len(location) < 3:
        return False, "Location too short"
    if len(location) > 100:
        return False, "Location too long"
    return True, "Valid"

def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    # Remove extra whitespace
    text = " ".join(text.split())
    return text

def save_to_json(data, filename):
    """Save data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

def load_from_json(filename):
    """Load data from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading from JSON: {e}")
        return None

def calculate_statistics(values):
    """Calculate basic statistics"""
    if not values:
        return {
            "count": 0,
            "sum": 0,
            "avg": 0,
            "min": 0,
            "max": 0
        }
    
    return {
        "count": len(values),
        "sum": sum(values),
        "avg": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }

def format_number(number, decimals=2):
    """Format number with thousands separator"""
    if isinstance(number, float):
        return f"{number:,.{decimals}f}"
    return f"{number:,}"

def get_time_of_day():
    """Get current time of day category"""
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

def generate_report_summary(emergencies):
    """Generate text summary of emergencies"""
    if not emergencies:
        return "No emergencies to report."
    
    total = len(emergencies)
    by_type = {}
    by_priority = {}
    
    for e in emergencies:
        e_type = e.get("type", "Unknown")
        priority = e.get("priority", 5)
        
        by_type[e_type] = by_type.get(e_type, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
    
    summary = f"Total Emergencies: {total}\n\n"
    summary += "By Type:\n"
    for e_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        summary += f"  - {e_type}: {count}\n"
    
    summary += "\nBy Priority:\n"
    for priority in sorted(by_priority.keys()):
        count = by_priority[priority]
        summary += f"  - Priority {priority}: {count}\n"
    
    return summary