# %%
from fairplay.agents.basic_drafter import BasicDrafter
from fairplay.agents.claims_processor import ClaimsProcessor
from fairplay.utils.prenup_templates import PRENUP_TEMPLATE

# %%
bd = BasicDrafter()
cp = ClaimsProcessor()
# %%
with open("../src/docs/LeVan vs LeVan/LeVan_vs_LeVan_initial_conditions_free_text.txt", "r") as file:
    free_text = file.read()

# %%
cp.load_free_text(free_text)
claims = cp.process_claims()
print(claims)

# %%
draft = bd.draft_agreement(PRENUP_TEMPLATE, claims, free_text)
print(draft)

with open("../src/docs/LeVan vs LeVan/LeVan vs LeVan initial agreement.md", 'w') as file:
    file.write(draft)
