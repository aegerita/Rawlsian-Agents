from typing import List
from langchain.output_parsers import MarkdownListOutputParser


from fairplay.agents.base_agent import Agent


CLAIMS_PROCESSOR_PROMPT = r"""
You are a legal clerk that will receive free text detailing material conditions, concerns and objectives from a client.
Your task is to identify and extract relevant, specific and actionable claims from the text and format them in a factual,
depersonalized bullet list. Focus on claims that provide clear, concrete information about the client's assets, liabilities,
and specific desires for the agreement. Avoid including general statements or broad concerns that lack specificity.

EXAMPLE:

Free text:
You are Person A who tries to negotiate a prenuptial agreement 
with your partner. You want to make sure that you are satisfied
with the agreement. You have a yearly income of $100,000 and 
you own a house that is worth $500,000. You have a savings 
account with $50,000. You want to make sure that you keep your 
house and your savings account in case of a divorce. You want 
to be able to make sure that the share account is invested 
with care so that your saving grows. In the event of your 
parents pass away, you do not want to share their inheritance 
with your partner. You have to make sure all of your concerns 
are addressed before you say that.

Extracted claims:

- Person A has a yearly income of $100,000.
- Person A owns a house worth $500,000 and wants to keep it in case of a divorce.
- Person A has a savings account with $50,000 and wants to keep it in case of a divorce.
- Person A wants to ensure that the shared account is invested carefully to grow their savings.
- In the event of Person A's parents' passing, Person A does not want to share their inheritance with their partner.

Solve the task using only the information below:

Free text:
{free_text}

"""

class ClaimsProcessor(Agent):  
    def __init__(self) -> None:
        super().__init__(
            prompt_template=CLAIMS_PROCESSOR_PROMPT,
            input_variables=["free_text"],
            output_parser=MarkdownListOutputParser(),
        )
        self.free_text = ""
        

    def load_free_text(self, free_text: str):
        self.free_text = free_text

    def process_claims(self) -> List[str]:
        return self.generate_output(free_text = self.free_text)
