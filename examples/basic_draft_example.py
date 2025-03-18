# %%
from fairplay.agents.basic_drafter import BasicDrafter
from fairplay.agents.claims_processor import ClaimsProcessor
from fairplay.utils.prenup_templates import ENGLAND_AND_WALES_PRENUP_TEMPLATE

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

# %%
draft = bd.draft_agreement(ENGLAND_AND_WALES_PRENUP_TEMPLATE, claims)
print(draft)

with open("../src/docs/SC vs TC/initial_agreement.md", 'w') as file:
    file.write(draft)
