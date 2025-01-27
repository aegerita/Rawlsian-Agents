from typing import List
from pydantic import BaseModel, Field

class Risk(BaseModel):
    rate: int = Field(description="how much this risk will affects the person's interests, rated in a number from 1 to 5")
    title: str = Field(description="short summary of the situation")
    description: str = Field(description="detailed explanation of the situation")
    
class Risks(BaseModel):
    risks: List[Risk] = Field(description="list of risks that the person is taking")
    
class Clauses(BaseModel):
    clauses: List[str] = Field(description="list of clauses in the agreement")
