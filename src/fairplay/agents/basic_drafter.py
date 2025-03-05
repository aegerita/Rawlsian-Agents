from fairplay.agents.base_agent import Agent

BASE_AGENT_PROMPT = r"""
You are a legal drafter working for a law firm. Your clients are a couple who are about to get married.
Your task is to fill the template below with the factual claims and antecedents provided:

**Template:**
{template}

**Claims:**
{claims}

**Antecedents:**
{antecedents}

Make sure you include all the claims and antecedents relevant to the template, 
change them only so they make sense within the template, and return the output.
"""


class BasicDrafter(Agent):
    """
    A non rawlsian agent who takes claims and free text as input and drafts a prenup based on a template.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=BASE_AGENT_PROMPT,
            input_variables=["template", "claims", "antecedents"],
        )

    def draft_agreement(self, template: str, claims: str, antecedents: str) -> str:
        """
        Drafts the final prenuptial agreement based on the claims and free text.

        :param template: The template to use for the prenuptial agreement.
        :param claims: The list of factual claims to include in the agreement.
        :param antecedents: The list of antecedents to include in the agreement.
        :return: The final prenuptial agreement.
        """
        return self.generate_output(template=template, claims=claims, antecedents=antecedents).text()
