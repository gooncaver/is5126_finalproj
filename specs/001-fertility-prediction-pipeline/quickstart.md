# Quickstart Guide: Fertility Prediction Pipeline

**Feature**: End-to-end data science project for predicting fertility using WVS data  
**Branch**: `001-fertility-prediction-pipeline`  
**Last Updated**: 2025-11-01

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Running the Pipeline](#running-the-pipeline)
4. [Testing the LLM Integration](#testing-the-llm-integration)
5. [Troubleshooting](#troubleshooting)
6. [Next Steps](#next-steps)

---

## Prerequisites

### Required Software
- **Python**: 3.8 or higher
- **Jupyter**: Notebook or JupyterLab (or use Google Colab)
- **Git**: For version control
- **Text Editor**: VS Code recommended

### Required Accounts (for LLM integration only)
- **OpenAI API Key** (for GPT-4) or **Anthropic API Key** (for Claude)
  - Get OpenAI key: https://platform.openai.com/api-keys
  - Get Anthropic key: https://console.anthropic.com/

### Hardware Requirements
- **RAM**: 4GB minimum (8GB recommended for ensemble models)
- **Storage**: 500MB free space
- **Processor**: Any modern CPU (no GPU required)

---

## Environment Setup

### Step 1: Clone Repository

```powershell
# Navigate to your projects directory
cd "C:\Users\user\OneDrive\Masters_Materials\IS5126\Final Project\final_proj_working"

# Clone if not already cloned
git clone <repository-url> is5126_finalproj
cd is5126_finalproj

# Switch to feature branch
git checkout 001-fertility-prediction-pipeline
```

### Step 2: Create Python Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# If PowerShell execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify Python version
python --version  # Should show Python 3.8+
```

### Step 3: Install Dependencies

```powershell
# Install core dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installations
python -c "import pandas, sklearn, statsmodels, seaborn; print('Core packages OK')"

# For LLM integration (optional - needed for User Story 4)
pip install langchain openai fastapi uvicorn pydantic

# Verify LLM packages
python -c "import langchain, openai, fastapi; print('LLM packages OK')"
```

**Expected `requirements.txt` contents** (create if missing):
```text
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
statsmodels>=0.13.0
matplotlib>=3.4.0
seaborn>=0.11.0
scipy>=1.7.0
xgboost>=1.5.0
lightgbm>=3.3.0
pytest>=7.0.0
jupyter>=1.0.0

# LLM integration (optional)
langchain>=0.1.0
openai>=0.27.0
# anthropic>=0.3.0  # Uncomment if using Claude
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.9.0
```

### Step 4: Set Up API Keys (Optional - for LLM integration)

```powershell
# Windows PowerShell - Set environment variable for session
$env:OPENAI_API_KEY = "sk-your-openai-api-key-here"

# Or create .env file in project root (more permanent)
# echo "OPENAI_API_KEY=sk-your-api-key" > .env
```

**Security Note**: Never commit `.env` files to Git. Add to `.gitignore`:
```text
# .gitignore
venv/
.env
*.pkl
*.joblib
Data/01 Raw/*.csv  # Large files
```

### Step 5: Verify Data Files

```powershell
# Check for raw data
ls "Data\01 Raw\"

# Should see: wvs_data_sample20rows.csv
# If full dataset needed, download from: https://www.worldvaluessurvey.org/
```

---

## Running the Pipeline

### Execution Order

Execute notebooks sequentially in `Scripts/` folder:

#### 📓 Notebook 1: Data Loading & EDA

```powershell
# Open in Jupyter
jupyter notebook "Scripts\01_data_loading_eda.ipynb"

# Or use VS Code Jupyter extension
code "Scripts\01_data_loading_eda.ipynb"
```

**What it does**:
- Loads WVS CSV from `Data/01 Raw/`
- Filters to Singapore respondents (`B_COUNTRY_ALPHA == 'SGP'`)
- Performs exploratory data analysis (distributions, correlations)
- **Output**: `Data/02 Clean/singapore_raw.csv` (n ≈ 1,000-2,000)

**Expected runtime**: 2-5 minutes

---

#### 📓 Notebook 2: Data Cleaning

```powershell
jupyter notebook "Scripts\02_data_cleaning.ipynb"
```

**What it does**:
- Applies age filter (25-49 years from Q262)
- Handles missing values (MICE for 5-20% missingness, exclusion >20%)
- Detects outliers (Z-score > 3)
- Generates data quality report
- **Output**: `Data/02 Clean/singapore_clean.csv`, `exclusion_log.csv`, `data_quality_report.csv`

**Expected runtime**: 3-7 minutes (MICE imputation can be slow)

**Key check**: Verify sample size ≥ 500 (Constitution SC-001)

---

#### 📓 Notebook 3: Feature Engineering

```powershell
jupyter notebook "Scripts\03_feature_engineering.ipynb"
```

**What it does**:
- Encodes categorical variables (one-hot for nominal, ordinal for ordered)
- Creates composite indices (family values, gender attitudes)
- Generates interaction terms (marital status × income)
- Splits into train/test sets (70/30 if n permits, else prepared for CV)
- **Output**: `Data/03 Transformed/features_train.csv`, `features_test.csv`, `feature_metadata.json`

**Expected runtime**: 2-4 minutes

**Key check**: Verify feature metadata maps all features to Q-codes (FR-011)

---

#### 📓 Notebook 4: Model Training (Baseline)

```powershell
jupyter notebook "Scripts\04_model_training_baseline.ipynb"
```

**What it does**:
- Trains linear regression (OLS) baseline
- Trains Poisson regression (checks for overdispersion)
- Trains LASSO with cross-validated alpha
- Optionally trains ensemble models (Random Forest, XGBoost)
- Serializes models to `Modelling/Outputs/models/*.pkl`
- **Output**: `linear_regression.pkl`, `poisson_regression.pkl`, `lasso_regression.pkl`, `baseline_results.json`

**Expected runtime**: 5-10 minutes (ensemble models slower)

**Key check**: Verify R² ≥ 0.15 for at least one model (SC-005)

---

#### 📓 Notebook 5: Model Validation

```powershell
jupyter notebook "Scripts\05_model_validation.ipynb"
```

**What it does**:
- Performs 10-fold cross-validation (stratified by age)
- Computes performance metrics (R², RMSE, MAE)
- Generates residual diagnostic plots
- Creates model comparison table
- Tests on comparable countries (Hong Kong, Taiwan, South Korea) if full WVS data available
- **Output**: `Modelling/Outputs/metrics/cv_results.json`, `model_comparison.csv`, visualizations

**Expected runtime**: 8-15 minutes (CV across folds)

**Key check**: Verify CV RMSE coefficient of variation <20% (SC-007)

---

#### 📓 Notebook 6: LLM Integration (Optional)

```powershell
# Requires OPENAI_API_KEY environment variable set
jupyter notebook "Scripts\06_llm_integration.ipynb"
```

**What it does**:
- Tests FastAPI service with trained model
- Demonstrates Langchain chatbot extracting features from conversation
- Generates example conversation flow (data collection → prediction → interpretation)
- **Output**: Demo conversation logs, API endpoint documentation

**Expected runtime**: 3-5 minutes (includes LLM API calls)

**Key check**: Verify API response time <2 seconds (SC-014)

---

### Quick Verification

After running all notebooks, verify outputs:

```powershell
# Check data files
ls "Data\02 Clean\"  # Should have singapore_clean.csv, exclusion_log.csv, data_quality_report.csv
ls "Data\03 Transformed\"  # Should have features_train.csv, features_test.csv, feature_metadata.json

# Check models
ls "Modelling\Outputs\models\"  # Should have *.pkl files

# Check metrics
ls "Modelling\Outputs\metrics\"  # Should have cv_results.json, model_comparison.csv

# Check visualizations
ls "Modelling\Outputs\visualizations\"  # Should have residual plots, coefficient plots
```

---

## Testing the LLM Integration

### Start FastAPI Server

```powershell
# From project root, activate venv if not already active
.\venv\Scripts\Activate.ps1

# Start FastAPI server
cd Modelling\LLMs
uvicorn api_service:app --reload --port 8000

# Server will run at http://localhost:8000
# Interactive API docs: http://localhost:8000/docs
```

### Test with cURL (PowerShell)

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get | ConvertTo-Json

# Make prediction
$body = @{
    Q1 = 1
    Q260 = 2
    Q262 = 28
    Q273 = 1
    Q275 = 5
    Q288 = 6
    Q28 = 2
    Q37 = 3
    Q38 = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json
```

**Expected output**:
```json
{
  "predicted_children": 1.8,
  "confidence_interval": [1.0, 2.6],
  "drivers": [
    {
      "name": "Q1_family_importance",
      "coefficient": 0.45,
      "interpretation": "High family importance increases predicted fertility"
    }
  ],
  "metadata": {
    "model_id": "linear_regression_v1",
    "model_type": "OLS",
    "r_squared": 0.23,
    "rmse": 0.85
  }
}
```

### Test Langchain Chatbot

```powershell
# Run interactive chatbot (from notebook or Python script)
python Modelling\LLMs\langchain_agent.py

# Example conversation:
# User: "Family is very important to me. I'm 28 years old, married, and earn a middle income."
# Chatbot: [Extracts Q1=1, Q262=28, Q273=1, Q288=6, calls /predict, returns insights]
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution**:
```powershell
# Ensure virtual environment activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: "Singapore sample size < 500"

**Solution**:
- Check if using sample CSV (20 rows) instead of full WVS dataset
- Download full dataset from https://www.worldvaluessurvey.org/
- Place in `Data/01 Raw/` and rerun Notebook 1

---

### Issue: "Poisson model shows severe overdispersion"

**Solution**:
- Expected behavior per research.md (R3)
- Notebook 4 should automatically escalate to Negative Binomial regression
- Check dispersion parameter in output logs

---

### Issue: "OPENAI_API_KEY not found"

**Solution**:
```powershell
# Set environment variable
$env:OPENAI_API_KEY = "sk-your-key-here"

# Or create .env file in project root
echo "OPENAI_API_KEY=sk-your-key" > .env

# Install python-dotenv if using .env
pip install python-dotenv

# In your script:
# from dotenv import load_dotenv
# load_dotenv()
```

---

### Issue: "Jupyter kernel crashes during MICE imputation"

**Solution**:
```powershell
# Increase memory allocation or reduce max_iter
# In notebook cell:
# imputer = IterativeImputer(random_state=42, max_iter=5)  # Reduce from 10

# Or switch to simple imputation for high-missingness variables
```

---

### Issue: "pylint score < 8.0"

**Solution**:
```powershell
# Check code quality
pylint Scripts\utils.py

# Common fixes:
# - Add docstrings to all functions
# - Remove unused imports
# - Fix line length (max 100 characters)
# - Add type hints
```

---

## Next Steps

### 1. Generate Deliverables (User Story 5)

```powershell
# Create 15-page report
# - Copy report template from Docs/Report/
# - Fill in results from notebooks
# - Include figures from Modelling/Outputs/visualizations/

# Create presentation slides
# - Use PowerPoint template from Docs/Presentation/
# - Summarize key findings, methodology, LLM integration demo
```

### 2. Package for Submission

```powershell
# Create submission zip
Compress-Archive -Path Data,Scripts,Modelling,Docs,requirements.txt,README.md -DestinationPath IS5126_FertilityPrediction_Submission.zip

# Verify contents:
# - PDF report (15 pages)
# - All notebooks (.ipynb)
# - utils.py
# - Cleaned data (CSV)
# - Trained models (.pkl)
# - Presentation slides (.pptx)
# - README with setup instructions
```

### 3. Run Quality Checks

```powershell
# Constitution compliance checklist
# - Principle I: Verify reproducibility (run all notebooks in fresh env)
# - Principle II: Confirm interpretable models used
# - Principle III: Check data quality gates documented
# - Principle IV: Review limitations section in report
# - Principle V: Verify modular notebooks

# Code quality
pylint Scripts\utils.py
pytest tests\test_utils.py
```

### 4. Explore Extensions (Optional)

- **HES Integration**: Map household expenditure data to income deciles
- **Longitudinal Analysis**: If WVS Wave 8 available, compare temporal trends
- **Advanced LLM Features**: Multi-turn conversation, user profile persistence
- **Interactive Dashboard**: Streamlit app for exploratory analysis

---

## Additional Resources

- **WVS Documentation**: [https://www.worldvaluessurvey.org/](https://www.worldvaluessurvey.org/)
- **Feature Specification**: `specs/001-fertility-prediction-pipeline/spec.md`
- **Data Model**: `specs/001-fertility-prediction-pipeline/data-model.md`
- **API Schema**: `specs/001-fertility-prediction-pipeline/contracts/api-schema.yaml`
- **Research Decisions**: `specs/001-fertility-prediction-pipeline/research.md`
- **Constitution**: `.specify/memory/constitution.md`

---

## Support

For issues or questions:
1. Check Troubleshooting section above
2. Review specification documents in `specs/001-fertility-prediction-pipeline/`
3. Consult refined proposal (`Docs/refined_proposal.md`) for research context
4. Contact course instructor or TA per IS5126 guidelines

**Happy analyzing! 🎓📊**
