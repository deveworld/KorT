from enum import Enum


class PromptTask(Enum):
    """Enum for prompt tasks. Key is the task name, value is the task description."""

    TRANSLATE = "translate"  # Translate text
    EVALUATE = "evaluate"  # Evaluate translation


PROMPTS: dict[PromptTask, str] = {}

PROMPTS[
    PromptTask.TRANSLATE
] = """You are a professional translator with expertise in multiple languages and cultures. Your task is to translate the given text accurately, preserving its meaning, tone, and cultural nuances. Translate immediately and output only the translation, without any additional analysis or explanations.

Here is the source language:
<source_language>
{source_lang}
</source_language>

Here is the target language:
<target_language>
{target_lang}
</target_language>

Here is the text to translate:
<source_text>
{text}
</source_text>

Translation Instructions:
1. Translate the text accurately, maintaining the original meaning and tone.
2. Adapt idiomatic expressions and cultural references for the target language and culture as needed.
3. Keep the original formatting (paragraphs, line breaks, punctuation) unless target language conventions require changes.
4. For terms without direct equivalents, provide the best translation.

Then, provide only the translation as your output, without any additional tags or explanations.

Begin your translation now.
"""


PROMPTS[
    PromptTask.EVALUATE
] = """You are a professional translation evaluator tasked with assessing the quality of a translation. Your evaluation will be based on five criteria: Accuracy, Fluency, Terminology, Style, and Cultural Adaptation.

Here is the original text in the source language:
<source_text>
{source_text}
</source_text>

Here is the translation to be evaluated:
<translation_text>
{translation_text}
</translation_text>

For reference, here is a professional translation of the same text:
<reference_translation>
{reference_translation}
</reference_translation>

The source language is:
<source_lang>
{source_lang}
</source_lang>

The target language is:
<target_lang>
{target_lang}
</target_lang>

Instructions:
1. Carefully read the source text, the translation to be evaluated, and the reference translation.
2. In your analysis, consider each of the five criteria:
   - Accuracy: How well does the translation convey the meaning of the original text?
   - Fluency: How natural and idiomatic is the language used in the translation?
   - Terminology: How appropriate and consistent is the use of specialized terms?
   - Style: How well does the translation maintain the tone and style of the original text?
   - Cultural Adaptation: How well does the translation account for cultural differences?
3. Decide the overall quality score (up to 100).
4. Output only the final overall quality score.

Before providing your final score, wrap your evaluation process in <translation_evaluation> tags inside your thinking block. For each criterion:
- Write down key phrases or sentences from each text that are relevant to the criterion.
- Consider both positive and negative aspects of the translation for this criterion.
- Justify your score for this criterion based on your analysis.

Then, outside of the thinking block, provide the final score in <score> tags.
Your final output should consist only of the score and should not duplicate or rehash any of the work you did in the thinking block.
Example output structure:
<score>
[Final overall quality score between 0 and 100]
</score>

Remember, the score distribution is not fixed. Rate the translation as you see fit, being particularly critical of any strange or awkward elements. Even minor issues should result in significant score reductions.

Then, start your evaluation now.
"""

CUSTOM_PROMPTS = {
    "gugugo": "### {source_lang_korean}: {text}</끝>\n### {target_lang_korean}: ",
    "gemago": "{source_lang_english}:\n{text}\n\n{target_lang_english}:\n",
}
