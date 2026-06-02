"""
Multi-Language Support for AI Legal Assistant
Handles Hindi and Tamil language processing with automatic translation and embedding support
"""

import logging
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
import json

try:
    from google.cloud import translate_v2
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False
    logging.warning("google-cloud-translate not available. Install for production use.")

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("transformers not available. Install for embeddings.")

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    HINDI = "hi"
    TAMIL = "ta"


class TranslationEngine(Enum):
    """Translation engine options"""
    GOOGLE = "google"
    OFFLINE = "offline"


@dataclass
class LanguageResult:
    """Language processing result"""
    original_text: str
    translated_text: str
    source_language: Language
    target_language: Language
    confidence: float
    embedding: Optional[List[float]] = None


@dataclass
class MultilingualQuery:
    """Multilingual query wrapper"""
    original_query: str
    english_query: str
    source_language: Language
    query_type: str  # "ipc_section", "case_law", "act_inquiry", etc.


@dataclass
class MultilingualResponse:
    """Multilingual response wrapper"""
    english_response: str
    translated_response: str
    source_language: Language
    target_language: Language
    citations: List[str]
    sources: List[Dict]


# ============================================================================
# LANGUAGE DETECTION
# ============================================================================

class LanguageDetector:
    """Detect language of input text"""
    
    # Unicode ranges for Indian scripts
    HINDI_UNICODE_RANGE = (0x0900, 0x097F)  # Devanagari
    TAMIL_UNICODE_RANGE = (0x0B80, 0x0BFF)  # Tamil
    ENGLISH_ASCII_RANGE = (0x0000, 0x007F)  # ASCII
    
    HINDI_KEYWORDS = {
        'aapadhik', 'kanoon', 'nyay', 'dhara', 'saza', 'mukadma',
        'हिंदी', 'कानून', 'न्यायिक', 'धारा', 'सजा', 'मुकदमा'
    }
    
    TAMIL_KEYWORDS = {
        'koodal', 'nyayam', 'vidhi', 'adhigaram', 'tarum',
        'தமிழ்', 'கூடல்', 'நியாயம்', 'விதி', 'அதிகாரம்'
    }
    
    @staticmethod
    def detect(text: str) -> Tuple[Language, float]:
        """
        Detect language of text
        
        Returns:
            Tuple of (Language, confidence_score)
        """
        if not text:
            return Language.ENGLISH, 0.0
        
        # Count Unicode ranges
        devanagari_count = sum(1 for c in text if LanguageDetector.HINDI_UNICODE_RANGE[0] <= ord(c) <= LanguageDetector.HINDI_UNICODE_RANGE[1])
        tamil_count = sum(1 for c in text if LanguageDetector.TAMIL_UNICODE_RANGE[0] <= ord(c) <= LanguageDetector.TAMIL_UNICODE_RANGE[1])
        ascii_count = sum(1 for c in text if c.isascii())
        
        total = len(text)
        
        if total == 0:
            return Language.ENGLISH, 0.5
        
        devanagari_ratio = devanagari_count / total
        tamil_ratio = tamil_count / total
        ascii_ratio = ascii_count / total
        
        # Determine language
        if devanagari_ratio > 0.3:
            return Language.HINDI, devanagari_ratio
        elif tamil_ratio > 0.3:
            return Language.TAMIL, tamil_ratio
        else:
            return Language.ENGLISH, ascii_ratio
    
    @staticmethod
    def detect_with_keywords(text: str) -> Tuple[Language, float]:
        """Detect using keyword matching (fallback method)"""
        text_lower = text.lower()
        
        hindi_score = sum(1 for kw in LanguageDetector.HINDI_KEYWORDS if kw in text_lower)
        tamil_score = sum(1 for kw in LanguageDetector.TAMIL_KEYWORDS if kw in text_lower)
        
        if hindi_score > tamil_score and hindi_score > 0:
            return Language.HINDI, hindi_score / len(LanguageDetector.HINDI_KEYWORDS)
        elif tamil_score > hindi_score and tamil_score > 0:
            return Language.TAMIL, tamil_score / len(LanguageDetector.TAMIL_KEYWORDS)
        else:
            return Language.ENGLISH, 0.5


# ============================================================================
# TRANSLATION HANDLERS
# ============================================================================

