# Feature Specification: Fertility Prediction Data Science Pipeline

**Feature Branch**: `001-fertility-prediction-pipeline`  
**Created**: 2025-11-01  
**Status**: Draft  
**Input**: User description: "End-to-end data science project for predicting fertility intentions using WVS data, customized to IS5126 rubrics"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reproducible Data Pipeline (Priority: P1)

Research team needs to process raw WVS Wave 7 data into analysis-ready datasets with complete documentation of all transformations, enabling reviewers to verify data quality decisions and reproduce results from scratch.

**Why this priority**: Foundation for all downstream analysis. Without clean, validated data, model results are meaningless. IS5126 rubric emphasizes data collection/exploration (10%) and method validity (30%).

**Independent Test**: Can be fully tested by running data pipeline notebooks in sequence on raw WVS CSV and validating output schemas, sample sizes, and documented exclusions match specifications.

**Acceptance Scenarios**:

1. **Given** raw WVS CSV file, **When** data loading notebook executed, **Then** Singapore subset extracted with n≈1,000-2,000 respondents aged 25-49
2. **Given** loaded data, **When** missingness analysis performed, **Then** documented counts for each missing value code (-1, -2, -3, -5) by variable
3. **Given** preprocessing decisions, **When** filters applied, **Then** exclusion log shows counts and justification for each filter step
4. **Given** processed data, **When** schema validation runs, **Then** all expected Q-codes present with correct data types and value ranges

---

### User Story 2 - Interpretable Baseline Models (Priority: P2)

Research team needs simple, interpretable models (linear regression, Poisson) that identify key attitudinal predictors of fertility, enabling clear policy recommendations aligned with research questions.

**Why this priority**: Core research objective is understanding drivers, not prediction accuracy. IS5126 rubric prioritizes interpretation coherence (20%) over raw model performance. Constitution Principle II mandates simplicity.

**Independent Test**: Can be fully tested by training baseline models on Singapore subset, validating coefficient interpretability (sensible signs), and generating feature importance rankings without complex models.

**Acceptance Scenarios**:

1. **Given** analysis-ready data, **When** linear regression trained on Q274, **Then** coefficients for family importance, marital status, income have expected signs and p-values
2. **Given** baseline model results, **When** feature importance extracted, **Then** top 5-10 predictors identified with confidence intervals
3. **Given** model outputs, **When** assumptions validated, **Then** residual plots, multicollinearity checks documented
4. **Given** interpretation, **When** findings summarized, **Then** limitations explicitly stated (cross-sectional, no causality)

---

### User Story 3 - Model Validation & Comparison (Priority: P3)

Research team needs rigorous validation using cross-validation and comparative analysis across Singapore/global datasets to assess generalizability and robustness of findings.

**Why this priority**: IS5126 rubric emphasizes method validity (30%) and robustness. Constitution Principle III requires documented validation.

**Independent Test**: Can be fully tested by running k-fold CV on Singapore models and testing on comparable countries (HK, TW, KR) to generate performance metrics and comparative insights.

**Acceptance Scenarios**:

1. **Given** trained Singapore model, **When** 10-fold CV executed, **Then** R², RMSE metrics computed with stable performance across folds
2. **Given** Singapore coefficients, **When** global model trained, **Then** coefficient comparison table shows Singapore-specific vs universal predictors
3. **Given** validation results, **When** cohort models compared, **Then** age-specific patterns documented (25-29 vs 40-49)

---

### User Story 4 - LLM Integration Prototype (Priority: P4)

Stakeholders need an interactive chatbot prototype that demonstrates LLM integration for conversational data collection and personalized insights, showcasing novel application of Generative AI.

**Why this priority**: IS5126 rubric rewards LLM/Generative AI workflow integration (20% novelty criterion). Differentiates project from standard ML analysis.

**Independent Test**: Can be fully tested by running FastAPI server with trained model endpoint and LLM chatbot that extracts WVS features from conversation and returns predictions.

**Acceptance Scenarios**:

