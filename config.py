# config.py - Configuration Settings

# Application Settings
APP_TITLE = "CrisisFlow Advanced - Real-time Disaster Management System"
APP_VERSION = "2.0"
WINDOW_SIZE = "1400x800"
MIN_SIZE = (1200, 700)

# Color Scheme - Modern Professional
COLORS = {
    "primary": "#2563eb",      # Blue
    "success": "#10b981",      # Green
    "warning": "#f59e0b",      # Orange
    "danger": "#ef4444",       # Red
    "dark": "#1e293b",         # Dark Blue Gray
    "light": "#f8fafc",        # Light Gray
    "card_bg_dark": "#1e293b",
    "card_bg_light": "#ffffff",
    "text_dark": "#ffffff",
    "text_light": "#1e293b",
}

# Emergency Types and Priority Mapping
EMERGENCY_TYPES = {
    "Earthquake": {"priority": 1, "color": "#dc2626", "icon": "🏚️"},
    "Tsunami": {"priority": 1, "color": "#1e40af", "icon": "🌊"},
    "Tornado/Cyclone": {"priority": 1, "color": "#7c3aed", "icon": "🌪️"},
    "Fire": {"priority": 2, "color": "#ea580c", "icon": "🔥"},
    "Flood": {"priority": 2, "color": "#0891b2", "icon": "💧"},
    "Medical Emergency": {"priority": 2, "color": "#dc2626", "icon": "🚑"},
    "Accident": {"priority": 3, "color": "#f59e0b", "icon": "🚗"},
    "Crime": {"priority": 3, "color": "#7c3aed", "icon": "🚔"},
    "Power Outage": {"priority": 4, "color": "#64748b", "icon": "⚡"},
    "Gas Leak": {"priority": 2, "color": "#f97316", "icon": "💨"},
    "Building Collapse": {"priority": 1, "color": "#991b1b", "icon": "🏢"},
    "Other": {"priority": 5, "color": "#6b7280", "icon": "📋"},
}

# Resource Types
RESOURCE_TYPES = {
    "Ambulance": {"icon": "🚑", "capacity": 4},
    "Fire Truck": {"icon": "🚒", "capacity": 6},
    "Police Vehicle": {"icon": "🚓", "capacity": 4},
    "Rescue Team": {"icon": "👷", "capacity": 8},
    "Medical Team": {"icon": "👨‍⚕️", "capacity": 5},
    "Helicopter": {"icon": "🚁", "capacity": 10},
}

# Major Indian Cities for Simulation
MAJOR_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Bhopal", "Patna", "Indore", "Kochi",
]

# Mumbai Localities (for detailed simulation)
MUMBAI_AREAS = [
    "Andheri West", "Andheri East", "Bandra", "Borivali", 
    "Dadar", "Kurla", "Malad", "Powai", "Vashi", "Thane",
    "Worli", "Lower Parel", "Colaba", "Marine Drive", "Juhu",
    "Goregaon", "Kandivali", "Santacruz", "Chembur", "Ghatkopar"
]

# Data Generation Settings
SIMULATION_INTERVAL = 3000  # milliseconds
MAX_ACTIVE_EMERGENCIES = 50
HISTORY_RETENTION_DAYS = 30

# Graph Settings (for routes)
DEFAULT_GRAPH_NODES = 30
DEFAULT_GRAPH_EDGES = 60
MIN_DISTANCE = 1
MAX_DISTANCE = 50

# Analytics Settings
CHART_UPDATE_INTERVAL = 5000  # milliseconds
HEATMAP_GRID_SIZE = 20

# UI Settings
SIDEBAR_WIDTH = 240
CARD_CORNER_RADIUS = 12
BUTTON_HEIGHT = 40
ANIMATION_DURATION = 200