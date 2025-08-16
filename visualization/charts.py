import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

class ChartGenerator:
    def __init__(self):
        """Initialize chart generator with styling"""
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Configure matplotlib for better display
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def create_score_bar_chart(self, scores):
        """Create bar chart for current session scores"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(scores.keys())
        values = list(scores.values())
        
        # Create color map based on scores
        colors = []
        for value in values:
            if value >= 8:
                colors.append('#2E8B57')  # Green
            elif value >= 6:
                colors.append('#FFD700')  # Yellow
            elif value >= 4:
                colors.append('#FF8C00')  # Orange
            else:
                colors.append('#DC143C')  # Red
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{value}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Puntuación (0-10)')
        ax.set_title('Puntuaciones por Categoría', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 10.5)
        
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45, ha='right')
        
        # Add horizontal reference lines
        ax.axhline(y=8, color='green', linestyle='--', alpha=0.5, label='Excelente (8+)')
        ax.axhline(y=6, color='orange', linestyle='--', alpha=0.5, label='Bueno (6+)')
        ax.axhline(y=4, color='red', linestyle='--', alpha=0.5, label='Mejorable (4+)')
        
        ax.legend(loc='upper right', framealpha=0.9)
        
        plt.tight_layout()
        return fig
    
    def create_metrics_pie_chart(self, metrics, title):
        """Create pie chart for detailed metrics"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        labels = list(metrics.keys())
        values = list(metrics.values())
        
        # Create colors based on values
        colors = plt.cm.RdYlGn([v/10 for v in values])
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f',
            startangle=90,
            explode=[0.05] * len(values)  # Slightly separate slices
        )
        
        # Improve text formatting
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
    
    def create_progress_trend(self, history_df):
        """Create progress trend chart over time"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Convert timestamp to datetime
        history_df['datetime'] = pd.to_datetime(history_df['timestamp'])
        
        # Plot overall score trend
        ax.plot(history_df['datetime'], history_df['overall_score'], 
               marker='o', linewidth=2, markersize=8, label='Puntuación General', color='#1f77b4')
        
        # Plot individual category trends
        if 'voice_analysis' in history_df.columns:
            voice_scores = [data['score'] for data in history_df['voice_analysis']]
            ax.plot(history_df['datetime'], voice_scores, 
                   marker='s', linewidth=1.5, alpha=0.7, label='Voz', color='#ff7f0e')
        
        if 'body_analysis' in history_df.columns:
            body_scores = [data['score'] for data in history_df['body_analysis']]
            ax.plot(history_df['datetime'], body_scores, 
                   marker='^', linewidth=1.5, alpha=0.7, label='Lenguaje Corporal', color='#2ca02c')
        
        if 'facial_analysis' in history_df.columns:
            facial_scores = [data['score'] for data in history_df['facial_analysis']]
            ax.plot(history_df['datetime'], facial_scores, 
                   marker='d', linewidth=1.5, alpha=0.7, label='Expresiones Faciales', color='#d62728')
        
        # Formatting
        ax.set_ylabel('Puntuación (0-10)')
        ax.set_title('Progreso a lo Largo del Tiempo', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 10)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=45)
        
        # Add trend line for overall score
        if len(history_df) > 1:
            z = np.polyfit(range(len(history_df)), history_df['overall_score'], 1)
            trend_line = np.poly1d(z)
            ax.plot(history_df['datetime'], trend_line(range(len(history_df))), 
                   '--', alpha=0.8, color='red', label='Tendencia')
        
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_emotion_timeline(self, emotion_data):
        """Create timeline chart of emotions during presentation"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Extract data
        times = [point['time'] for point in emotion_data]
        confidences = [point['confidence'] for point in emotion_data]
        emotions = [point['emotion'] for point in emotion_data]
        smile_intensities = [point.get('smile_intensity', 0) for point in emotion_data]
        
        # Plot confidence over time
        ax1.plot(times, confidences, linewidth=2, color='#1f77b4', label='Confianza')
        ax1.fill_between(times, confidences, alpha=0.3, color='#1f77b4')
        ax1.set_ylabel('Nivel de Confianza')
        ax1.set_title('Confianza a lo Largo de la Presentación', fontweight='bold')
        ax1.set_ylim(0, 1)
        ax1.grid(True, alpha=0.3)
        
        # Plot smile intensity
        ax2.plot(times, smile_intensities, linewidth=2, color='#ff7f0e', label='Intensidad de Sonrisa')
        ax2.fill_between(times, smile_intensities, alpha=0.3, color='#ff7f0e')
        ax2.set_ylabel('Intensidad de Sonrisa')
        ax2.set_xlabel('Tiempo (segundos)')
        ax2.set_title('Expresiones Faciales a lo Largo de la Presentación', fontweight='bold')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3)
        
        # Add emotion annotations
        emotion_colors = {
            'confident': 'green',
            'nervous': 'red',
            'neutral': 'gray',
            'surprised': 'orange'
        }
        
        prev_emotion = None
        for i, (time, emotion) in enumerate(zip(times, emotions)):
            if emotion != prev_emotion:
                ax1.axvline(x=time, color=emotion_colors.get(emotion, 'black'), 
                           alpha=0.5, linestyle='--')
                if i < len(emotions) - 1:  # Don't annotate the last point
                    ax1.annotate(emotion.capitalize(), 
                               xy=(time, 0.9), 
                               xytext=(time, 0.95),
                               ha='center', va='bottom',
                               fontsize=8,
                               bbox=dict(boxstyle='round,pad=0.3', 
                                       facecolor=emotion_colors.get(emotion, 'white'),
                                       alpha=0.7))
                prev_emotion = emotion
        
        plt.tight_layout()
        return fig
    
    def create_confidence_timeline(self, confidence_data):
        """Create timeline of speech confidence"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        times = [point['time'] for point in confidence_data]
        confidences = [point['confidence'] for point in confidence_data]
        
        # Plot confidence
        ax.plot(times, confidences, linewidth=2, color='#2ca02c', alpha=0.8)
        ax.fill_between(times, confidences, alpha=0.3, color='#2ca02c')
        
        # Add moving average
        if len(confidences) > 5:
            window_size = min(5, len(confidences) // 3)
            moving_avg = pd.Series(confidences).rolling(window=window_size, center=True).mean()
            ax.plot(times, moving_avg, '--', linewidth=2, color='red', 
                   label=f'Promedio Móvil ({window_size} puntos)')
        
        ax.set_xlabel('Tiempo (segundos)')
        ax.set_ylabel('Confianza en el Habla')
        ax.set_title('Confianza del Habla a lo Largo del Tiempo', fontweight='bold')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        # Add confidence level bands
        ax.axhspan(0.8, 1.0, alpha=0.1, color='green', label='Alta Confianza')
        ax.axhspan(0.6, 0.8, alpha=0.1, color='yellow', label='Confianza Media')
        ax.axhspan(0.0, 0.6, alpha=0.1, color='red', label='Baja Confianza')
        
        ax.legend(loc='best', framealpha=0.9)
        
        plt.tight_layout()
        return fig
    
    def create_movement_timeline(self, movement_data):
        """Create timeline of body movement activity"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        times = [point['time'] for point in movement_data]
        movements = [point['movement_intensity'] for point in movement_data]
        gestures = [point['gesture_active'] for point in movement_data]
        
        # Plot movement intensity
        ax.plot(times, movements, linewidth=1, color='#ff7f0e', alpha=0.7, label='Intensidad de Movimiento')
        
        # Smooth the movement data
        if len(movements) > 3:
            smoothed = pd.Series(movements).rolling(window=3, center=True).mean()
            ax.plot(times, smoothed, linewidth=2, color='#d62728', label='Movimiento Suavizado')
        
        # Mark gesture periods
        gesture_times = [t for t, g in zip(times, gestures) if g]
        gesture_movements = [m for m, g in zip(movements, gestures) if g]
        
        if gesture_times:
            ax.scatter(gesture_times, gesture_movements, 
                      s=30, color='green', alpha=0.7, label='Gestos Activos', zorder=5)
        
        ax.set_xlabel('Tiempo (segundos)')
        ax.set_ylabel('Intensidad de Movimiento')
        ax.set_title('Actividad de Movimiento Corporal', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add movement level bands
        if movements:
            max_movement = max(movements)
            ax.axhspan(0, max_movement * 0.3, alpha=0.1, color='green', label='Movimiento Bajo')
            ax.axhspan(max_movement * 0.3, max_movement * 0.7, alpha=0.1, color='yellow', label='Movimiento Medio')
            ax.axhspan(max_movement * 0.7, max_movement, alpha=0.1, color='red', label='Movimiento Alto')
        
        ax.legend(loc='best', framealpha=0.9)
        
        plt.tight_layout()
        return fig
    
    def create_comparison_radar(self, scores_dict):
        """Create radar chart comparing different aspects"""
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        categories = list(scores_dict.keys())
        values = list(scores_dict.values())
        
        # Add first value to end to close the polygon
        categories += [categories[0]]
        values += [values[0]]
        
        # Create angles for each category
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=True)
        
        # Plot
        ax.plot(angles, values, 'o-', linewidth=2, color='#1f77b4')
        ax.fill(angles, values, alpha=0.25, color='#1f77b4')
        
        # Add category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories[:-1])
        
        # Set y-axis limits and labels
        ax.set_ylim(0, 10)
        ax.set_yticks(range(0, 11, 2))
        ax.set_yticklabels(range(0, 11, 2))
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        ax.set_title('Perfil de Habilidades de Presentación', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
    
    def create_summary_dashboard(self, analysis_results):
        """Create comprehensive dashboard with multiple charts"""
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Overall scores (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        scores = {
            'Voz': analysis_results['voice_analysis']['score'],
            'Cuerpo': analysis_results['body_analysis']['score'],
            'Facial': analysis_results['facial_analysis']['score']
        }
        bars = ax1.bar(scores.keys(), scores.values(), color=['#ff7f0e', '#2ca02c', '#d62728'])
        ax1.set_title('Puntuaciones por Categoría', fontweight='bold')
        ax1.set_ylim(0, 10)
        
        # Add value labels
        for bar, value in zip(bars, scores.values()):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        # Voice metrics (top middle)
        ax2 = fig.add_subplot(gs[0, 1])
        voice_metrics = {
            'Claridad': analysis_results['voice_analysis']['clarity_score'],
            'Velocidad': min(10, analysis_results['voice_analysis']['speaking_rate'] / 20),
            'Sin Muletillas': max(0, 10 - analysis_results['voice_analysis']['filler_count'])
        }
        ax2.pie(voice_metrics.values(), labels=voice_metrics.keys(), autopct='%1.1f')
        ax2.set_title('Métricas de Voz', fontweight='bold')
        
        # Overall score gauge (top right)
        ax3 = fig.add_subplot(gs[0, 2])
        overall_score = analysis_results['overall_score']
        self._create_gauge_chart(ax3, overall_score, 'Puntuación General')
        
        # Body language timeline (middle, full width)
        ax4 = fig.add_subplot(gs[1, :])
        if 'movement_timeline' in analysis_results['body_analysis']:
            movement_data = analysis_results['body_analysis']['movement_timeline']
            times = [point['time'] for point in movement_data]
            movements = [point['movement_intensity'] for point in movement_data]
            ax4.plot(times, movements, linewidth=2, color='#2ca02c')
            ax4.fill_between(times, movements, alpha=0.3, color='#2ca02c')
        ax4.set_title('Actividad de Movimiento Corporal', fontweight='bold')
        ax4.set_xlabel('Tiempo (segundos)')
        ax4.set_ylabel('Intensidad')
        
        # Emotion timeline (bottom, full width)
        ax5 = fig.add_subplot(gs[2, :])
        if 'emotion_timeline' in analysis_results['facial_analysis']:
            emotion_data = analysis_results['facial_analysis']['emotion_timeline']
            times = [point['time'] for point in emotion_data]
            confidences = [point['confidence'] for point in emotion_data]
            ax5.plot(times, confidences, linewidth=2, color='#1f77b4')
            ax5.fill_between(times, confidences, alpha=0.3, color='#1f77b4')
        ax5.set_title('Confianza a lo Largo del Tiempo', fontweight='bold')
        ax5.set_xlabel('Tiempo (segundos)')
        ax5.set_ylabel('Nivel de Confianza')
        
        plt.suptitle('Dashboard de Análisis de Presentación', fontsize=16, fontweight='bold')
        return fig
    
    def _create_gauge_chart(self, ax, value, title):
        """Create a gauge chart for a single metric"""
        # Create gauge background
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        # Color segments
        ax.fill_between(theta[0:33], 0, r[0:33], color='red', alpha=0.3)
        ax.fill_between(theta[33:66], 0, r[33:66], color='yellow', alpha=0.3)
        ax.fill_between(theta[66:100], 0, r[66:100], color='green', alpha=0.3)
        
        # Add needle
        needle_angle = np.pi * (1 - value / 10)
        ax.plot([needle_angle, needle_angle], [0, 0.8], 'k-', linewidth=3)
        ax.plot(needle_angle, 0.8, 'ko', markersize=8)
        
        # Add center circle
        ax.add_patch(plt.Circle((0, 0), 0.1, color='black'))
        
        # Formatting
        ax.set_xlim(-0.1, np.pi + 0.1)
        ax.set_ylim(0, 1.1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title and value
        ax.text(np.pi/2, 1.05, title, ha='center', va='bottom', fontweight='bold')
        ax.text(np.pi/2, 0.3, f'{value:.1f}/10', ha='center', va='center', 
               fontsize=14, fontweight='bold')
