from fairplay.agents.arbitrator import Arbitrator
from fairplay.agents.reviewer import Reviewer
from fairplay.models import Clauses


CURRENT_CLAUSES = Clauses(clauses=[
    "Person A’s house (valued at $500,000) remains the sole property of Person A",
    "Person B’s car (valued at $20,000) remains the sole property of Person B",
    "Person A’s savings ($50,000) remains with Person A",
    "Person B’s savings ($10,000) remains with Person B",
    "Any future inheritance received by either party is to remain exclusively that party’s separate property.",
    "Any joint investments or shared funds will follow a conservative or mutually agreed-upon strategy",
    "Major financial decisions will require mutual consent.",
    "Each party may deposit a portion of their salary into a joint account for shared expenses",
    "Any funds contributed to the joint account are considered marital property",
    "Funds kept in individual accounts remain separate property"
    "In the event of divorce, each party retains their separate property (house, car, individual savings, and inheritances",
    "Jointly held assets (including joint accounts funds) will be divided according to agreed-upon law or equitable distribution."
    "Both parties confirm complete disclosure of their assets, debts, and income",
    "Both parties affirm they will seek independent legal representation prior to finalizing the agreement."
])

reviewer = Reviewer()
risks_A = reviewer.generate_risks(name="Person A", clauses=CURRENT_CLAUSES)
risks_B = reviewer.generate_risks(name="Person B", clauses=CURRENT_CLAUSES)
combined_risks = risks_A + risks_B
sorted_risks = sorted(combined_risks, key=lambda x: x.rate, reverse=True)
print("Risks for Person A and Person B combined:")
print("\n")

arbitrator = Arbitrator()
for risk in sorted_risks:
    print(f"Title: {risk.title}")
    print(f"Rate: {risk.rate}")
    print(f"Description: {risk.description}")
    
    clauses = arbitrator.propose_clause(clauses=CURRENT_CLAUSES, risk=risk.description)
    print("Proposed clauses:")
    print(clauses)
    
    CURRENT_CLAUSES.clauses.extend(clauses)
    

print("\n")
print("Final clauses:")
print(CURRENT_CLAUSES.clauses)

