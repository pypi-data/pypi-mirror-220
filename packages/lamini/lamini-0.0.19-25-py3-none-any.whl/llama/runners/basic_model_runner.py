from typing import List, Union
from llama import Type, Context, LLMEngine
import jsonlines
import pandas as pd

from llama.prompts.blank_prompt import BlankPrompt

class Input(Type):
    input: str = Context("input")

class Output(Type):
    output: str = Context("output")

class BasicModelRunner:
    """A class for running and training a model with a blank prompt (string in, string out)"""

    def __init__(self, model_name: str = "EleutherAI/pythia-410m-deduped", config={}):
        self.model_name = model_name
        self.llm = LLMEngine("basic_model_runner", model_name=model_name, config=config)
        self.prompt = BlankPrompt()
        self.job_id = None
        self.data = []

    def __call__(self, inputs: Union[str, List[str]]) -> str:
        """Call the model runner on prompt"""
        # output = self.llm(self.prompt.input(input=input_string), self.prompt.output)
        if isinstance(inputs, list):
            print("Running batch job on %d number of inputs" % len(inputs))
            input_objects = [Input(input=i) for i in inputs]
        else:
            # Singleton
            input_objects = Input(input=inputs)
        output_objects = self.llm(
            input=input_objects,
            output_type=Output,
            model_name=self.model_name,
        )
        if isinstance(output_objects, list):
            outputs = [o.output for o in output_objects]
            return [{"input": i, "output": o} for i, o in zip(inputs, outputs)]
        else:
            return output_objects.output

    def load_data(self, data):
        """
        Load a list of json objects with input-output keys into the LLM
        Each object must have 'input' and 'output' as keys.
        """
        try:
            input_output_objects = [
                [Input(input=d["input"]), Output(output=d["output"])]
                for d in data
            ]
        except KeyError:
            raise ValueError("Each object must have 'input' and 'output' as keys")
        self.data.extend(input_output_objects)

    def load_data_from_jsonlines(self, file_path: str):
        """
        Load a jsonlines file with input output keys into the LLM.
        Each line must be a json object with 'input' and 'output' as keys.
        """
        data = []
        with open(file_path) as dataset_file:
            reader = jsonlines.Reader(dataset_file)
            data = list(reader)
        self.load_data(data)

    def load_data_from_dataframe(self, df: pd.DataFrame):
        """
        Load a pandas dataframe with input output keys into the LLM.
        Each row must have 'input' and 'output' as keys.
        """
        try:
            for _, row in df.iterrows():
                self.data.append(
                    [Input(question=row["input"]), Output(answer=row["output"])]
                )
        except KeyError:
            raise ValueError("Each object must have 'input' and 'output' as keys")

    def load_data_from_csv(self, file_path: str):
        """
        Load a csv file with input output keys into the LLM.
        Each row must have 'input' and 'output' as keys.
        """
        df = pd.read_csv(file_path)
        self.load_data_from_dataframe(df)

    def clear_data(self):
        """Clear the data from the LLM"""
        self.llm.clear_data()
        self.data = []

    def train(
        self,
        verbose: bool = False,
        finetune_args={},
        limit=500
    ):
        """
        Train the LLM on added data. This function blocks until training is complete.
        """
        if len(self.data) < 10:
            raise Exception("Submit at least 10 data pairs to train")
        if len(self.data) > limit:
            data = self.data[:limit]
        else:
            data = self.data
        self.llm.save_data(data)

        final_status = self.llm.train(
            verbose=verbose,
            finetune_args=finetune_args
        )
        try:
            self.model_name = final_status["model_name"]
            self.job_id = final_status["job_id"]
            self.llm = LLMEngine("question_answer_runner", model_name=self.model_name)
            self.llm.clear_data()
        except KeyError:
            raise Exception("Training failed")

    def get_eval_results(self) -> List:
        """Get evaluation results"""
        if self.job_id is None:
            raise Exception("Must train before getting results")
        return self.llm.eval(self.job_id)
