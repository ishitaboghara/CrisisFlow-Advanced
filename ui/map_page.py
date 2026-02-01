# ui/map_page.py - Routes and Graph Management

import customtkinter as ctk
from ui.components import ResourceCard, AlertBanner

class MapPage(ctk.CTkScrollableFrame):
    """Routes, Graph, and Resource Management Page"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app_controller
        
        # Title
        ctk.CTkLabel(
            self,
            text="Routes & Resources",
            font=("Segoe UI", 32, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Main container with two columns
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Left: Route Management
        route_frame = ctk.CTkFrame(main_container, corner_radius=12)
        route_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            route_frame,
            text="🗺️ Route Management",
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w", padx=16, pady=(16, 12))
        
        # Add route form
        add_form = ctk.CTkFrame(route_frame, fg_color="transparent")
        add_form.pack(fill="x", padx=16, pady=8)
        
        ctk.CTkLabel(add_form, text="From:", font=("Segoe UI", 11)).pack(anchor="w")
        self.from_entry = ctk.CTkEntry(add_form, height=35)
        self.from_entry.pack(fill="x", pady=(2, 8))
        
        ctk.CTkLabel(add_form, text="To:", font=("Segoe UI", 11)).pack(anchor="w")
        self.to_entry = ctk.CTkEntry(add_form, height=35)
        self.to_entry.pack(fill="x", pady=(2, 8))
        
        ctk.CTkLabel(add_form, text="Distance (km):", font=("Segoe UI", 11)).pack(anchor="w")
        self.distance_entry = ctk.CTkEntry(add_form, height=35)
        self.distance_entry.pack(fill="x", pady=(2, 8))
        
        ctk.CTkButton(
            add_form,
            text="Add Route",
            command=self.add_route,
            height=35,
            fg_color="#10b981"
        ).pack(fill="x", pady=8)
        
        # Dijkstra pathfinding
        path_form = ctk.CTkFrame(route_frame, fg_color="transparent")
        path_form.pack(fill="x", padx=16, pady=16)
        
        ctk.CTkLabel(
            path_form,
            text="🎯 Find Shortest Path (Dijkstra)",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", pady=(0, 8))
        
        ctk.CTkLabel(path_form, text="Source:", font=("Segoe UI", 11)).pack(anchor="w")
        self.source_entry = ctk.CTkEntry(path_form, height=35)
        self.source_entry.pack(fill="x", pady=(2, 8))
        
        ctk.CTkLabel(path_form, text="Destination:", font=("Segoe UI", 11)).pack(anchor="w")
        self.dest_entry = ctk.CTkEntry(path_form, height=35)
        self.dest_entry.pack(fill="x", pady=(2, 8))
        
        ctk.CTkButton(
            path_form,
            text="Find Path",
            command=self.find_path,
            height=35,
            fg_color="#3b82f6"
        ).pack(fill="x", pady=8)
        
        # Graph stats
        stats_frame = ctk.CTkFrame(route_frame, corner_radius=8, fg_color="#1e293b")
        stats_frame.pack(fill="x", padx=16, pady=(8, 16))
        
        ctk.CTkLabel(
            stats_frame,
            text="Graph Statistics",
            font=("Segoe UI Semibold", 13)
        ).pack(anchor="w", padx=12, pady=(12, 8))
        
        self.graph_stats_label = ctk.CTkLabel(
            stats_frame,
            text="Loading...",
            font=("Segoe UI", 11),
            justify="left"
        )
        self.graph_stats_label.pack(anchor="w", padx=12, pady=(0, 12))
        
        # Right: Resources
        resource_frame = ctk.CTkFrame(main_container, corner_radius=12)
        resource_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            resource_frame,
            text="🚑 Resource Management",
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w", padx=16, pady=(16, 12))
        
        # Add resource form
        res_form = ctk.CTkFrame(resource_frame, fg_color="transparent")
        res_form.pack(fill="x", padx=16, pady=8)
        
        ctk.CTkLabel(res_form, text="Resource Type:", font=("Segoe UI", 11)).pack(anchor="w")
        self.resource_type_var = ctk.StringVar(value="Ambulance")
        self.resource_type_menu = ctk.CTkOptionMenu(
            res_form,
            variable=self.resource_type_var,
            values=["Ambulance", "Fire Truck", "Police Vehicle", "Rescue Team", "Medical Team", "Helicopter"],
            height=35
        )
        self.resource_type_menu.pack(fill="x", pady=(2, 8))
        
        ctk.CTkLabel(res_form, text="Location:", font=("Segoe UI", 11)).pack(anchor="w")
        self.resource_location_entry = ctk.CTkEntry(res_form, height=35)
        self.resource_location_entry.pack(fill="x", pady=(2, 8))
        
        ctk.CTkButton(
            res_form,
            text="Add Resource",
            command=self.add_resource,
            height=35,
            fg_color="#f59e0b"
        ).pack(fill="x", pady=8)
        
        # Resource list
        ctk.CTkLabel(
            resource_frame,
            text="Available Resources",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        self.resource_scroll = ctk.CTkScrollableFrame(
            resource_frame,
            height=300,
            fg_color="transparent"
        )
        self.resource_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        # Output area
        output_frame = ctk.CTkFrame(self, corner_radius=12)
        output_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            output_frame,
            text="📋 Output",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 8))
        
        self.output_text = ctk.CTkTextbox(
            output_frame,
            height=150,
            font=("Consolas", 11)
        )
        self.output_text.pack(fill="x", padx=16, pady=(0, 16))
        
        # Initial load
        self.refresh_data()
    
    def add_route(self):
        """Add new route to graph"""
        from_loc = self.from_entry.get().strip()
        to_loc = self.to_entry.get().strip()
        distance = self.distance_entry.get().strip()
        
        if not from_loc or not to_loc or not distance:
            self._output("❌ Please fill all route fields\n")
            return
        
        try:
            distance = float(distance)
        except:
            self._output("❌ Distance must be a number\n")
            return
        
        self.app.resource_manager.add_route(from_loc, to_loc, distance)
        self._output(f"✅ Route added: {from_loc} ↔ {to_loc} ({distance} km)\n")
        
        self.from_entry.delete(0, "end")
        self.to_entry.delete(0, "end")
        self.distance_entry.delete(0, "end")
        
        self.refresh_data()
    
    def find_path(self):
        """Find shortest path using Dijkstra"""
        source = self.source_entry.get().strip()
        dest = self.dest_entry.get().strip()
        
        if not source or not dest:
            self._output("❌ Please enter both source and destination\n")
            return
        
        distance, path = self.app.resource_manager.find_shortest_path(source, dest)
        
        if distance is None:
            self._output(f"❌ No path found from {source} to {dest}\n")
        else:
            self._output(f"✅ Shortest path found!\n")
            self._output(f"Distance: {distance:.2f} km\n")
            self._output(f"Path: {' → '.join(path)}\n")
    
    def add_resource(self):
        """Add new resource"""
        resource_type = self.resource_type_var.get()
        location = self.resource_location_entry.get().strip()
        
        if not location:
            self._output("❌ Please enter resource location\n")
            return
        
        resource_id = self.app.resource_manager.add_resource(resource_type, location)
        self._output(f"✅ {resource_type} added at {location} (ID: {resource_id})\n")
        
        self.resource_location_entry.delete(0, "end")
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh all data"""
        # Update graph stats
        graph_stats = self.app.resource_manager.get_graph_stats()
        stats_text = f"Nodes: {graph_stats['nodes']}\n"
        stats_text += f"Edges: {graph_stats['edges']}\n"
        stats_text += f"Connected: {'Yes' if graph_stats['connected'] else 'No'}"
        self.graph_stats_label.configure(text=stats_text)
        
        # Update resources
        self._update_resources()
    
    def _update_resources(self):
        """Update resource list"""
        for widget in self.resource_scroll.winfo_children():
            widget.destroy()
        
        resources = self.app.resource_manager.get_available_resources()
        
        if not resources:
            ctk.CTkLabel(
                self.resource_scroll,
                text="No resources available",
                font=("Segoe UI", 12),
                text_color="gray"
            ).pack(pady=20)
            return
        
        for resource in resources[:10]:  # Show top 10
            card = ResourceCard(self.resource_scroll, resource)
            card.pack(fill="x", pady=4)
    
    def _output(self, text):
        """Add text to output"""
        self.output_text.insert("end", text)
        self.output_text.see("end")