# KorT (Korean Translation) - Comprehensive Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Installation and Setup](#installation-and-setup)
5. [Usage Guide](#usage-guide)
6. [Development](#development)
7. [API Reference](#api-reference)
8. [Data Format](#data-format)
9. [Extending KorT](#extending-kort)

## Project Overview

KorT (Korean Translation) is a comprehensive benchmark and evaluation framework for Korean-English translation quality assessment using Large Language Models (LLMs) as judges. The project aims to provide quantitative evaluation metrics for translation services by leveraging the advanced language understanding capabilities of modern LLMs.

### Key Features
- **LLM-as-a-Judge Paradigm**: Uses state-of-the-art language models to evaluate translation quality
- **Comprehensive Test Suite**: Includes challenging translation examples across multiple categories
- **Multi-Provider Support**: Integrates with various translation APIs and language models
- **Batch Processing**: Supports batch API operations for efficient large-scale evaluation
- **Leaderboard System**: Provides comparative rankings of translation services
- **Extensible Architecture**: Easy to add new models, translators, and evaluation criteria

### Background
The project addresses the limitations of traditional translation evaluation metrics like BLEU, which struggle to capture nuanced linguistic elements such as idioms, cultural references, and contextual appropriateness. KorT provides a more sophisticated evaluation system that correlates better with human judgment.

## Architecture

### System Architecture

```
KorT
├── Data Layer (src/kort/data/)
│   ├── Evaluation Data (EVAL_DATA)
│   ├── Generation Examples
│   └── Language Codes
├── Model Layer (src/kort/models/)
│   ├── Base Model Interface
│   ├── API Models (OpenAI, Anthropic, Google)
│   ├── Local Models (Transformers)
│   └── Batch Processing Models
├── Translation Layer (src/kort/translators/)
│   ├── Base Translator Interface
│   ├── Free Services (Papago, Google, Kakao)
│   ├── Paid APIs (DeepL)
│   └── Model-based Translation
├── Evaluation Layer (src/kort/evaluators/)
│   ├── Base Evaluator Interface
│   ├── Model-based Evaluation
│   └── Human Evaluation Support
├── Presentation Layer (src/kort/leaderboards/)
│   ├── Text Output
│   └── Web Interface (Gradio)
└── Utilities (src/kort/utils/)
    ├── Exception Handling
    ├── Retry Logic
    └── Import Management
```

### Design Principles
1. **Modularity**: Each component is independent and replaceable
2. **Abstraction**: Common interfaces for models, translators, and evaluators
3. **Lazy Loading**: Components are loaded only when needed for performance
4. **Error Resilience**: Built-in retry mechanisms and error handling
5. **Configuration Management**: Centralized configuration with environment variable support

## Core Components

### 1. Data Module (`src/kort/data/`)

#### Evaluation Data (`generate.py`)
- **Categories**: Idioms/Proverbs, Wordplay/Puns, Cultural References, Slang, Literary Allusions
- **Languages**: Korean (KOR) and English (ENG)
- **Structure**: Dictionary mapping language codes to categories to examples
- **Example Format**: Source text with reference translations

#### Data Models
- `GenerationExample`: Represents a single translation example
- `Generated`: Collection of translation results with metadata
- `EvaluationResult`: Score and details for a single evaluation
- `Evaluated`: Complete evaluation results with statistics

### 2. Models Module (`src/kort/models/`)

#### Base Model (`base_model.py`)
Abstract base class providing:
- API key management
- Error retry logic
- Safe inference wrapper
- Device configuration for local models

#### Supported Models
- **OpenAI**: GPT series models via OpenAI API
- **Anthropic**: Claude models via Anthropic API
- **Google**: Gemini models via Google API
- **Transformers**: Local models via Hugging Face Transformers
- **Custom Models**: Gugugo (Korean-English), Gemago (Korean-multilingual)

#### Batch Processing
Special batch model implementations for:
- OpenAI Batch API
- Anthropic Batch API

### 3. Translators Module (`src/kort/translators/`)

#### Base Translator (`base_translator.py`)
Abstract interface for translation services:
- Language pair specification
- Error handling and retry logic
- Safe translation wrapper

#### Translation Services
- **Free Services**:
  - PapagoFree: Naver Papago unofficial API
  - GoogleFree: Google Translate unofficial API
  - KakaoFree: Kakao Translate unofficial API
- **Paid APIs**:
  - DeepL API: Official DeepL translation service
  - DeepL Free: Limited free tier
- **Model-based**: Uses language models for translation

### 4. Evaluators Module (`src/kort/evaluators/`)

#### Evaluation Process
1. Takes generated translation and reference translation
2. Applies evaluation prompt to LLM judge
3. Considers five criteria:
   - Accuracy: Meaning preservation
   - Fluency: Natural language flow
   - Terminology: Consistent term usage
   - Style: Tone and register maintenance
   - Cultural Adaptation: Appropriate localization
4. Returns score (0-100)

#### Evaluator Types
- **Model-based**: Uses LLMs for evaluation
- **Batch**: Processes multiple evaluations in batch
- **Human**: Interface for human evaluation (future)

### 5. Leaderboard Module (`src/kort/leaderboards/`)

#### Display Options
- **Text Leaderboard**: Console output with formatted tables
- **Web Leaderboard**: Interactive Gradio interface
- Displays average scores, category breakdowns, and rankings

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- Optional: CUDA-capable GPU for local models

### Installation Methods

#### 1. From PyPI
```bash
# Full installation with local model support
pip install -U kort-cli[all]

# Minimal installation (API-based only)
pip install -U kort-cli
```

#### 2. From Source
```bash
git clone https://github.com/deveworld/kort
cd kort
pip install .[all]  # or pip install . for minimal
```

#### 3. Using uvx (no installation)
```bash
uvx kort-cli
```

### Configuration

#### Environment Variables
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
export DEEPL_API_KEY="..."
```

#### Configuration File
The system uses dataclasses for configuration:
- `APIConfig`: API keys and endpoints
- `EvaluationConfig`: Retry settings, timeouts, token limits
- `TranslationConfig`: Translation-specific settings

## Usage Guide

### 1. Generate Translations

#### List Available Translators
```bash
python -m kort.scripts.generate -l
```

#### Generate with Free Translator
```bash
python -m kort.scripts.generate -t papagofree
```

#### Generate with API Model
```bash
python -m kort.scripts.generate \
    -t openai \
    -n gpt-4-mini \
    --api_key sk-xxx
```

#### Generate with Local Model
```bash
python -m kort.scripts.generate \
    -t gugugo \
    -n squarelike/Gugugo-koen-7B-V1.1 \
    -d cuda
```

### 2. Evaluate Translations

#### List Available Evaluators
```bash
python -m kort.scripts.evaluate -l
```

#### Run Evaluation
```bash
python -m kort.scripts.evaluate \
    -t gemini \
    -n gemini-2.0-pro-preview-0325 \
    --api_key AIzaxxx \
    --input generated/openai_gpt-4-mini.json
```

### 3. Batch Evaluation

#### Submit Batch Job
```bash
python -m kort.scripts.eval_batch \
    -t claudebatch \
    -n claude-3-5-sonnet-20241022 \
    --api_key sk-ant-api03-xxx \
    --input generated/openai_gpt-4-mini.json
```

#### Retrieve Batch Results
```bash
python -m kort.scripts.eval_batch \
    -t claudebatch \
    -n claude-3-5-sonnet-20241022 \
    --api_key sk-ant-api03-xxx \
    --input generated/openai_gpt-4-mini.json \
    --job_id msgbatch_xxx
```

### 4. View Leaderboard

#### Web Interface
```bash
python -m kort.scripts.leaderboard
# Opens browser at http://localhost:7860
```

#### Text Output
```bash
python -m kort.scripts.leaderboard -t
```

## Development

### Project Structure
```
KorT/
├── src/kort/           # Main package
├── pyproject.toml      # Project configuration
├── Makefile           # Development commands
├── uv.lock            # Dependency lock file
└── CLAUDE.md          # Development instructions
```

### Development Commands

#### Code Formatting
```bash
make format  # Runs ruff format
```

#### Code Checking
```bash
make check   # Runs ruff, type checking, and pyrefly
```

#### Testing
```bash
make test    # Runs pytest
```

#### Generate Requirements
```bash
make requirements  # Exports requirements.txt
```

### Development Workflow
1. Follow TDD principles (Red → Green → Refactor)
2. Write tests first for new features
3. Implement minimal code to pass tests
4. Refactor only when tests pass
5. Separate structural and behavioral changes
6. Commit only when all tests pass

## API Reference

### BaseModel Class
```python
class BaseModel(ABC):
    def __init__(self, api_key: Optional[str] = None, 
                 evaluation: bool = False,
                 device: Optional[str] = None,
                 stop: Optional[str] = None)
    
    @abstractmethod
    def inference(self, input: str) -> str
    
    def safe_inference(self, input: str) -> str
```

### BaseTranslator Class
```python
class BaseTranslator(ABC):
    def __init__(self, api_key: Optional[str] = None)
    
    @abstractmethod
    def translate(self, text: str, 
                 source_lang: LangCode, 
                 target_lang: LangCode) -> str
    
    def safe_translate(self, text: str,
                      source_lang: LangCode,
                      target_lang: LangCode) -> str
```

### Data Models
```python
class GenerationExample(BaseModel):
    source: str
    translated: str
    source_lang: LangCode
    target_lang: LangCode
    category: Categories
    reference_translation: str
    
    def get_hash(self) -> str

class EvaluationResult(BaseModel):
    generated: GenerationExample
    score: float
```

## Data Format

### Input Format (EVAL_DATA)
```python
{
    LangCode.ENG: {
        Categories.IDIOM_PROVERB: [
            Example(
                source="You're barking up the wrong tree.",
                translation={
                    LangCode.KOR: "너 완전 헛다리 짚고 있는 거야."
                }
            )
        ]
    }
}
```

### Generated Output Format
```json
{
    "metadata": {
        "model_type": "openai",
        "model_name": "gpt-4",
        "model_org": "openai",
        "timestamp": "2024-01-01T00:00:00"
    },
    "generated_examples": [
        {
            "source": "Original text",
            "translated": "Translated text",
            "source_lang": "ENG",
            "target_lang": "KOR",
            "category": "IDIOM_PROVERB",
            "reference_translation": "Reference"
        }
    ]
}
```

### Evaluation Output Format
```json
{
    "metadata": {
        "eval_model_type": "anthropic",
        "eval_model_name": "claude-3-5-sonnet",
        "mean_score": 85.5,
        "timestamp": "2024-01-01T00:00:00"
    },
    "evaluation_results": [
        {
            "generated": {...},
            "score": 85.0
        }
    ]
}
```

## Extending KorT

### Adding a New Model

1. Create a new file in `src/kort/models/provider/`
2. Inherit from `BaseModel`:
```python
from ..base_model import BaseModel

class NewProviderModel(BaseModel):
    model_org: str = "newprovider"
    _need_api_key: bool = True
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        self.model_name = model_name
        super().__init__(api_key=api_key, **kwargs)
        # Initialize client
    
    def inference(self, input: str) -> str:
        # Implement inference logic
        pass
```

3. Register in `src/kort/models/__init__.py`

### Adding a New Translator

1. Create a new file in `src/kort/translators/provider/`
2. Inherit from `BaseTranslator`:
```python
from ..base_translator import BaseTranslator

class NewTranslator(BaseTranslator):
    translator_org: str = "newprovider"
    translator_name: str = "newservice"
    _need_api_key: bool = True
    
    def translate(self, text: str, source_lang: LangCode, target_lang: LangCode) -> str:
        # Implement translation logic
        pass
```

3. Register in `src/kort/translators/__init__.py`

### Adding New Evaluation Data

Edit `src/kort/data/generate.py`:
```python
EVAL_DATA[LangCode.ENG][Categories.NEW_CATEGORY] = [
    Example(
        source="New example text",
        translation={
            LangCode.KOR: "새로운 예제 텍스트"
        }
    )
]
```

### Custom Evaluation Prompts

Edit `src/kort/data/prompts.py`:
```python
CUSTOM_PROMPTS["new_model"] = "Custom prompt template with {variables}"
```

## Best Practices

### For Translation Generation
1. Use appropriate models for the task complexity
2. Consider API rate limits for large datasets
3. Save intermediate results frequently
4. Use batch APIs when available for efficiency

### For Evaluation
1. Use consistent evaluation models for fair comparison
2. Consider multiple evaluation runs for reliability
3. Document any custom prompts or modifications
4. Validate scores against human judgment periodically

### For Development
1. Follow the existing code structure and patterns
2. Add comprehensive docstrings to new components
3. Include type hints for all functions
4. Write tests for new functionality
5. Update documentation when adding features

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure environment variables are set or pass keys explicitly
2. **Model Not Found**: Check model name spelling and availability
3. **Out of Memory**: Use smaller batch sizes or CPU for local models
4. **Rate Limiting**: Implement delays between API calls or use batch APIs
5. **Import Errors**: Ensure all dependencies are installed (`pip install -e .[all]`)

### Debug Mode
Set environment variables for debugging:
```bash
export KORT_DEBUG=1
export KORT_LOG_LEVEL=DEBUG
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the Apache 2.0 License. See [LICENSE](LICENSE) for details.

## Contact

- **Author**: World (world@worldsw.dev)
- **GitHub**: https://github.com/deveworld/KorT
- **Issues**: https://github.com/deveworld/KorT/issues
- **Leaderboard**: https://kort.worldsw.dev

For model evaluation requests or questions, contact: world@worldsw.dev