1. **Given** trained model, **When** serialized and served via FastAPI, **Then** /predict endpoint accepts feature JSON and returns predicted fertility + drivers
2. **Given** LLM chatbot, **When** user conversation simulated, **Then** WVS features extracted into structured format matching model input schema
3. **Given** model prediction, **When** LLM interprets output, **Then** natural language insights generated with policy signposting

---

### User Story 5 - Professional Deliverables Package (Priority: P5)

Course evaluators need complete submission package (report, code, data, slides) meeting IS5126 specifications for reproducibility and presentation quality.

**Why this priority**: Direct requirement for course completion. Rubric allocates 20% to presentation/report quality.

**Independent Test**: Can be fully tested by verifying zip file contains all required artifacts and report follows 15-page guideline with methods, results, insights.

**Acceptance Scenarios**:

1. **Given** analysis complete, **When** report drafted, **Then** includes problem formulation, data work, methods, interpretation, limitations per rubric
2. **Given** code notebooks, **When** executed sequentially, **Then** reproduces all figures/tables in report from raw data
3. **Given** deliverables, **When** packaged, **Then** zip contains: PDF report, CSV data, .ipynb notebooks, .pptx slides, API endpoints documentation

---

### Edge Cases

- **Small Singapore sample (n<1,000)**: If Singapore subset smaller than expected, document power limitations and focus on effect sizes rather than p-values
- **High missingness (>20% in key variables)**: If critical predictors have excessive missing data, perform multiple imputation sensitivity analysis vs complete-case analysis
- **Model convergence issues**: If Poisson/negative binomial models fail to converge, fall back to OLS linear regression with documented justification
- **API deployment constraints**: If FastAPI deployment infeasible for demo, provide local testing instructions and mock conversation examples
- **HES integration failure**: If HES data mapping unsuccessful, proceed with WVS-only analysis per Constitution (HES is supplementary, not required)

## Requirements *(mandatory)*

### Functional Requirements

**Data Pipeline**

- **FR-001**: Load WVS Wave 7 CSV data (wvs_data_sample20rows.csv or full dataset) into pandas DataFrame with automated column detection
- **FR-002**: Filter respondents where `B_COUNTRY_ALPHA == "SGP"` to create Singapore subset
- **FR-003**: Apply age filter `25 <= Q262 <= 49` to focus on active family planning cohort
- **FR-004**: Document missing value codes (-1, -2, -3, -5) with count tables and handle via exclusion or imputation per documented rules
- **FR-005**: Generate data quality report showing sample size, missingness %, value ranges, outliers for all Q-codes
- **FR-006**: Export cleaned datasets to `Data/02 Clean/` with schema documentation and exclusion logs

**Feature Engineering**

- **FR-007**: Create target variable from Q274 (number of children) with validation for non-negative integers
- **FR-008**: Encode categorical predictors (Q260, Q273, Q275, Q288) using one-hot or ordinal encoding per variable type
- **FR-009**: Construct composite indices from attitudinal scales (family importance Q_FAMILY, gender Q_GENDER, religion Q_RELIG) using PCA or mean scoring
- **FR-010**: Generate interaction terms for theoretically motivated combinations (e.g., marital status × income, religiosity × gender attitudes)
- **FR-011**: Document feature transformations in metadata file mapping Q-codes to engineered features with interpretation guides

**Model Training**

- **FR-012**: Implement linear regression baseline using scikit-learn with Q274 as target, demographics + attitudes as predictors
- **FR-013**: Train Poisson regression for count data using statsmodels with model diagnostics (deviance, overdispersion tests)
- **FR-014**: Fit LASSO regularized regression with cross-validated alpha tuning for feature selection
- **FR-015**: Train ensemble methods (Random Forest, XGBoost/LightGBM) with hyperparameter tuning via GridSearchCV or Optuna
- **FR-016**: Serialize trained models to `.pkl` or `.joblib` format in `Modelling/Outputs/` directory

**Model Validation**

