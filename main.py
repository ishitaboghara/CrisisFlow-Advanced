# FIXED: main.py - Complete CrisisFlow Application

import customtkinter as ctk
from datetime import datetime
import random

# Core imports
from core import EmergencyManager, ResourceManager, AnalyticsEngine

# UI imports
from ui import DashboardPage, ReportPage, AnalyticsPage, MapPage
from ui.history_page import HistoryPage  # NEW

# Config
from config import APP_TITLE, WINDOW_SIZE, MIN_SIZE, COLORS, RESOURCE_TYPES

# Utils
from utils.data_generator import data_generator


class CrisisFlowApp(ctk.CTk):
    """Main Application Controller"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_SIZE)
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Core managers
        self.emergency_manager = EmergencyManager()
        self.resource_manager = ResourceManager()
        self.analytics = AnalyticsEngine(self.emergency_manager)
        
        # Initialize with sample data
        self._initialize_sample_data()
        
        # UI Setup
        self._setup_ui()
        
        # Auto-refresh timer
        self._start_auto_refresh()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(12, weight=1)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 20))
        
        ctk.CTkLabel(
            logo_frame,
            text="🚨",
            font=("Segoe UI", 40)
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="CrisisFlow",
            font=("Segoe UI", 24, "bold")
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="Advanced",
            font=("Segoe UI", 12),
            text_color="gray"
        ).pack()
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Dashboard", "dashboard", self.show_dashboard),
            ("📝 Report Emergency", "report", self.show_report),
            ("📜 History (LL + BST)", "history", self.show_history),
            ("📊 Analytics", "analytics", self.show_analytics),
            ("🗺️ Routes & Resources", "map", self.show_map),
        ]
        
        for i, (text, key, command) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=45,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                font=("Segoe UI", 13)
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons[key] = btn
        
        # Separator
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30")
        separator.grid(row=9, column=0, padx=20, pady=20, sticky="ew")
        
        # Quick stats in sidebar
        self.sidebar_stats = ctk.CTkFrame(self.sidebar, fg_color="#1e293b", corner_radius=10)
        self.sidebar_stats.grid(row=10, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            self.sidebar_stats,
            text="Quick Stats",
            font=("Segoe UI Semibold", 12)
        ).pack(padx=10, pady=(10, 5))
        
        self.quick_active_label = ctk.CTkLabel(
            self.sidebar_stats,
            text="Active: 0",
            font=("Segoe UI", 11)
        )
        self.quick_active_label.pack(padx=10, pady=2)
        
        self.quick_resolved_label = ctk.CTkLabel(
            self.sidebar_stats,
            text="Resolved: 0",
            font=("Segoe UI", 11)
        )
        self.quick_resolved_label.pack(padx=10, pady=(2, 10))
        
        # Theme toggle
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.grid(row=13, column=0, padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=("Segoe UI", 11)
        ).pack(side="left", padx=(0, 10))
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark",
            command=self._toggle_theme,
            font=("Segoe UI", 11)
        )
        self.theme_switch.select()
        self.theme_switch.pack(side="left")
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        # Pages
        self.pages = {}
        self.current_page = None
        
        # Create pages
        self.pages["dashboard"] = DashboardPage(self.content_frame, self)
        self.pages["report"] = ReportPage(self.content_frame, self)
        self.pages["history"] = HistoryPage(self.content_frame, self)  # NEW
        self.pages["analytics"] = AnalyticsPage(self.content_frame, self)
        self.pages["map"] = MapPage(self.content_frame, self)
        
        # Show dashboard initially
        self.show_dashboard()
    
    def _initialize_sample_data(self):
        """Initialize with MORE sample data"""
        # Add resources
        for resource_type in list(RESOURCE_TYPES.keys()):
            for _ in range(5):  # 5 of each type
                resource = data_generator.generate_resource(resource_type)
                self.resource_manager.add_resource(
                    resource["type"],
                    resource["location"],
                    resource["capacity"]
                )
        
        # Add active emergencies
        for _ in range(8):
            emergency = data_generator.generate_emergency()
            self.report_emergency(emergency)
        
        # Add resolved emergencies (for history/BST)
        for _ in range(50):
            emergency = data_generator.generate_emergency()
            emergency_id = self.report_emergency(emergency)
            # Immediately resolve it
            self.resolve_emergency(emergency_id)
    
    def _start_auto_refresh(self):
        """Start auto-refresh timer"""
        self._update_quick_stats()
        # Refresh every 3 seconds
        self.after(3000, self._start_auto_refresh)
    
    def _update_quick_stats(self):
        """Update quick stats in sidebar"""
        stats = self.emergency_manager.get_statistics()
        self.quick_active_label.configure(text=f"Active: {stats['total_active']}")
        self.quick_resolved_label.configure(text=f"Resolved: {stats['total_resolved']}")
    
    def _toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Dark")
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Light")
    
    def _switch_page(self, page_key):
        """Switch to a different page"""
        if self.current_page:
            self.current_page.pack_forget()
        
        self.current_page = self.pages[page_key]
        self.current_page.pack(fill="both", expand=True)
        
        # Highlight active nav button
        for key, btn in self.nav_buttons.items():
            if key == page_key:
                btn.configure(fg_color=COLORS["primary"])
            else:
                btn.configure(fg_color="transparent")
    
    def show_dashboard(self):
        """Show dashboard page"""
        self._switch_page("dashboard")
        if hasattr(self.pages["dashboard"], "refresh_dashboard"):
            self.pages["dashboard"].refresh_dashboard()
    
    def show_report(self):
        """Show report page"""
        self._switch_page("report")
    
    def show_history(self):
        """Show history page - NEW"""
        self._switch_page("history")
        if hasattr(self.pages["history"], "refresh_history"):
            self.pages["history"].refresh_history()
    
    def show_analytics(self):
        """Show analytics page"""
        self._switch_page("analytics")
        if hasattr(self.pages["analytics"], "refresh_analytics"):
            self.pages["analytics"].refresh_analytics()
    
    def show_map(self):
        """Show map/routes page"""
        self._switch_page("map")
        if hasattr(self.pages["map"], "refresh_data"):
            self.pages["map"].refresh_data()
    
    def report_emergency(self, emergency_data):
        """Report a new emergency"""
        emergency_id = self.emergency_manager.report_emergency(emergency_data)
        return emergency_id
    
    def resolve_emergency(self, emergency_id=None):
        """Resolve an emergency - ENHANCED"""
        emergency = self.emergency_manager.resolve_emergency(emergency_id)
        
        # Release assigned resources
        if emergency and "assigned_resources" in emergency:
            for resource_id in emergency.get("assigned_resources", []):
                self.resource_manager.release_resource(resource_id)
                print(f"✓ Resource {resource_id} released and marked as 'available'")
        
        return emergency


def main():
    """Main entry point"""
    app = CrisisFlowApp()
    app.mainloop()


if __name__ == "__main__":
    main()