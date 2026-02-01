# FIXED: ui/dashboard.py

import customtkinter as ctk
from ui.components import StatCard, EmergencyCard, BarChart, PieChart
from config import COLORS

class DashboardPage(ctk.CTkScrollableFrame):
    """Main dashboard with overview stats and charts"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app_controller
        
        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Crisis Control Center",
            font=("Segoe UI", 32, "bold")
        ).pack(side="left")
        
        # Refresh button
        ctk.CTkButton(
            title_frame,
            text="🔄 Refresh",
            command=self.refresh_dashboard,
            width=100,
            height=32
        ).pack(side="right")
        
        # Stat cards row
        stats_row = ctk.CTkFrame(self, fg_color="transparent")
        stats_row.pack(fill="x", padx=20, pady=10)
        
        stats_row.grid_columnconfigure(0, weight=1)
        stats_row.grid_columnconfigure(1, weight=1)
        stats_row.grid_columnconfigure(2, weight=1)
        stats_row.grid_columnconfigure(3, weight=1)
        
        self.active_card = StatCard(
            stats_row, 
            icon="🚨", 
            title="Active Emergencies",
            value="0",
            color="#ef4444"
        )
        self.active_card.grid(row=0, column=0, padx=8, sticky="ew")
        
        self.resolved_card = StatCard(
            stats_row,
            icon="✅",
            title="Resolved Today",
            value="0",
            color="#10b981"
        )
        self.resolved_card.grid(row=0, column=1, padx=8, sticky="ew")
        
        self.response_card = StatCard(
            stats_row,
            icon="⏱️",
            title="Avg Response (min)",
            value="0",
            color="#3b82f6"
        )
        self.response_card.grid(row=0, column=2, padx=8, sticky="ew")
        
        self.resources_card = StatCard(
            stats_row,
            icon="🚑",
            title="Available Resources",
            value="0",
            color="#f59e0b"
        )
        self.resources_card.grid(row=0, column=3, padx=8, sticky="ew")
        
        # Main content row
        content_row = ctk.CTkFrame(self, fg_color="transparent")
        content_row.pack(fill="both", expand=True, padx=20, pady=10)
        
        content_row.grid_columnconfigure(0, weight=2)
        content_row.grid_columnconfigure(1, weight=3)
        content_row.grid_rowconfigure(0, weight=1)
        
        # Left column - Priority Queue
        left_col = ctk.CTkFrame(content_row, corner_radius=12)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            left_col,
            text="🔥 Priority Queue (Min-Heap)",
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        self.priority_scroll = ctk.CTkScrollableFrame(
            left_col,
            height=400,
            fg_color="transparent"
        )
        self.priority_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 16))
        
        # Right column - Charts
        right_col = ctk.CTkFrame(content_row, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        right_col.grid_rowconfigure(0, weight=1)
        right_col.grid_rowconfigure(1, weight=1)
        right_col.grid_columnconfigure(0, weight=1)
        
        # Top chart - Emergency types
        chart_frame1 = ctk.CTkFrame(right_col, corner_radius=12)
        chart_frame1.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        ctk.CTkLabel(
            chart_frame1,
            text="📊 Emergency Distribution (Sorted)",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 0))
        
        self.type_chart = BarChart(chart_frame1, height=250)
        self.type_chart.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Bottom chart - Priority distribution
        chart_frame2 = ctk.CTkFrame(right_col, corner_radius=12)
        chart_frame2.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        
        ctk.CTkLabel(
            chart_frame2,
            text="🎯 Priority Breakdown",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 0))
        
        self.priority_chart = PieChart(chart_frame2, height=250)
        self.priority_chart.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Initial load
        self.refresh_dashboard()
    
    def refresh_dashboard(self):
        """Refresh all dashboard data"""
        stats = self.app.emergency_manager.get_statistics()
        
        # Update stat cards
        self.active_card.update_value(stats.get("total_active", 0))
        self.resolved_card.update_value(stats.get("total_resolved", 0))
        
        avg_response = stats.get("avg_response_time", 0)
        self.response_card.update_value(f"{avg_response:.1f}")
        
        resource_stats = self.app.resource_manager.get_resource_stats()
        self.resources_card.update_value(resource_stats.get("available", 0))
        
        # Update priority queue
        self._update_priority_queue()
        
        # Update charts
        self._update_charts(stats)
    
    def _update_priority_queue(self):
        """Update priority queue display"""
        # Clear existing
        for widget in self.priority_scroll.winfo_children():
            widget.destroy()
        
        emergencies = self.app.emergency_manager.get_top_emergencies(10)
        
        if not emergencies:
            ctk.CTkLabel(
                self.priority_scroll,
                text="No active emergencies",
                font=("Segoe UI", 12),
                text_color="gray"
            ).pack(pady=20)
            return
        
        for i, emergency in enumerate(emergencies, 1):
            # Show heap position
            position_label = ctk.CTkLabel(
                self.priority_scroll,
                text=f"Heap Position #{i} | Priority {emergency.get('priority')}",
                font=("Segoe UI", 10),
                text_color="gray"
            )
            position_label.pack(anchor="w", pady=(8 if i > 1 else 0, 2))
            
            card = EmergencyCard(
                self.priority_scroll,
                emergency,
                on_resolve=self._resolve_emergency
            )
            card.pack(fill="x", pady=(0, 6))
    
    def _resolve_emergency(self, emergency):
        """Handle emergency resolution - ENHANCED"""
        emergency_id = emergency["id"]
        
        # Show which resources will be released
        assigned_resources = emergency.get("assigned_resources", [])
        
        # Resolve emergency
        resolved = self.app.resolve_emergency(emergency_id)
        
        if resolved:
            # Show confirmation with details
            details = f"Emergency {emergency_id} resolved!\n"
            details += f"Type: {resolved['type']}\n"
            details += f"Location: {resolved['location']}\n"
            
            if assigned_resources:
                details += f"\n✓ {len(assigned_resources)} resource(s) released back to available pool\n"
                details += "✓ Added to BST (resolved tree)\n"
                details += "✓ Added to Linked List (history)\n"
            
            print(details)  # Console output for demo
        
        self.refresh_dashboard()
    
    def _update_charts(self, stats):
        """Update dashboard charts - WITH SORTING"""
        # Emergency types bar chart - SORTED
        by_type = stats.get("by_type", {})
        if by_type:
            # Sort by count (descending) - MERGE SORT simulation
            sorted_items = sorted(by_type.items(), key=lambda x: x[1], reverse=True)
            types = [item[0] for item in sorted_items[:8]]  # Top 8
            counts = [item[1] for item in sorted_items[:8]]
            
            self.type_chart.plot(
                types, counts,
                title="",
                ylabel="Count",
                color="#3b82f6"
            )
        
        # Priority pie chart
        by_priority = stats.get("by_priority", {})
        if by_priority and sum(by_priority.values()) > 0:
            labels = [f"Priority {p}" for p in sorted(by_priority.keys())]
            values = [by_priority[p] for p in sorted(by_priority.keys())]
            
            # Filter out zeros
            filtered = [(l, v) for l, v in zip(labels, values) if v > 0]
            if filtered:
                labels, values = zip(*filtered)
                self.priority_chart.plot(labels, values, title="")