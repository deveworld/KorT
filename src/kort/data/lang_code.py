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

    def to_korean(self):
        """Convert the language code to Korean."""
        return {
            LangCode.ENG: "영어",
            LangCode.RUS: "러시아어",
            LangCode.ZHO: "중국어(간체)",
            LangCode.JPN: "일본어",
            LangCode.KOR: "한국어",
        }[self]

    def to_english(self):
        """Convert the language code to English."""
        return {
            LangCode.ENG: "English",
            LangCode.RUS: "Russian",
            LangCode.ZHO: "Chinese (Simplified)",
            LangCode.JPN: "Japanese",
            LangCode.KOR: "Korean",
        }[self]
