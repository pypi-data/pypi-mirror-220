import logging
from llama.prompts.prompt import BasePrompt

logger = logging.getLogger(__name__)


class GeneralPrompt(BasePrompt):
    prompt_template = """Given:
{#input(Question)}
Generate:
{#output(Answer)}
{#cue(Answer)}"""

    input_template = "{#field} ({#context}): {#value}"
