import os
from typing import List, Any
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

class Agent:
    """
    Base class for creating prompt-driven agents.

    :param prompt_template: Template string for the prompt.
    :param input_variables: List of input variable names for the prompt template.
    :param output_model: A Pydantic model defining the structured output schema.
    :param model: Name of the model to be used.
    """
    def __init__(
        self,
        prompt_template: str,
        input_variables: List[str],
        output_model: BaseModel = None,
        model = os.environ["MODEL"],
    ) -> None:
        self.model = ChatOpenAI(model=model) if output_model is None else ChatOpenAI(model=model).with_structured_output(output_model)
        self.prompt = PromptTemplate(template=prompt_template, input_variables=input_variables)
        # Pre-build the chain so we don’t have to reconstruct it each time.
        self.chain = self.prompt | self.model

    def generate_output(self, **input_data: Any) -> Any:
        """
        Invokes the prompt-model chain with the given input data and returns the structured output.
        """
        return self.chain.invoke(input_data)
