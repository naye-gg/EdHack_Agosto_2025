import whisper
import numpy as np
import re
import librosa
from collections import Counter
import tempfile
import os

class VoiceAnalyzer:
    def __init__(self):
        """Initialize the voice analyzer with Whisper model"""
        try:
            # Load smaller Whisper model for faster processing
            self.model = whisper.load_model("base")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None
        
        # Spanish filler words (muletillas)
        self.filler_words = [
            'eh', 'ehh', 'ehhh', 'em', 'emm', 'emmm',
            'este', 'esta', 'esto', 'entonces', 'pues',
            'bueno', 'o sea', 'digamos', 'como que',
            'tipo', 'mmm', 'aaa', 'eee', 'ooo'
        ]
    
    def analyze(self, video_path):
        """Analyze voice and prosody from video"""
        
        try:
            # Extract audio from video
            audio_path = self._extract_audio(video_path)
            
            # Transcribe audio
            transcription_result = self._transcribe_audio(audio_path)
            
            # Analyze transcription
            text_analysis = self._analyze_text(transcription_result['text'])
            
            # Analyze audio features
            audio_analysis = self._analyze_audio_features(audio_path)
            
            # Calculate overall voice score
            score = self._calculate_voice_score(text_analysis, audio_analysis)
            
            # Generate feedback
            feedback = self._generate_feedback(text_analysis, audio_analysis, score)
            
            # Clean up temporary audio file
            os.unlink(audio_path)
            
            return {
                'score': score,
                'transcription': transcription_result['text'],
                'clarity_score': audio_analysis['clarity_score'],
                'speaking_rate': text_analysis['speaking_rate'],
                'filler_count': text_analysis['filler_count'],
                'word_count': text_analysis['word_count'],
                'confidence_timeline': self._create_confidence_timeline(transcription_result),
                'feedback': feedback
            }
            
        except Exception as e:
            return {
                'score': 0,
                'transcription': "",
                'clarity_score': 0,
                'speaking_rate': 0,
                'filler_count': 0,
                'word_count': 0,
                'confidence_timeline': [],
                'feedback': [f"Error en el análisis de voz: {str(e)}"]
            }
    
    def _extract_audio(self, video_path):
        """Extract audio from video file"""
        audio_path = tempfile.mktemp(suffix='.wav')
        
        try:
            # Use librosa to load video and extract audio
            y, sr = librosa.load(video_path, sr=16000)
            
            # Save as WAV file
            import soundfile as sf
            sf.write(audio_path, y, sr)
            
            return audio_path
            
        except Exception:
            # Fallback: create dummy audio file
            import soundfile as sf
            dummy_audio = np.zeros(16000)  # 1 second of silence
            sf.write(audio_path, dummy_audio, 16000)
            return audio_path
    
    def _transcribe_audio(self, audio_path):
        """Transcribe audio using Whisper"""
        
        if self.model is None:
            return {
                'text': "No se pudo cargar el modelo de transcripción",
                'segments': []
            }
        
        try:
            result = self.model.transcribe(
                audio_path,
                language='es',
                word_timestamps=True
            )
            return result
            
        except Exception as e:
            return {
                'text': f"Error en transcripción: {str(e)}",
                'segments': []
            }
    
    def _analyze_text(self, text):
        """Analyze transcribed text for speech patterns"""
        
        # Clean and tokenize text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Count filler words
        filler_count = sum(1 for word in words if word in self.filler_words)
        
        # Calculate speaking rate (words per minute)
        # Assuming average video length of 2-5 minutes
        estimated_duration = max(2, len(words) / 150)  # Rough estimate
        speaking_rate = len(words) / estimated_duration if estimated_duration > 0 else 0
        
        # Analyze sentence structure
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
        
        return {
            'word_count': len(words),
            'filler_count': filler_count,
            'filler_ratio': filler_count / max(1, len(words)),
            'speaking_rate': round(speaking_rate),
            'avg_sentence_length': avg_sentence_length,
            'unique_words': len(set(words))
        }
    
    def _analyze_audio_features(self, audio_path):
        """Analyze audio features for clarity and prosody"""
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=16000)
            
            # Voice activity detection (simple energy-based)
            energy = librosa.feature.rms(y=y)[0]
            voice_frames = energy > np.percentile(energy, 20)
            voice_ratio = np.sum(voice_frames) / len(voice_frames)
            
            # Pitch analysis
            pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            pitch_variation = np.std(pitch_values) if pitch_values else 0
            
            # Spectral features for clarity
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            
            # Calculate clarity score based on spectral features
            clarity_score = min(10, (spectral_centroid / 1000) + (spectral_rolloff / 2000))
            
            return {
                'voice_ratio': voice_ratio,
                'pitch_variation': pitch_variation,
                'clarity_score': round(clarity_score, 1),
                'spectral_centroid': spectral_centroid
            }
            
        except Exception:
            return {
                'voice_ratio': 0.7,
                'pitch_variation': 50,
                'clarity_score': 5.0,
                'spectral_centroid': 1000
            }
    
    def _calculate_voice_score(self, text_analysis, audio_analysis):
        """Calculate overall voice score"""
        
        # Clarity component (30%)
        clarity_component = (audio_analysis['clarity_score'] / 10) * 3
        
        # Speaking rate component (25%)
        ideal_rate = 150  # words per minute
        rate_score = max(0, 10 - abs(text_analysis['speaking_rate'] - ideal_rate) / 10)
        rate_component = (rate_score / 10) * 2.5
        
        # Filler words component (25%)
        filler_penalty = min(5, text_analysis['filler_count'] * 0.5)
        filler_component = max(0, 2.5 - filler_penalty)
        
        # Voice activity component (20%)
        voice_component = audio_analysis['voice_ratio'] * 2
        
        total_score = clarity_component + rate_component + filler_component + voice_component
        return round(min(10, max(0, total_score)), 1)
    
    def _create_confidence_timeline(self, transcription_result):
        """Create timeline of speech confidence"""
        timeline = []
        
        if 'segments' in transcription_result:
            for segment in transcription_result['segments']:
                timeline.append({
                    'time': segment.get('start', 0),
                    'confidence': segment.get('avg_logprob', -1) + 1,  # Normalize to 0-1
                    'text': segment.get('text', '')
                })
        
        return timeline
    
    def _generate_feedback(self, text_analysis, audio_analysis, score):
        """Generate actionable feedback in Spanish"""
        feedback = []
        
        # Overall performance
        if score >= 8:
            feedback.append("¡Excelente trabajo! Tu dicción y fluidez son muy buenas.")
        elif score >= 6:
            feedback.append("Buen desempeño general, pero hay áreas de mejora.")
        else:
            feedback.append("Necesitas trabajar en tu técnica vocal y fluidez.")
        
        # Speaking rate feedback
        if text_analysis['speaking_rate'] > 180:
            feedback.append("Hablas muy rápido. Intenta reducir la velocidad para mayor claridad.")
        elif text_analysis['speaking_rate'] < 120:
            feedback.append("Hablas muy lento. Intenta aumentar ligeramente la velocidad.")
        else:
            feedback.append("Tu velocidad de habla es adecuada.")
        
        # Filler words feedback
        if text_analysis['filler_count'] > 10:
            feedback.append("Usas demasiadas muletillas. Practica pausas conscientes en lugar de 'eh', 'este', etc.")
        elif text_analysis['filler_count'] > 5:
            feedback.append("Reduce el uso de muletillas para sonar más profesional.")
        else:
            feedback.append("Excelente control de muletillas.")
        
        # Clarity feedback
        if audio_analysis['clarity_score'] < 6:
            feedback.append("Trabaja en tu articulación. Abre más la boca y pronuncia claramente.")
        else:
            feedback.append("Tu claridad vocal es buena.")
        
        # Voice activity feedback
        if audio_analysis['voice_ratio'] < 0.6:
            feedback.append("Incrementa tu presencia vocal. Evita pausas muy largas.")
        
        return feedback
