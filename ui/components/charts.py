# ui/components/charts.py - Chart widgets using matplotlib

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk

class ChartWidget(ctk.CTkFrame):
    """Base chart widget"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor='#1e293b')
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def clear(self):
        """Clear the chart"""
        self.figure.clear()
        self.canvas.draw()

class LineChart(ChartWidget):
    """Line chart for time series data"""
    
    def plot(self, x_data, y_data, title="", xlabel="", ylabel="", color="#3b82f6"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        ax.plot(x_data, y_data, color=color, linewidth=2, marker='o', markersize=4)
        ax.set_title(title, color='white', fontsize=12, pad=10)
        ax.set_xlabel(xlabel, color='white', fontsize=10)
        ax.set_ylabel(ylabel, color='white', fontsize=10)
        
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.2, color='white')
        
        for spine in ax.spines.values():
            spine.set_color('#475569')
        
        self.figure.tight_layout()
        self.canvas.draw()

class BarChart(ChartWidget):
    """Bar chart for categorical data"""
    
    def plot(self, labels, values, title="", xlabel="", ylabel="", color="#10b981"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        bars = ax.bar(labels, values, color=color, alpha=0.8, edgecolor='white', linewidth=0.5)
        
        ax.set_title(title, color='white', fontsize=12, pad=10)
        ax.set_xlabel(xlabel, color='white', fontsize=10)
        ax.set_ylabel(ylabel, color='white', fontsize=10)
        
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.2, color='white', axis='y')
        
        # Rotate labels if too many
        if len(labels) > 5:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        for spine in ax.spines.values():
            spine.set_color('#475569')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', color='white', fontsize=8)
        
        self.figure.tight_layout()
        self.canvas.draw()

class PieChart(ChartWidget):
    """Pie chart for distribution"""
    
    def plot(self, labels, values, title=""):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors[:len(labels)],
            startangle=90,
            textprops={'color': 'white', 'fontsize': 9}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)
        
        ax.set_title(title, color='white', fontsize=12, pad=10)
        ax.set_facecolor('#1e293b')
        
        self.figure.tight_layout()
        self.canvas.draw()

class HeatmapChart(ChartWidget):
    """Heatmap for spatial data"""
    
    def plot(self, data, title="Emergency Hotspots"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        im = ax.imshow(data, cmap='YlOrRd', interpolation='nearest', aspect='auto')
        
        ax.set_title(title, color='white', fontsize=12, pad=10)
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='white', labelsize=8)
        
        # Add colorbar
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.ax.tick_params(colors='white', labelsize=8)
        
        for spine in ax.spines.values():
            spine.set_color('#475569')
        
        self.figure.tight_layout()
        self.canvas.draw()