- **FR-017**: Perform 10-fold cross-validation on Singapore data with stratified splits by age group
- **FR-018**: Compute performance metrics: R², RMSE, MAE for continuous; pseudo-R² for count models
- **FR-019**: Generate coefficient tables with p-values, confidence intervals, standardized effect sizes
- **FR-020**: Create residual diagnostic plots (Q-Q plots, residuals vs fitted, scale-location) for assumption validation
- **FR-021**: Test model on comparable countries (Hong Kong, Taiwan, South Korea) for generalizability assessment
- **FR-022**: Document model comparison table showing performance across methods with winner selection criteria

**LLM Integration**

- **FR-023**: Build FastAPI service with `/predict` endpoint accepting JSON feature payload and returning fertility prediction + feature importance
- **FR-024**: Implement conversational LLM (GPT-4 or Claude) integration that extracts WVS features from natural language user input
- **FR-025**: Design prompt template that maps chatbot responses to Q-code schema (e.g., "family is important" → Q1 = 1)
- **FR-026**: Create LLM interpretation layer that generates natural language insights from model predictions with policy signposting
- **FR-027**: Provide example conversation flow demonstrating data collection → prediction → interpretation workflow

**Documentation & Deliverables**

- **FR-028**: Generate Jupyter notebooks with clear sections: Introduction, Data Loading, EDA, Preprocessing, Modeling, Results, Conclusions
- **FR-029**: Create comprehensive README with setup instructions, dependency requirements, execution order, expected outputs
- **FR-030**: Draft 15-page report following IS5126 rubric structure: Problem, Data Work, Methods, Results, Insights, Limitations, References

### Non-Functional Requirements

- **NFR-001**: All code must be executable in Google Colab or local Jupyter environment with Python 3.8+
- **NFR-002**: Execution time for full pipeline <30 minutes on standard hardware (excluding model tuning)
- **NFR-003**: All visualizations must follow consistent color scheme with accessible colorblind-friendly palettes
- **NFR-004**: Code must pass pylint checks with score ≥8.0 and follow PEP 8 style guidelines
- **NFR-005**: All data transformations must be logged with timestamps and reversibility documentation
- **NFR-006**: Model artifacts must include versioning metadata (training date, hyperparameters, performance metrics)

### Entity Relationships

**Primary Entities**:

- **Respondent**: Individual survey participant (row-level unit)
  - Attributes: B_COUNTRY_ALPHA, Q262 (age), Q260 (sex), Q274 (children), Q1-Q288 (survey responses)
  - Relationships: Belongs to Country, belongs to Age Cohort, has Multiple Responses

- **Feature Set**: Processed predictor variables
  - Attributes: feature_name, data_type, encoding_method, source_q_code
  - Relationships: Derived from Respondent, used by Model

- **Model**: Trained statistical/ML model
  - Attributes: model_type, hyperparameters, training_date, performance_metrics
  - Relationships: Trained on Feature Set, produces Predictions, generates Interpretations

- **Prediction**: Model output for fertility estimation
  - Attributes: respondent_id, predicted_children, feature_importance, confidence_interval
  - Relationships: Generated by Model, linked to Respondent

**Data Flow**:
```
Raw CSV → Singapore Subset → Cleaned Data → Engineered Features → Trained Models → Predictions → LLM Insights
```

**Key Constraints**:
- Singapore subset must have n ≥ 500 for statistical power (target n ≈ 1,000-2,000)
- Age filter 25-49 strictly enforced (no exceptions per refined proposal)
- Models must use same train/test split for fair comparison
- LLM integration uses trained model as backend (not training LLM itself)

## Success Criteria *(mandatory)*

### Data Quality Metrics

- **SC-001**: Singapore subset size n ≥ 500 respondents after all filters applied (target n ≈ 1,000-2,000)
- **SC-002**: Missing data documentation complete for all Q-codes with >5% missingness, showing code counts and handling strategy
- **SC-003**: Data quality report shows ≤ 10% outliers flagged for investigation across numeric variables
- **SC-004**: Feature engineering metadata file maps all engineered features back to source Q-codes with clear interpretation guidance

