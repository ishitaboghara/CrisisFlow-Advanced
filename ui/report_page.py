# FIXED: ui/report_page.py - With Autocomplete & Dijkstra Details

import customtkinter as ctk
from config import EMERGENCY_TYPES
from ui.components import AlertBanner

class ReportPage(ctk.CTkScrollableFrame):
    """Page for reporting new emergencies"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app_controller
        
        # Title
        ctk.CTkLabel(
            self,
            text="Report Emergency",
            font=("Segoe UI", 32, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            self,
            text="Fill in the details below to report a new emergency incident",
            font=("Segoe UI", 13),
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Form container
        form = ctk.CTkFrame(self, corner_radius=16)
        form.pack(fill="x", padx=20, pady=10)
        
        # Emergency Type
        type_frame = ctk.CTkFrame(form, fg_color="transparent")
        type_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            type_frame,
            text="Emergency Type *",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", pady=(0, 8))
        
        self.type_var = ctk.StringVar(value="Select Type")
        self.type_menu = ctk.CTkOptionMenu(
            type_frame,
            variable=self.type_var,
            values=list(EMERGENCY_TYPES.keys()),
            height=40,
            font=("Segoe UI", 12)
        )
        self.type_menu.pack(fill="x")
        
        # Location with autocomplete - FIXED
        location_frame = ctk.CTkFrame(form, fg_color="transparent")
        location_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            location_frame,
            text="Location * (Start typing for suggestions)",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", pady=(0, 8))
        
        self.location_entry = ctk.CTkEntry(
            location_frame,
            placeholder_text="e.g., Mumbai - Andheri West",
            height=40,
            font=("Segoe UI", 12)
        )
        self.location_entry.pack(fill="x")
        self.location_entry.bind("<KeyRelease>", self._on_location_type)
        
        # Autocomplete suggestions - ADDED
        self.suggestions_frame = ctk.CTkFrame(location_frame, fg_color="#2b2b2b", height=0)
        self.suggestions_frame.pack(fill="x", pady=(5, 0))
        self.suggestions_frame.pack_forget()  # Hidden by default
        
        # Description
        desc_frame = ctk.CTkFrame(form, fg_color="transparent")
        desc_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            desc_frame,
            text="Description *",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", pady=(0, 8))
        
        self.desc_text = ctk.CTkTextbox(
            desc_frame,
            height=100,
            font=("Segoe UI", 12)
        )
        self.desc_text.pack(fill="x")
        
        # Severity
        severity_frame = ctk.CTkFrame(form, fg_color="transparent")
        severity_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            severity_frame,
            text="Severity Level",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", pady=(0, 8))
        
        self.severity_var = ctk.StringVar(value="Medium")
        severity_options = ctk.CTkFrame(severity_frame, fg_color="transparent")
        severity_options.pack(fill="x")
        
        for severity in ["Low", "Medium", "High", "Critical"]:
            ctk.CTkRadioButton(
                severity_options,
                text=severity,
                variable=self.severity_var,
                value=severity,
                font=("Segoe UI", 11)
            ).pack(side="left", padx=10)
        
        # Affected people
        affected_frame = ctk.CTkFrame(form, fg_color="transparent")
        affected_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            affected_frame,
            text="Estimated Affected People",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w", pady=(0, 8))
        
        self.affected_entry = ctk.CTkEntry(
            affected_frame,
            placeholder_text="Number of people affected",
            height=40,
            font=("Segoe UI", 12)
        )
        self.affected_entry.pack(fill="x")
        
        # Buttons
        button_frame = ctk.CTkFrame(form, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkButton(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            height=40,
            fg_color="#6b7280",
            hover_color="#4b5563"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="Submit Report",
            command=self.submit_report,
            height=40,
            width=200,
            font=("Segoe UI Semibold", 13),
            fg_color="#10b981",
            hover_color="#059669"
        ).pack(side="right")
        
        # Status message
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        # Details panel - ADDED
        self.details_panel = ctk.CTkFrame(self, corner_radius=12)
        self.details_panel.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            self.details_panel,
            text="📋 Operation Details",
            font=("Segoe UI Semibold", 16)
        ).pack(anchor="w", padx=16, pady=(12, 8))
        
        self.details_text = ctk.CTkTextbox(
            self.details_panel,
            height=200,
            font=("Consolas", 11)
        )
        self.details_text.pack(fill="x", padx=16, pady=(0, 16))
    
    def _on_location_type(self, event):
        """Handle location input for autocomplete - ADDED"""
        text = self.location_entry.get()
        
        if len(text) < 2:
            self.suggestions_frame.pack_forget()
            return
        
        # Get suggestions from Trie
        suggestions = self.app.emergency_manager.search_locations(text)
        
        if not suggestions:
            self.suggestions_frame.pack_forget()
            return
        
        # Clear previous suggestions
        for widget in self.suggestions_frame.winfo_children():
            widget.destroy()
        
        # Show suggestions
        self.suggestions_frame.pack(fill="x", pady=(5, 0))
        
        for suggestion in suggestions[:5]:
            btn = ctk.CTkButton(
                self.suggestions_frame,
                text=suggestion,
                command=lambda s=suggestion: self._select_suggestion(s),
                height=30,
                anchor="w",
                fg_color="transparent",
                hover_color="#3b82f6"
            )
            btn.pack(fill="x", padx=5, pady=2)
    
    def _select_suggestion(self, suggestion):
        """Select a suggestion - ADDED"""
        self.location_entry.delete(0, "end")
        self.location_entry.insert(0, suggestion)
        self.suggestions_frame.pack_forget()
    
    def submit_report(self):
        """Submit emergency report - ENHANCED"""
        # Clear details
        self.details_text.delete("1.0", "end")
        
        # Validate
        emergency_type = self.type_var.get()
        location = self.location_entry.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
        
        if emergency_type == "Select Type" or not location or not description:
            self._show_status("Please fill all required fields", "error")
            return
        
        # Get affected people
        try:
            affected = int(self.affected_entry.get() or "1")
        except:
            affected = 1
        
        # Step 1: Create emergency
        self.details_text.insert("end", "=== EMERGENCY REPORTING PROCESS ===\n\n")
        self.details_text.insert("end", "STEP 1: Creating Emergency Object\n")
        
        emergency_data = {
            "type": emergency_type,
            "location": location,
            "description": description,
            "severity": self.severity_var.get(),
            "affected_people": affected,
            "priority": EMERGENCY_TYPES[emergency_type]["priority"]
        }
        
        self.details_text.insert("end", f"  Type: {emergency_type}\n")
        self.details_text.insert("end", f"  Priority: {emergency_data['priority']}\n")
        self.details_text.insert("end", f"  Location: {location}\n\n")
        
        # Step 2: Report emergency
        self.details_text.insert("end", "STEP 2: Data Structure Operations\n")
        emergency_id = self.app.report_emergency(emergency_data)
        
        self.details_text.insert("end", f"  ✓ Emergency ID generated: {emergency_id}\n")
        self.details_text.insert("end", f"  ✓ Min-Heap Insert: O(log n) - Added to priority queue\n")
        self.details_text.insert("end", f"  ✓ Hash Table Insert: O(1) - Indexed by ID and location\n")
        self.details_text.insert("end", f"  ✓ Trie Insert: O(k) - Location added for autocomplete\n\n")
        
        # Step 3: Get emergency object
        emergency = self.app.emergency_manager.get_emergency_by_id(emergency_id)
        
        if emergency:
            # Step 4: Auto-assign resources with Dijkstra - ENHANCED
            self.details_text.insert("end", "STEP 3: Resource Assignment (Dijkstra's Algorithm)\n")
            
            assignments = self.app.resource_manager.auto_assign_resources(emergency)
            
            if assignments:
                self.details_text.insert("end", f"  Graph has {len(self.app.resource_manager.route_graph.nodes)} locations\n")
                self.details_text.insert("end", f"  Running Dijkstra for each available resource...\n\n")
                
                resource_names = []
                for assignment in assignments:
                    resource = assignment["resource"]
                    distance = assignment["distance"]
                    path = assignment["path"]
                    eta = assignment["eta"]
                    
                    resource_names.append(resource["type"])
                    
                    self.details_text.insert("end", f"  🚑 {resource['type']} (ID: {resource['id']})\n")
                    self.details_text.insert("end", f"     Location: {resource['location']}\n")
                    self.details_text.insert("end", f"     Distance: {distance:.2f} km (Dijkstra found shortest path)\n")
                    self.details_text.insert("end", f"     Path: {' → '.join(path)}\n")
                    self.details_text.insert("end", f"     ETA: {eta:.1f} minutes\n")
                    self.details_text.insert("end", f"     Complexity: O((V+E) log V) = O(({len(self.app.resource_manager.route_graph.nodes)}+{len(self.app.resource_manager.route_graph.edges)}) log {len(self.app.resource_manager.route_graph.nodes)})\n\n")
                
                # Store assignments in emergency
                emergency["assigned_resources"] = [a["resource"]["id"] for a in assignments]
                
                self._show_status(
                    f"✅ Emergency reported! Assigned: {', '.join(resource_names)}",
                    "success"
                )
                
                self.details_text.insert("end", "STEP 4: Final Status\n")
                self.details_text.insert("end", f"  ✅ Emergency {emergency_id} successfully reported\n")
                self.details_text.insert("end", f"  ✅ {len(assignments)} resource(s) assigned automatically\n")
                self.details_text.insert("end", f"  ✅ All data structures updated\n")
            else:
                self.details_text.insert("end", "  ⚠️ No resources available for assignment\n")
                self._show_status(
                    f"Emergency reported with ID: {emergency_id}",
                    "warning"
                )
        
        # Clear form
        self.clear_form()
        
        # Scroll to bottom
        self.details_text.see("end")
    
    def clear_form(self):
        """Clear all form fields"""
        self.type_var.set("Select Type")
        self.location_entry.delete(0, "end")
        self.desc_text.delete("1.0", "end")
        self.severity_var.set("Medium")
        self.affected_entry.delete(0, "end")
        self.suggestions_frame.pack_forget()
    
    def _show_status(self, message, type="info"):
        """Show status message"""
        # Clear previous
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Show new
        banner = AlertBanner(self.status_frame, message, type)
        banner.pack(fill="x")
        
        # Auto-hide after 5 seconds
        self.after(5000, lambda: banner.destroy() if banner.winfo_exists() else None)