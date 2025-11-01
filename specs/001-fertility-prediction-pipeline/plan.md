# Implementation Plan: Fertility Prediction Data Science Pipeline

**Branch**: `001-fertility-prediction-pipeline` | **Date**: 2025-11-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-fertility-prediction-pipeline/spec.md`

## Summary

Build end-to-end data science pipeline for predicting fertility (number of children) using World Values Survey (WVS) Wave 7 data, focusing on Singapore respondents aged 25-49. Pipeline implements reproducible data processing, interpretable baseline models (linear regression, Poisson), advanced ML methods (LASSO, ensemble models), rigorous validation via cross-validation and comparative analysis, and LLM integration prototype using Langchain + FastAPI for conversational data collection and personalized insights. Deliverables include Jupyter notebooks (modular, single-stage), Python utils library, 15-page academic report, and API endpoints meeting IS5126 rubric requirements.

## Technical Context

**Language/Version**: Python 3.8+  
**Primary Dependencies**: 
- Data: pandas ≥1.3.0, numpy ≥1.21.0
- Modeling: scikit-learn ≥1.0.0, statsmodels ≥0.13.0, xgboost, lightgbm
- Visualization: matplotlib ≥3.4.0, seaborn ≥0.11.0
- LLM: langchain ≥0.1.0, openai ≥0.27.0 or anthropic ≥0.3.0
- API: fastapi ≥0.68.0, uvicorn ≥0.15.0, pydantic

**Storage**: CSV files (WVS raw data in `Data/01 Raw/`, cleaned in `Data/02 Clean/`, transformed in `Data/03 Transformed/`)  
**Testing**: pytest for utils.py functions, notebook execution tests via papermill  
**Target Platform**: Local Jupyter environment or Google Colab, FastAPI server for LLM integration  
**Project Type**: Data science project (notebooks + utils library + API service)  
**Performance Goals**: Pipeline execution <30 minutes for Singapore subset (n≈1,000-2,000), API response <2 seconds per prediction  
**Constraints**: Singapore sample n ≥ 500, age filter 25-49 strictly enforced, models must be interpretable (coefficients + p-values), LLM integration prototype-only (no production deployment)  
**Scale/Scope**: ~97k WVS respondents globally, Singapore subset n≈1,000-2,000, 30 functional requirements, 5 user stories, 6 modular notebooks, 1 utils.py library, 1 FastAPI service

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Reproducibility First ✅
- **Requirement**: All analysis reproducible from raw data with fixed seeds, environment specs, documentation
- **Implementation**: 
  - `requirements.txt` with pinned versions (pandas ≥1.3.0, scikit-learn ≥1.0.0)
  - Every notebook includes random seed setting (`np.random.seed(42), random_state=42`)
  - Execution order documented in README with clear inputs/outputs per notebook
  - Exclusion logs track every data filter with counts
- **Status**: COMPLIANT - FR-010, FR-028, FR-029, SC-010 to SC-013

### Principle II: Simplicity Over Complexity ✅
- **Requirement**: Interpretable models preferred (linear, Poisson), complexity justified by performance
- **Implementation**:
  - User Story 2 (P2) prioritizes baseline models over advanced ML
  - Linear regression + Poisson as primary methods (FR-012, FR-013)
  - Ensemble models (FR-015) secondary, used for feature importance validation
  - No deep learning (explicitly excluded in Out of Scope)
  - Modular notebooks with single-stage focus (Constitution Principle V)
- **Status**: COMPLIANT - User Story 2 priority, Out of Scope section

### Principle III: Data Quality Gates (NON-NEGOTIABLE) ✅
- **Requirement**: Document input validation, missing value handling, outlier detection, filter rationale
- **Implementation**:
  - FR-004: Missing value documentation (-1, -2, -3, -5 codes) with count tables
  - FR-005: Data quality report (sample size, missingness %, value ranges, outliers)
  - SC-002: Missingness docs for all Q-codes >5% missingness
  - SC-003: Outlier flagging ≤ 10% threshold
  - SC-012: Exclusion logs show exact respondent counts at each step
- **Status**: COMPLIANT - FR-004 to FR-006, SC-001 to SC-004

### Principle IV: Limitation-Aware Interpretation ✅
- **Requirement**: Findings presented with explicit caveats (cross-sectional, temporal, no causality)
- **Implementation**:
  - SC-022: Limitations section addresses cross-sectional design, no causal claims, Singapore-specific
  - Edge cases documented (small sample, high missingness, convergence issues)
  - Refined proposal Section 10 (Study Limitations) with 7 categories integrated
  - Model performance expectations realistic (SC-005: R² ≥ 0.15, not 0.90)
- **Status**: COMPLIANT - SC-022 to SC-024, proposal Section 10 alignment

### Principle V: Modular Notebooks ✅
- **Requirement**: Notebooks organized by phase, standalone executable, clear inputs/outputs
- **Implementation**:
  - 6 notebooks planned (see Project Structure below):
    1. Data Loading & EDA
    2. Data Cleaning & Preprocessing
    3. Feature Engineering
    4. Model Training (Baseline)
    5. Model Validation & Comparison
    6. LLM Integration Prototype
  - Each notebook single-stage (FR-028: clear sections)
  - utils.py centralizes reusable functions (user requirement)
  - NFR-001: All notebooks executable in fresh environment
- **Status**: COMPLIANT - FR-028, user-specified modular architecture

**GATE RESULT**: ✅ PASS - All 5 principles compliant, no violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/001-fertility-prediction-pipeline/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification (completed)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (API schemas)
│   └── api-schema.yaml  # FastAPI endpoint definitions
├── checklists/          # Quality validation
│   └── requirements.md  # Requirements checklist (completed)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

**EXISTING STRUCTURE** (per user requirement: "do not add new subfolders or folders without asking"):

```text
is5126_finalproj/
├── Data/
│   ├── 01 Raw/                    # WVS CSV, HES data (if available)
│   │   └── wvs_data_sample20rows.csv
│   ├── 02 Clean/                  # Post-cleaning datasets (FR-006 output)
│   │   ├── singapore_subset.csv
│   │   ├── exclusion_log.csv
│   │   └── data_quality_report.csv
│   └── 03 Transformed/            # Engineered features (FR-011 output)
│       ├── features_train.csv
│       ├── features_test.csv
│       └── feature_metadata.json
│
├── Scripts/
│   ├── preprocessing.ipynb        # EXISTING - to be expanded
│   ├── test_script.py             # EXISTING - to be adapted
│   ├── utils.py                   # NEW - Centralized function library
│   │                              # Contains: load_wvs(), filter_singapore(),
│   │                              # handle_missing(), encode_categorical(),
│   │                              # train_model(), cross_validate(), etc.
│   ├── 01_data_loading_eda.ipynb          # NEW - User Story 1 (P1)
│   ├── 02_data_cleaning.ipynb             # NEW - User Story 1 (P1)
│   ├── 03_feature_engineering.ipynb       # NEW - User Story 1 (P1)
│   ├── 04_model_training_baseline.ipynb   # NEW - User Story 2 (P2)
│   ├── 05_model_validation.ipynb          # NEW - User Story 3 (P3)
│   └── 06_llm_integration.ipynb           # NEW - User Story 4 (P4)
│
├── Modelling/
│   ├── LLMs/
│   │   ├── api_service.py         # NEW - FastAPI server (FR-023)
│   │   ├── langchain_agent.py     # NEW - Langchain chatbot (FR-024 to FR-027)
│   │   ├── prompts/               # NEW - LLM prompt templates
│   │   │   ├── feature_extraction.txt
│   │   │   └── interpretation.txt
│   │   └── requirements.txt       # LLM-specific dependencies
│   │
│   ├── Notebooks/                 # Empty - notebooks are in Scripts/
│   │
│   ├── Outputs/                   # Model artifacts (FR-016)
│   │   ├── models/
│   │   │   ├── linear_regression.pkl
│   │   │   ├── poisson_regression.pkl
│   │   │   ├── lasso_regression.pkl
│   │   │   └── ensemble_model.pkl
│   │   ├── metrics/
│   │   │   ├── cv_results.json
│   │   │   ├── model_comparison.csv
│   │   │   └── feature_importance.csv
│   │   └── visualizations/
│   │       ├── residual_plots/
│   │       ├── feature_importance/
│   │       └── coefficient_plots/
│   │
│   └── utils/                     # Empty - utils consolidated in Scripts/utils.py
│
├── Docs/
│   ├── final_group_project_2025.txt       # EXISTING - IS5126 rubric
│   ├── new_proposal.md                    # EXISTING - original proposal
│   ├── refined_proposal.md                # EXISTING - refined proposal
│   ├── WVS Survey.md                      # EXISTING - survey documentation
│   ├── Presentation/
│   │   └── README.md
│   └── Report/
│       └── README.md
│
├── .specify/                      # Speckit workflow (generated)
├── .github/                       # Prompts and workflows
├── specs/                         # Feature specifications
├── requirements.txt               # NEW - Python dependencies
└── README.md                      # NEW - Project setup and execution guide (FR-029)
```

**Structure Decision**: 
- **Notebooks in `Scripts/`**: Per user requirement, all `.ipynb` files in existing `Scripts/` folder (not `Modelling/Notebooks/`)
- **Single `utils.py`**: Per user requirement, all reusable functions centralized in `Scripts/utils.py` (not `Modelling/utils/`)
- **6 modular notebooks**: Each performs single stage (Constitution Principle V): loading, cleaning, features, training, validation, LLM
- **LLM code in `Modelling/LLMs/`**: FastAPI service and Langchain agent separate from notebooks per existing structure
- **No new top-level folders**: Utilized existing `Data/`, `Scripts/`, `Modelling/`, `Docs/` structure

## Complexity Tracking

**No violations detected - section not applicable.**

All Constitution principles compliant (see Constitution Check above). No additional complexity beyond what's justified by project requirements and academic standards.

---

## Phase 0: Research & Technology Decisions ✅

**Status**: COMPLETE  
**Output**: [`research.md`](research.md)

**Key Decisions Documented**:
1. **R1**: WVS data loading strategy (pandas with schema validation)
2. **R2**: Missing value handling (multi-strategy: MICE for 5-20%, exclusion >20%)
3. **R3**: Count data modeling (Poisson → Negative Binomial if overdispersion)
4. **R4**: Cross-validation strategy (10-fold stratified by age)
5. **R5**: Feature selection (domain knowledge → univariate → LASSO)
6. **R6**: Langchain architecture (ConversationChain + function calling)
7. **R7**: FastAPI endpoint design (single `/predict` POST with Pydantic validation)
8. **R8**: Visualization best practices (Seaborn with colorblind palettes)
9. **R9**: Notebook organization (6 sequential notebooks, linear dependency)
10. **R10**: Testing strategy (pytest for utils.py, 80% coverage target)

**All NEEDS CLARIFICATION items from Technical Context resolved.**

---

## Phase 1: Design & Contracts ✅

**Status**: COMPLETE  
**Outputs**: 
- [`data-model.md`](data-model.md)
- [`contracts/api-schema.yaml`](contracts/api-schema.yaml)
- [`quickstart.md`](quickstart.md)
- `.github/copilot-instructions.md` (agent context updated)

### Phase 1 Deliverables

#### 1. Data Model (`data-model.md`)
**Entities Defined**: 6 core entities with validation rules
- WVS Respondent (survey participant, row-level)
- Feature Set (engineered predictors)
- Model (trained statistical/ML models)
- Prediction (model outputs)
- Data Quality Report (transformation metadata)
- HES Spending Data (optional supplementary)

**Data Flow**: Linear pipeline through 6 notebooks documented with state transitions

**Validation Rules**: Schema checks, age/Singapore filters, sample size thresholds, feature encoding standards

#### 2. API Contracts (`contracts/api-schema.yaml`)
**OpenAPI 3.0 Specification** for FastAPI service:
- **POST /predict**: Main prediction endpoint
  - Input: PredictionRequest (9 required WVS features: Q1, Q260, Q262, Q273, Q275, Q288, Q28, Q37, Q38)
  - Output: PredictionResponse (predicted_children, confidence_interval, drivers, metadata)
  - Validation: Pydantic schemas with min/max constraints
- **GET /health**: Health check endpoint
- **GET /models**: List available models
- **Components**: 8 schemas (PredictionRequest, PredictionResponse, FeatureImportance, ErrorResponse, etc.)

**Contract Compliance**: All endpoints align with FR-023 to FR-027 (LLM Integration requirements)

#### 3. Quickstart Guide (`quickstart.md`)
**Complete setup and execution guide**:
- Prerequisites (Python 3.8+, Jupyter, API keys)
- Environment setup (venv, pip install, API key configuration)
- Pipeline execution (6 notebooks with runtime estimates)
- LLM integration testing (FastAPI server, cURL examples, Langchain chatbot)
- Troubleshooting (10 common issues with solutions)
- Next steps (deliverables, quality checks, extensions)

**User-Friendly**: Step-by-step PowerShell commands for Windows environment per user context

#### 4. Agent Context Update
**Updated**: `.github/copilot-instructions.md`
- Added Python 3.8+ as project language
- Added CSV files storage context
- Added data science project type
- Preserved manual additions between markers

---

## Constitution Check (Post-Design Re-Evaluation)

*GATE: Re-check after Phase 1 design complete.*

### Principle I: Reproducibility First ✅
**Design Validation**:
- Data model includes pipeline_state.json for tracking progress
- API schema includes model versioning metadata (training_date, hyperparameters)
- Quickstart guide provides complete setup instructions with verification steps
- research.md documents all technical decisions with rationale

**Status**: COMPLIANT - Design enforces reproducibility through metadata tracking and documentation

### Principle II: Simplicity Over Complexity ✅
**Design Validation**:
- Data model uses 6 entities (minimal for requirements)
- API has 3 endpoints (predict, health, models) - focused scope
- Notebook pipeline is linear (no complex DAG orchestration)
- research.md R9 confirms single responsibility per notebook

**Status**: COMPLIANT - Design maintains simplicity, no unnecessary abstractions

### Principle III: Data Quality Gates (NON-NEGOTIABLE) ✅
**Design Validation**:
- Data model defines validation rules for each entity (validate_wvs_schema, validate_clean_data, validate_features, validate_model)
- Data Quality Report entity tracks exclusions, missingness, outliers
- API schema enforces input validation (min/max, required fields)
- Quickstart includes sample size verification steps

**Status**: COMPLIANT - Quality gates embedded in entity validation

### Principle IV: Limitation-Aware Interpretation ✅
**Design Validation**:
- API response includes confidence_interval (acknowledges uncertainty)
- Model metadata includes r_squared, rmse (transparent performance)
- research.md documents all assumption trade-offs
- Quickstart troubleshooting section addresses realistic issues

**Status**: COMPLIANT - Design promotes transparent limitations

### Principle V: Modular Notebooks ✅
**Design Validation**:
- Data model data flow shows 6 distinct stages matching 6 notebooks
- Each notebook has clear input/output contract (documented in data-model.md)
- Quickstart execution order enforces sequential dependency
- pipeline_state.json tracks completed_notebooks

**Status**: COMPLIANT - Modular design validated

**GATE RESULT (Post-Design)**: ✅ PASS - All 5 principles remain compliant after design phase

---

## Phase 2: Task Generation (NOT PART OF /speckit.plan)

**Status**: PENDING  
**Next Command**: `/speckit.tasks`  
**Purpose**: Break down Phase 1 design into actionable implementation tasks

Phase 2 will generate `tasks.md` with:
- Task breakdown from FR-001 to FR-030
- Dependencies between tasks
- Estimated effort (hours)
- Acceptance criteria per task
- Grouped by notebook (01-06)

**Do not proceed with Phase 2 until `/speckit.tasks` command executed.**

---

## Summary & Next Steps

### ✅ Completed in This Plan

| Phase | Output | Status | Lines |
|-------|--------|--------|-------|
| Phase 0 | research.md | ✅ Complete | 400+ |
| Phase 1 | data-model.md | ✅ Complete | 500+ |
| Phase 1 | contracts/api-schema.yaml | ✅ Complete | 300+ |
| Phase 1 | quickstart.md | ✅ Complete | 400+ |
| Phase 1 | copilot-instructions.md | ✅ Updated | - |

**Total Documentation**: ~1,600+ lines across 4 files

### 🎯 Feature Readiness

**Branch**: `001-fertility-prediction-pipeline`  
**Spec File**: `specs/001-fertility-prediction-pipeline/spec.md`  
**Plan File**: `specs/001-fertility-prediction-pipeline/plan.md` (this file)

**Readiness Gates**:
- ✅ Constitution Check passed (pre-design and post-design)
- ✅ Technical Context resolved (no NEEDS CLARIFICATION)
- ✅ Data model defined with 6 entities, validation rules, state transitions
- ✅ API contracts specified (OpenAPI 3.0)
- ✅ Quickstart guide created (setup, execution, troubleshooting)
- ✅ Agent context updated

**Ready for**: `/speckit.tasks` command to generate implementation tasks

### 📋 Recommended Next Actions

1. **Review Planning Artifacts**:
   - Read `research.md` to understand technology stack decisions
   - Review `data-model.md` for entity relationships and validation rules
   - Check `contracts/api-schema.yaml` for API endpoint specifications
   - Follow `quickstart.md` for initial environment setup

2. **Run `/speckit.tasks`**:
   - Generates `tasks.md` with breakdown of FR-001 to FR-030
   - Provides task dependencies and effort estimates
   - Groups tasks by notebook for implementation order

3. **Begin Implementation** (after tasks generated):
   - Create `Scripts/utils.py` with utility functions
   - Implement `Scripts/01_data_loading_eda.ipynb` (User Story 1, P1)
   - Follow notebook sequence per quickstart guide
   - Run pytest on utils.py functions as implemented

4. **Track Progress**:
   - Update `Data/pipeline_state.json` as notebooks complete
   - Check Constitution compliance per `.specify/memory/constitution.md`
   - Validate against requirements checklist (`specs/001-fertility-prediction-pipeline/checklists/requirements.md`)

---

## Artifact Locations

All generated artifacts in `specs/001-fertility-prediction-pipeline/`:
```
specs/001-fertility-prediction-pipeline/
├── spec.md                      # Feature specification (from /speckit.specify)
├── plan.md                      # This file (from /speckit.plan)
├── research.md                  # Phase 0 output
├── data-model.md                # Phase 1 output
├── quickstart.md                # Phase 1 output
├── contracts/
│   └── api-schema.yaml          # Phase 1 output
├── checklists/
│   └── requirements.md          # Validation checklist (from /speckit.specify)
└── tasks.md                     # PENDING - /speckit.tasks will generate
```

**Next**: Execute `/speckit.tasks` to proceed to implementation phase.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
