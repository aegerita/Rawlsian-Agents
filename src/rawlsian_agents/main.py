#%%
from rawlsian_agents.agents.arbitrator import Arbitrator
from rawlsian_agents.agents.basic_drafter import BasicDrafter
from rawlsian_agents.agents.claims_processor import ClaimsProcessor
from rawlsian_agents.agents.drafter import Drafter
from rawlsian_agents.agents.reviewer import Reviewer
from rawlsian_agents.utils.commercial_lease_templates import BC_LEASE_TEMPLATE
from rawlsian_agents.utils.prenup_templates import PRENUP_TEMPLATE
from argparse import ArgumentParser

from rawlsian_agents.utils.prompts import COMMERCIAL_LEASE_PROMPT, PRENUPTIAL_PROMPT

#%%
PROMPT_TEMPLATES = {
    "prenuptial": PRENUPTIAL_PROMPT,
    "commercial_lease": COMMERCIAL_LEASE_PROMPT,
}
AGREEMENT_TEMPLATES = {
    "prenuptial": PRENUP_TEMPLATE,
    "commercial_lease": BC_LEASE_TEMPLATE,
}

#%%
parser = ArgumentParser()
parser.add_argument("-fp", "--folder_path", default="src/docs/LeVan vs LeVan/", dest="folder_path", help="Folder path for relevant documents.")
parser.add_argument("-t", "--contract_type", default="prenuptial", choices=["prenuptial", "commercial_lease"], dest="contract_type", help="Type of contract to process.")

args = parser.parse_args()
folder_path = args.folder_path
contract_type = args.contract_type
if contract_type not in AGREEMENT_TEMPLATES:
    raise ValueError(f"Unsupported contract type: {contract_type}. Supported types are: {list(AGREEMENT_TEMPLATES.keys())}")
input_template = AGREEMENT_TEMPLATES[contract_type]
prompts = PROMPT_TEMPLATES[contract_type]
input_file = "case_file.txt"
output_file = "final_agreement.md"

# %%
with open(folder_path + input_file, "r") as file:
    free_text = file.read()

# %%
claims_processor = ClaimsProcessor(prompts)
claims_processor.load_free_text(free_text)
claims = claims_processor.process_claims()
print(claims)

with open(folder_path + "recovered_claims.txt", "w") as file:
    file.write(str(claims))

# %%
basic_drafter = BasicDrafter()
initial_agreement = basic_drafter.draft_agreement(input_template, claims)
print(initial_agreement)

with open(folder_path + "initial_agreement.md", 'w') as file:
    file.write(initial_agreement)

#%%
reviewer = Reviewer(prompts)
risks_A = reviewer.generate_risks(name="Landlord", claims=initial_agreement)
risks_B = reviewer.generate_risks(name="Tenant", claims=initial_agreement)
combined_risks = risks_A + risks_B

with open(folder_path + "combined_risks.md", "w") as file:
    file.write("## Combined Risks Identified\n")
    for risk in combined_risks:
        file.write(f"{risk}\n\n")

#%%
edits = ["Proposed edits to the agreement:"]
arbitrator = Arbitrator(prompts)
with open(folder_path + "risks_and_mitigations.md", "w") as file:
    for risk in combined_risks:
        print(risk)
        file.write(f"{risk}\n")
        arbitration = arbitrator.propose_clause(claims=initial_agreement, risk=risk)
        print(arbitration)
        edits.append(arbitration.edit)
        file.write(f"Arbitrator's POV:\n {arbitration}\n\n")
print("\n")
for edit in edits:
    print(edit)

#%%
drafter = Drafter(prompts)
final_agreement = drafter.draft_agreement(agreement=initial_agreement, edits=edits)
print("\nFinal agreement:")
print(final_agreement)
with open(folder_path + output_file, 'w') as file:
    file.write(final_agreement)
