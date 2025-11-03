# Fertility Prediction Pipeline - IS5126 Final Project

> **Predicting Fertility Intentions: Understanding Value-Based Drivers of Family Size in Singapore**

An end-to-end data science project leveraging the World Values Survey (WVS) Wave 7 dataset to predict fertility outcomes and identify attitudinal drivers of family size decisions in Singapore.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [LLM Integration](#llm-integration)
- [Project Specifications](#project-specifications)
- [Contributing](#contributing)

---

## Project Overview

### Research Objectives

**Primary Objective**: Develop predictive models to identify key attitudinal and value-based factors associated with fertility outcomes (number of children) among Singaporeans of childbearing age.

**Secondary Objectives**:
1. Compare Singapore-specific patterns with global trends to identify culturally unique factors
2. Integrate household economic data to understand the relationship between values, spending patterns, and fertility
3. Develop an AI-powered advisory tool to provide personalized insights on family planning considerations

### Key Features

- **Reproducible Pipeline**: Modular notebooks covering data loading → cleaning → feature engineering → modeling → validation
- **Interpretable Models**: Baseline models (Linear Regression, Poisson) with clear coefficient interpretation
- **Advanced Validation**: K-fold cross-validation and comparative analysis across countries
- **LLM Integration**: Interactive chatbot using Langchain + FastAPI for conversational data collection
- **Professional Deliverables**: Complete documentation, report templates, and presentation materials

### Technology Stack

- **Python 3.8+**: Core programming language
- **Data Science**: pandas, numpy, scikit-learn, statsmodels, scipy
- **Visualization**: matplotlib, seaborn
- **Machine Learning**: xgboost, lightgbm
- **LLM Integration**: langchain, openai, fastapi, uvicorn
- **Development**: jupyter, pytest

---

## Repository Structure

```
is5126_finalproj/
│
├── Data/                          # Data pipeline artifacts
│   ├── 01 Raw/                    # Original datasets (WVS, HES)
│   │   └── wvs_data_sample20rows.csv
│   ├── 02 Clean/                  # Cleaned datasets after preprocessing
│   ├── 03 Transformed/            # Feature-engineered datasets
│   └── Scripts/                   # Data processing notebooks
│       └── preprocessing.ipynb    # Initial data exploration
│
├── Docs/                          # Project documentation
│   ├── refined_proposal.md        # Research proposal and objectives
│   ├── WVS Survey.md             # WVS dataset documentation
│   ├── final_group_project_2025.pdf  # Course requirements
│   ├── Presentation/              # Presentation materials
│   └── Report/                    # Final report materials
│
├── Modelling/                     # Machine learning pipeline
│   ├── LLMs/                      # LLM integration components
│   │   └── utils.py              # Langchain agent implementation
│   ├── Notebooks/                 # Model training notebooks (planned)
│   ├── Outputs/                   # Trained models and results
│   └── utils/                     # Shared modeling utilities
│
├── specs/                         # Project specifications
│   └── 001-fertility-prediction-pipeline/
│       ├── spec.md               # Feature specification
│       ├── plan.md               # Implementation plan
│       ├── research.md           # Technology research decisions
│       ├── data-model.md         # Data models and schemas
│       ├── quickstart.md         # Quick start guide
│       ├── contracts/            # API contracts
│       └── checklists/           # Quality assurance checklists
│
└── README.md                      # This file
```

### Key Directory Purposes

#### `Data/`
Contains the complete data pipeline from raw survey data to model-ready features:
- **01 Raw/**: Unmodified source data (WVS CSV, HES spending data)
- **02 Clean/**: Cleaned data after handling missing values, outliers, and applying filters
- **03 Transformed/**: Feature-engineered datasets ready for model training
- **Scripts/**: Jupyter notebooks for data processing and exploration

#### `Docs/`
Comprehensive project documentation:
- Research proposal with detailed objectives and methodology
- WVS survey codebook and variable descriptions
- Course rubric and requirements (final_group_project_2025.pdf)
- Presentation and report templates

#### `Modelling/`
Machine learning pipeline and model artifacts:
- **LLMs/**: Langchain agent and FastAPI service for LLM integration
- **Notebooks/**: Modular notebooks for model training and validation (planned: 01-06)
- **Outputs/**: Trained model files (.pkl), evaluation metrics, visualizations
- **utils/**: Shared utility functions for modeling

#### `specs/`
Detailed project specifications following speckit methodology:
- **spec.md**: Complete feature specification with user stories and acceptance criteria
- **plan.md**: Phased implementation plan with constitution compliance
- **research.md**: Technology decisions (WVS loading, missing values, model selection, etc.)
- **data-model.md**: Entity definitions, validation rules, data flow diagrams
- **quickstart.md**: Step-by-step setup and execution guide
- **contracts/**: API schemas (OpenAPI 3.0 for FastAPI endpoints)

---

## Getting Started

### Prerequisites

- **Python 3.8+** installed
- **Jupyter Notebook** or **JupyterLab**
- **Git** for version control
- **OpenAI API key** (for LLM integration)

### Installation

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/gooncaver/is5126_finalproj.git
   cd is5126_finalproj
   ```

2. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   # source venv/bin/activate    # Linux/Mac
   ```

3. **Install dependencies**:
   ```powershell
   pip install --upgrade pip
   pip install pandas numpy scikit-learn statsmodels matplotlib seaborn scipy
   pip install xgboost lightgbm jupyter pytest
   pip install langchain openai fastapi uvicorn pydantic requests python-dotenv
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **Important**: Never commit `.env` to version control!

### Quick Verification

Test your setup:
```powershell
python -c "import pandas, sklearn, langchain; print('All packages installed successfully!')"
```

---

## Usage Guide

### Data Pipeline Workflow

The project follows a modular 6-stage pipeline. Each notebook handles one stage:

#### Stage 1: Data Loading & EDA
**Notebook**: `Data/Scripts/preprocessing.ipynb` (current exploration notebook)  
**Planned**: `Scripts/01_data_loading_eda.ipynb`

**Inputs**: 
- `Data/01 Raw/wvs_data_sample20rows.csv` (sample)
- Full WVS Wave 7 CSV (to be downloaded)

**Outputs**:
- `Data/02 Clean/singapore_raw.csv` - Singapore subset (ages 25-49)
- Initial data quality report

**Runtime**: 2-5 minutes

#### Stage 2: Data Cleaning
**Planned**: `Scripts/02_data_cleaning.ipynb`

**Tasks**:
- Handle missing values (MICE for 5-20%, simple imputation <5%, exclude >20%)
- Apply filters (Singapore residents, childbearing age)
- Document exclusions

**Outputs**:
- `Data/02 Clean/singapore_clean.csv`
- `Data/02 Clean/exclusion_log.csv`
- Missingness analysis report

**Runtime**: 3-7 minutes

#### Stage 3: Feature Engineering
**Planned**: `Scripts/03_feature_engineering.ipynb`

**Tasks**:
- Create derived features (importance indices, value clusters)
- Encode categorical variables
- Train/test split

**Outputs**:
- `Data/03 Transformed/features_train.csv`
- `Data/03 Transformed/features_test.csv`
- `Data/03 Transformed/feature_metadata.json`

**Runtime**: 2-4 minutes

#### Stage 4: Model Training (Baseline)
**Planned**: `Scripts/04_model_training_baseline.ipynb`

**Models**:
- Linear Regression (interpretability baseline)
- Poisson Regression (count data specialist)
- Ridge/Lasso (regularization)

**Outputs**:
- `Modelling/Outputs/models/linear_baseline.pkl`
- `Modelling/Outputs/models/poisson_baseline.pkl`
- `Modelling/Outputs/metrics/baseline_performance.csv`

**Runtime**: 5-10 minutes

#### Stage 5: Model Validation
**Planned**: `Scripts/05_model_validation.ipynb`

**Tasks**:
- 10-fold stratified cross-validation
- Model comparison (R², RMSE, interpretability)
- Residual diagnostics

**Outputs**:
- `Modelling/Outputs/metrics/cv_results.csv`
- `Modelling/Outputs/visualizations/model_comparison.png`

**Runtime**: 8-15 minutes

#### Stage 6: LLM Integration Demo
**Planned**: `Scripts/06_llm_integration.ipynb`

**Tasks**:
- Load trained model into FastAPI
- Test Langchain agent conversation flow
- Generate sample predictions

**Outputs**:
- Demo logs
- Example conversations

**Runtime**: 3-5 minutes

### Running the Pipeline

**Option A: Run All Notebooks Sequentially**
```powershell
cd Data\Scripts
jupyter notebook
# Open and run each notebook in order: 01 → 02 → 03 → 04 → 05 → 06
```

**Option B: Run Individual Stages**
```powershell
jupyter notebook Scripts/03_feature_engineering.ipynb
```

---

## LLM Integration

The project includes a prototype LLM-powered chatbot for conversational fertility prediction.

### Architecture

```
User Question
    ↓
Langchain Agent (GPT-5)
    ↓
Feature Extraction (Function Calling)
    ↓
FastAPI Endpoint (/predict)
    ↓
Trained Model (Poisson/Linear)
    ↓
Prediction + Feature Importance
    ↓
LLM Interpretation
    ↓
Natural Language Response
```

### Quick Start

**1. Navigate to LLM directory**:
```powershell
cd Modelling\LLMs
```

**2. Review the agent implementation**:
- `utils.py`: Langchain agent with GPT-5 and prediction tool

**3. Run the agent**:
```powershell
python utils.py
```

**Expected Output**:
```
Loaded .env from path: C:\...\is5126_finalproj\.env
Key loaded: True

=== Full Conversation ===
Message 0: HumanMessage
Content: I am male, Q217 is True, Q281 is False. How many children will I have?

Message 1: AIMessage
Tool Calls: [predict_number_of_children(gender='male', Q217=True, Q281=False)]

Message 2: ToolMessage
Tool returned: 1

Message 3: AIMessage
Content: Based on the model prediction, you are likely to have 1 child...
```

### Advanced Usage (Planned)

When the FastAPI service is implemented:

**Terminal 1 - Start API Server**:
```powershell
cd Modelling\LLMs
python api_service.py
```

**Terminal 2 - Run Agent**:
```powershell
cd Modelling\LLMs
python utils.py
```

See `specs/001-fertility-prediction-pipeline/quickstart.md` for detailed LLM integration guide.

---

## Project Specifications

### Design Principles

The project follows a **Constitution-based Development** approach with 5 core principles:

1. **Reproducibility**: All analysis steps documented, versioned, and executable
2. **Simplicity**: Prefer interpretable models over black boxes
3. **Data Quality**: Transparent handling of missing data and outliers
4. **Limitations**: Explicit documentation of assumptions and constraints
5. **Modularity**: Each notebook performs one clear stage

### User Stories (Priority Order)

| Priority | Story | Description |
|----------|-------|-------------|
| **P1** | Reproducible Pipeline | Raw data → clean → features → models with full audit trail |
| **P2** | Interpretable Models | Linear/Poisson baselines with coefficient interpretation |
| **P3** | Model Validation | K-fold CV, comparative analysis, robustness checks |
| **P4** | LLM Integration | Langchain + FastAPI chatbot prototype |
| **P5** | Deliverables Package | Report, slides, code documentation |

### Success Criteria

**Data Quality**:
- ✅ Singapore subset: n ≈ 1,000-2,000 (ages 25-49)
- ✅ Missing value documentation: Counts for each code (-1, -2, -3, -5)
- ✅ Exclusion log: Justified removals at each filter step

**Model Performance**:
- Target: R² > 0.15 (modest but interpretable)
- Target: RMSE < 1.2 children
- Poisson overdispersion: Document if dispersion parameter > 2.0

**LLM Integration**:
- ✅ Feature extraction from natural language
- ✅ API response parsing and interpretation
- ✅ Conversational context maintenance

**Documentation**:
- ✅ Complete specification (spec.md)
- ✅ Implementation plan (plan.md)
- ✅ Technology research (research.md)
- ✅ API contracts (OpenAPI 3.0)

---

## Key Files Reference

### Documentation
| File | Purpose |
|------|---------|
| `Docs/refined_proposal.md` | Research objectives, dataset description, methodology |
| `Docs/WVS Survey.md` | WVS codebook and variable definitions |
| `specs/001-fertility-prediction-pipeline/spec.md` | Complete feature specification |
| `specs/001-fertility-prediction-pipeline/quickstart.md` | Step-by-step setup guide |

### Data
| File | Purpose |
|------|---------|
| `Data/01 Raw/wvs_data_sample20rows.csv` | Sample WVS data for testing |
| `Data/Scripts/preprocessing.ipynb` | Initial data exploration notebook |

### Implementation
| File | Purpose |
|------|---------|
| `Modelling/LLMs/utils.py` | Langchain agent implementation |
| `specs/001-fertility-prediction-pipeline/data-model.md` | Entity definitions and validation rules |
| `specs/001-fertility-prediction-pipeline/contracts/api-schema.yaml` | FastAPI OpenAPI specification |

---

## Development Workflow

### Branching Strategy

- **main**: Stable releases only
- **001-fertility-prediction-pipeline**: Active development branch

### Adding New Features

1. Review `specs/001-fertility-prediction-pipeline/spec.md` for requirements
2. Check `specs/001-fertility-prediction-pipeline/plan.md` for implementation phases
3. Consult `specs/001-fertility-prediction-pipeline/research.md` for technology decisions
4. Follow modular notebook structure (1 notebook = 1 stage)
5. Update documentation as you go

### Quality Assurance

- **Code Style**: Follow PEP 8 for Python
- **Testing**: Pytest for utility functions (target: 80% coverage)
- **Documentation**: Update README when adding major features
- **Version Control**: Meaningful commit messages

---

## Expected Deliverables

Upon completion, the project will produce:

### 1. Code Artifacts
- ✅ 6 modular Jupyter notebooks (data → models)
- ✅ Trained model files (.pkl)
- ✅ FastAPI service for model serving
- ✅ Langchain agent for LLM integration

### 2. Documentation
- ✅ Complete project specification
- ✅ Research methodology documentation
- ✅ API contracts (OpenAPI 3.0)
- Academic report (planned)

### 3. Visualizations
- Exploratory data analysis plots
- Feature importance rankings
- Model comparison charts
- Coefficient interpretation diagrams

### 4. Presentation
- Slide deck (planned)
- Demo video (optional)

---

## Contributing

This is an academic project for IS5126. For questions or suggestions:

1. Check `specs/001-fertility-prediction-pipeline/quickstart.md` for troubleshooting
2. Review `specs/001-fertility-prediction-pipeline/spec.md` for requirements
3. Consult course materials in `Docs/final_group_project_2025.pdf`

---

## License

This project is developed for academic purposes as part of the IS5126 course requirements.

---

## Acknowledgments

- **World Values Survey**: Data source
- **IS5126 Course Team**: Project guidance
- **Langchain**: LLM integration framework
- **FastAPI**: API framework

---

## Contact

**Repository**: [is5126_finalproj](https://github.com/gooncaver/is5126_finalproj)  
**Branch**: main  
**Last Updated**: November 2, 2025

---

**Ready to get started?** Head to [Getting Started](#getting-started) or jump to the [Quick Start Guide](specs/001-fertility-prediction-pipeline/quickstart.md)!
