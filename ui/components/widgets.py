# ui/components/widgets.py - Custom UI widgets

import customtkinter as ctk
from config import COLORS, EMERGENCY_TYPES

class StatCard(ctk.CTkFrame):
    """Stat card widget for dashboard"""
    
    def __init__(self, parent, icon, title, value="0", color="#3b82f6", **kwargs):
        super().__init__(parent, corner_radius=12, **kwargs)
        
        self.color = color
        
        # Icon and title row
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(12, 0))
        
        icon_label = ctk.CTkLabel(
            top_row, 
            text=icon, 
            font=("Segoe UI", 24),
            text_color=color
        )
        icon_label.pack(side="left")
        
        self.title_label = ctk.CTkLabel(
            top_row,
            text=title,
            font=("Segoe UI", 12),
            anchor="w"
        )
        self.title_label.pack(side="left", padx=(8, 0))
        
        # Value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI Semibold", 36),
            text_color=color
        )
        self.value_label.pack(anchor="w", padx=16, pady=(4, 12))
    
    def update_value(self, value):
        """Update the displayed value"""
        self.value_label.configure(text=str(value))

class EmergencyCard(ctk.CTkFrame):
    """Card for displaying emergency details"""
    
    def __init__(self, parent, emergency, on_resolve=None, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.emergency = emergency
        self.on_resolve = on_resolve
        
        # Get emergency config
        e_type = emergency.get("type", "Other")
        e_config = EMERGENCY_TYPES.get(e_type, EMERGENCY_TYPES["Other"])
        
        # Header with type and priority
        header = ctk.CTkFrame(self, fg_color=e_config["color"], corner_radius=8)
        header.pack(fill="x", padx=8, pady=8)
        
        ctk.CTkLabel(
            header,
            text=f"{e_config['icon']} {e_type}",
            font=("Segoe UI Semibold", 13),
            text_color="white"
        ).pack(side="left", padx=10, pady=6)
        
        ctk.CTkLabel(
            header,
            text=f"Priority: {emergency.get('priority', 'N/A')}",
            font=("Segoe UI", 11),
            text_color="white"
        ).pack(side="right", padx=10, pady=6)
        
        # Content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=8)
        
        # Location
        ctk.CTkLabel(
            content,
            text=f"📍 {emergency.get('location', 'Unknown')}",
            font=("Segoe UI", 11),
            anchor="w"
        ).pack(fill="x", pady=2)
        
        # Description
        ctk.CTkLabel(
            content,
            text=emergency.get('description', 'No description'),
            font=("Segoe UI", 10),
            anchor="w",
            wraplength=250,
            justify="left"
        ).pack(fill="x", pady=2)
        
        # ID and timestamp
        info_text = f"ID: {emergency.get('id', 'N/A')}"
        if 'timestamp' in emergency:
            info_text += f" • {emergency['timestamp'].strftime('%H:%M')}"
        
        ctk.CTkLabel(
            content,
            text=info_text,
            font=("Segoe UI", 9),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=2)
        
        # Actions
        if on_resolve:
            action_btn = ctk.CTkButton(
                self,
                text="Resolve",
                command=lambda: on_resolve(emergency),
                height=30,
                fg_color="#10b981",
                hover_color="#059669"
            )
            action_btn.pack(pady=(0, 8), padx=12)

class ResourceCard(ctk.CTkFrame):
    """Card for displaying resource details"""
    
    def __init__(self, parent, resource, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.resource = resource
        
        # Status color
        status_colors = {
            "available": "#10b981",
            "deployed": "#f59e0b",
            "maintenance": "#ef4444"
        }
        status_color = status_colors.get(resource.get("status", "available"), "#6b7280")
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(
            header,
            text=resource.get("type", "Resource"),
            font=("Segoe UI Semibold", 12),
            anchor="w"
        ).pack(side="left")
        
        status_badge = ctk.CTkLabel(
            header,
            text=resource.get("status", "available").upper(),
            font=("Segoe UI", 9),
            text_color="white",
            fg_color=status_color,
            corner_radius=4
        )
        status_badge.pack(side="right", padx=4, pady=2)
        
        # Details
        details = ctk.CTkFrame(self, fg_color="transparent")
        details.pack(fill="x", padx=12, pady=(0, 8))
        
        ctk.CTkLabel(
            details,
            text=f"📍 {resource.get('location', 'Unknown')}",
            font=("Segoe UI", 10),
            anchor="w"
        ).pack(fill="x", pady=1)
        
        ctk.CTkLabel(
            details,
            text=f"ID: {resource.get('id', 'N/A')} • Capacity: {resource.get('capacity', 0)}",
            font=("Segoe UI", 9),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=1)

class AlertBanner(ctk.CTkFrame):
    """Alert/notification banner"""
    
    def __init__(self, parent, message, type="info", **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)
        
        colors = {
            "info": "#3b82f6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        color = colors.get(type, "#3b82f6")
        icon = icons.get(type, "ℹ️")
        
        self.configure(fg_color=color)
        
        ctk.CTkLabel(
            self,
            text=f"{icon} {message}",
            font=("Segoe UI", 11),
            text_color="white"
        ).pack(padx=16, pady=10)

class SearchBar(ctk.CTkFrame):
    """Search bar with autocomplete"""
    
    def __init__(self, parent, on_search=None, placeholder="Search...", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.on_search = on_search
        
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            height=40,
            font=("Segoe UI", 12)
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        if on_search:
            self.entry.bind("<Return>", lambda e: self.on_search(self.entry.get()))
        
        self.search_btn = ctk.CTkButton(
            self,
            text="🔍",
            width=40,
            height=40,
            command=self._do_search
        )
        self.search_btn.pack(side="right")
    
    def _do_search(self):
        if self.on_search:
            self.on_search(self.entry.get())
    
    def get(self):
        return self.entry.get()
    
    def clear(self):
        self.entry.delete(0, "end")

class ProgressRing(ctk.CTkFrame):
    """Circular progress indicator"""
    
    def __init__(self, parent, size=100, **kwargs):
        super().__init__(parent, width=size, height=size, fg_color="transparent", **kwargs)
        
        self.size = size
        
        self.label = ctk.CTkLabel(
            self,
            text="0%",
            font=("Segoe UI Semibold", 24)
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")
    
    def set_value(self, value, text=None):
        """Update progress value (0-100)"""
        if text is None:
            text = f"{int(value)}%"
        self.label.configure(text=text)