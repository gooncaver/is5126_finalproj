# Predicting Fertility Intentions: Understanding Value-Based Drivers of Family Size in Singapore

## 1. Executive Summary

Singapore faces a persistent fertility challenge with a total fertility rate (TFR) of 1.04 (2023), well below the replacement level of 2.1. This project leverages the World Values Survey (WVS) Wave 7 dataset to identify attitudinal and value-based predictors of family size, with the goal of informing evidence-based policy interventions to support family formation.

## 2. Research Objectives

### Primary Objective
Develop predictive models to identify key attitudinal and value-based factors associated with fertility outcomes (number of children) among Singaporeans of childbearing age.

### Secondary Objectives
1. Compare Singapore-specific patterns with global trends to identify culturally unique factors
2. Integrate household economic data to understand the relationship between values, spending patterns, and fertility
3. Develop an AI-powered advisory tool to provide personalized insights on family planning considerations

## 3. Dataset Description

### 3.1 Primary Dataset: World Values Survey (WVS) Wave 7
- **File**: `WVS_Cross-National_Wave_7_csv_v6_0.csv`
- **Survey Period**: 2017-2021
- **Total Respondents**: ~97,000 across 66 countries
- **Coverage**: Comprehensive attitudes on social values, family importance, gender equality, religious beliefs, economic security, and political engagement

### 3.2 Target Variable
- **Q274**: Number of children (continuous variable, 0 to n)
- **Distribution** (from sample): Ranges from 0 to 3+, with variation suitable for regression modeling

### 3.3 Key Predictor Variables

#### Demographic Controls
- **Q262**: Age (years)
- **Q260**: Gender
- **Q275**: Respondent's education level (ISCED classification)
- **Q273**: Marital status
- **Q288**: Household income (10-point scale)

#### Attitudinal Features
- **Q1-Q6**: Importance of family, friends, leisure, politics, work, religion (4-point scale)
- **Q7-Q17**: Important qualities to teach children (independence, hard work, religious faith, tolerance, etc.)
- **Q28-Q38**: Gender equality and family values
  - Q28: "When a mother works for pay, the children suffer"
  - Q37: "A woman has to have children in order to be fulfilled"
  - Q38: "It is a duty towards society to have children"
- **Q164-Q174**: Religious values and religiosity
- **Q186**: Attitudes toward sex before marriage (justifiability, 1-10 scale)

#### Socioeconomic Indicators
- **Q50**: Financial satisfaction (1-10 scale)
- **Q286**: Family savings behavior (saved money, just get by, spent savings, borrowed)
- **Q287**: Social class (1-5 scale)
- **Q279**: Employment status

## 4. Problem Statement

**Context**: Singapore is experiencing a sustained fertility decline despite multiple government interventions (baby bonuses, parental leave, housing subsidies). Current policies primarily address economic barriers but may not adequately address underlying value-based and attitudinal factors influencing family planning decisions.

**Research Question**: What attitudinal, value-based, and socioeconomic factors are most predictive of fertility outcomes among Singaporeans of childbearing age, and how do these patterns compare to global trends?

**Policy Relevance**: By identifying specific attitudes and values associated with higher fertility, policymakers can design more targeted interventions that address both material and normative barriers to family formation.

## 5. Data Preparation & Filtering

### 5.1 Geographic Filtering
- **Primary Analysis**: Filter to Singapore respondents (`B_COUNTRY_ALPHA == 'SGP'`)
- **Comparative Analysis**: Retain full dataset for cross-national benchmarking

### 5.2 Age Filtering
- **Target Population**: Adults aged 25-49 (Q262)
  - **Rationale**: Age 25-49 captures the prime childbearing and family formation years
  - **Cohort Analysis**: Segment into age groups (25-29, 30-34, 35-39, 40-44, 45-49) to examine age-specific patterns

