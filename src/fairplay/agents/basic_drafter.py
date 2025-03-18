from fairplay.agents.base_agent import Agent

BASE_AGENT_PROMPT = r"""
You are a skilled legal drafter working for a reputable law firm. Your clients, a couple preparing to enter into marriage, require a professionally drafted agreement tailored to their specific circumstances. Your task is to clearly and accurately fill out the provided template using the factual claims and antecedents supplied below.

**Template:**
{template}

**Claims:**
{claims}

**Antecedents:**
{antecedents}

Ensure you integrate all provided claims and antecedents relevant to the template. Adjust wording only as necessary for coherence, clarity, and seamless integration into the template's structure. Your completed document should maintain precision, legal accuracy, and readability suitable for the clients' understanding and formal execution.
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
