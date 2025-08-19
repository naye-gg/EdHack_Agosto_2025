import re
import json
from collections import Counter
import math
from datetime import datetime

class ContentAnalyzer:
    def __init__(self):
        """Initialize content analyzer for script evaluation"""
        self.readability_weights = {
            'sentence_length': 0.3,
            'word_complexity': 0.25,
            'structure': 0.25,
            'coherence': 0.2
        }
        
        # Common transition words in Spanish and English
        self.transition_words = {
            'es': [
                'además', 'por otro lado', 'sin embargo', 'por lo tanto', 
                'en consecuencia', 'finalmente', 'en primer lugar', 'segundo',
                'también', 'asimismo', 'no obstante', 'por consiguiente',
                'en resumen', 'para concluir', 'en definitiva'
            ],
            'en': [
                'furthermore', 'however', 'therefore', 'consequently', 
                'finally', 'first', 'second', 'also', 'moreover',
                'nevertheless', 'thus', 'in conclusion', 'to summarize'
            ]
        }
        
        # Key presentation elements
        self.presentation_elements = {
            'introduction': ['introducción', 'saludo', 'presentación', 'comenzar'],
            'objectives': ['objetivo', 'meta', 'propósito', 'fin'],
            'development': ['desarrollo', 'explicación', 'detalle', 'análisis'],
            'conclusion': ['conclusión', 'resumen', 'cierre', 'finalizar'],
            'call_to_action': ['acción', 'implementar', 'aplicar', 'próximos pasos']
        }
    
    def analyze_script(self, text, language='es'):
        """Analyze presentation script content"""
        
        try:
            # Basic text statistics
            words = self._tokenize_text(text)
            sentences = self._split_sentences(text)
            paragraphs = self._split_paragraphs(text)
            
            # Content analysis
            structure_analysis = self._analyze_structure(text, sentences, language)
            readability_analysis = self._analyze_readability(words, sentences)
            coherence_analysis = self._analyze_coherence(text, language)
            presentation_flow = self._analyze_presentation_flow(text, language)
            
            # Calculate overall content score
            content_score = self._calculate_content_score(
                structure_analysis, readability_analysis, 
                coherence_analysis, presentation_flow
            )
            
            # Generate feedback
            feedback = self._generate_content_feedback(
                structure_analysis, readability_analysis,
                coherence_analysis, presentation_flow, language
            )
            
            return {
                'content_score': content_score,
                'word_count': len(words),
                'sentence_count': len(sentences),
                'paragraph_count': len(paragraphs),
                'average_sentence_length': len(words) / max(1, len(sentences)),
                'structure_analysis': structure_analysis,
                'readability_analysis': readability_analysis,
                'coherence_analysis': coherence_analysis,
                'presentation_flow': presentation_flow,
                'feedback': feedback,
                'detailed_metrics': {
                    'vocabulary_diversity': self._calculate_vocabulary_diversity(words),
                    'technical_terms': self._count_technical_terms(words),
                    'engagement_elements': self._count_engagement_elements(text),
                    'time_estimation': self._estimate_presentation_time(words)
                }
            }
            
        except Exception as e:
            return {
                'content_score': 0,
                'word_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'average_sentence_length': 0,
                'structure_analysis': {},
                'readability_analysis': {},
                'coherence_analysis': {},
                'presentation_flow': {},
                'feedback': [f"Error en análisis de contenido: {str(e)}"],
                'detailed_metrics': {}
            }
    
    def _tokenize_text(self, text):
        """Tokenize text into words"""
        # Remove punctuation and convert to lowercase
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = clean_text.split()
        return [word for word in words if len(word) > 2]  # Filter short words
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_paragraphs(self, text):
        """Split text into paragraphs"""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _analyze_structure(self, text, sentences, language):
        """Analyze presentation structure"""
        
        structure_score = 0
        elements_found = {}
        
        text_lower = text.lower()
        
        # Check for introduction
        intro_keywords = ['buenos días', 'buenas tardes', 'hola', 'mi nombre es', 
                         'me llamo', 'soy', 'presentar', 'hablar sobre']
        intro_found = any(keyword in text_lower[:200] for keyword in intro_keywords)
        elements_found['introduction'] = intro_found
        if intro_found:
            structure_score += 2
        
        # Check for objectives
        obj_keywords = ['objetivo', 'meta', 'propósito', 'vamos a ver', 'explicaré']
        obj_found = any(keyword in text_lower for keyword in obj_keywords)
        elements_found['objectives'] = obj_found
        if obj_found:
            structure_score += 2
        
        # Check for conclusion
        concl_keywords = ['en conclusión', 'para terminar', 'finalmente', 'resumiendo',
                         'para concluir', 'en resumen']
        concl_found = any(keyword in text_lower[-300:] for keyword in concl_keywords)
        elements_found['conclusion'] = concl_found
        if concl_found:
            structure_score += 2
        
        # Check for transitions
        transition_count = sum(1 for word in self.transition_words.get(language, []) 
                              if word in text_lower)
        elements_found['transitions'] = transition_count
        if transition_count >= 3:
            structure_score += 2
        elif transition_count >= 1:
            structure_score += 1
        
        # Check paragraph structure
        paragraphs = self._split_paragraphs(text)
        if len(paragraphs) >= 3:
            structure_score += 2
        
        return {
            'score': min(10, structure_score),
            'elements_found': elements_found,
            'has_introduction': intro_found,
            'has_objectives': obj_found,
            'has_conclusion': concl_found,
            'transition_count': transition_count,
            'paragraph_count': len(paragraphs)
        }
    
    def _analyze_readability(self, words, sentences):
        """Analyze text readability"""
        
        if not words or not sentences:
            return {'score': 0, 'level': 'unknown'}
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Calculate syllable count (approximation for Spanish)
        syllable_count = sum(self._count_syllables(word) for word in words)
        avg_syllables_per_word = syllable_count / len(words)
        
        # Flesch Reading Ease formula (adapted for Spanish)
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Convert to 0-10 scale
        readability_score = max(0, min(10, flesch_score / 10))
        
        # Determine readability level
        if flesch_score >= 90:
            level = 'very_easy'
        elif flesch_score >= 80:
            level = 'easy'
        elif flesch_score >= 70:
            level = 'fairly_easy'
        elif flesch_score >= 60:
            level = 'standard'
        elif flesch_score >= 50:
            level = 'fairly_difficult'
        elif flesch_score >= 30:
            level = 'difficult'
        else:
            level = 'very_difficult'
        
        return {
            'score': round(readability_score, 1),
            'level': level,
            'flesch_score': round(flesch_score, 1),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 1)
        }
    
    def _count_syllables(self, word):
        """Estimate syllable count for a word"""
        # Simple heuristic for Spanish syllable counting
        vowels = 'aeiouáéíóúü'
        word = word.lower()
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        return max(1, count)
    
    def _analyze_coherence(self, text, language):
        """Analyze text coherence and flow"""
        
        sentences = self._split_sentences(text)
        coherence_score = 0
        
        if len(sentences) < 2:
            return {'score': 5, 'connection_strength': 0}
        
        # Check for logical connectors
        connectors = self.transition_words.get(language, [])
        connected_sentences = sum(1 for sentence in sentences 
                                if any(conn in sentence.lower() for conn in connectors))
        
        connection_ratio = connected_sentences / len(sentences)
        coherence_score += connection_ratio * 4
        
        # Check for repetitive patterns (keyword consistency)
        all_words = self._tokenize_text(text)
        word_freq = Counter(all_words)
        
        # Key terms should appear multiple times for coherence
        key_terms = [word for word, freq in word_freq.most_common(10) 
                    if freq > 1 and len(word) > 4]
        
        if len(key_terms) >= 3:
            coherence_score += 3
        elif len(key_terms) >= 1:
            coherence_score += 1
        
        # Check for proper sequencing words
        sequence_words = ['primero', 'segundo', 'tercero', 'luego', 'después', 
                         'finalmente', 'first', 'second', 'then', 'finally']
        sequence_count = sum(1 for word in sequence_words if word in text.lower())
        
        if sequence_count >= 2:
            coherence_score += 3
        
        return {
            'score': min(10, coherence_score),
            'connection_strength': round(connection_ratio * 10, 1),
            'key_terms_count': len(key_terms),
            'sequence_indicators': sequence_count
        }
    
    def _analyze_presentation_flow(self, text, language):
        """Analyze presentation flow and engagement"""
        
        flow_score = 0
        text_lower = text.lower()
        
        # Check for questions (engagement)
        question_count = text.count('?')
        if question_count >= 2:
            flow_score += 2
        elif question_count >= 1:
            flow_score += 1
        
        # Check for examples
        example_indicators = ['por ejemplo', 'como', 'tal como', 'for example', 'such as']
        example_count = sum(1 for indicator in example_indicators 
                           if indicator in text_lower)
        if example_count >= 2:
            flow_score += 2
        
        # Check for emphasis words
        emphasis_words = ['importante', 'clave', 'fundamental', 'esencial', 
                         'crucial', 'important', 'key', 'essential']
        emphasis_count = sum(1 for word in emphasis_words if word in text_lower)
        if emphasis_count >= 2:
            flow_score += 2
        
        # Check for audience engagement
        engagement_phrases = ['ustedes', 'you', 'pregunta', 'question', 'opinión', 'opinion']
        engagement_count = sum(1 for phrase in engagement_phrases 
                              if phrase in text_lower)
        if engagement_count >= 1:
            flow_score += 2
        
        # Check for clear sections
        section_indicators = ['parte', 'sección', 'punto', 'tema', 'part', 'section', 'point']
        section_count = sum(1 for indicator in section_indicators 
                           if indicator in text_lower)
        if section_count >= 2:
            flow_score += 2
        
        return {
            'score': min(10, flow_score),
            'question_count': question_count,
            'example_count': example_count,
            'emphasis_count': emphasis_count,
            'engagement_count': engagement_count,
            'section_count': section_count
        }
    
    def _calculate_content_score(self, structure, readability, coherence, flow):
        """Calculate overall content score"""
        weights = {
            'structure': 0.3,
            'readability': 0.25,
            'coherence': 0.25,
            'flow': 0.2
        }
        
        total_score = (
            structure['score'] * weights['structure'] +
            readability['score'] * weights['readability'] +
            coherence['score'] * weights['coherence'] +
            flow['score'] * weights['flow']
        )
        
        return round(total_score, 1)
    
    def _calculate_vocabulary_diversity(self, words):
        """Calculate vocabulary diversity (TTR)"""
        if not words:
            return 0
        unique_words = len(set(words))
        total_words = len(words)
        return round(unique_words / total_words, 3)
    
    def _count_technical_terms(self, words):
        """Count technical or specialized terms"""
        # Words longer than 7 characters often indicate technical language
        long_words = [word for word in words if len(word) > 7]
        return len(set(long_words))
    
    def _count_engagement_elements(self, text):
        """Count elements that increase audience engagement"""
        engagement_count = 0
        
        # Questions
        engagement_count += text.count('?')
        
        # Direct address
        direct_address = ['ustedes', 'vosotros', 'tú', 'usted']
        engagement_count += sum(1 for addr in direct_address 
                               if addr in text.lower())
        
        # Call to action verbs
        action_verbs = ['piensen', 'imaginen', 'consideren', 'recuerden']
        engagement_count += sum(1 for verb in action_verbs 
                               if verb in text.lower())
        
        return engagement_count
    
    def _estimate_presentation_time(self, words):
        """Estimate presentation time based on word count"""
        # Average speaking rate: 150-160 words per minute
        avg_wpm = 155
        minutes = len(words) / avg_wpm
        return round(minutes, 1)
    
    def _generate_content_feedback(self, structure, readability, coherence, flow, language):
        """Generate actionable feedback for content"""
        feedback = []
        
        # Structure feedback
        if structure['score'] >= 8:
            feedback.append("Excelente estructura de presentación con todos los elementos clave.")
        elif structure['score'] >= 6:
            feedback.append("Buena estructura general, pero puedes mejorar algunos elementos.")
        else:
            feedback.append("Mejora la estructura: incluye introducción clara, objetivos y conclusión.")
        
        if not structure['has_introduction']:
            feedback.append("Agrega una introducción que capte la atención del público.")
        
        if not structure['has_conclusion']:
            feedback.append("Incluye una conclusión sólida que resuma los puntos clave.")
        
        if structure['transition_count'] < 2:
            feedback.append("Usa más palabras de transición para conectar tus ideas.")
        
        # Readability feedback
        if readability['score'] >= 7:
            feedback.append("Tu texto tiene buena legibilidad y es fácil de seguir.")
        elif readability['avg_sentence_length'] > 20:
            feedback.append("Acorta tus oraciones para mejorar la claridad.")
        elif readability['avg_sentence_length'] < 8:
            feedback.append("Combina algunas oraciones cortas para mejor fluidez.")
        
        # Coherence feedback
        if coherence['score'] >= 7:
            feedback.append("Tu presentación mantiene buena coherencia y flujo lógico.")
        else:
            feedback.append("Mejora la conexión entre ideas usando más conectores lógicos.")
        
        # Flow feedback
        if flow['score'] >= 7:
            feedback.append("Excelente uso de elementos que mantienen el interés del público.")
        else:
            if flow['question_count'] == 0:
                feedback.append("Incluye preguntas para involucrar más al público.")
            if flow['example_count'] < 1:
                feedback.append("Agrega ejemplos concretos para ilustrar tus puntos.")
        
        return feedback
    
    def evaluate_with_rubric(self, content_analysis, rubric_data):
        """Evaluate content against a specific rubric"""
        
        try:
            if isinstance(rubric_data, str):
                # Parse rubric text
                rubric = self._parse_rubric_text(rubric_data)
            else:
                # Assume rubric_data is already structured
                rubric = rubric_data
            
            evaluation = {}
            total_score = 0
            max_possible = 0
            
            for criterion, details in rubric.items():
                criterion_score = self._evaluate_criterion(
                    criterion, details, content_analysis
                )
                evaluation[criterion] = criterion_score
                total_score += criterion_score['score']
                max_possible += criterion_score['max_score']
            
            overall_percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
            
            return {
                'overall_score': round(total_score, 1),
                'max_possible_score': max_possible,
                'percentage': round(overall_percentage, 1),
                'criteria_evaluation': evaluation,
                'recommendations': self._generate_rubric_feedback(evaluation)
            }
            
        except Exception as e:
            return {
                'overall_score': 0,
                'max_possible_score': 0,
                'percentage': 0,
                'criteria_evaluation': {},
                'recommendations': [f"Error evaluando con rúbrica: {str(e)}"]
            }
    
    def _parse_rubric_text(self, rubric_text):
        """Parse rubric from text format"""
        # Simple rubric parsing - can be enhanced based on format
        rubric = {
            'contenido': {'weight': 0.3, 'max_score': 10},
            'organizacion': {'weight': 0.25, 'max_score': 10},
            'claridad': {'weight': 0.25, 'max_score': 10},
            'engagement': {'weight': 0.2, 'max_score': 10}
        }
        
        return rubric
    
    def _evaluate_criterion(self, criterion, details, content_analysis):
        """Evaluate a single rubric criterion"""
        
        score = 0
        max_score = details.get('max_score', 10)
        
        if criterion.lower() in ['contenido', 'content']:
            score = content_analysis['content_score']
        elif criterion.lower() in ['organizacion', 'organization', 'estructura']:
            score = content_analysis['structure_analysis']['score']
        elif criterion.lower() in ['claridad', 'clarity', 'legibilidad']:
            score = content_analysis['readability_analysis']['score']
        elif criterion.lower() in ['engagement', 'participacion']:
            score = content_analysis['presentation_flow']['score']
        else:
            # Default evaluation based on overall content quality
            score = content_analysis['content_score']
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1) if max_score > 0 else 0
        }
    
    def _generate_rubric_feedback(self, evaluation):
        """Generate feedback based on rubric evaluation"""
        recommendations = []
        
        for criterion, results in evaluation.items():
            if results['percentage'] < 70:
                recommendations.append(
                    f"Mejora necesaria en {criterion}: {results['percentage']:.1f}%"
                )
            elif results['percentage'] < 85:
                recommendations.append(
                    f"Buen trabajo en {criterion}, pero aún hay espacio para mejora"
                )
        
        if not recommendations:
            recommendations.append("¡Excelente trabajo! Cumples con todos los criterios de la rúbrica.")
        
        return recommendations
    
    def analyze_with_script(self, transcribed_text, script_content):
        """Analyze content comparing transcribed speech with provided script"""
        try:
            # Basic content analysis of transcribed text
            content_analysis = self.analyze(transcribed_text)
            
            # Script comparison metrics
            script_adherence = self._calculate_script_adherence(transcribed_text, script_content)
            message_clarity = self._calculate_message_clarity(transcribed_text, script_content)
            
            # Calculate overall content score (weighted average)
            content_score = content_analysis['content_score']
            overall_score = round((content_score * 0.4) + (script_adherence * 0.3) + (message_clarity * 0.3), 1)
            
            # Generate feedback
            feedback = self._generate_script_feedback(content_analysis, script_adherence, message_clarity)
            
            return {
                'score': overall_score,
                'content_score': content_score,
                'script_adherence': script_adherence,
                'message_clarity': message_clarity,
                'feedback': feedback,
                'transcribed_length': len(transcribed_text.split()),
                'script_length': len(script_content.split()),
                'similarity_ratio': self._calculate_similarity(transcribed_text, script_content)
            }
            
        except Exception as e:
            return {
                'score': 0,
                'content_score': 0,
                'script_adherence': 0,
                'message_clarity': 0,
                'feedback': [f"Error en el análisis de contenido: {str(e)}"],
                'transcribed_length': 0,
                'script_length': 0,
                'similarity_ratio': 0
            }
    
    def _calculate_script_adherence(self, transcribed_text, script_content):
        """Calculate how well the speech follows the script"""
        if not script_content or not transcribed_text:
            return 0
            
        # Normalize texts
        transcript_words = set(self._normalize_text(transcribed_text).split())
        script_words = set(self._normalize_text(script_content).split())
        
        # Calculate word overlap
        common_words = transcript_words.intersection(script_words)
        script_coverage = len(common_words) / len(script_words) if script_words else 0
        
        # Calculate length similarity
        length_ratio = min(len(transcribed_text), len(script_content)) / max(len(transcribed_text), len(script_content)) if max(len(transcribed_text), len(script_content)) > 0 else 0
        
        # Combined adherence score
        adherence_score = (script_coverage * 0.7) + (length_ratio * 0.3)
        
        return round(adherence_score * 10, 1)
    
    def _calculate_message_clarity(self, transcribed_text, script_content):
        """Calculate clarity of the spoken message compared to script"""
        if not transcribed_text:
            return 0
            
        # Analyze structure and coherence of transcribed text
        sentences = self._split_sentences(transcribed_text)
        
        # Clarity metrics
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        coherence_score = self._calculate_coherence(transcribed_text)
        
        # Optimal sentence length (10-20 words)
        length_score = 1 - abs(avg_sentence_length - 15) / 15 if avg_sentence_length > 0 else 0
        length_score = max(0, min(1, length_score))
        
        # Combined clarity score
        clarity_score = (length_score * 0.4) + (coherence_score * 0.6)
        
        return round(clarity_score * 10, 1)
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity ratio between two texts"""
        if not text1 or not text2:
            return 0
            
        words1 = set(self._normalize_text(text1).split())
        words2 = set(self._normalize_text(text2).split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def _normalize_text(self, text):
        """Normalize text for comparison"""
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _generate_script_feedback(self, content_analysis, script_adherence, message_clarity):
        """Generate feedback for script-based analysis"""
        feedback = []
        
        # Content feedback
        if content_analysis['content_score'] < 6:
            feedback.append("El contenido de tu presentación necesita mejorar en estructura y calidad")
        elif content_analysis['content_score'] < 8:
            feedback.append("Buen contenido, pero puedes mejorarlo con más detalles y ejemplos")
        else:
            feedback.append("Excelente calidad de contenido en tu presentación")
        
        # Script adherence feedback
        if script_adherence < 6:
            feedback.append("Te desviaste considerablemente del guión planificado")
        elif script_adherence < 8:
            feedback.append("Siguiste parcialmente el guión, pero hubo algunas desviaciones")
        else:
            feedback.append("Excelente adherencia al guión planificado")
        
        # Message clarity feedback
        if message_clarity < 6:
            feedback.append("Tu mensaje podría ser más claro y mejor estructurado")
        elif message_clarity < 8:
            feedback.append("Mensaje relativamente claro, pero puede mejorarse")
        else:
            feedback.append("Tu mensaje fue claro y bien estructurado")
        
        return feedback