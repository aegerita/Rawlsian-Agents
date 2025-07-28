from typing import List
from langchain.output_parsers import MarkdownListOutputParser

from rawlsian_agents.agents.base_agent import Agent


class ClaimsProcessor(Agent):  
    def __init__(self, prompt_template: dict) -> None:
        super().__init__(
            prompt_template=prompt_template["claims_processor"],
            input_variables=["free_text"],
            output_parser=MarkdownListOutputParser(),
        )
        self.free_text = ""
        

    def load_free_text(self, free_text: str):
        self.free_text = free_text

    def process_claims(self) -> List[str]:
        return self.generate_output(free_text = self.free_text)
