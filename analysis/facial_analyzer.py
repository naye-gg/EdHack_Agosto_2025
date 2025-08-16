import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import math

class FacialAnalyzer:
    def __init__(self):
        """Initialize MediaPipe face detection and analysis"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Face landmark indices for key features
        self.left_eye_indices = [33, 160, 158, 133, 153, 144]
        self.right_eye_indices = [362, 385, 387, 263, 373, 380]
        self.mouth_indices = [61, 84, 17, 314, 405, 320, 307, 375]
        
    def analyze(self, video_path):
        """Analyze facial expressions and eye contact from video"""
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("No se pudo abrir el video")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            # Analysis variables
            eye_contact_scores = []
            smile_detections = []
            emotion_timeline = []
            confidence_scores = []
            blink_count = 0
            
            frame_count = 0
            last_blink_state = False
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every 3rd frame for efficiency
                if frame_count % 3 == 0:
                    results = self._process_frame(frame)
                    
                    if results:
                        # Eye contact analysis
                        eye_contact_score = self._analyze_eye_contact(results)
                        eye_contact_scores.append(eye_contact_score)
                        
                        # Smile detection
                        smile_score = self._detect_smile(results)
                        smile_detections.append(smile_score)
                        
                        # Emotion and confidence analysis
                        emotion_data = self._analyze_emotion(results, frame)
                        emotion_timeline.append({
                            'time': frame_count / fps if fps > 0 else 0,
                            'confidence': emotion_data['confidence'],
                            'emotion': emotion_data['emotion'],
                            'smile_intensity': smile_score
                        })
                        
                        confidence_scores.append(emotion_data['confidence'])
                        
                        # Blink detection
                        blink_detected = self._detect_blink(results)
                        if blink_detected and not last_blink_state:
                            blink_count += 1
                        last_blink_state = blink_detected
                
                frame_count += 1
            
            cap.release()
            
            # Calculate final metrics
            analysis_results = self._calculate_facial_metrics(
                eye_contact_scores, smile_detections, confidence_scores,
                blink_count, duration
            )
            
            # Generate feedback
            feedback = self._generate_facial_feedback(analysis_results)
            
            return {
                'score': analysis_results['overall_score'],
                'eye_contact_score': analysis_results['eye_contact_score'],
                'confidence_score': analysis_results['confidence_score'],
                'smile_count': analysis_results['smile_count'],
                'blink_rate': analysis_results['blink_rate'],
                'emotion_timeline': emotion_timeline,
                'feedback': feedback
            }
            
        except Exception as e:
            return {
                'score': 0,
                'eye_contact_score': 0,
                'confidence_score': 0,
                'smile_count': 0,
                'blink_rate': 0,
                'emotion_timeline': [],
                'feedback': [f"Error en análisis facial: {str(e)}"]
            }
    
    def _process_frame(self, frame):
        """Process single frame for facial analysis"""
        
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process face mesh
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                # Get first face landmarks
                face_landmarks = results.multi_face_landmarks[0]
                
                # Convert landmarks to pixel coordinates
                h, w, _ = frame.shape
                landmarks = []
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    landmarks.append([x, y, landmark.z])
                
                return {
                    'landmarks': landmarks,
                    'frame_shape': (h, w)
                }
            
            return None
            
        except Exception:
            return None
    
    def _analyze_eye_contact(self, face_data):
        """Analyze eye contact quality"""
        
        try:
            landmarks = face_data['landmarks']
            
            # Get eye landmarks
            left_eye_points = [landmarks[i] for i in self.left_eye_indices]
            right_eye_points = [landmarks[i] for i in self.right_eye_indices]
            
            # Calculate eye direction (simplified)
            # This is a basic approximation - more sophisticated gaze estimation would be needed
            
            # Calculate eye center
            left_eye_center = np.mean(left_eye_points, axis=0)
            right_eye_center = np.mean(right_eye_points, axis=0)
            
            # Calculate eye aspect ratio (for openness)
            left_ear = self._calculate_eye_aspect_ratio(left_eye_points)
            right_ear = self._calculate_eye_aspect_ratio(right_eye_points)
            
            # Average eye openness
            eye_openness = (left_ear + right_ear) / 2
            
            # Simple eye contact estimation based on eye openness and position
            # In a real implementation, this would use more sophisticated gaze estimation
            eye_contact_score = min(1.0, eye_openness * 3)  # Normalize to 0-1
            
            return eye_contact_score
            
        except Exception:
            return 0.5
    
    def _calculate_eye_aspect_ratio(self, eye_points):
        """Calculate eye aspect ratio for blink detection"""
        
        try:
            # Vertical eye landmarks
            A = math.sqrt((eye_points[1][0] - eye_points[5][0])**2 + 
                         (eye_points[1][1] - eye_points[5][1])**2)
            B = math.sqrt((eye_points[2][0] - eye_points[4][0])**2 + 
                         (eye_points[2][1] - eye_points[4][1])**2)
            
            # Horizontal eye landmark
            C = math.sqrt((eye_points[0][0] - eye_points[3][0])**2 + 
                         (eye_points[0][1] - eye_points[3][1])**2)
            
            # Eye aspect ratio
            ear = (A + B) / (2.0 * C)
            return ear
            
        except Exception:
            return 0.25
    
    def _detect_smile(self, face_data):
        """Detect smile intensity"""
        
        try:
            landmarks = face_data['landmarks']
            
            # Get mouth landmarks
            mouth_points = [landmarks[i] for i in self.mouth_indices]
            
            # Calculate mouth width
            mouth_width = math.sqrt(
                (mouth_points[0][0] - mouth_points[4][0])**2 + 
                (mouth_points[0][1] - mouth_points[4][1])**2
            )
            
            # Calculate mouth height
            mouth_height = math.sqrt(
                (mouth_points[2][0] - mouth_points[6][0])**2 + 
                (mouth_points[2][1] - mouth_points[6][1])**2
            )
            
            # Smile ratio (width to height)
            if mouth_height > 0:
                smile_ratio = mouth_width / mouth_height
                # Normalize smile score (higher ratio indicates more smile)
                smile_score = min(1.0, max(0.0, (smile_ratio - 2.5) / 2.0))
            else:
                smile_score = 0.0
            
            return smile_score
            
        except Exception:
            return 0.0
    
    def _analyze_emotion(self, face_data, frame):
        """Analyze emotional state and confidence"""
        
        try:
            # This is a simplified emotion analysis
            # In a real implementation, you would use a trained emotion recognition model
            
            landmarks = face_data['landmarks']
            
            # Calculate facial features for emotion estimation
            
            # Eyebrow position (higher = surprise/happiness, lower = anger/sadness)
            eyebrow_left = landmarks[70]  # Left eyebrow
            eyebrow_right = landmarks[300]  # Right eyebrow
            nose_tip = landmarks[1]  # Nose tip
            
            # Eyebrow height relative to nose
            eyebrow_height = (nose_tip[1] - eyebrow_left[1] + nose_tip[1] - eyebrow_right[1]) / 2
            
            # Mouth corners
            mouth_left = landmarks[61]
            mouth_right = landmarks[291]
            mouth_center = landmarks[13]
            
            # Mouth curve (positive = smile, negative = frown)
            mouth_curve = (mouth_left[1] + mouth_right[1]) / 2 - mouth_center[1]
            
            # Simple emotion classification
            if mouth_curve > 5:  # Smiling
                emotion = "confident"
                confidence = 0.8
            elif mouth_curve < -3:  # Frowning
                emotion = "nervous"
                confidence = 0.3
            elif eyebrow_height > 50:  # Raised eyebrows
                emotion = "surprised"
                confidence = 0.6
            else:
                emotion = "neutral"
                confidence = 0.5
            
            # Add some variation based on eye contact
            eye_contact_score = self._analyze_eye_contact(face_data)
            confidence = (confidence + eye_contact_score) / 2
            
            return {
                'emotion': emotion,
                'confidence': confidence
            }
            
        except Exception:
            return {
                'emotion': "neutral",
                'confidence': 0.5
            }
    
    def _detect_blink(self, face_data):
        """Detect if person is blinking"""
        
        try:
            landmarks = face_data['landmarks']
            
            # Get eye landmarks
            left_eye_points = [landmarks[i] for i in self.left_eye_indices]
            right_eye_points = [landmarks[i] for i in self.right_eye_indices]
            
            # Calculate eye aspect ratios
            left_ear = self._calculate_eye_aspect_ratio(left_eye_points)
            right_ear = self._calculate_eye_aspect_ratio(right_eye_points)
            
            # Average EAR
            ear = (left_ear + right_ear) / 2.0
            
            # Blink threshold (adjust based on testing)
            blink_threshold = 0.2
            
            return ear < blink_threshold
            
        except Exception:
            return False
    
    def _calculate_facial_metrics(self, eye_contact_scores, smile_detections, 
                                confidence_scores, blink_count, duration):
        """Calculate overall facial analysis metrics"""
        
        # Eye contact score
        avg_eye_contact = np.mean(eye_contact_scores) if eye_contact_scores else 0
        eye_contact_score = round(avg_eye_contact * 10, 1)
        
        # Confidence score
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
        confidence_score = round(avg_confidence * 10, 1)
        
        # Smile analysis
        smile_threshold = 0.3
        smile_count = sum(1 for score in smile_detections if score > smile_threshold)
        smile_percentage = smile_count / len(smile_detections) if smile_detections else 0
        
        # Blink rate (normal is 15-20 per minute)
        blink_rate = (blink_count / max(1, duration)) * 60 if duration > 0 else 0
        
        # Overall score calculation
        eye_weight = 0.4
        confidence_weight = 0.35
        smile_weight = 0.25
        
        # Smile score (optimal range 20-40% of time)
        if smile_percentage < 0.1:
            smile_score = smile_percentage * 50  # Encourage some smiling
        elif smile_percentage > 0.5:
            smile_score = max(0, 10 - (smile_percentage - 0.5) * 20)  # Discourage excessive smiling
        else:
            smile_score = 10  # Optimal range
        
        overall_score = (
            eye_contact_score * eye_weight +
            confidence_score * confidence_weight +
            smile_score * smile_weight
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'eye_contact_score': eye_contact_score,
            'confidence_score': confidence_score,
            'smile_count': smile_count,
            'smile_percentage': round(smile_percentage * 100, 1),
            'blink_rate': round(blink_rate, 1)
        }
    
    def _generate_facial_feedback(self, metrics):
        """Generate actionable feedback for facial expressions"""
        feedback = []
        
        # Overall assessment
        if metrics['overall_score'] >= 8:
            feedback.append("Excelente expresión facial y contacto visual.")
        elif metrics['overall_score'] >= 6:
            feedback.append("Buena expresión facial con oportunidades de mejora.")
        else:
            feedback.append("Trabaja en tu expresión facial y contacto visual.")
        
        # Eye contact feedback
        if metrics['eye_contact_score'] >= 8:
            feedback.append("Mantuviste excelente contacto visual con la audiencia.")
        elif metrics['eye_contact_score'] >= 6:
            feedback.append("Buen contacto visual, trata de mantenerlo más consistente.")
        else:
            feedback.append("Mejora tu contacto visual. Mira directamente a la cámara más frecuentemente.")
        
        # Confidence feedback
        if metrics['confidence_score'] >= 8:
            feedback.append("Proyectaste mucha confianza y seguridad.")
        elif metrics['confidence_score'] >= 6:
            feedback.append("Buena confianza general, relájate un poco más.")
        else:
            feedback.append("Trabaja en proyectar más confianza. Relaja tu expresión facial.")
        
        # Smile feedback
        if metrics['smile_percentage'] < 10:
            feedback.append("Sonríe más durante tu presentación para conectar mejor con la audiencia.")
        elif metrics['smile_percentage'] > 50:
            feedback.append("Reduce ligeramente las sonrisas para mantener seriedad cuando sea apropiado.")
        else:
            feedback.append("Buen equilibrio de expresiones faciales.")
        
        # Blink rate feedback
        if metrics['blink_rate'] > 30:
            feedback.append("Parpadeas demasiado, puede indicar nerviosismo. Trata de relajarte.")
        elif metrics['blink_rate'] < 10:
            feedback.append("Parpadea más naturalmente para evitar verse muy tenso.")
        
        return feedback
