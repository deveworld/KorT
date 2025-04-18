from enum import Enum


class LangCode(Enum):
    """Enum for language codes. Key is ISO 639-3, value is ISO 639-2."""

    ENG = "en"  # English
    RUS = "ru"  # Russian
    ZHO = "zh"  # Chinese (Simplified)
    JPN = "ja"  # Japanese
    KOR = "ko"  # Korean

    def to_iso639_3(self):
        """Convert the language code to ISO 639-3 format."""
        return self.name.lower()

    def to_iso639_2(self):
        """Convert the language code to ISO 639-2 format."""
        return str(self.value).lower()
