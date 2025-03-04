# %%
from fairplay.agents.claims_processor import ClaimsProcessor

cp = ClaimsProcessor()

# %%
free_text = """You are Person A who tries to negotiate a prenuptial agreement 
with your partner. You want to make sure that you are satisfied
with the agreement. You have a yearly income of $100,000 and 
you own a house that is worth $500,000. You have a savings 
account with $50,000. You want to make sure that you keep your 
house and your savings account in case of a divorce. You want 
to be able to make sure that the share account is invested 
with care so that your saving grows. In the event of your 
parents pass away, you do not want to share their inheritance 
with your partner. You have to make sure all of your concerns 
are addressed."""

cp.load_free_text(free_text)

# %%
claims = cp.process_claims()

# %%
print(claims)
