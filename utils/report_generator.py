import os
from datetime import datetime
from pathlib import Path
import json
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from fpdf import FPDF
import matplotlib.pyplot as plt
import io
import base64

class ReportGenerator:
    def __init__(self):
        """Initialize report generator"""
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
    
    def generate_individual_pdf_report(self, student_data, analysis_results, language='es'):
        """Generate individual student PDF report"""
        
        try:
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_individual_{student_data.get('anonymous_id', 'EST_000')}_{timestamp}.pdf"
            filepath = self.reports_dir / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            story = []
            
            # Title
            title_text = self._get_text('individual_report_title', language)
            story.append(Paragraph(title_text, self.title_style))
            story.append(Spacer(1, 20))
            
            # Student information
            student_info = self._create_student_info_section(student_data, language)
            story.extend(student_info)
            story.append(Spacer(1, 15))
            
            # Analysis summary
            summary_section = self._create_analysis_summary_section(analysis_results, language)
            story.extend(summary_section)
            story.append(Spacer(1, 15))
            
            # Detailed results
            detailed_section = self._create_detailed_results_section(analysis_results, language)
            story.extend(detailed_section)
            story.append(Spacer(1, 15))
            
            # Recommendations
            recommendations_section = self._create_recommendations_section(analysis_results, language)
            story.extend(recommendations_section)
            
            # Footer
            footer_section = self._create_footer_section(language)
            story.extend(footer_section)
            
            # Build PDF
            doc.build(story)
            
            return str(filepath)
            
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            return None
    
    def generate_class_excel_report(self, teacher_data, students_data, language='es'):
        """Generate Excel report for entire class"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_clase_{teacher_data['username']}_{timestamp}.xlsx"
            filepath = self.reports_dir / filename
            
            # Create Excel writer
            with pd.ExcelWriter(str(filepath), engine='openpyxl') as writer:
                
                # Summary sheet
                self._create_summary_sheet(writer, teacher_data, students_data, language)
                
                # Individual scores sheet
                self._create_scores_sheet(writer, students_data, language)
                
                # Progress tracking sheet
                self._create_progress_sheet(writer, students_data, language)
                
                # Detailed feedback sheet
                self._create_feedback_sheet(writer, students_data, language)
                
                # Statistics sheet
                self._create_statistics_sheet(writer, students_data, language)
            
            return str(filepath)
            
        except Exception as e:
            print(f"Error generating Excel report: {e}")
            return None
    
    def generate_class_pdf_report(self, teacher_data, students_data, language='es'):
        """Generate comprehensive PDF report for entire class"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_general_{teacher_data['username']}_{timestamp}.pdf"
            filepath = self.reports_dir / filename
            
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            story = []
            
            # Title page
            title_text = self._get_text('class_report_title', language)
            story.append(Paragraph(title_text, self.title_style))
            story.append(Spacer(1, 20))
            
            # Teacher information
            teacher_info = self._create_teacher_info_section(teacher_data, language)
            story.extend(teacher_info)
            story.append(Spacer(1, 15))
            
            # Class overview
            overview_section = self._create_class_overview_section(students_data, language)
            story.extend(overview_section)
            story.append(Spacer(1, 15))
            
            # Performance analysis
            performance_section = self._create_performance_analysis_section(students_data, language)
            story.extend(performance_section)
            story.append(Spacer(1, 15))
            
            # Individual summaries
            individual_summaries = self._create_individual_summaries_section(students_data, language)
            story.extend(individual_summaries)
            
            # Recommendations for class
            class_recommendations = self._create_class_recommendations_section(students_data, language)
            story.extend(class_recommendations)
            
            doc.build(story)
            
            return str(filepath)
            
        except Exception as e:
            print(f"Error generating class PDF report: {e}")
            return None
    
    def _create_student_info_section(self, student_data, language):
        """Create student information section"""
        section = []
        
        # Section title
        title = self._get_text('student_information', language)
        section.append(Paragraph(title, self.heading_style))
        
        # Student details table
        data = [
            [self._get_text('anonymous_id', language), student_data.get('anonymous_id', 'N/A')],
            [self._get_text('analysis_date', language), datetime.now().strftime("%d/%m/%Y %H:%M")],
            [self._get_text('total_sessions', language), str(student_data.get('total_sessions', 0))],
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        section.append(table)
        return section
    
    def _create_analysis_summary_section(self, analysis_results, language):
        """Create analysis summary section"""
        section = []
        
        # Section title
        title = self._get_text('analysis_summary', language)
        section.append(Paragraph(title, self.heading_style))
        
        # Scores table
        overall_score = analysis_results.get('overall_score', 0)
        voice_score = analysis_results.get('voice_analysis', {}).get('score', 0)
        body_score = analysis_results.get('body_analysis', {}).get('score', 0)
        facial_score = analysis_results.get('facial_analysis', {}).get('score', 0)
        
        data = [
            [self._get_text('category', language), self._get_text('score', language), self._get_text('level', language)],
            [self._get_text('overall_score', language), f"{overall_score}/10", self._get_level_text(overall_score, language)],
            [self._get_text('voice_score', language), f"{voice_score}/10", self._get_level_text(voice_score, language)],
            [self._get_text('body_score', language), f"{body_score}/10", self._get_level_text(body_score, language)],
            [self._get_text('facial_score', language), f"{facial_score}/10", self._get_level_text(facial_score, language)],
        ]
        
        table = Table(data, colWidths=[2*inch, 1*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        section.append(table)
        return section
    
    def _create_detailed_results_section(self, analysis_results, language):
        """Create detailed results section"""
        section = []
        
        # Voice analysis details
        section.append(Paragraph(self._get_text('voice_analysis_details', language), self.heading_style))
        
        voice_analysis = analysis_results.get('voice_analysis', {})
        voice_feedback = voice_analysis.get('feedback', [])
        
        for feedback in voice_feedback:
            section.append(Paragraph(f"• {feedback}", self.body_style))
        
        section.append(Spacer(1, 10))
        
        # Body language details
        section.append(Paragraph(self._get_text('body_analysis_details', language), self.heading_style))
        
        body_analysis = analysis_results.get('body_analysis', {})
        body_feedback = body_analysis.get('feedback', [])
        
        for feedback in body_feedback:
            section.append(Paragraph(f"• {feedback}", self.body_style))
        
        section.append(Spacer(1, 10))
        
        # Facial analysis details
        section.append(Paragraph(self._get_text('facial_analysis_details', language), self.heading_style))
        
        facial_analysis = analysis_results.get('facial_analysis', {})
        facial_feedback = facial_analysis.get('feedback', [])
        
        for feedback in facial_feedback:
            section.append(Paragraph(f"• {feedback}", self.body_style))
        
        return section
    
    def _create_recommendations_section(self, analysis_results, language):
        """Create recommendations section"""
        section = []
        
        section.append(Paragraph(self._get_text('recommendations', language), self.heading_style))
        
        # Generate specific recommendations based on scores
        overall_score = analysis_results.get('overall_score', 0)
        
        if overall_score >= 8:
            recommendations = [
                self._get_text('maintain_excellence', language),
                self._get_text('focus_on_details', language),
                self._get_text('practice_regularly', language)
            ]
        elif overall_score >= 6:
            recommendations = [
                self._get_text('good_foundation', language),
                self._get_text('work_on_weaknesses', language),
                self._get_text('increase_practice', language)
            ]
        else:
            recommendations = [
                self._get_text('fundamental_improvement', language),
                self._get_text('focus_on_basics', language),
                self._get_text('seek_additional_help', language)
            ]
        
        for rec in recommendations:
            section.append(Paragraph(f"• {rec}", self.body_style))
        
        return section
    
    def _create_footer_section(self, language):
        """Create footer section"""
        section = []
        
        section.append(Spacer(1, 30))
        footer_text = f"{self._get_text('generated_by', language)} PresentAI - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        footer_style = ParagraphStyle('Footer', parent=self.body_style, fontSize=8, textColor=colors.grey)
        section.append(Paragraph(footer_text, footer_style))
        
        return section
    
    def _create_summary_sheet(self, writer, teacher_data, students_data, language):
        """Create summary sheet for Excel report"""
        
        # Calculate class statistics
        total_students = len(students_data)
        students_with_data = [s for s in students_data if s.get('analyses')]
        total_analyses = sum(len(s.get('analyses', [])) for s in students_data)
        
        if students_with_data:
            avg_score = sum(
                s['analyses'][-1]['data']['overall_score'] 
                for s in students_with_data
            ) / len(students_with_data)
        else:
            avg_score = 0
        
        # Create summary data
        summary_data = {
            self._get_text('metric', language): [
                self._get_text('teacher_name', language),
                self._get_text('institution', language),
                self._get_text('report_date', language),
                self._get_text('total_students', language),
                self._get_text('students_with_analyses', language),
                self._get_text('total_analyses', language),
                self._get_text('class_average', language)
            ],
            self._get_text('value', language): [
                teacher_data.get('full_name', 'N/A'),
                teacher_data.get('institution', 'N/A'),
                datetime.now().strftime("%d/%m/%Y"),
                total_students,
                len(students_with_data),
                total_analyses,
                f"{avg_score:.1f}/10"
            ]
        }
        
        df = pd.DataFrame(summary_data)
        df.to_excel(writer, sheet_name=self._get_text('summary', language), index=False)
    
    def _create_scores_sheet(self, writer, students_data, language):
        """Create individual scores sheet"""
        
        scores_data = []
        
        for student in students_data:
            if student.get('analyses'):
                latest_analysis = student['analyses'][-1]['data']
                
                scores_data.append({
                    self._get_text('student_id', language): student.get('anonymous_id', 'N/A'),
                    self._get_text('analysis_date', language): student['analyses'][-1]['timestamp'][:10],
                    self._get_text('overall_score', language): latest_analysis.get('overall_score', 0),
                    self._get_text('voice_score', language): latest_analysis.get('voice_analysis', {}).get('score', 0),
                    self._get_text('body_score', language): latest_analysis.get('body_analysis', {}).get('score', 0),
                    self._get_text('facial_score', language): latest_analysis.get('facial_analysis', {}).get('score', 0),
                    self._get_text('total_sessions', language): student.get('total_sessions', 0)
                })
        
        if scores_data:
            df = pd.DataFrame(scores_data)
            df.to_excel(writer, sheet_name=self._get_text('scores', language), index=False)
    
    def _create_progress_sheet(self, writer, students_data, language):
        """Create progress tracking sheet"""
        
        progress_data = []
        
        for student in students_data:
            for i, analysis in enumerate(student.get('analyses', [])):
                progress_data.append({
                    self._get_text('student_id', language): student.get('anonymous_id', 'N/A'),
                    self._get_text('session_number', language): i + 1,
                    self._get_text('date', language): analysis['timestamp'][:10],
                    self._get_text('overall_score', language): analysis['data'].get('overall_score', 0),
                    self._get_text('voice_score', language): analysis['data'].get('voice_analysis', {}).get('score', 0),
                    self._get_text('body_score', language): analysis['data'].get('body_analysis', {}).get('score', 0),
                    self._get_text('facial_score', language): analysis['data'].get('facial_analysis', {}).get('score', 0)
                })
        
        if progress_data:
            df = pd.DataFrame(progress_data)
            df.to_excel(writer, sheet_name=self._get_text('progress', language), index=False)
    
    def _create_feedback_sheet(self, writer, students_data, language):
        """Create detailed feedback sheet"""
        
        feedback_data = []
        
        for student in students_data:
            if student.get('analyses'):
                latest_analysis = student['analyses'][-1]['data']
                
                # Combine all feedback
                all_feedback = []
                all_feedback.extend(latest_analysis.get('voice_analysis', {}).get('feedback', []))
                all_feedback.extend(latest_analysis.get('body_analysis', {}).get('feedback', []))
                all_feedback.extend(latest_analysis.get('facial_analysis', {}).get('feedback', []))
                
                feedback_data.append({
                    self._get_text('student_id', language): student.get('anonymous_id', 'N/A'),
                    self._get_text('feedback', language): ' | '.join(all_feedback)
                })
        
        if feedback_data:
            df = pd.DataFrame(feedback_data)
            df.to_excel(writer, sheet_name=self._get_text('feedback', language), index=False)
    
    def _create_statistics_sheet(self, writer, students_data, language):
        """Create statistics sheet"""
        
        # Calculate various statistics
        all_scores = []
        voice_scores = []
        body_scores = []
        facial_scores = []
        
        for student in students_data:
            if student.get('analyses'):
                latest = student['analyses'][-1]['data']
                all_scores.append(latest.get('overall_score', 0))
                voice_scores.append(latest.get('voice_analysis', {}).get('score', 0))
                body_scores.append(latest.get('body_analysis', {}).get('score', 0))
                facial_scores.append(latest.get('facial_analysis', {}).get('score', 0))
        
        if all_scores:
            stats_data = {
                self._get_text('statistic', language): [
                    self._get_text('mean_overall', language),
                    self._get_text('median_overall', language),
                    self._get_text('std_overall', language),
                    self._get_text('min_overall', language),
                    self._get_text('max_overall', language),
                    self._get_text('mean_voice', language),
                    self._get_text('mean_body', language),
                    self._get_text('mean_facial', language)
                ],
                self._get_text('value', language): [
                    f"{sum(all_scores)/len(all_scores):.2f}",
                    f"{sorted(all_scores)[len(all_scores)//2]:.2f}",
                    f"{(sum((x - sum(all_scores)/len(all_scores))**2 for x in all_scores)/len(all_scores))**0.5:.2f}",
                    f"{min(all_scores):.2f}",
                    f"{max(all_scores):.2f}",
                    f"{sum(voice_scores)/len(voice_scores):.2f}" if voice_scores else "N/A",
                    f"{sum(body_scores)/len(body_scores):.2f}" if body_scores else "N/A",
                    f"{sum(facial_scores)/len(facial_scores):.2f}" if facial_scores else "N/A"
                ]
            }
            
            df = pd.DataFrame(stats_data)
            df.to_excel(writer, sheet_name=self._get_text('statistics', language), index=False)
    
    def _get_text(self, key, language):
        """Get translated text (simplified version)"""
        # This would typically use the language configuration
        translations = {
            'es': {
                'individual_report_title': 'Reporte Individual de Análisis de Presentación',
                'class_report_title': 'Reporte General de Clase - Análisis de Presentaciones',
                'student_information': 'Información del Estudiante',
                'analysis_summary': 'Resumen del Análisis',
                'category': 'Categoría',
                'score': 'Puntuación',
                'level': 'Nivel',
                'voice_analysis_details': 'Detalles del Análisis de Voz',
                'body_analysis_details': 'Detalles del Análisis Corporal',
                'facial_analysis_details': 'Detalles del Análisis Facial',
                'recommendations': 'Recomendaciones',
                'generated_by': 'Generado por',
                'anonymous_id': 'ID Anónimo',
                'analysis_date': 'Fecha de Análisis',
                'total_sessions': 'Total de Sesiones',
                'overall_score': 'Puntuación General',
                'voice_score': 'Puntuación de Voz',
                'body_score': 'Puntuación Corporal',
                'facial_score': 'Puntuación Facial',
                'maintain_excellence': 'Mantén tu excelente desempeño',
                'focus_on_details': 'Enfócate en perfeccionar los detalles',
                'practice_regularly': 'Practica regularmente para mantener el nivel',
                'good_foundation': 'Tienes una buena base',
                'work_on_weaknesses': 'Trabaja en las áreas de mejora identificadas',
                'increase_practice': 'Incrementa la frecuencia de práctica',
                'fundamental_improvement': 'Necesitas mejoras fundamentales',
                'focus_on_basics': 'Enfócate en los aspectos básicos',
                'seek_additional_help': 'Busca ayuda adicional del profesor'
            }
        }
        
        return translations.get(language, translations['es']).get(key, key)
    
    def _get_level_text(self, score, language):
        """Get performance level text based on score"""
        if score >= 8:
            return self._get_text('excellent', language) if language == 'es' else 'Excelente'
        elif score >= 6:
            return self._get_text('good', language) if language == 'es' else 'Bueno'
        elif score >= 4:
            return self._get_text('regular', language) if language == 'es' else 'Regular'
        else:
            return self._get_text('needs_improvement', language) if language == 'es' else 'Necesita Mejora'