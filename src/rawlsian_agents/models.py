from typing import List
from pydantic import BaseModel, Field

class Risk(BaseModel):
    title: str = Field(description="short summary of the situation")
    impact: str = Field(description="brief explanation of the situation")
    scenario: str = Field(description="Counterfactual scenario that are potential outcomes of the situation")
    mitigation: str = Field(description="strategies or alternative negotiation terms that could mitigate risks while maintaining fairness for both parties")

    def __str__(self):
        return f"Title: {self.title}\nImpact: {self.impact}\nScenario: {self.scenario}\nMitigation: {self.mitigation}\n"
    
class Risks(BaseModel):
    risks: List[Risk] = Field(description="list of risks that the person is taking")
    
class Claim(BaseModel):
    title: str = Field(description="short summary of the claim")
    description: str = Field(description="details of the claim including all the relevant context")

class Claims(BaseModel):
    claims: List[Claim] = Field(description="list of claims in the agreement")

class Arbitration(BaseModel):
    analysis: str = Field(description="detailed evaluation of the risk from multiple perspectives")
    edit: str = Field(description="suggested one edit to the agreement to mitigate the risk")

    def __str__(self):
        return f"Analysis: {self.analysis}\nEdit: {self.edit}\n"
