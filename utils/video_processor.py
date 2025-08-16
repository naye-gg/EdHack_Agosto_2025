import cv2
import os
import tempfile
import numpy as np

class VideoProcessor:
    def __init__(self):
        """Initialize video processor"""
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
        self.max_duration = 600  # 10 minutes max
        self.min_duration = 10   # 10 seconds min
    
    def process_video(self, video_path):
        """Process and validate video file"""
        try:
            # Check if file exists
            if not os.path.exists(video_path):
                return {
                    'success': False,
                    'error': 'El archivo de video no existe'
                }
            
            # Check file format
            file_ext = os.path.splitext(video_path)[1].lower()
            if file_ext not in self.supported_formats:
                return {
                    'success': False,
                    'error': f'Formato no soportado. Use: {", ".join(self.supported_formats)}'
                }
            
            # Open video file
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {
                    'success': False,
                    'error': 'No se pudo abrir el archivo de video'
                }
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Calculate duration
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            # Validate duration
            if duration < self.min_duration:
                return {
                    'success': False,
                    'error': f'El video es muy corto. Mínimo {self.min_duration} segundos'
                }
            
            if duration > self.max_duration:
                return {
                    'success': False,
                    'error': f'El video es muy largo. Máximo {self.max_duration/60:.1f} minutos'
                }
            
            # Check resolution
            if width < 320 or height < 240:
                return {
                    'success': False,
                    'error': 'Resolución muy baja. Mínimo 320x240'
                }
            
            # Validate that video has content
            quality_check = self._check_video_quality(video_path)
            if not quality_check['success']:
                return quality_check
            
            return {
                'success': True,
                'duration': duration,
                'fps': fps,
                'frame_count': frame_count,
                'resolution': (width, height),
                'file_size': os.path.getsize(video_path),
                'quality_metrics': quality_check['metrics']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error procesando video: {str(e)}'
            }
    
    def _check_video_quality(self, video_path):
        """Check video quality and detect issues"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {
                    'success': False,
                    'error': 'No se pudo abrir el video para verificar calidad'
                }
            
            # Sample frames throughout the video
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            sample_points = np.linspace(0, frame_count - 1, min(10, frame_count), dtype=int)
            
            brightness_values = []
            contrast_values = []
            motion_values = []
            face_detection_count = 0
            
            # Initialize face detector
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            prev_frame = None
            
            for frame_idx in sample_points:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Convert to grayscale for analysis
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Calculate brightness
                brightness = np.mean(gray)
                brightness_values.append(brightness)
                
                # Calculate contrast (standard deviation)
                contrast = np.std(gray)
                contrast_values.append(contrast)
                
                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) > 0:
                    face_detection_count += 1
                
                # Calculate motion (if not first frame)
                if prev_frame is not None:
                    motion = np.mean(np.abs(gray.astype(float) - prev_frame.astype(float)))
                    motion_values.append(motion)
                
                prev_frame = gray
            
            cap.release()
            
            # Analyze quality metrics
            avg_brightness = np.mean(brightness_values) if brightness_values else 0
            avg_contrast = np.mean(contrast_values) if contrast_values else 0
            avg_motion = np.mean(motion_values) if motion_values else 0
            face_detection_rate = face_detection_count / len(sample_points) if sample_points.size > 0 else 0
            
            # Check quality thresholds
            issues = []
            
            if avg_brightness < 50:
                issues.append("Video muy oscuro")
            elif avg_brightness > 200:
                issues.append("Video muy brillante")
            
            if avg_contrast < 20:
                issues.append("Contraste muy bajo")
            
            if face_detection_rate < 0.3:
                issues.append("Cara no detectada consistentemente")
            
            if avg_motion > 50:
                issues.append("Demasiado movimiento de cámara")
            
            # Determine overall quality
            quality_score = self._calculate_quality_score(
                avg_brightness, avg_contrast, face_detection_rate, avg_motion
            )
            
            if quality_score < 3:
                return {
                    'success': False,
                    'error': f'Calidad de video insuficiente. Problemas: {", ".join(issues)}'
                }
            
            return {
                'success': True,
                'metrics': {
                    'brightness': avg_brightness,
                    'contrast': avg_contrast,
                    'motion': avg_motion,
                    'face_detection_rate': face_detection_rate,
                    'quality_score': quality_score,
                    'issues': issues
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error verificando calidad: {str(e)}'
            }
    
    def _calculate_quality_score(self, brightness, contrast, face_rate, motion):
        """Calculate overall quality score (0-10)"""
        score = 0
        
        # Brightness score (0-3)
        if 80 <= brightness <= 170:
            score += 3
        elif 60 <= brightness <= 190:
            score += 2
        elif 40 <= brightness <= 210:
            score += 1
        
        # Contrast score (0-2)
        if contrast >= 40:
            score += 2
        elif contrast >= 25:
            score += 1
        
        # Face detection score (0-3)
        if face_rate >= 0.8:
            score += 3
        elif face_rate >= 0.6:
            score += 2
        elif face_rate >= 0.4:
            score += 1
        
        # Motion score (0-2)
        if motion <= 20:
            score += 2
        elif motion <= 40:
            score += 1
        
        return score
    
    def optimize_video(self, input_path, output_path=None):
        """Optimize video for analysis (optional preprocessing)"""
        try:
            if output_path is None:
                output_path = tempfile.mktemp(suffix='.mp4')
            
            cap = cv2.VideoCapture(input_path)
            
            if not cap.isOpened():
                return None
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Limit resolution for faster processing
            max_width = 1280
            max_height = 720
            
            if width > max_width or height > max_height:
                scale = min(max_width / width, max_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
            else:
                new_width = width
                new_height = height
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, min(fps, 30), (new_width, new_height))
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Resize if necessary
                if new_width != width or new_height != height:
                    frame = cv2.resize(frame, (new_width, new_height))
                
                # Apply basic enhancement
                frame = self._enhance_frame(frame)
                
                out.write(frame)
                frame_count += 1
            
            cap.release()
            out.release()
            
            return output_path if frame_count > 0 else None
            
        except Exception as e:
            print(f"Error optimizing video: {e}")
            return None
    
    def _enhance_frame(self, frame):
        """Apply basic frame enhancement"""
        try:
            # Convert to LAB color space for better enhancement
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            # Merge channels and convert back to BGR
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            
            return enhanced
            
        except Exception:
            # Return original frame if enhancement fails
            return frame
    
    def extract_thumbnail(self, video_path, timestamp=None):
        """Extract thumbnail from video at specified timestamp"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return None
            
            # If no timestamp specified, use middle of video
            if timestamp is None:
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                timestamp = (frame_count / fps) / 2 if fps > 0 else 0
            
            # Seek to timestamp
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Resize thumbnail
                height, width = frame.shape[:2]
                max_size = 200
                
                if width > height:
                    new_width = max_size
                    new_height = int(height * (max_size / width))
                else:
                    new_height = max_size
                    new_width = int(width * (max_size / height))
                
                thumbnail = cv2.resize(frame, (new_width, new_height))
                return thumbnail
            
            return None
            
        except Exception as e:
            print(f"Error extracting thumbnail: {e}")
            return None
