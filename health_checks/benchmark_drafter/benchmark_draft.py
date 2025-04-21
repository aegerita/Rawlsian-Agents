#%%
from fairplay.agents.best_effort_drafter import BestEffortDrafter
# %%
with open("./benchmark_drafter_input/initial_agreement.md", 'r') as file:
    initial_agreement = file.read()

output_file = "./benchmark_drafter_output/final_agreement.md"
#%%
best_effort_drafter = BestEffortDrafter()
final_agreement = best_effort_drafter.draft_agreement(agreement=initial_agreement)
print("\nFinal agreement:")
print(final_agreement)
with open(output_file, 'w') as file:
    file.write(final_agreement)
