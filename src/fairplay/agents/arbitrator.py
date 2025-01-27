
from fairplay.agents.base_agent import Agent
from fairplay.models import Clauses

PROMPT = r"""
You have a detailed prenuptial agreement that outlines the specific terms and conditions both parties have agreed upon. One of the clients has raised a concern about a potential future risk that could have serious implications for both individuals. If necessary, suggest adding specific clauses to the agreement that address this identified risk and help prevent any negative consequences. It is essential not to repeat any clauses that are already included in the agreement or to introduce any redundant clauses. In the case that the risk is sufficiently resolved by the agreement, return nothing in the list of clauses. Be clear and concise in your language to ensure understanding. 

You should analyze this situation using John Rawls' concept of the "veil of ignorance," which highlights the importance of fairness and an unbiased perspective in decision-making. It is vital to thoroughly assess ethical considerations to ensure that the proposed solution benefits both clients involved in this prenuptial agreement.

Current clauses for the prenuptial agreement:
{clauses}

The identified risk:
{risk}
"""


class Arbitrator(Agent):
    """
    An agent specialized in analyzing and proposing clauses for identified risks.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["clauses", "risk"],
            output_model=Clauses,
        )

    def propose_clause(self, clauses: str, risk: str) -> Clauses:
        """
        Analyzes risks and proposes clauses given existing clauses and a risk.

        :param clauses: The clauses or terms to be considered or enhanced.
        :param risk: The specific risk scenario to analyze.
        :return: A structured output conforming to the `CLAUSES` Pydantic model.
        """
        return self.generate_output(clauses=clauses, risk=risk).clauses