### Model Performance Metrics

- **SC-005**: Baseline linear regression achieves R² ≥ 0.15 on Singapore data (indicating meaningful explanatory power beyond noise)
- **SC-006**: Poisson/count model shows no severe overdispersion (dispersion parameter <3.0) or convergence warnings
- **SC-007**: Cross-validation metrics stable across folds (RMSE coefficient of variation <20%)
- **SC-008**: At least 3 predictors show statistically significant effects (p < 0.05) with theoretically sensible coefficient signs
- **SC-009**: Model comparison table identifies best-performing method based on defined criteria (R², interpretability, parsimony)

### Reproducibility Metrics

- **SC-010**: All notebooks execute sequentially without errors in fresh Python 3.8+ environment after installing `requirements.txt`
- **SC-011**: Pipeline recreates all report figures/tables from raw CSV with <1% numerical difference (accounting for random seed)
- **SC-012**: Exclusion logs show exact respondent counts at each filtering step, summing to total sample size
- **SC-013**: Model artifacts include versioning metadata (date, hyperparameters, performance) enabling future retraining comparisons

### LLM Integration Metrics

- **SC-014**: FastAPI `/predict` endpoint returns prediction + feature importance JSON in <2 seconds for single request
- **SC-015**: LLM chatbot extracts ≥70% of required WVS features correctly from sample conversation (validated against ground truth mapping)
- **SC-016**: LLM interpretation layer generates coherent natural language insights (no hallucinations, policy signposting present)
- **SC-017**: Example conversation flow demonstrates full cycle: user input → feature extraction → prediction → interpretation

### Deliverables Quality Metrics

- **SC-018**: Report follows 15-page guideline with all required sections (Problem, Data, Methods, Results, Insights, Limitations, References)
- **SC-019**: Code README enables independent reproduction with clear setup steps, dependency list, execution order
- **SC-020**: Submission package contains all artifacts: PDF report, CSV data, .ipynb notebooks, .pptx slides, API documentation
- **SC-021**: Visualizations use colorblind-friendly palettes and include axis labels, legends, titles per academic standards

### Academic Rigor Metrics

- **SC-022**: Limitations section explicitly addresses cross-sectional design, no causal claims, Singapore-specific findings, sample size constraints
- **SC-023**: Model assumptions documented with diagnostic tests (residual plots for OLS, deviance tests for Poisson)
- **SC-024**: Feature importance interpretations reference WVS codebook definitions and avoid overgeneralization beyond data scope

## Assumptions *(mandatory)*

### Data Assumptions

1. **WVS Wave 7 completeness**: Full dataset contains Singapore respondents with n ≥ 500 after age filtering (sample CSV shows SGP entries exist)
2. **Q274 validity**: Self-reported number of children is accurate and reflects actual fertility (no systematic misreporting)
3. **Missing data mechanism**: Missing values (-1, -2, -3, -5) are Missing At Random (MAR) or Missing Completely At Random (MCAR), not Missing Not At Random (MNAR)
4. **Q-code stability**: Variable meanings consistent across WVS documentation and actual dataset (no undocumented recoding)

### Technical Assumptions

5. **Python environment**: Execution environment has Python 3.8+ with standard data science libraries (pandas, numpy, scikit-learn, statsmodels)
6. **Computational resources**: Standard laptop/cloud environment sufficient for Singapore subset analysis (no GPU/cluster needed)
7. **API access**: If LLM integration requires API keys (OpenAI, Anthropic), user has valid credentials with sufficient quota

### Methodological Assumptions

8. **Cross-sectional validity**: Despite temporal limitations, cross-sectional patterns provide meaningful insights for policy exploration
9. **Singapore focus**: Singapore-specific findings provide sufficient value even if generalizability limited
10. **Baseline models sufficient**: Simple interpretable models (OLS, Poisson) provide actionable insights; complex ML models are supplementary

