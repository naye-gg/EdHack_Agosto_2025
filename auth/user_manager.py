import bcrypt
import json
import os
from datetime import datetime
from pathlib import Path
import streamlit as st

class UserManager:
    def __init__(self, users_file="auth/users.json"):
        """Initialize user manager with file-based storage"""
        self.users_file = Path(users_file)
        self.users_file.parent.mkdir(exist_ok=True)
        self.users = self._load_users()
    
    def _load_users(self):
        """Load users from JSON file"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading users: {e}")
                return {}
        return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def _hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def register_teacher(self, username, password, full_name, institution=""):
        """Register a new teacher"""
        if username in self.users:
            return {"success": False, "message": "El usuario ya existe"}
        
        if len(password) < 6:
            return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}
        
        user_data = {
            "type": "teacher",
            "username": username,
            "full_name": full_name,
            "institution": institution,
            "password_hash": self._hash_password(password),
            "created_at": datetime.now().isoformat(),
            "students": {},
            "settings": {
                "language": "es",
                "model_version": "basic",
                "max_video_size_mb": 350
            }
        }
        
        self.users[username] = user_data
        
        if self._save_users():
            return {"success": True, "message": "Profesor registrado exitosamente"}
        else:
            return {"success": False, "message": "Error al guardar usuario"}
    
    def register_student(self, teacher_username, dni, student_name=""):
        """Register a student under a teacher"""
        if teacher_username not in self.users:
            return {"success": False, "message": "Profesor no encontrado"}
        
        teacher = self.users[teacher_username]
        
        if dni in teacher["students"]:
            return {"success": False, "message": "Estudiante ya registrado"}
        
        # Generate anonymous student ID
        student_count = len(teacher["students"]) + 1
        anonymous_id = f"EST_{student_count:03d}"
        
        student_data = {
            "dni": dni,
            "anonymous_id": anonymous_id,
            "name": student_name or f"Estudiante {student_count}",
            "registered_at": datetime.now().isoformat(),
            "analyses": [],
            "total_sessions": 0
        }
        
        teacher["students"][dni] = student_data
        
        if self._save_users():
            return {
                "success": True, 
                "message": "Estudiante registrado exitosamente",
                "anonymous_id": anonymous_id
            }
        else:
            return {"success": False, "message": "Error al guardar estudiante"}
    
    def authenticate(self, username, password):
        """Authenticate user login"""
        if username not in self.users:
            return {"success": False, "message": "Usuario no encontrado"}
        
        user = self.users[username]
        
        if self._verify_password(password, user["password_hash"]):
            return {
                "success": True,
                "user": {
                    "username": username,
                    "type": user["type"],
                    "full_name": user["full_name"],
                    "institution": user.get("institution", ""),
                    "settings": user.get("settings", {})
                }
            }
        else:
            return {"success": False, "message": "Contraseña incorrecta"}
    
    def get_teacher_students(self, teacher_username):
        """Get all students for a teacher"""
        if teacher_username not in self.users:
            return []
        
        teacher = self.users[teacher_username]
        return list(teacher["students"].values())
    
    def get_student_by_dni(self, teacher_username, dni):
        """Get student data by DNI"""
        if teacher_username not in self.users:
            return None
        
        teacher = self.users[teacher_username]
        return teacher["students"].get(dni)
    
    def update_user_settings(self, username, settings):
        """Update user settings"""
        if username not in self.users:
            return False
        
        self.users[username]["settings"].update(settings)
        return self._save_users()
    
    def add_student_analysis(self, teacher_username, dni, analysis_data):
        """Add analysis data to student record"""
        if teacher_username not in self.users:
            return False
        
        teacher = self.users[teacher_username]
        if dni not in teacher["students"]:
            return False
        
        student = teacher["students"][dni]
        student["analyses"].append({
            "timestamp": datetime.now().isoformat(),
            "data": analysis_data
        })
        student["total_sessions"] += 1
        
        return self._save_users()
    
    def get_teacher_stats(self, teacher_username):
        """Get statistics for teacher dashboard"""
        if teacher_username not in self.users:
            return None
        
        teacher = self.users[teacher_username]
        students = teacher["students"]
        
        total_students = len(students)
        total_analyses = sum(s["total_sessions"] for s in students.values())
        active_students = len([s for s in students.values() if s["total_sessions"] > 0])
        
        return {
            "total_students": total_students,
            "total_analyses": total_analyses,
            "active_students": active_students,
            "recent_activity": self._get_recent_activity(students)
        }
    
    def _get_recent_activity(self, students):
        """Get recent analysis activity"""
        recent = []
        for student in students.values():
            if student["analyses"]:
                last_analysis = student["analyses"][-1]
                recent.append({
                    "student_id": student["anonymous_id"],
                    "timestamp": last_analysis["timestamp"],
                    "score": last_analysis["data"].get("overall_score", 0)
                })
        
        # Sort by timestamp, most recent first
        recent.sort(key=lambda x: x["timestamp"], reverse=True)
        return recent[:10]  # Return last 10 activities