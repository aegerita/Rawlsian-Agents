import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

class Risk(BaseModel):
    rate: int = Field(description="how much this risk will affects the person's interests, rated in a number from 1 to 5")
    title: str = Field(description="short summary of the situation")
    description: str = Field(description="detailed explanation of the situation")
    
class Risks(BaseModel):
    risks: List[Risk] = Field(description="list of risks that the person is taking")
    
class CLAUSES(BaseModel):
    clauses: List[str] = Field(description="list of clauses in the agreement")
    
    
CURRENT_CLAUSES = CLAUSES(clauses=[
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

DA_PROMPT = r"""
You are an AI representative who has been specifically assigned the important and significant task of considering and prioritizing the interests of {name} within the context of the specified scenario that has been presented to you. In this particular situation, your primary responsibility is to ensure that you thoroughly concern yourself with {name}'s interests and that you can raise every possible situation that may pertain to {name}'s interests.

Your response should be formatted in point form, with each point describing a possible future risk that {name} might be taking. Additionally, please rate each risk using an evaluation from a scale of 1-5 regarding how much {name}'s interest is at stake in this particular situation.

Scenario: {scenario}
"""

PROPOSE_PROMPT = r"""
You have a detailed prenuptial agreement that outlines the specific terms and conditions both parties have agreed upon. One of the clients has raised a concern about a potential future risk that could have serious implications for both individuals. If necessary, suggest adding specific clauses to the agreement that address this identified risk and help prevent any negative consequences. It is essential not to repeat any clauses that are already included in the agreement or to introduce any redundant clauses. In the case that the risk is sufficiently resolved by the agreement, return nothing in the list of clauses. Be clear and concise in your language to ensure understanding. 

You should analyze this situation using John Rawls' concept of the "veil of ignorance," which highlights the importance of fairness and an unbiased perspective in decision-making. It is vital to thoroughly assess ethical considerations to ensure that the proposed solution benefits both clients involved in this prenuptial agreement.

Current clauses for the prenuptial agreement:
{clauses}

The identified risk:
{risk}
"""
    

prompt = PromptTemplate(
    template=DA_PROMPT,
    input_variables=["name", "scenario"],
)
model = ChatOpenAI(model=os.environ["MODEL"]).with_structured_output(Risks)

chain = prompt | model


# risks_A = chain.invoke({"name": "Person A", "scenario": CURRENT_CLAUSES}).risks
risks_A = [
    Risk(rate=3, title='Potential Disputes Over Joint Account Contributions', description='If there is ambiguity around the contributions to the joint account, Person A could face disputes with Person B over the ownership and division of these funds in the event of separation.'), Risk(rate=4, title='Risk of Financial Instability Due to Mutual Consent Clause', description="Financial decisions require mutual consent, which may cause delays or hindrances in responding to urgent financial needs, potentially impacting Person A's financial stability."), Risk(rate=2, title='Limitations on Investment Opportunities', description="The conservative investment strategy may limit Person A's ability to pursue potentially lucrative investment opportunities, affecting long-term wealth accumulation."), Risk(rate=5, title='Inheritance and Its Impact on Future Financial Planning', description='Any inheritance received by either party remains separate property. However, failure to plan adequately for the implications of significant inheritances could lead to disputes or financial difficulties for Person A.'), Risk(rate=1, title='Lack of Control Over Joint Decisions', description='Person A may feel a lack of control over major financial decisions due to the requirement for mutual consent, which can lead to personal dissatisfaction.'), Risk(rate=3, title='Potential for Miscommunication Regarding Asset Disclosure', description="Even with complete asset disclosure affirmed, misunderstandings or lack of communication regarding debts or hidden assets could negatively impact Person A's financial situation."), Risk(rate=2, title='Risk of Asset Value Depreciation', description='If the value of jointly held assets declines (e.g., if properties or investments underperform), this could adversely affect the financial landscape for Person A in a division of assets.'), Risk(rate=4, title='Jointly Held Assets and Divorce Outcomes', description='In the event of divorce, the division of jointly held assets could lead to significant financial loss or reduced stability for Person A if asset division is not favorably negotiated.')
]

# risks_B = chain.invoke({"name": "Person B", "scenario": CURRENT_CLAUSES}).risks
risks_B = [
    Risk(rate=4, title='Unequal Financial Power Post-Divorce', description='In the event of a divorce, Person B could risk losing potential access to shared funds that could have previously been utilized for a more equitable lifestyle. While they retain their separate property, the reliance on a joint account means future earnings and savings might not be as accessible.'), Risk(rate=3, title='Impact of Joint Investment Decisions', description='The requirement for mutual consent on major financial decisions exposes Person B to risks if Person A makes conservative or unwise choices with their joint investments, potentially jeopardizing future financial goals for Person B.'), Risk(rate=2, title='Shared Expenses Liability', description='By depositing portions of their salary into a joint account for shared expenses, Person B risks the possibility of overextending financially if Person A does not contribute equally or consistently, which could lead to resentment or financial strain.'), Risk(rate=5, title='Risk of Future Inheritance Loss', description='Any inheritance Person B receives will remain their separate property, which generally protects it. However, if they commingle those funds with joint assets, there may be a risk of losing that inheritance in a divorce settlement.'), Risk(rate=3, title='Lack of Control Over Joint Assets', description='Since jointly held assets will be subject to agreed-upon law or equitable distribution, Person B may find themselves at risk of losing a significant portion of their contributions based on decisions made collaboratively without their full agreement.'), Risk(rate=4, title='Dependence on Mutual Consent for Major Decisions', description="The requirement for mutual consent for major financial decisions means Person B may feel pressured or blocked by Person A's decisions which could lead to dissatisfaction or financial hardship for Person B."), Risk(rate=2, title='Potential Misrepresentation in Financial Disclosure', description='If either party fails to fully disclose their assets or debts, Person B risks entering into financial agreements that are not in their best interest, potentially resulting in hidden liabilities or risks.'), Risk(rate=1, title='Legal Representation Risks', description="Although both parties affirm to seek independent legal representation, there's a risk that if Person B doesn't advocate strongly for their own interests, they may inadvertently agree to unfavorable terms."), Risk(rate=5, title='Changes in Joint Account Contributions', description='Should the financial contributions to the joint account change unexpectedly (such as loss of income), Person B may find themselves financially destabilized if they depend solely on this for shared expenses.')]

combined_risks = risks_A + risks_B
sorted_risks = sorted(combined_risks, key=lambda x: x.rate, reverse=True)
print("Risks for Person A and Person B combined:")
print("\n")


for risk in sorted_risks:
    print(f"Title: {risk.title}")
    print(f"Rate: {risk.rate}")
    print(f"Description: {risk.description}")
    print("\n")
    
    prompt = PromptTemplate(
        template=PROPOSE_PROMPT,
        input_variables=["clauses", "risk"],
    )
    model = ChatOpenAI(model=os.environ["MODEL"]).with_structured_output(CLAUSES)
    chain = prompt | model
    clauses = chain.invoke({"clauses": CURRENT_CLAUSES.clauses, "risk": risk.title})
    print("Proposed clauses:")
    print(clauses.clauses)
    
    CURRENT_CLAUSES.clauses.extend(clauses.clauses)
    
    
print("Final clauses:")
print(CURRENT_CLAUSES.clauses)