## Dependencies *(mandatory)*

### Internal Dependencies (Within Project)

- **Constitution compliance**: All implementation must follow IS5126 Constitution v1.0.0 principles (Reproducibility First, Simplicity Over Complexity, Data Quality Gates, Limitation-Aware Interpretation, Modular Notebooks)
- **Refined proposal alignment**: Analysis design follows specifications in `Docs/refined_proposal.md` (age filter 25-49, Singapore focus, HES integration strategy)
- **Data availability**: Raw WVS data must be accessible in `Data/01 Raw/` before pipeline execution
- **Directory structure**: Existing folder structure (`Data/`, `Scripts/`, `Modelling/`, `Docs/`) must be maintained per project organization

### External Dependencies

**Data Sources**:
- WVS Wave 7 (2017-2021): Official dataset download from World Values Survey website or pre-loaded CSV
- HES 2022/23 (supplementary): If HES integration pursued, requires SINGSTAT access and join key mapping

**Python Libraries** (minimum versions):
- pandas ≥ 1.3.0: Data manipulation
- numpy ≥ 1.21.0: Numerical operations
- scikit-learn ≥ 1.0.0: Modeling, cross-validation, preprocessing
- statsmodels ≥ 0.13.0: Statistical models (OLS, Poisson, diagnostics)
- matplotlib ≥ 3.4.0: Visualization
- seaborn ≥ 0.11.0: Statistical plots
- scipy ≥ 1.7.0: Statistical tests
- fastapi ≥ 0.68.0 (optional): LLM integration API backend
- uvicorn ≥ 0.15.0 (optional): FastAPI server
- openai ≥ 0.27.0 or anthropic ≥ 0.3.0 (optional): LLM API clients

**Development Tools**:
- Jupyter Notebook or JupyterLab: Interactive development
- Git: Version control (already initialized)
- pylint: Code quality checks (NFR-004)

### Academic Dependencies

- **WVS Codebook**: Official documentation for Q-code interpretations and value mappings
- **IS5126 Rubric**: Final project grading criteria (from `Docs/final_group_project_2025.txt`)
- **Statistical theory**: Understanding of regression diagnostics, count data models, cross-validation principles

## Out of Scope *(mandatory)*

### Explicitly Excluded

1. **Causal inference**: No causal claims, instrumental variable analysis, difference-in-differences, or regression discontinuity designs (cross-sectional data limitation)
2. **Longitudinal analysis**: No panel data models, growth curve modeling, or within-subject comparisons (single wave of data)
3. **Advanced deep learning**: No neural networks, transformers, or LLM fine-tuning for prediction (focus on interpretability per Constitution Principle II)
4. **Production deployment**: No cloud hosting, containerization (Docker/Kubernetes), CI/CD pipelines, or monitoring infrastructure (prototype only)
5. **Multi-country hierarchical models**: No mixed-effects models with country-level random effects (Singapore-focused analysis)
6. **Survey weighting**: No complex survey design adjustments or population weighting (unless explicitly required by WVS documentation)
7. **HES mandatory integration**: HES data is supplementary; project proceeds without it if integration infeasible (per refined proposal Section 10.4)

### Future Considerations (Not This Phase)

- **Real-time data collection**: Integration with live survey platforms for continuous model updating
- **Mobile app development**: Native iOS/Android apps for chatbot interface
- **Multi-language support**: Chatbot localization beyond English
- **Advanced feature engineering**: Sentiment analysis of open-ended responses, topic modeling, network analysis of social values
- **External validation**: Testing on non-WVS datasets (DHS, Pew Global Attitudes)
- **Policy simulation**: Counterfactual scenario modeling for policy impact assessment

### Boundaries

- **Scope limited to IS5126 deliverables**: Project prioritizes meeting course requirements over research publication standards
- **Timeline constrained**: Analysis completed within academic semester timeframe (no multi-year longitudinal follow-up)
- **Resource constrained**: Standard computing environment only (no access to supercomputing clusters or proprietary data sources)
