from fairplay.agents.base_agent import Agent
from fairplay.models import Arbitration

PROMPT = r"""
You have a detailed prenuptial agreement that outlines the specific terms and conditions both parties have agreed upon. One of the clients has raised a concern about a potential future risk that could have serious implications for both individuals. Your task is to assess this risk comprehensively and, if necessary, suggest specific claims or strategies to mitigate it. 

Power imbalances in prenuptial agreements can arise from financial disparities, emotional leverage, legal knowledge gaps, or external influences such as family pressure. Consider how these factors may affect fairness over time. 

To ensure a well-rounded analysis, evaluate the risk from multiple perspectives:

Legal & Financial: Could disparities in financial knowledge or access to legal counsel create an unfair advantage for one party?
Emotional & Psychological: Is there potential for emotional coercion, implicit pressure, or fear of retaliation to impact decision-making?
Social & External Influences: Could external factors, such as family expectations or social norms, introduce additional power imbalances?
Adaptive Solutions: How can the agreement remain fair over time, even if circumstances change (e.g., one party’s financial situation improves, a legal loophole is discovered, or a major life event occurs)?
For each identified risk, propose specific contractual clauses or safeguards that can prevent power imbalances, promote fairness, and ensure ethical negotiation. If necessary, suggest counterfactual scenarios—what happens if one party refuses mediation, exploits financial disclosure, or challenges the fairness of the agreement?

Your response should align with John Rawls' concept of the "veil of ignorance", ensuring fairness is upheld regardless of either party’s status. 

Then, for each identified risk, propose one edit to the current contractual clauses or safeguards that can prevent power imbalances, promote fairness, and ensure ethical negotiation. If the risk is already sufficiently addressed in the existing agreement, return nothing in the list of claims. Be clear and concise in your language to ensure understanding. The edit must be summarized in a single sentence. Updating existing clauses is strongly preferred over adding new ones.

Current claims for the prenuptial agreement:
{claims}

The identified risk:
{risk}
"""


class Arbitrator(Agent):
    """
    An agent specialized in analyzing and proposing claims for identified risks.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=PROMPT,
            input_variables=["claims", "risk"],
            output_model=Arbitration,
        )

    def propose_clause(self, claims: str, risk: str) -> Arbitration:
        """
        Analyzes risks and proposes claims given existing claims and a risk.

        :param claims: The claims or terms to be considered or enhanced.
        :param risk: The specific risk scenario to analyze.
        :return: A structured output conforming to the `CLAIMS` Pydantic model.
        """
        return self.generate_output(claims=claims, risk=risk)
