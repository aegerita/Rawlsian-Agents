from typing import List
from langchain.output_parsers import MarkdownListOutputParser


from rawlsian_agents.agents.base_agent import Agent


CLAIMS_PROCESSOR_PROMPT = r"""
You are a legal clerk tasked with reviewing free-text inputs from clients detailing their material conditions, specific concerns, and objectives for a legal agreement.

Your responsibility is to identify and extract relevant, specific, and actionable claims from the provided text. Format these extracted claims into a clear, factual, and depersonalized bullet-point list. Prioritize claims that explicitly detail concrete information about the client's assets, liabilities, and distinct objectives for the agreement. Avoid general statements or broad concerns that lack specificity or actionable clarity.

If there exists any direct quotes or specific numerical values in the text, ensure these are accurately transcribed into the extracted claims and stay in quotes. Maintain a neutral and professional tone throughout the claims extraction process, focusing solely on the factual content provided in the text.

**Example:**

Free text:
You are Person A negotiating a prenuptial agreement with your partner. You have a yearly income of $100,000, own a house worth $500,000, and possess a savings account containing $50,000. You wish to retain sole ownership of your house and savings account in the event of a divorce. Additionally, you want to ensure shared financial accounts are carefully managed to protect and grow your savings. You do not wish to share any future inheritance from your parents with your partner.

Extracted claims:

- Person A has a yearly income of $100,000.
- Person A owns a house valued at $500,000 and wishes to retain ownership in case of divorce.
- Person A holds a savings account with $50,000 and desires exclusive ownership in case of divorce.
- Person A requires shared financial accounts to be carefully managed to ensure savings growth.
- Person A intends not to share future inheritance from parents with their partner.

Solve the task using only the information provided below:

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
