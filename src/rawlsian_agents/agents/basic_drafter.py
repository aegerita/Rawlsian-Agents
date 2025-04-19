from rawlsian_agents.agents.base_agent import Agent

BASE_AGENT_PROMPT = r"""
You are a skilled legal drafter working for a reputable law firm. Your clients, a couple preparing to enter into marriage, require a professionally drafted agreement tailored to their specific circumstances. Your task is to clearly and accurately fill out the provided template using the factual claims supplied below.

Ensure you integrate all provided claims relevant to the template. Adjust wording only as necessary for coherence, clarity, and integration into the template's structure. All claims should be accurately and thoroughly represented in the agreement. If there exists any direct quotes or specific numerical values in the text, ensure these are verbatim. In addition, if there are conflicting information between the claims and the template, prioritize the claims provided, and adjust the template accordingly. Your goal is to create a legally sound and comprehensive prenuptial agreement that reflects the clients' intentions truthfully and completely.

**Claims:**
{claims}

**Template:**
{template}
"""


class BasicDrafter(Agent):
    """
    A non rawlsian agent who takes claims and free text as input and drafts a prenup based on a template.
    """
    def __init__(self) -> None:
        super().__init__(
            prompt_template=BASE_AGENT_PROMPT,
            input_variables=["template", "claims"],
        )

    def draft_agreement(self, template: str, claims: str) -> str:
        """
        Drafts the final prenuptial agreement based on the claims and free text.

        :param template: The template to use for the prenuptial agreement.
        :param claims: The list of factual claims to include in the agreement.
        :return: The final prenuptial agreement.
        """
        return self.generate_output(template=template, claims=claims).text()
