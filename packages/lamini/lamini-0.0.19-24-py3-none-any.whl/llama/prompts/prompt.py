from abc import ABCMeta, abstractmethod
from typing import List
from llama import Type
import re

from llama.types.type import Type


class BasePrompt(object, metaclass=ABCMeta):
    prompt_template = ""

    input_template = ""

    def input_to_str(self, input: Type):
        input_dict = input.dict()
        input_schema = input.schema()
        input_str = ""
        properties = input_schema.get("properties")
        for i, key in enumerate(properties):
            prop_info = properties.get(key)
            hydrated_input_template = self.input_template
            x = re.search(r"{#field}", hydrated_input_template)
            if x is not None:
                entire_match = x.group(0)
                hydrated_input_template = hydrated_input_template.replace(
                    entire_match, key
                )
            x = re.search(r"{#context}", hydrated_input_template)
            if x is not None:
                entire_match = x.group(0)
                hydrated_input_template = hydrated_input_template.replace(
                    entire_match, prop_info.get("description", "")
                )
            x = re.search(r"{#value}", hydrated_input_template)
            if x is not None:
                entire_match = x.group(0)
                hydrated_input_template = hydrated_input_template.replace(
                    entire_match, str(input_dict.get(key))
                )
            input_str += hydrated_input_template
            if i < len(properties) - 1:
                input_str += "\n"
        return str(input_str)

    def output_to_str(self, output_type: type):
        output_dict = output_type.schema()
        output_str = ""
        properties = output_dict.get("properties")
        for i, key in enumerate(properties):
            prop_info = properties.get(key)
            output_str += key + f' ({prop_info.get("description", "")}), after "{key}:"'
            if i < len(properties) - 1:
                output_str += "\n"
        return output_str

    def cue_to_str(self, cue_type: type):
        cue_dict = cue_type.schema()
        cue_str = ""
        properties = cue_dict.get("properties")
        for key, prop_info in properties.items():
            cue_str += key + ": "
            break
        return cue_str

    def construct_prompt(
        self,
        input: Type,
        output_type: type,
    ) -> str:
        # Validate that input type matches prompt template
        # Validate that output type matches output prompt template
        # Validate that cue type batches output prompt template

        # Substitute input into prompt template
        hydrated_prompt = self.prompt_template
        x = re.search(r"{#input\((\w+)\)}", hydrated_prompt)
        if x is not None:
            entire_match = x.group(0)
            group_match = x.group(1)
            input_string = self.input_to_str(input)
            hydrated_prompt = hydrated_prompt.replace(entire_match, f"{input_string}")
        # Substitute output into output prompt template
        x = re.search(r"{#output\((\w+)\)}", hydrated_prompt)
        if x is not None:
            entire_match = x.group(0)
            group_match = x.group(1)
            output_string = self.output_to_str(output_type)
            hydrated_prompt = hydrated_prompt.replace(entire_match, f"{output_string}")
        # Substitute cue into cue prompt template
        x = re.search(r"{#cue\((\w+)\)}", hydrated_prompt)
        if x is not None:
            entire_match = x.group(0)
            group_match = x.group(1)
            cue_string = self.cue_to_str(output_type)
            hydrated_prompt = hydrated_prompt.replace(entire_match, f"{cue_string}")

        return hydrated_prompt
