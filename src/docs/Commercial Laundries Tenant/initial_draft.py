# %%
import os

from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.utils.commercial_lease_templates import BC_LEASE_TEMPLATE

# %%
COMMERCIAL_LEASE_MODIFIED_PROMPT = r"""
You are a skilled legal drafter working for a reputable law firm. Your clients, two corporations, require a professionally drafted agreement tailored to their specific circumstances. Your task is to clearly and accurately fill out the provided template using the factual claims supplied below.

Ensure you integrate ALL provided claims relevant to the template, make new sections if necessary. Adjust wording as necessary for coherence, clarity, and integration into the template's structure. All claims should be accurately and thoroughly represented in the agreement. If there exists any direct quotes or specific numerical values in the text, ensure these are verbatim. In addition, if there are conflicting information between the claims and the template, prioritize the claims provided, and adjust the template accordingly. Your goal is to create a legally sound and overarching lease agreement that reflects the clients' intentions truthfully and comprehensively.

**Claims:**
{claims}

**Template:**
{template}
"""

cwd = os.path.dirname(os.path.abspath(__file__))

# %%
bd = BasicDrafter()
bd.set_prompt(
    COMMERCIAL_LEASE_MODIFIED_PROMPT,
    bd.input_variables,
    bd.partial_variables,)
bd.set_chain()
# %%
with open(f"{cwd}/initial_conditions.txt", "r") as file:
    free_text = file.read()

# %%
cp = ClaimsProcessor()
cp.load_free_text(free_text)
claims = cp.process_claims()
print(claims)

with open(f"{cwd}/recovered_claims.txt", "w") as file:
    file.write(str(claims))

# %%
draft = bd.draft_agreement(BC_LEASE_TEMPLATE, claims)
print(draft)

with open(f"{cwd}/initial_agreement.md", 'w') as file:
    file.write(draft)
