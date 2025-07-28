# %%
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.utils.prenup_templates import ENGLAND_AND_WALES_PRENUP_TEMPLATE

# %%
COMMERCIAL_LEASE_MODIFIED_PROMPT = r"""
You are a skilled legal drafter working for a reputable law firm. Your clients, two corporations, require a professionally drafted agreement tailored to their specific circumstances. Your task is to clearly and accurately fill out the provided template using the factual claims supplied below.

Ensure you integrate all provided claims relevant to the template. Adjust wording only as necessary for coherence, clarity, and integration into the template's structure. All claims should be accurately and thoroughly represented in the agreement. If there exists any direct quotes or specific numerical values in the text, ensure these are verbatim. In addition, if there are conflicting information between the claims and the template, prioritize the claims provided, and adjust the template accordingly. Your goal is to create a legally sound and overarching lease agreement that reflects the clients' intentions truthfully and comprehensively.

**Claims:**
{claims}

**Template:**
{template}
"""

# %%
bd = BasicDrafter()
bd.prompt_template = COMMERCIAL_LEASE_MODIFIED_PROMPT
cp = ClaimsProcessor()
# %%
with open("../src/docs/SC vs TC/initial_conditions_free_text.txt", "r") as file:
    free_text = file.read()

# %%
cp.load_free_text(free_text)
claims = cp.process_claims()
print(claims)

with open("../src/docs/SC vs TC/recovered_claims.txt", "w") as file:
    file.write(str(claims))

# %%
draft = bd.draft_agreement(ENGLAND_AND_WALES_PRENUP_TEMPLATE, claims)
print(draft)

with open("../src/docs/SC vs TC/initial_agreement.md", 'w') as file:
    file.write(draft)
