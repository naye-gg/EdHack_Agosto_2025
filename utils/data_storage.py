import json
import os
from datetime import datetime
from pathlib import Path

class DataStorage:
    def __init__(self, data_dir="data"):
        """Initialize data storage with specified directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.students_dir = self.data_dir / "students"
        self.students_dir.mkdir(exist_ok=True)
        
        self.analyses_dir = self.data_dir / "analyses"
        self.analyses_dir.mkdir(exist_ok=True)
    
    def save_analysis(self, student_name, analysis_data):
        """Save analysis results for a student"""
        try:
            # Sanitize student name for filename
            safe_name = self._sanitize_filename(student_name)
            
            # Create student directory if it doesn't exist
            student_dir = self.students_dir / safe_name
            student_dir.mkdir(exist_ok=True)
            
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.json"
            filepath = student_dir / filename
            
            # Add metadata
            analysis_data['saved_at'] = datetime.now().isoformat()
            analysis_data['student_id'] = safe_name
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)
            
            # Update student summary
            self._update_student_summary(safe_name, analysis_data)
            
            return True
            
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return False
    
    def get_student_history(self, student_name):
        """Get all analysis history for a student"""
        try:
            safe_name = self._sanitize_filename(student_name)
            student_dir = self.students_dir / safe_name
            
            if not student_dir.exists():
                return []
            
            # Get all analysis files
            analysis_files = list(student_dir.glob("analysis_*.json"))
            analysis_files.sort()  # Sort by filename (timestamp)
            
            history = []
            for file_path in analysis_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        history.append(data)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
            
            return history
            
        except Exception as e:
            print(f"Error getting student history: {e}")
            return []
    
    def get_student_summary(self, student_name):
        """Get summary statistics for a student"""
        try:
            safe_name = self._sanitize_filename(student_name)
            summary_file = self.students_dir / safe_name / "summary.json"
            
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            print(f"Error getting student summary: {e}")
            return None
    
    def get_all_students(self):
        """Get list of all students with data"""
        try:
            students = []
            for student_dir in self.students_dir.iterdir():
                if student_dir.is_dir():
                    # Check if has analysis files
                    analysis_files = list(student_dir.glob("analysis_*.json"))
                    if analysis_files:
                        students.append({
                            'name': student_dir.name,
                            'analysis_count': len(analysis_files),
                            'last_analysis': max(f.stat().st_mtime for f in analysis_files)
                        })
            
            # Sort by last analysis time
            students.sort(key=lambda x: x['last_analysis'], reverse=True)
            return students
            
        except Exception as e:
            print(f"Error getting all students: {e}")
            return []
    
    def _sanitize_filename(self, name):
        """Sanitize name for use as filename"""
        # Remove special characters and replace spaces with underscores
        import re
        safe_name = re.sub(r'[^\w\s-]', '', name)
        safe_name = re.sub(r'[\s_-]+', '_', safe_name)
        return safe_name.strip('_').lower()
    
    def _update_student_summary(self, student_id, analysis_data):
        """Update student summary with new analysis"""
        try:
            summary_file = self.students_dir / student_id / "summary.json"
            
            # Load existing summary or create new one
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
            else:
                summary = {
                    'student_id': student_id,
                    'student_name': analysis_data.get('student_name', ''),
                    'total_analyses': 0,
                    'first_analysis': None,
                    'last_analysis': None,
                    'average_scores': {
                        'overall': 0,
                        'voice': 0,
                        'body': 0,
                        'facial': 0
                    },
                    'improvement_trend': 0,
                    'total_practice_time': 0
                }
            
            # Update summary
            summary['total_analyses'] += 1
            summary['last_analysis'] = analysis_data['timestamp']
            
            if summary['first_analysis'] is None:
                summary['first_analysis'] = analysis_data['timestamp']
            
            # Calculate running averages
            current_scores = {
                'overall': analysis_data['overall_score'],
                'voice': analysis_data['voice_analysis']['score'],
                'body': analysis_data['body_analysis']['score'],
                'facial': analysis_data['facial_analysis']['score']
            }
            
            for key, score in current_scores.items():
                old_avg = summary['average_scores'][key]
                count = summary['total_analyses']
                new_avg = ((old_avg * (count - 1)) + score) / count
                summary['average_scores'][key] = round(new_avg, 2)
            
            # Add practice time
            if 'video_duration' in analysis_data:
                summary['total_practice_time'] += analysis_data['video_duration']
            
            # Calculate improvement trend (simple)
            if summary['total_analyses'] >= 2:
                # Get last few scores to calculate trend
                history = self.get_student_history(analysis_data['student_name'])
                if len(history) >= 2:
                    recent_scores = [h['overall_score'] for h in history[-3:]]
                    older_scores = [h['overall_score'] for h in history[:-3] or history[:1]]
                    
                    recent_avg = sum(recent_scores) / len(recent_scores)
                    older_avg = sum(older_scores) / len(older_scores)
                    
                    summary['improvement_trend'] = round(recent_avg - older_avg, 2)
            
            # Save updated summary
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"Error updating student summary: {e}")
    
    def export_student_data(self, student_name):
        """Export all data for a student as a single JSON file"""
        try:
            safe_name = self._sanitize_filename(student_name)
            history = self.get_student_history(student_name)
            summary = self.get_student_summary(student_name)
            
            export_data = {
                'export_date': datetime.now().isoformat(),
                'student_name': student_name,
                'summary': summary,
                'history': history
            }
            
            export_file = self.data_dir / f"export_{safe_name}_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return str(export_file)
            
        except Exception as e:
            print(f"Error exporting student data: {e}")
            return None
    
    def cleanup_old_data(self, days_old=30):
        """Clean up analysis files older than specified days"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            deleted_count = 0
            for student_dir in self.students_dir.iterdir():
                if student_dir.is_dir():
                    analysis_files = student_dir.glob("analysis_*.json")
                    for file_path in analysis_files:
                        if datetime.fromtimestamp(file_path.stat().st_mtime) < cutoff_date:
                            file_path.unlink()
                            deleted_count += 1
            
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up old data: {e}")
            return 0