class TranslationHandler:
    """Handle translation between languages"""
    
    def __init__(self, engine: TranslationEngine = TranslationEngine.OFFLINE):
        """
        Initialize translation handler
        
        Args:
            engine: Translation engine to use (GOOGLE or OFFLINE)
        """
        self.engine = engine
        self.translator = None
        
        if engine == TranslationEngine.GOOGLE and GOOGLE_TRANSLATE_AVAILABLE:
            self.translator = translate_v2.Client()
        elif engine == TranslationEngine.OFFLINE:
            logger.info("Using offline translation (requires M2M-100 model)")
    
    def translate(
        self,
        text: str,
        source_lang: Language,
        target_lang: Language
    ) -> Tuple[str, float]:
        """
        Translate text between languages
        
        Args:
            text: Text to translate
            source_lang: Source language
            target_lang: Target language
        
        Returns:
            Tuple of (translated_text, confidence)
        """
        if source_lang == target_lang:
            return text, 1.0
        
        try:
            if self.engine == TranslationEngine.GOOGLE and self.translator:
                return self._translate_google(text, source_lang, target_lang)
            else:
                return self._translate_offline(text, source_lang, target_lang)
        
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text, 0.0
    
    def _translate_google(
        self,
        text: str,
        source_lang: Language,
        target_lang: Language
    ) -> Tuple[str, float]:
        """Translate using Google Cloud Translation API"""
        try:
            result = self.translator.translate_text(
                text,
                source_language=source_lang.value,
                target_language=target_lang.value
            )
            
            translated = result['translatedText']
            # Google API doesn't provide confidence, estimate as 0.85
            return translated, 0.85
        
        except Exception as e:
            logger.error(f"Google translation error: {e}")
            return text, 0.0
    
    @staticmethod
    def _translate_offline(
        text: str,
        source_lang: Language,
        target_lang: Language
    ) -> Tuple[str, float]:
        """
        Offline translation using simple rules and mapping
        For production, use M2M-100 model or similar
        """
        
        # Simple legal term translations
        legal_terms = {
            Language.ENGLISH: {
                "Section": {"hi": "धारा", "ta": "பிரிவு"},
                "IPC": {"hi": "आईपीसी", "ta": "IPC"},
                "punishment": {"hi": "सजा", "ta": "தண்டனை"},
                "court": {"hi": "अदालत", "ta": "நீதிமன்றம்"},
                "judge": {"hi": "न्यायाधीश", "ta": "நீதிபதி"},
                "bail": {"hi": "जमानत", "ta": "பிணையம்"},
                "verdict": {"hi": "फैसला", "ta": "தீர்ப்பு"},
                "evidence": {"hi": "साक्ष्य", "ta": "சாட்சியம்"},
                "witness": {"hi": "गवाह", "ta": "சாட்சி"},
                "case": {"hi": "मामला", "ta": "வழக்கு"},
                "charge": {"hi": "आरोप", "ta": "குற்றச்சாட்டு"},
                "guilty": {"hi": "दोषी", "ta": "குற்றவாளி"},
                "innocent": {"hi": "निर्दोष", "ta": "குற்றமற்றவர்"},
            }
        }
        
        # Simple substitution for legal terms (production would use proper MT model)
        translated = text
        
        if source_lang == Language.ENGLISH and target_lang in (Language.HINDI, Language.TAMIL):
            target_lang_code = target_lang.value
            for eng_term, translations in legal_terms[Language.ENGLISH].items():
                if target_lang_code in translations:
                    # Case-insensitive replacement
                    pattern = re.compile(re.escape(eng_term), re.IGNORECASE)
                    translated = pattern.sub(translations[target_lang_code], translated)
        
        # Confidence is lower for offline (rule-based)
        confidence = 0.60
        return translated, confidence
    
    @staticmethod
    def translate_query_to_english(
        query: str,
        source_lang: Language
    ) -> Tuple[str, float]:
        """Translate query to English for processing"""
        handler = TranslationHandler()
        return handler.translate(query, source_lang, Language.ENGLISH)
    
    @staticmethod
    def translate_response_to_language(
        response: str,
        target_lang: Language
    ) -> Tuple[str, float]:
        """Translate response to target language for display"""
        if target_lang == Language.ENGLISH:
            return response, 1.0
        
        handler = TranslationHandler()
        return handler.translate(response, Language.ENGLISH, target_lang)


# ============================================================================
# MULTILINGUAL EMBEDDINGS
# ============================================================================

class MultilingualEmbedder:
    """Generate embeddings for multiple languages using IndicBERT"""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize multilingual embedder
        
        Args:
            model_name: HuggingFace model name
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = None
        
        if TRANSFORMERS_AVAILABLE:
            self._load_model()
    
    def _load_model(self) -> None:
        """Load tokenizer and model"""
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
            self.model.eval()
            logger.info(f"Loaded multilingual model on {self.device}")
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            TRANSFORMERS_AVAILABLE = False
    
    def embed(self, text: str, language: Language) -> Optional[List[float]]:
        """
        Generate embedding for multilingual text
        
        Args:
            text: Text to embed
            language: Language of text
        
        Returns:
            Embedding vector or None
        """
        if not TRANSFORMERS_AVAILABLE or not self.model:
            logger.warning("Transformers not available, using fallback embedding")
            return self._fallback_embedding(text)
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate embedding
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1)
            
            # Normalize
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            return embeddings[0].cpu().numpy().tolist()
        
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return self._fallback_embedding(text)
    
    @staticmethod
    def _fallback_embedding(text: str) -> List[float]:
        """Simple fallback embedding (production should use proper model)"""
        # Hash-based simple embedding (384-dimensional to match main embedder)
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        embedding = []
        for i in range(384):
            embedding.append(float((hash_int >> i) & 1))
        
        return embedding


