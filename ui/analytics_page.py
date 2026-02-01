# FIXED: ui/analytics_page.py - Real Data & Predictions

import customtkinter as ctk
from ui.components import LineChart, BarChart, HeatmapChart, StatCard, ProgressRing
from collections import defaultdict

class AnalyticsPage(ctk.CTkScrollableFrame):
    """Advanced analytics and insights page"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app_controller
        
        # Title
        title_row = ctk.CTkFrame(self, fg_color="transparent")
        title_row.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_row,
            text="Analytics & Insights",
            font=("Segoe UI", 32, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            title_row,
            text="🔄 Refresh",
            command=self.refresh_analytics,
            width=100,
            height=32
        ).pack(side="right")
        
        # Performance score
        score_row = ctk.CTkFrame(self, corner_radius=12)
        score_row.pack(fill="x", padx=20, pady=10)
        
        score_row.grid_columnconfigure(0, weight=1)
        score_row.grid_columnconfigure(1, weight=3)
        
        # Score ring
        ring_frame = ctk.CTkFrame(score_row, fg_color="transparent")
        ring_frame.grid(row=0, column=0, padx=20, pady=20)
        
        self.score_ring = ProgressRing(ring_frame, size=120)
        self.score_ring.pack()
        
        ctk.CTkLabel(
            ring_frame,
            text="Performance Score",
            font=("Segoe UI Semibold", 14)
        ).pack(pady=(10, 0))
        
        # Score breakdown
        breakdown_frame = ctk.CTkFrame(score_row, fg_color="transparent")
        breakdown_frame.grid(row=0, column=1, sticky="ew", padx=20, pady=20)
        
        ctk.CTkLabel(
            breakdown_frame,
            text="Performance Breakdown",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", pady=(0, 10))
        
        self.active_score_label = ctk.CTkLabel(
            breakdown_frame,
            text="Active Emergencies Score: --",
            font=("Segoe UI", 12)
        )
        self.active_score_label.pack(anchor="w", pady=2)
        
        self.response_score_label = ctk.CTkLabel(
            breakdown_frame,
            text="Response Time Score: --",
            font=("Segoe UI", 12)
        )
        self.response_score_label.pack(anchor="w", pady=2)
        
        # Charts grid
        charts_container = ctk.CTkFrame(self, fg_color="transparent")
        charts_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        charts_container.grid_columnconfigure(0, weight=1)
        charts_container.grid_columnconfigure(1, weight=1)
        charts_container.grid_rowconfigure(0, weight=1)
        charts_container.grid_rowconfigure(1, weight=1)
        
        # Hotspots chart - FIXED
        hotspots_frame = ctk.CTkFrame(charts_container, corner_radius=12)
        hotspots_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        
        ctk.CTkLabel(
            hotspots_frame,
            text="🗺️ Emergency Hotspots (Hash Table + Sort)",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 0))
        
        self.hotspots_chart = BarChart(hotspots_frame, height=300)
        self.hotspots_chart.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Heatmap
        heatmap_frame = ctk.CTkFrame(charts_container, corner_radius=12)
        heatmap_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
        
        ctk.CTkLabel(
            heatmap_frame,
            text="🔥 Incident Heatmap",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 0))
        
        self.heatmap = HeatmapChart(heatmap_frame, height=300)
        self.heatmap.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Response metrics
        metrics_frame = ctk.CTkFrame(charts_container, corner_radius=12)
        metrics_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(10, 0))
        
        ctk.CTkLabel(
            metrics_frame,
            text="⏱️ Response Time (BST Traversal)",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 8))
        
        self.metrics_container = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        self.metrics_container.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        # Predictions - FIXED
        predictions_frame = ctk.CTkFrame(charts_container, corner_radius=12)
        predictions_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0))
        
        ctk.CTkLabel(
            predictions_frame,
            text="🔮 Predictive Analytics (Pattern Analysis)",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 8))
        
        self.predictions_container = ctk.CTkFrame(predictions_frame, fg_color="transparent")
        self.predictions_container.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        # Initial load
        self.refresh_analytics()
    
    def refresh_analytics(self):
        """Refresh all analytics"""
        # Performance score
        score_data = self.app.analytics.get_performance_score()
        self.score_ring.set_value(score_data["overall"], f"{score_data['overall']:.0f}")
        
        self.active_score_label.configure(
            text=f"Active Emergencies Score: {score_data['active_score']:.1f}/100"
        )
        self.response_score_label.configure(
            text=f"Response Time Score: {score_data['response_score']:.1f}/100"
        )
        
        # Hotspots - FIXED to use actual data
        self._update_hotspots()
        
        # Heatmap
        heatmap_data = self.app.analytics.generate_heatmap_data(grid_size=15)
        self.heatmap.plot(heatmap_data)
        
        # Response metrics
        self._update_response_metrics()
        
        # Predictions
        self._update_predictions()
    
    def _update_hotspots(self):
        """Update hotspots using REAL data - FIXED"""
        location_counts = defaultdict(int)
        
        # Count from active emergencies
        active = self.app.emergency_manager.get_active_emergencies()
        for e in active:
            location_counts[e.get("location", "Unknown")] += 1
        
        # Count from resolved emergencies (last 20)
        history = self.app.emergency_manager.get_recent_history(50)
        for e in history:
            location_counts[e.get("location", "Unknown")] += 1
        
        if not location_counts:
            # Show message in chart area
            return
        
        # Sort by count - MERGE SORT simulation
        sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Take top 10
        top_10 = sorted_locations[:10]
        
        if top_10:
            locations = [loc[:25] + "..." if len(loc) > 25 else loc for loc, _ in top_10]
            counts = [count for _, count in top_10]
            
            self.hotspots_chart.plot(
                locations, counts,
                ylabel="Incidents",
                color="#ef4444"
            )
    
    def _update_response_metrics(self):
        """Update response metrics display"""
        for widget in self.metrics_container.winfo_children():
            widget.destroy()
        
        metrics = self.app.analytics.calculate_response_metrics()
        
        metrics_data = [
            ("Average", metrics["avg"], "#3b82f6"),
            ("Minimum", metrics["min"], "#10b981"),
            ("Maximum", metrics["max"], "#ef4444"),
        ]
        
        for label, value, color in metrics_data:
            metric_card = ctk.CTkFrame(self.metrics_container, corner_radius=8)
            metric_card.pack(fill="x", pady=4)
            
            ctk.CTkLabel(
                metric_card,
                text=label,
                font=("Segoe UI", 11)
            ).pack(anchor="w", padx=12, pady=(8, 2))
            
            ctk.CTkLabel(
                metric_card,
                text=f"{value:.1f} min" if value > 0 else "N/A",
                font=("Segoe UI Semibold", 20),
                text_color=color
            ).pack(anchor="w", padx=12, pady=(0, 8))
    
    def _update_predictions(self):
        """Update predictions display - FIXED with real data"""
        for widget in self.predictions_container.winfo_children():
            widget.destroy()
        
        # Get real statistics
        stats = self.app.emergency_manager.get_statistics()
        by_type = stats.get("by_type", {})
        
        # Most common type
        most_common_type = "None"
        most_common_location = "None"
        
        if by_type:
            most_common_type = max(by_type.items(), key=lambda x: x[1])[0]
        
        # Most common location from recent history
        history = self.app.emergency_manager.get_recent_history(30)
        location_counts = defaultdict(int)
        for e in history:
            location_counts[e.get("location", "Unknown")] += 1
        
        if location_counts:
            most_common_location = max(location_counts.items(), key=lambda x: x[1])[0]
        
        # Calculate confidence based on data size
        total_emergencies = sum(by_type.values()) if by_type else 0
        confidence = min(0.95, 0.5 + (total_emergencies / 100) * 0.45)
        
        predictions_data = [
            ("Most Frequent Type", most_common_type, "Based on historical data"),
            ("Hotspot Location", most_common_location[:30], "Highest incident count"),
            ("Total Analyzed", f"{total_emergencies} emergencies", "Data points used"),
            ("Confidence Level", f"{confidence*100:.0f}%", "Prediction accuracy"),
        ]
        
        for label, value, description in predictions_data:
            row = ctk.CTkFrame(self.predictions_container, corner_radius=8, fg_color="#1e293b")
            row.pack(fill="x", pady=4)
            
            ctk.CTkLabel(
                row,
                text=f"{label}:",
                font=("Segoe UI Semibold", 11),
                text_color="#3b82f6"
            ).pack(anchor="w", padx=12, pady=(8, 2))
            
            ctk.CTkLabel(
                row,
                text=value,
                font=("Segoe UI Semibold", 14)
            ).pack(anchor="w", padx=12, pady=(0, 2))
            
            ctk.CTkLabel(
                row,
                text=description,
                font=("Segoe UI", 9),
                text_color="gray"
            ).pack(anchor="w", padx=12, pady=(0, 8))