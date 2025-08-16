import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import math

class BodyLanguageAnalyzer:
    def __init__(self):
        """Initialize MediaPipe pose detection"""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    def analyze(self, video_path):
        """Analyze body language from video"""
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("No se pudo abrir el video")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            # Analysis variables
            pose_data = []
            gesture_count = 0
            movement_history = deque(maxlen=30)  # Last 30 frames for smoothing
            stability_scores = []
            
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every 5th frame for efficiency
                if frame_count % 5 == 0:
                    results = self._process_frame(frame)
                    
                    if results:
                        pose_data.append(results)
                        
                        # Track movement
                        movement_score = self._calculate_movement(results, movement_history)
                        movement_history.append(movement_score)
                        
                        # Detect gestures
                        if self._detect_gesture(results):
                            gesture_count += 1
                        
                        # Calculate posture stability
                        stability = self._calculate_posture_stability(results)
                        stability_scores.append(stability)
                
                frame_count += 1
            
            cap.release()
            
            # Calculate final metrics
            analysis_results = self._calculate_body_metrics(
                pose_data, gesture_count, stability_scores, duration
            )
            
            # Generate feedback
            feedback = self._generate_body_feedback(analysis_results)
            
            return {
                'score': analysis_results['overall_score'],
                'posture_stability': analysis_results['posture_stability'],
                'movement_score': analysis_results['movement_score'],
                'gesture_count': gesture_count,
                'movement_timeline': self._create_movement_timeline(pose_data),
                'feedback': feedback
            }
            
        except Exception as e:
            return {
                'score': 0,
                'posture_stability': 0,
                'movement_score': 0,
                'gesture_count': 0,
                'movement_timeline': [],
                'feedback': [f"Error en análisis corporal: {str(e)}"]
            }
    
    def _process_frame(self, frame):
        """Process single frame for pose detection"""
        
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process pose
            results = self.pose.process(rgb_frame)
            
            if results.pose_landmarks:
                # Extract key landmarks
                landmarks = results.pose_landmarks.landmark
                
                return {
                    'nose': [landmarks[0].x, landmarks[0].y],
                    'left_shoulder': [landmarks[11].x, landmarks[11].y],
                    'right_shoulder': [landmarks[12].x, landmarks[12].y],
                    'left_elbow': [landmarks[13].x, landmarks[13].y],
                    'right_elbow': [landmarks[14].x, landmarks[14].y],
                    'left_wrist': [landmarks[15].x, landmarks[15].y],
                    'right_wrist': [landmarks[16].x, landmarks[16].y],
                    'left_hip': [landmarks[23].x, landmarks[23].y],
                    'right_hip': [landmarks[24].x, landmarks[24].y],
                    'visibility': [l.visibility for l in landmarks]
                }
            
            return None
            
        except Exception:
            return None
    
    def _calculate_movement(self, current_pose, movement_history):
        """Calculate movement intensity for current frame"""
        
        if not movement_history:
            return 0
        
        try:
            # Compare with previous frame
            prev_pose = movement_history[-1] if movement_history else None
            
            if prev_pose is None:
                return 0
            
            # Calculate movement of key points
            movement = 0
            key_points = ['nose', 'left_wrist', 'right_wrist', 'left_shoulder', 'right_shoulder']
            
            for point in key_points:
                if point in current_pose and point in prev_pose:
                    dx = current_pose[point][0] - prev_pose[point][0]
                    dy = current_pose[point][1] - prev_pose[point][1]
                    movement += math.sqrt(dx*dx + dy*dy)
            
            return movement
            
        except Exception:
            return 0
    
    def _detect_gesture(self, pose_data):
        """Detect if current pose represents a gesture"""
        
        try:
            # Simple gesture detection based on hand position relative to body
            left_wrist = pose_data.get('left_wrist', [0, 0])
            right_wrist = pose_data.get('right_wrist', [0, 0])
            left_shoulder = pose_data.get('left_shoulder', [0, 0])
            right_shoulder = pose_data.get('right_shoulder', [0, 0])
            
            # Check if hands are raised (above shoulder level)
            left_raised = left_wrist[1] < left_shoulder[1] - 0.1
            right_raised = right_wrist[1] < right_shoulder[1] - 0.1
            
            # Check if hands are extended (away from body center)
            body_center_x = (left_shoulder[0] + right_shoulder[0]) / 2
            left_extended = abs(left_wrist[0] - body_center_x) > 0.2
            right_extended = abs(right_wrist[0] - body_center_x) > 0.2
            
            # Gesture detected if at least one hand is raised or extended
            return left_raised or right_raised or left_extended or right_extended
            
        except Exception:
            return False
    
    def _calculate_posture_stability(self, pose_data):
        """Calculate posture stability score"""
        
        try:
            # Calculate shoulder alignment
            left_shoulder = pose_data.get('left_shoulder', [0, 0])
            right_shoulder = pose_data.get('right_shoulder', [0, 0])
            
            # Shoulder level difference (should be minimal for good posture)
            shoulder_diff = abs(left_shoulder[1] - right_shoulder[1])
            shoulder_stability = max(0, 1 - shoulder_diff * 10)
            
            # Head position relative to shoulders
            nose = pose_data.get('nose', [0, 0])
            shoulder_center_x = (left_shoulder[0] + right_shoulder[0]) / 2
            head_alignment = max(0, 1 - abs(nose[0] - shoulder_center_x) * 5)
            
            # Overall stability
            stability = (shoulder_stability + head_alignment) / 2
            return min(1, max(0, stability))
            
        except Exception:
            return 0.5
    
    def _calculate_body_metrics(self, pose_data, gesture_count, stability_scores, duration):
        """Calculate overall body language metrics"""
        
        if not pose_data:
            return {
                'overall_score': 0,
                'posture_stability': 0,
                'movement_score': 0,
                'gesture_density': 0
            }
        
        # Average posture stability
        avg_stability = np.mean(stability_scores) if stability_scores else 0
        posture_stability = round(avg_stability * 10, 1)
        
        # Movement analysis
        total_movement = sum(self._calculate_movement(pose, []) for pose in pose_data)
        avg_movement = total_movement / len(pose_data) if pose_data else 0
        
        # Optimal movement range (not too static, not too fidgety)
        optimal_movement = 0.1  # Adjust based on testing
        movement_score = max(0, 10 - abs(avg_movement - optimal_movement) * 50)
        movement_score = round(min(10, movement_score), 1)
        
        # Gesture density (gestures per minute)
        gesture_density = (gesture_count / max(1, duration)) * 60 if duration > 0 else 0
        
        # Overall score calculation
        posture_weight = 0.4
        movement_weight = 0.3
        gesture_weight = 0.3
        
        # Ideal gesture rate: 8-15 per minute
        gesture_score = 10
        if gesture_density < 5:
            gesture_score = max(0, gesture_density * 2)
        elif gesture_density > 20:
            gesture_score = max(0, 10 - (gesture_density - 20) * 0.5)
        
        overall_score = (
            posture_stability * posture_weight +
            movement_score * movement_weight +
            gesture_score * gesture_weight
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'posture_stability': posture_stability,
            'movement_score': movement_score,
            'gesture_density': gesture_density,
            'gesture_score': gesture_score
        }
    
    def _create_movement_timeline(self, pose_data):
        """Create timeline of movement intensity"""
        timeline = []
        
        for i, pose in enumerate(pose_data):
            # Calculate time stamp (assuming 5 fps processing)
            timestamp = i * 0.2  # 5 frames per second
            
            # Calculate movement intensity
            if i > 0:
                movement = self._calculate_movement(pose, [pose_data[i-1]])
            else:
                movement = 0
            
            timeline.append({
                'time': timestamp,
                'movement_intensity': movement,
                'gesture_active': self._detect_gesture(pose)
            })
        
        return timeline
    
    def _generate_body_feedback(self, metrics):
        """Generate actionable feedback for body language"""
        feedback = []
        
        # Overall assessment
        if metrics['overall_score'] >= 8:
            feedback.append("Excelente presencia corporal y uso del espacio.")
        elif metrics['overall_score'] >= 6:
            feedback.append("Buena presencia corporal con algunas áreas de mejora.")
        else:
            feedback.append("Necesitas trabajar en tu lenguaje corporal y presencia.")
        
        # Posture feedback
        if metrics['posture_stability'] >= 8:
            feedback.append("Mantuviste una postura excelente durante la presentación.")
        elif metrics['posture_stability'] >= 6:
            feedback.append("Tu postura es generalmente buena, pero puedes mejorar la alineación.")
        else:
            feedback.append("Trabaja en mantener una postura más erguida y estable.")
        
        # Movement feedback
        if metrics['movement_score'] >= 8:
            feedback.append("Tus movimientos son naturales y apropiados.")
        elif metrics['movement_score'] >= 6:
            feedback.append("Buen control de movimientos, evita movimientos nerviosos.")
        else:
            feedback.append("Controla mejor tus movimientos. Evita balancearte o moverte excesivamente.")
        
        # Gesture feedback
        if metrics['gesture_density'] > 20:
            feedback.append("Reduces la cantidad de gestos. Úsalos de forma más estratégica.")
        elif metrics['gesture_density'] < 5:
            feedback.append("Incluye más gestos para hacer tu presentación más dinámica.")
        else:
            feedback.append("Buen uso de gestos para complementar tu mensaje.")
        
        return feedback