# ============================================================================
# MULTILINGUAL QUERY PROCESSOR
# ============================================================================

class MultilingualQueryProcessor:
    """Process queries in multiple languages"""
    
    def __init__(self):
        """Initialize query processor"""
        self.detector = LanguageDetector()
        self.translator = TranslationHandler()
        self.embedder = MultilingualEmbedder()
    
    def process_query(self, query: str) -> MultilingualQuery:
        """
        Process input query in any language and convert to English
        
        Args:
            query: Input query in any language
        
        Returns:
            MultilingualQuery with English translation
        """
        # Detect language
        detected_lang, confidence = self.detector.detect(query)
        logger.info(f"Detected language: {detected_lang.name} (confidence: {confidence:.2f})")
        
        # Translate to English if needed
        if detected_lang == Language.ENGLISH:
            english_query = query
            translation_confidence = 1.0
        else:
            english_query, translation_confidence = self.translator.translate_query_to_english(
                query, detected_lang
            )
        
        # Identify query type
        query_type = self._identify_query_type(english_query)
        
        return MultilingualQuery(
            original_query=query,
            english_query=english_query,
            source_language=detected_lang,
            query_type=query_type
        )
    
    def process_response(
        self,
        response: str,
        target_language: Language,
        citations: List[str] = None,
        sources: List[Dict] = None
    ) -> MultilingualResponse:
        """
        Process response and translate to target language
        
        Args:
            response: English response text
            target_language: Target language for response
            citations: List of citations
            sources: List of source documents
        
        Returns:
            MultilingualResponse with translated text
        """
        # Translate response
        if target_language == Language.ENGLISH:
            translated_response = response
            translation_confidence = 1.0
        else:
            translated_response, translation_confidence = self.translator.translate_response_to_language(
                response, target_language
            )
        
        return MultilingualResponse(
            english_response=response,
            translated_response=translated_response,
            source_language=Language.ENGLISH,
            target_language=target_language,
            citations=citations or [],
            sources=sources or []
        )
    
    @staticmethod
    def _identify_query_type(query: str) -> str:
        """Identify type of legal query"""
        query_lower = query.lower()
        
        keywords = {
            "ipc_section": ["section", "ipc", "धारा", "பிரிவு"],
            "case_law": ["case", "verdict", "judgment", "मामला", "வழக்கு"],
            "act_inquiry": ["act", "law", "legislation", "कानून", "சட்டம்"],
            "punishment": ["punishment", "sentence", "penalty", "सजा", "தண்டனை"],
            "bail": ["bail", "release", "जमानत", "பிணையம்"],
            "process": ["procedure", "process", "how to", "कैसे", "எவ்வாறு"],
        }
        
        for query_type, keywords_list in keywords.items():
            if any(kw in query_lower for kw in keywords_list):
                return query_type
        
        return "general_inquiry"


# ============================================================================
# UNIFIED MULTILINGUAL INTERFACE
# ============================================================================

class MultilingualAssistant:
    """Unified interface for multilingual legal assistance"""
    
    def __init__(self, rag_chain):
        """
        Initialize multilingual assistant
        
        Args:
            rag_chain: LegalRAGChain instance
        """
        self.rag_chain = rag_chain
        self.query_processor = MultilingualQueryProcessor()
        self.embedder = MultilingualEmbedder()
    
    def query(
        self,
        question: str,
        target_language: Language = Language.ENGLISH,
        top_k: int = 5
    ) -> MultilingualResponse:
        """
        Query system in any language and get response in desired language
        
        Args:
            question: Question in any language
            target_language: Desired language for response
            top_k: Number of sources to retrieve
        
        Returns:
            MultilingualResponse with translated answer
        """
        # Process input query
        processed_query = self.query_processor.process_query(question)
        logger.info(f"Query type: {processed_query.query_type}")
        
        # Get answer from RAG chain (in English)
        english_answer = self.rag_chain.query(
            question=processed_query.english_query,
            top_k=top_k
        )
        
        # Process response for target language
        response = self.query_processor.process_response(
            response=english_answer.answer,
            target_language=target_language,
            citations=english_answer.citations,
            sources=english_answer.sources
        )
        
        return response


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_supported_languages() -> Dict[str, str]:
    """Get list of supported languages"""
    return {
        "en": "English",
        "hi": "हिंदी (Hindi)",
        "ta": "தமிழ் (Tamil)"
    }


def auto_detect_and_process(query: str) -> Tuple[str, Language]:
    """Auto-detect language and return detection info"""
    detector = LanguageDetector()
    lang, confidence = detector.detect(query)
    return lang.name, confidence


if __name__ == "__main__":
    # Test language detection
    test_queries = [
        "What is Section 302 IPC?",
        "आईपीसी की धारा 302 क्या है?",
        "IPC பிரிவு 302 என்ன?"
    ]
    
    for query in test_queries:
        lang, conf = auto_detect_and_process(query)
        print(f"Query: {query}")
        print(f"Language: {lang} (confidence: {conf:.2%})\n")
