### Analyzing the Influence of Housing Characteristics and Neighbourhood Amenities on Family-Oriented Household Expenditures in Singapore

#### Overview and Problem Formulation

- Singapore faces challenges with a declining Total Fertility Rate (TFR), which stood at 0.97 in 2024 according to SingStat data, influenced by factors like high living costs and urban pressures.
- Interest lies in how housing features (e.g., flat type, size) and neighborhood amenities (e.g., proximity to parks, schools, childcare centers) impact family-oriented household expenditures (e.g., on education, healthcare, and recreation).
- Insights provide understanding of household priorities for child-rearing support, indirectly tied to fertility decisions and housing demand dynamics.
- Families may seek larger or better-located homes to accommodate growing needs, but the analysis emphasizes spending patterns rather than demand volume.
- The business problem addresses policymakers (e.g., HDB, Ministry of Social and Family Development) and real estate developers:
  - How can urban planning optimize amenities to encourage family investments, potentially alleviating cost barriers to larger families?
- Publicly available data is used to model these relationships, revealing novel insights like amenity-driven spending disparities across planning areas.

#### Hypothesis

- Households in housing areas with greater access to family-friendly amenities (e.g., parks and schools within 1km) exhibit higher family-oriented expenditures, as these reduce logistical burdens and enhance quality of life, even after controlling for income and flat size.
- This could highlight under-served areas where amenity improvements might boost family support.

#### Assumptions

- Expenditure is independent of income (e.g., percentage of income spent is proportional to the amount earned).
- Families with the same income band spend proportionally more when they have more children (an indirect proxy of Total Fertility Rate or TFR).
- Household spending across planning areas is independent of cost of living, i.e., no significant differences in cost of living affect household spending, and any significant drivers can be mitigated by moving to a new planning area.
- Free amenities such as parks do not act as substitutes for paid amenities like shopping, and are instead complementary in nature.

#### Objective Function

- The target variable is the average monthly family-oriented household expenditure per member (in SGD), aggregated from categories like education, healthcare, and child-related recreation.
- This is a spending metric derived from survey data, modeled as a regression problem to predict and optimize based on housing/amenity features.

#### Method of Collecting Information

- The target feature can be found in the Household Expenditure Survey (HES) 2023 Report [1].
- Data is aggregated at the income band level.
- By utilizing an ecological inference technique, data from the Singapore Department of Statistics Report on income distributions within each Household Planning Area [2] is combined using the following approach:
  - T8 of the HES contains a mapping between HDB dwellings and Monthly Income Group.
  - House Size is used as an approximation for income, allowing for nuanced comparison between spending categories.
  - House size is mapped to expenditure. For categories where the HES only captured house sizes, these are mapped to the relevant income bins.
  - Expenditure distribution is calculated as a weighted average:
    - E.g., For "education" in Jurong West:  
      - (SGD 300 for 2000-2999 SGD/mth bin × 0.40) + (SGD 250 for 2000-2999 SGD/mth bin × 0.30) + ... = Weighted avg.

#### Data Model (Proposed)

- First draft of a proposed data model for data synthesis:
  - Dataset will be income expenditures aggregated at the planning area level, split into spend categories (T20 of the HES [1]).
  - Spend categories are defined by food, services, equipment, etc., and will need to be mapped to either “Is Family-Oriented Expenditure” or “Is not Family-Oriented Expenditure”.

#### Potential AI or LLM Integration

##### Automated Labelling

- Spending categories can be automatically mapped to “Family Oriented” or “Not Family Oriented” utilizing an LLM.
- Example prompt:
  - “Classify the following HES expenditure item as 'family_oriented' or 'not_family_oriented' if it directly supports the health, education, or recreation of children under 18. Return only the label and confidence score.”
- Model output examples:
  - “tuition and other fees for academic courses → family_oriented (0.99)”
  - “alcoholic beverages → not_family_oriented (0.98)”
- LLM-generated labels are compiled into a mapping table and applied to aggregate education, health, and child recreation into the final family_oriented_expenditure target.

##### Automated Insight Summarization for Stakeholder Communication

- After regression, an LLM is prompted with structured inputs:
  - “Given: Planning Area = Punggol, Family-Oriented Expenditure = SGD 1,050, % High-Income Households = 42%, Avg. Distance to Childcare = 0.8 km. Summarize in two sentences why this area outperforms expectations.”
- Model output example:
  - “Punggol’s high family investment is driven primarily by ... This suggests income acts as a buffer against urban friction, reducing the marginal benefit of additional facilities.”
- These human-readable summaries are embedded in the report and slides, making complex statistical outputs accessible to policymakers.

#### Limitations

- Four critical limitations are proactively identified and addressed to ensure transparency, robustness, and credibility.

##### Ecological Fallacy in Income-Weighted Fusion

- **Issue:** Assumes all households within an income bin and planning area spend identically. In reality, lifestyle variations exist (e.g., frugal vs. high-earning spenders).
- **Mitigation:**
  - Conduct sensitivity analysis (±15% variation in HES bin averages).
  - Validate national weighted average matches HES totals.
  - Report finding as “indicative of area-level trends”, not household-level.

##### Temporal Misalignment Between Datasets

- **Issue:** HES 2023 expenditure data is fused with Census 2020 income distribution, a 2–3 year gap during which inflation and behaviour shifted.
- **Mitigation:**
  - Apply SingStat CPI adjustment (2017/18 → 2020) to education.
  - Clearly state “2020-equivalent SGD” in all outputs.

##### Sampling Bias in HES Toward Urban, Employed Households

- **Issue:** HES under-samples outer estates and non-working households, potentially overestimating national averages for family spending.
- **Mitigation:**
  - Weight HES bins using Census 2020 employment status distribution per planning area.
  - Flag “No Employed Person” bin (18% nationally) with conservative spend (SGD 190/month).
  - Discuss in report: “Findings may understate challenges in lower-income areas.”

#### Managerial Action (Potential Conclusion)

- Income is the dominant driver of family investment, amplified by amenities in Low/Middle/High Income Areas (based on model outcomes).
- High-income planning areas (e.g., Bukit Timah, SGD 1,480/month) exhibit strong family-oriented spending regardless of amenity access, indicating that affluence enables outsourcing (private tutors, healthcare, enrichment).
- In middle-income areas (e.g., Sengkang, SGD 820), a 1 km reduction in childcare distance increases spending by SGD 78/month — a 9.5% uplift.
- **Possible Managerial Action:** URA and HDB should prioritize amenity density in middle-income new towns (e.g., Tengah, Yishun) to maximize return on infrastructure investment.

#### Citations

- [1] Department of Statistics Singapore. (2024). Household Expenditure Survey. Retrieved from https://www.singstat.gov.sg/publications/households/household-expenditure-survey
- [2] Singapore Department of Statistics. "Resident Households by Planning Area of Residence and Monthly Household Income from Work (Census Of Population 2020)." data.gov.sg, 22 Oct. 2024, https://data.gov.sg/datasets/d_2d6793de474551149c438ba349a108fd/view.