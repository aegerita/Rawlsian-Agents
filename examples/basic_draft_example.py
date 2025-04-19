# %%
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.utils.prenup_templates import ENGLAND_AND_WALES_PRENUP_TEMPLATE

# %%
bd = BasicDrafter()
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
