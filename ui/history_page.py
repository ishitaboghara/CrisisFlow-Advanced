# NEW: ui/history_page.py - Show Linked List & BST

import customtkinter as ctk
from ui.components import EmergencyCard

class HistoryPage(ctk.CTkScrollableFrame):
    """History page showing Linked List and BST operations"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app_controller
        
        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Emergency History",
            font=("Segoe UI", 32, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            title_frame,
            text="🔄 Refresh",
            command=self.refresh_history,
            width=100,
            height=32
        ).pack(side="right")
        
        # Two columns
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Left: Linked List History
        left_frame = ctk.CTkFrame(main_container, corner_radius=12)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            left_frame,
            text="📜 Linked List History (Chronological)",
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        ctk.CTkLabel(
            left_frame,
            text="Shows emergencies in order they were resolved\nO(1) append, O(n) traversal",
            font=("Segoe UI", 10),
            text_color="gray"
        ).pack(anchor="w", padx=16, pady=(0, 8))
        
        self.history_scroll = ctk.CTkScrollableFrame(
            left_frame,
            height=500,
            fg_color="transparent"
        )
        self.history_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        # Right: BST Search
        right_frame = ctk.CTkFrame(main_container, corner_radius=12)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            right_frame,
            text="🌳 BST Search (By Emergency Type)",
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        ctk.CTkLabel(
            right_frame,
            text="Binary Search Tree allows O(log n) search by type",
            font=("Segoe UI", 10),
            text_color="gray"
        ).pack(anchor="w", padx=16, pady=(0, 8))
        
        # Search controls
        search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=16, pady=8)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter emergency type (e.g., Fire)",
            height=35
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ctk.CTkButton(
            search_frame,
            text="Search BST",
            command=self.search_bst,
            height=35,
            width=120
        ).pack(side="right")
        
        # BST stats
        self.bst_stats_label = ctk.CTkLabel(
            right_frame,
            text="BST Stats: Loading...",
            font=("Segoe UI", 11),
            text_color="gray"
        )
        self.bst_stats_label.pack(anchor="w", padx=16, pady=8)
        
        # Search results
        self.search_scroll = ctk.CTkScrollableFrame(
            right_frame,
            height=400,
            fg_color="transparent"
        )
        self.search_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        # Initial load
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history display"""
        # Update linked list history
        self._update_linked_list()
        
        # Update BST stats
        self._update_bst_stats()
    
    def _update_linked_list(self):
        """Update linked list display"""
        for widget in self.history_scroll.winfo_children():
            widget.destroy()
        
        # Get history from linked list
        history = self.app.emergency_manager.get_history()
        
        if not history:
            ctk.CTkLabel(
                self.history_scroll,
                text="No resolved emergencies yet\nResolve some emergencies to see them here",
                font=("Segoe UI", 12),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Show recent 20
        recent = history[-20:][::-1]  # Reverse to show newest first
        
        for i, emergency in enumerate(recent, 1):
            # Position in linked list
            pos_label = ctk.CTkLabel(
                self.history_scroll,
                text=f"Node #{len(history) - i + 1} in Linked List",
                font=("Segoe UI", 10),
                text_color="gray"
            )
            pos_label.pack(anchor="w", pady=(8 if i > 1 else 0, 2))
            
            # Emergency details
            detail_frame = ctk.CTkFrame(self.history_scroll, corner_radius=8)
            detail_frame.pack(fill="x", pady=(0, 6))
            
            ctk.CTkLabel(
                detail_frame,
                text=f"{emergency.get('type')} @ {emergency.get('location')}",
                font=("Segoe UI Semibold", 12)
            ).pack(anchor="w", padx=12, pady=(8, 2))
            
            resolved_time = emergency.get("resolution_time", 0)
            ctk.CTkLabel(
                detail_frame,
                text=f"Resolved in {resolved_time:.1f} minutes | ID: {emergency.get('id')}",
                font=("Segoe UI", 10),
                text_color="gray"
            ).pack(anchor="w", padx=12, pady=(0, 8))
    
    def _update_bst_stats(self):
        """Update BST statistics"""
        stats = self.app.emergency_manager.get_statistics()
        
        tree_size = stats.get("tree_size", 0)
        tree_height = stats.get("tree_height", 0)
        resolved_by_type = stats.get("resolved_by_type", {})
        
        stats_text = f"Tree Size: {tree_size} nodes | Height: {tree_height} | "
        stats_text += f"Types: {len(resolved_by_type)}"
        
        self.bst_stats_label.configure(text=stats_text)
    
    def search_bst(self):
        """Search BST by emergency type"""
        search_type = self.search_entry.get().strip()
        
        # Clear results
        for widget in self.search_scroll.winfo_children():
            widget.destroy()
        
        if not search_type:
            ctk.CTkLabel(
                self.search_scroll,
                text="Enter an emergency type to search",
                font=("Segoe UI", 12),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Search BST - O(log n) average
        results = self.app.emergency_manager.get_resolved_by_type(search_type)
        
        if not results:
            ctk.CTkLabel(
                self.search_scroll,
                text=f"No resolved emergencies of type '{search_type}' found",
                font=("Segoe UI", 12),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Show results
        result_header = ctk.CTkLabel(
            self.search_scroll,
            text=f"Found {len(results)} result(s) - BST Search O(log n)",
            font=("Segoe UI Semibold", 13),
            text_color="#10b981"
        )
        result_header.pack(anchor="w", pady=(0, 10))
        
        for i, emergency in enumerate(results[:10], 1):
            detail_frame = ctk.CTkFrame(self.search_scroll, corner_radius=8)
            detail_frame.pack(fill="x", pady=4)
            
            ctk.CTkLabel(
                detail_frame,
                text=f"{i}. {emergency.get('location')}",
                font=("Segoe UI Semibold", 12)
            ).pack(anchor="w", padx=12, pady=(8, 2))
            
            ctk.CTkLabel(
                detail_frame,
                text=f"{emergency.get('description', 'No description')[:60]}...",
                font=("Segoe UI", 10)
            ).pack(anchor="w", padx=12, pady=(0, 2))
            
            resolved_time = emergency.get("resolution_time", 0)
            ctk.CTkLabel(
                detail_frame,
                text=f"Resolved in {resolved_time:.1f} min | ID: {emergency.get('id')}",
                font=("Segoe UI", 9),
                text_color="gray"
            ).pack(anchor="w", padx=12, pady=(0, 8))