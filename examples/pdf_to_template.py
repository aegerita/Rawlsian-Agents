# %%
from markitdown import MarkItDown

# %%
md = MarkItDown()
result = md.convert("../src/docs/lease_agreements_sample/2017-03-12-Lease-Agreement-DRAFT.pdf")
with open("../src/docs/lease_agreements_sample/2017-03-12-Lease-Agreement-DRAFT.md", "w") as file:
    file.write(result.markdown)
# %%