### 5.3 Data Quality & Missingness
- **Missing Value Codes**: -1 (Don't know), -2 (No answer), -3 (Not applicable), -5 (Missing)
- **Handling Strategy**:
  - Exclude respondents with missing Q274 (target variable)
  - Multiple imputation for predictor variables with <20% missingness
  - Sensitivity analysis to assess impact of missingness

### 5.4 Sample Size Considerations
- **Expected Singapore Sample**: Estimated n ≈ 1,000-2,000 respondents
- **Power Analysis**: Sufficient for regression modeling with 20-30 predictors
- **Validation Strategy**: If sample size permits, use 70/30 train-test split; otherwise, k-fold cross-validation

## 6. Data Enrichment: Household Economic Survey (HES) Integration

### 6.1 Rationale
While WVS captures values and attitudes, integrating actual household expenditure patterns can reveal whether family-oriented values translate into family-oriented spending behaviors.

### 6.2 Data Source
- **Dataset**: Singapore Department of Statistics Household Expenditure Survey
- **Access**: Available via [data.gov.sg](https://data.gov.sg)

### 6.3 Integration Strategy

#### Join Key: Income Decile Mapping
1. **WVS Q288**: Self-reported income scale (1-10)
2. **HES**: Household income by decile with detailed expenditure breakdown
3. **Mapping Approach**: Match WVS income scale values to HES income deciles

#### Feature Engineering from HES
Create a **Family-Oriented Spending Index** by categorizing expenditure items:

**Family-Oriented Expenses**:
- Education
- Childcare
- Children's clothing
- Recreation (family-oriented)
- Health expenditure (family members)
- Housing (family-appropriate size)

**Non-Family-Oriented Expenses**:
- Individual entertainment
- Dining out (adult-oriented)
- Alcohol and tobacco
- Personal luxury items

**Derived Features**:
- `pct_family_oriented_spending` = (Family expenses / Total expenses) × 100
- `education_spending_per_capita` = Education expenses / Household size
- `childcare_intensity` = Childcare expenses / Total income

### 6.4 Limitations & Mitigation
- **Limitation**: Ecological fallacy – HES data is aggregated by income bracket, not individual-level
- **Mitigation**: 
  - Clearly acknowledge this as a contextual enrichment, not causal evidence
  - Use as supplementary features in sensitivity models
  - Primary analysis focuses on WVS attitudinal predictors

## 7. Modeling Approach

### 7.1 Model Selection

#### Primary Model: Multiple Linear Regression
- **Target**: Q274 (number of children, treated as continuous)
- **Advantages**: Interpretable coefficients, statistical inference
- **Feature Selection**: Stepwise regression, LASSO regularization to handle multicollinearity

#### Alternative Models
1. **Poisson Regression**: If Q274 is treated as count data (theoretically more appropriate)
2. **Negative Binomial Regression**: If overdispersion is detected in count data
3. **Gradient Boosting (XGBoost/LightGBM)**: For predictive accuracy and feature importance
4. **Random Forest**: Non-linear relationships, interaction detection

### 7.2 Model Variants

#### Model 1: Singapore-Only (Attitudinal Model)
- **Features**: WVS attitudes, values, demographics (Q1-Q288)
- **Goal**: Identify Singapore-specific attitudinal drivers

#### Model 2: Singapore + HES Enrichment
- **Features**: Model 1 + family spending indicators
- **Goal**: Test whether spending patterns add predictive power beyond attitudes

#### Model 3: Global Comparative Model
- **Features**: All WVS countries with country fixed effects
- **Goal**: Identify universal vs. culturally specific fertility predictors
- **Analysis**: Compare Singapore coefficients to global averages

#### Model 4: Cohort-Specific Models
- **Stratification**: Separate models for age cohorts (25-29, 30-34, 35-39, 40-49)
- **Goal**: Examine generational differences in fertility determinants

### 7.3 Evaluation Metrics
- **R² and Adjusted R²**: Proportion of variance explained
- **RMSE (Root Mean Squared Error)**: Prediction accuracy
- **Feature Importance**: Coefficient magnitudes, SHAP values
- **Cross-Validation**: K-fold CV to assess generalizability

### 7.4 Validation Strategy
- **Internal Validation**: 10-fold cross-validation on Singapore subset
- **External Validation**: Test Singapore model on comparable countries (Hong Kong, Taiwan, South Korea)

## 8. Critical Assumptions & Limitations

### 8.1 Temporal Assumptions
**Assumption**: Current attitudes are representative of attitudes at the time of childbearing decisions.

**Limitation**: 
- Q274 captures cumulative fertility (total children ever born)
- Attitudes measured at survey time (2017-2021) but children may have been born years earlier
- **Reverse Causality Risk**: Having children may change attitudes toward family values (e.g., parents become more family-oriented after having children)

**Mitigation**:
- Acknowledge this as a **cross-sectional correlation study**, not causal inference
- Use younger cohorts (25-34) for whom childbearing is more recent
- Interpret findings as "attitudes associated with fertility" rather than "attitudes causing fertility"
- Consider longitudinal data (if available in future WVS waves) for causal inference

### 8.2 Generalizability Assumptions
**Assumption**: WVS Singapore sample is representative of the broader Singaporean population.

**Considerations**:
- Survey sampling methodology (household-based, representative sampling)
- Response bias (certain demographics may be underrepresented)
- Compare WVS demographics to Singapore Census data

### 8.3 Cross-Cultural Comparability
**Assumption**: Attitude questions are interpreted consistently across cultures.

**Limitation**: Cultural differences in understanding concepts like "family duty" or "gender equality"

**Mitigation**: Focus on within-Singapore analysis; use global models cautiously

### 8.4 Data Integration Assumptions
**Assumption**: Income self-reporting in WVS is accurate and mappable to HES income brackets.

**Limitation**: Self-reported income may have measurement error and social desirability bias

## 9. LLM Integration: AI-Powered Family Planning Advisory Tool

### 9.1 Architecture Overview
Develop an interactive chatbot that leverages the trained predictive model to provide personalized insights on family planning considerations.

### 9.2 Technical Implementation

#### Backend: Model Serving
- **Framework**: FastAPI + Uvicorn
- **Model Deployment**: Trained regression model serialized (pickle/joblib) and served via REST API
- **Endpoint**: `/predict` accepts user inputs (attitudes, demographics) and returns predicted family size and key drivers

#### Frontend: Conversational Interface
- **LLM**: OpenAI GPT-4 or Claude (for natural conversation)
- **Integration**: LLM uses function calling to:
  1. Engage user in conversation about values and life goals
  2. Extract structured features matching WVS questions
  3. Call `/predict` endpoint with user data
  4. Interpret model output in conversational language

### 9.3 User Interaction Flow

1. **Engagement**: "I'm here to help you think through family planning considerations. Let's talk about what matters most to you."

2. **Data Collection** (conversational extraction of WVS features):
   - Family importance: "How important is family in your life?"
   - Work-life balance: "How do you feel about balancing career and family?"
   - Gender roles: "What are your views on parenting responsibilities?"
   - Financial security: "How satisfied are you with your current financial situation?"

3. **Model Inference**: 
   - LLM constructs feature vector from conversation
   - Calls prediction API: `{"age": 28, "family_importance": 1, "income": 6, ...}`
   - Receives: `{"predicted_children": 1.8, "key_drivers": ["family_importance", "marital_status", "financial_satisfaction"]}`

4. **Personalized Insights**:
   - "Based on your values and circumstances, people with similar profiles typically have 1-2 children."
   - "Key factors influencing family size for people like you include: [driver insights]"
   - "Here are some considerations that might help you think about your family planning goals..."

5. **Policy Signposting**:
   - "Did you know about these Singapore government support schemes?"
   - Link to baby bonus, childcare subsidies, parental leave policies

## 10. Study Limitations

This study acknowledges several important limitations arising from the dataset characteristics, data collection methodology, temporal factors, and contextual relevance to Singapore. These limitations inform the interpretation of findings and constrain the generalizability of results.

### 10.1 Temporal Limitations

#### 10.1.1 Survey Time Range (2017-2021)
- **Data Recency**: WVS Wave 7 data was collected between 2017-2021, meaning Singapore respondents were surveyed 4-8 years prior to the current analysis (2025)
- **Policy Landscape Changes**: Singapore's family policy environment has evolved since data collection (e.g., enhanced parental leave schemes, housing grants, childcare subsidies introduced or expanded post-2021)
- **Post-Pandemic Effects**: COVID-19 pandemic (2020-2022) may have altered fertility intentions and family values in ways not captured in pre-/early-pandemic data
- **Implication**: Findings may not fully reflect current attitudes and may underestimate or miss recent shifts in fertility determinants

#### 10.1.2 Cross-Sectional Design & Reverse Causality
- **Snapshot in Time**: Attitudes measured at a single point (survey date), while Q274 (number of children) represents cumulative lifetime fertility
- **Temporal Mismatch**: For respondents aged 40-49, children may have been born 15-25 years ago, when attitudes were likely different
- **Reverse Causality**: Having children may change attitudes (e.g., parents may become more family-oriented *because* they had children, not vice versa)
- **Limitation on Inference**: Cannot establish causal relationships; findings represent correlations/associations only
- **Implication**: Results should be interpreted as "attitudes associated with completed fertility" rather than "attitudes that cause fertility decisions"

### 10.2 Sampling & Data Collection Limitations

#### 10.2.1 Sample Size Constraints
- **Singapore Sample**: Expected n ≈ 1,000-2,000 respondents from a population of ~5.7 million
- **Sampling Error**: Small sample size increases margin of error and reduces statistical power for detecting small effects
- **Subgroup Analysis**: Insufficient sample size for robust analysis of specific demographic subgroups (e.g., ethnic minorities, low-income households)
- **Implication**: May only detect strong associations; modest effects may not reach statistical significance

#### 10.2.2 Sampling Methodology & Representativeness
- **Household-Based Sampling**: WVS uses household-based probability sampling, which may underrepresent:
  - Young, single individuals not living in family households
  - Transient populations (foreign workers, students)
  - Institutionalized populations
- **Response Bias**: Voluntary participation may skew toward respondents with stronger opinions on family/social issues
- **Non-Response Bias**: Certain demographics (busy professionals, shift workers) may be systematically underrepresented
- **Language Barriers**: Survey conducted in primary languages may exclude non-native speakers or recent immigrants
- **Implication**: Sample may not be fully representative of Singapore's diverse population, particularly younger, mobile, or transient groups

#### 10.2.3 Self-Report Bias
- **Social Desirability**: Respondents may provide socially acceptable answers rather than true attitudes (e.g., overstating family importance, understating materialist values)
- **Income Misreporting**: Q288 (self-reported income scale) may suffer from:
  - Upward bias (inflating income for status)
  - Downward bias (underreporting for privacy)
  - Measurement error in mapping subjective 1-10 scale to actual income
- **Recall Bias**: Questions about past behaviors or family background may be subject to imperfect memory
- **Implication**: Attitudinal measures may be biased toward normative ideals rather than actual beliefs; income-based analyses may contain measurement error

### 10.3 Cultural & Contextual Relevance to Singapore

#### 10.3.1 Cross-Cultural Question Interpretation
- **Concept Validity**: Terms like "family duty," "gender equality," or "religious values" may be understood differently in Singapore compared to Western contexts where WVS was designed
- **Cultural Nuances**: Singapore's multicultural society (Chinese, Malay, Indian, Eurasian) may interpret questions through different cultural lenses, introducing heterogeneity in responses
- **Familialism vs. Individualism**: Asian cultural context (filial piety, extended family obligations) may not be fully captured by Western-centric survey items
- **Implication**: Some predictors may be less meaningful or differently calibrated in Singapore context

#### 10.3.2 Policy & Institutional Context Differences
- **Singapore-Specific Factors Not Captured**: 
  - Housing policy (HDB eligibility, proximity to parents, flat sizes)
  - CPF (Central Provident Fund) system and savings requirements
  - Educational system pressures (PSLE, streaming, tuition culture)
  - National Service obligations affecting family timing
- **Global Model Applicability**: Predictors identified in global comparative models may not translate to Singapore's unique institutional environment
- **Implication**: Models may miss Singapore-specific drivers of fertility; external validity of global findings to Singapore is limited

#### 10.3.3 Economic Development Stage
- **High-Income Context**: Singapore is a high-income, developed economy; fertility patterns may differ systematically from developing countries in the dataset
- **Opportunity Cost Mechanisms**: Economic trade-offs of childbearing (career interruption, housing costs) may operate differently than in lower-income contexts
- **Implication**: Singapore-specific models are necessary; pooled global models may introduce bias

### 10.4 Data Integration Limitations

#### 10.4.1 HES Integration Challenges
- **Ecological Fallacy**: Household Expenditure Survey (HES) data is aggregated by income decile; merging with individual-level WVS data creates ecological inference problems
- **Income Scale Mapping**: Mapping WVS Q288 (subjective 1-10 scale) to HES objective income deciles introduces:
  - Arbitrary alignment assumptions
  - Loss of individual variation within income brackets
  - Potential misclassification error
- **Temporal Mismatch**: HES data may be from different years than WVS data collection
- **Causality Ambiguity**: Cannot determine whether values drive spending patterns or spending patterns shape values
- **Implication**: HES-enriched models should be treated as exploratory/supplementary; cannot make individual-level causal claims about spending behaviors

#### 10.4.2 Missing External Validation Data
- **No Ground Truth**: No independent dataset to validate fertility predictions (e.g., longitudinal fertility outcomes)
- **No Experimental Variation**: Observational data lacks exogenous shocks or natural experiments to test causal mechanisms
- **Implication**: Limited ability to validate model predictions against real-world fertility outcomes

### 10.5 Measurement Limitations

#### 10.5.1 Target Variable (Q274) Limitations
- **Completed vs. Intended Fertility**: Q274 measures number of children *ever born*, not fertility intentions or desires
- **No Timing Information**: Cannot distinguish between:
  - Voluntary childlessness vs. delayed fertility (still planning)
  - Completed fertility vs. ongoing family formation
- **Censoring Issue**: Younger respondents (25-34) may still plan to have more children, leading to right-censored data
- **Implication**: For younger cohorts, current Q274 values underestimate ultimate completed fertility; age-stratified analysis required

#### 10.5.2 Attitudinal Measure Limitations
- **Ordinal Scales**: Many attitude questions use 4-point or 10-point ordinal scales, which may not have interval properties (distance between points not equal)
- **Single-Item Measures**: Some constructs (e.g., gender equality) measured with single questions rather than validated multi-item scales, reducing reliability
- **Response Compression**: Tendency for respondents to cluster at scale midpoints or endpoints, reducing variance
- **Implication**: Measurement error in predictors may attenuate effect sizes; multi-item composite indices preferred where possible

#### 10.5.3 Missing Data Patterns
- **Non-Random Missingness**: WVS codes -1 (Don't know), -2 (No answer), -3 (Not applicable), -5 (Missing)
  - "Don't know" may indicate ambivalence or lower political/social engagement
  - "No answer" may indicate sensitivity of question or respondent discomfort
  - Patterns may be systematic, not random (MCAR assumption violated)
- **Item-Specific Missingness**: Sensitive questions (income, political views, sexual attitudes) may have higher non-response
- **Implication**: Multiple imputation or complete-case analysis may introduce bias if missingness is not MCAR; sensitivity analyses required

### 10.6 Statistical & Methodological Limitations

#### 10.6.1 Model Specification Uncertainty
- **Omitted Variable Bias**: Unmeasured confounders (genetic factors, personality traits, childhood experiences) may influence both attitudes and fertility
- **Selection Bias**: Unobserved factors affecting both survey participation and fertility (e.g., time preferences, conscientiousness)
- **Model Form Uncertainty**: Unknown whether relationships are linear, non-linear, interactive, or threshold-based
- **Implication**: Estimated associations may be biased; cannot rule out confounding

#### 10.6.2 Multiple Testing & False Discoveries
- **Large Predictor Set**: Testing many predictors (Q1-Q288) increases risk of Type I errors (false positives)
- **Data Dredging Risk**: Exploratory modeling without pre-registration may capitalize on chance findings
- **Publication Bias**: Tendency to emphasize statistically significant results may overstate effect sizes
- **Implication**: Use cross-validation, regularization (LASSO), and conservative significance thresholds; interpret marginal findings cautiously

#### 10.6.3 Limited Generalizability Beyond Singapore
- **Singapore-Specific Findings**: Models trained on Singapore data may not generalize to other contexts
- **Cultural Specificity**: Attitudinal predictors identified may be unique to Singapore's socio-political environment
- **Implication**: Recommendations are Singapore-specific; external replication needed before broader application

### 10.7 Implications for Interpretation

Given these limitations, study findings should be interpreted with the following caveats:

1. **Descriptive, Not Causal**: Results identify associations between attitudes and fertility, not causal effects of attitudes on fertility
2. **Historical Snapshot**: Findings reflect 2017-2021 attitudes and may not predict future fertility under changing policy/economic conditions
3. **Modest Predictive Power Expected**: Given cross-sectional observational data, expect R² ≈ 0.20-0.40; higher values would be unusual
4. **Hypothesis-Generating**: Findings should inform future research and policy exploration, not definitive policy prescriptions
5. **Complementary Evidence Needed**: Should be triangulated with qualitative research, longitudinal data, and policy experiments for robust conclusions

## 11. References & Data Sources

### Primary Data
- World Values Survey Wave 7 (2017-2021). [doi.org/10.14281/18241.24](https://doi.org/10.14281/18241.24)
- WVS Master Questionnaire Documentation

### Supplementary Data
- Singapore Department of Statistics - Household Expenditure Survey (data.gov.sg)
- Singapore Department of Statistics - Population Trends (singstat.gov.sg)

### Methodological References
- To be added: Literature on fertility determinants, WVS methodology, count data regression models
