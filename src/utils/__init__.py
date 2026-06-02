"""Utility functions for citation tracking, multilingual support, etc."""

try:
    from .citation_tracker import (
        CitationExtractor,
        CitationFormatter,
        CitationLinker,
        Citation,
        CitationType,
    )
except Exception:
    CitationExtractor = None
    CitationFormatter = None
    CitationLinker = None
    Citation = None
    CitationType = None

try:
    from .multilingual_support import (
        Language,
        TranslationEngine,
        LanguageDetector,
        TranslationHandler,
        MultilingualEmbedder,
        MultilingualQueryProcessor,
        MultilingualAssistant,
        LanguageResult,
        MultilingualQuery,
        MultilingualResponse,
        get_supported_languages,
        auto_detect_and_process,
    )
except Exception:
    Language = None
    TranslationEngine = None
    LanguageDetector = None
    TranslationHandler = None
    MultilingualEmbedder = None
    MultilingualQueryProcessor = None
    MultilingualAssistant = None
    LanguageResult = None
    MultilingualQuery = None
    MultilingualResponse = None
    get_supported_languages = None
    auto_detect_and_process = None

__all__ = [
    # Citation tracking
    "CitationExtractor",
    "CitationFormatter",
    "CitationLinker",
    "Citation",
    "CitationType",
    # Multilingual support
    "Language",
    "TranslationEngine",
    "LanguageDetector",
    "TranslationHandler",
    "MultilingualEmbedder",
    "MultilingualQueryProcessor",
    "MultilingualAssistant",
    "LanguageResult",
    "MultilingualQuery",
    "MultilingualResponse",
    "get_supported_languages",
    "auto_detect_and_process",
]
