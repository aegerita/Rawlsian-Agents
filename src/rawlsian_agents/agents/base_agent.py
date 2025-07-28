import os
from typing import List, Any
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.transform import BaseTransformOutputParser

load_dotenv()

class Agent:
    """
    Base class for creating prompt-driven agents.

    :param prompt_template: Template string for the prompt.
    :param input_variables: List of input variable names for the prompt template.
    :param output_model: A Pydantic model defining the structured output schema for JSON based answers.
    :param model: Name of the model to be used.
    :param output_parser: Output parser to be used for parsing the model output. Can be None. 
    """
    def __init__(
        self,
        prompt_template: str,
        input_variables: List[str],
        output_model: BaseModel = None,
        model = os.environ["MODEL"],
        output_parser: BaseTransformOutputParser = None,
    ) -> None:
        self.prompt_template = prompt_template
        self.input_variables = input_variables
        self.output_model = output_model
        self.model = ChatOpenAI(model=model) if self.output_model is None else ChatOpenAI(model=model).with_structured_output(self.output_model)
        self.output_parser = output_parser
        self.partial_variables = {}
        if output_parser is not None:
            self.output_parser = output_parser
            format_instructions = output_parser.get_format_instructions()
            self.partial_variables = {"format_instructions": format_instructions}
        self.set_prompt(
            prompt_template=self.prompt_template,
            input_variables=self.input_variables,
            partial_variables=self.partial_variables,
        )
        self.set_chain()
        

    def set_prompt(self, prompt_template: str, input_variables: List[str], partial_variables: dict) -> None:
        """
        Sets a new prompt template for the agent.

        :param prompt_template: The new prompt template string.
        :param input_variables: List of input variable names for the prompt template.
        :param partial_variables: Dictionary of partial variables for the prompt.
        :return: A PromptTemplate instance.
        """
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_variables,
            partial_variables=partial_variables,
        )
    
    def set_chain(self) -> None:
        """
        Pre-build the chain so we don’t have to reconstruct it each time.
        """
        if self.output_parser is not None:
            self.chain = self.prompt | self.model | self.output_parser
        else:
            self.chain = self.prompt | self.model
            

    def generate_output(self, **input_data: Any) -> Any:
        """
        Invokes the prompt-model chain with the given input data and returns the structured output.
        """
        return self.chain.invoke(input_data)
