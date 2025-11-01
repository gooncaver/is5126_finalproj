# Phase 0: Research & Technology Decisions

**Feature**: Fertility Prediction Data Science Pipeline  
**Date**: 2025-11-01  
**Status**: Complete

## Purpose

Resolve technical unknowns from plan.md Technical Context and establish best practices for implementation. All decisions documented with rationale and alternatives considered.

---

## R1: WVS Data Format & Loading Strategy

### Decision
Load WVS CSV using `pandas.read_csv()` with automatic dtype inference, followed by explicit schema validation against expected Q-codes.

### Rationale
- **Sample file available**: `Data/01 Raw/wvs_data_sample20rows.csv` confirms CSV format
- **Standard approach**: Pandas is the de facto Python library for CSV processing
- **Schema validation**: WVS has 288 Q-codes + metadata columns; explicit validation prevents silent column drops or type mismatches

### Implementation
```python
# utils.py
def load_wvs(filepath, validate_schema=True):
    df = pd.read_csv(filepath, low_memory=False)
    if validate_schema:
        expected_cols = ['B_COUNTRY_ALPHA', 'Q262', 'Q274', ...]  # Full Q-code list
        missing = set(expected_cols) - set(df.columns)
        assert len(missing) == 0, f"Missing columns: {missing}"
    return df
```

### Alternatives Considered
- **Dask**: Rejected - Singapore subset (n≈1,000-2,000) fits in memory; no need for distributed computing
- **PySpark**: Rejected - Overkill for ~97k rows; adds complexity without performance benefit
- **Manual CSV parsing**: Rejected - Pandas handles edge cases (quotes, delimiters, encodings) better

---

## R2: Missing Value Handling Strategy

### Decision
Multi-strategy approach based on missingness level and variable type:
1. **Target variable (Q274)**: Exclude respondents with missing values (listwise deletion)
2. **<5% missingness**: Mean imputation (continuous), mode imputation (categorical)
3. **5-20% missingness**: Multiple imputation (MICE via `sklearn.impute.IterativeImputer`)
4. **>20% missingness**: Exclude variable from analysis (too unreliable)

### Rationale
- **Target integrity**: Cannot predict missing outcomes; listwise deletion mandatory
- **Low missingness**: Simple imputation preserves sample size without bias
- **Moderate missingness**: MICE leverages correlations to reduce imputation bias
- **High missingness**: Risk of imputation-induced patterns; better to exclude
- **Transparency**: All strategies documented in FR-004 data quality report

### Implementation
```python
# utils.py
def handle_missing(df, target_col='Q274', threshold_exclude=0.20):
    # 1. Drop rows with missing target
    df = df[df[target_col].notna()]
    
    # 2. Identify columns by missingness level
    miss_pct = df.isnull().mean()
    exclude_cols = miss_pct[miss_pct > threshold_exclude].index.tolist()
    low_miss = miss_pct[(miss_pct > 0) & (miss_pct < 0.05)].index.tolist()
    med_miss = miss_pct[(miss_pct >= 0.05) & (miss_pct <= threshold_exclude)].index.tolist()
    
    # 3. Apply strategies
    df = df.drop(columns=exclude_cols)
    for col in low_miss:
        df[col].fillna(df[col].mean() if df[col].dtype in ['int64', 'float64'] else df[col].mode()[0], inplace=True)
    
    if len(med_miss) > 0:
        from sklearn.impute import IterativeImputer
        imputer = IterativeImputer(random_state=42, max_iter=10)
        df[med_miss] = imputer.fit_transform(df[med_miss])
    
    return df, {'excluded': exclude_cols, 'low_miss': low_miss, 'med_miss': med_miss}
```

### Alternatives Considered
- **Complete-case analysis only**: Rejected - Would lose too many respondents; small Singapore sample cannot afford attrition
- **Single imputation (mean/mode)**: Rejected for moderate missingness - Underestimates standard errors, inflates significance
- **Predictive mean matching (PMM)**: Rejected - MICE is more robust for mixed data types in WVS

---

## R3: Count Data Modeling Approach (Poisson vs Negative Binomial)

### Decision
Start with **Poisson regression** as baseline count model. If overdispersion detected (dispersion parameter >2.0), escalate to **Negative Binomial regression**.

### Rationale
- **Q274 is count data**: Number of children is non-negative integer (0, 1, 2, 3, ...)
- **Poisson assumption**: Variance = mean (restrictive but interpretable)
- **Overdispersion common**: Fertility data often has variance > mean (e.g., high childless proportion + high parity families)
- **NB flexibility**: Negative binomial relaxes Poisson's variance assumption, handles overdispersion
- **Diagnostic-driven**: Test Poisson first, upgrade only if diagnostics fail (Constitution Principle II: simplicity)

### Implementation
```python
# utils.py
import statsmodels.api as sm

def train_count_model(X, y, model_type='poisson'):
    if model_type == 'poisson':
        model = sm.GLM(y, X, family=sm.families.Poisson()).fit()
        # Check overdispersion
        dispersion = model.pearson_chi2 / model.df_resid
        if dispersion > 2.0:
            warnings.warn(f"Overdispersion detected (φ={dispersion:.2f}). Consider Negative Binomial.")
    elif model_type == 'negativebinomial':
        model = sm.GLM(y, X, family=sm.families.NegativeBinomial()).fit()
    
    return model, {'dispersion': dispersion if model_type == 'poisson' else None}
```

### Alternatives Considered
- **OLS linear regression on counts**: Rejected as primary - Violates assumptions (negative predictions possible, heteroskedasticity), but retained as interpretable baseline per spec
- **Zero-inflated models (ZIP/ZINB)**: Rejected - Added complexity; only use if >30% zeros and theoretical justification (e.g., voluntary vs involuntary childlessness)
- **Ordered logistic regression**: Rejected - Treats children as ordinal categories, loses count nature

---

## R4: Cross-Validation Strategy for Small Samples

### Decision
**10-fold cross-validation** with stratified splits by age group (5-year bins: 25-29, 30-34, 35-39, 40-44, 45-49).

### Rationale
- **Small sample (n≈1,000-2,000)**: Train-test split (70/30) would leave only ~300-600 test cases; k-fold maximizes data use
- **10 folds standard**: Balance between bias (more folds = less bias) and variance (fewer folds = more stable)
- **Stratification**: Age strongly associated with fertility (completed vs ongoing); stratify to ensure age distribution consistent across folds
- **Reproducibility**: Fixed random seed (42) ensures same splits across runs

### Implementation
```python
# utils.py
from sklearn.model_selection import StratifiedKFold

def cross_validate_model(X, y, model_fn, age_col='Q262', n_splits=10, random_state=42):
    # Create age bins for stratification
    age_bins = pd.cut(X[age_col], bins=[25, 30, 35, 40, 45, 50], labels=['25-29', '30-34', '35-39', '40-44', '45-49'])
    
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    results = {'fold': [], 'r2': [], 'rmse': [], 'mae': []}
    
    for fold, (train_idx, test_idx) in enumerate(skf.split(X, age_bins)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        model = model_fn(X_train, y_train)
        y_pred = model.predict(X_test)
        
        results['fold'].append(fold)
        results['r2'].append(r2_score(y_test, y_pred))
        results['rmse'].append(np.sqrt(mean_squared_error(y_test, y_pred)))
        results['mae'].append(mean_absolute_error(y_test, y_pred))
    
    return pd.DataFrame(results)
```

### Alternatives Considered
- **Leave-one-out CV (LOOCV)**: Rejected - Computationally expensive for n>1,000; minimal bias improvement over 10-fold
- **5-fold CV**: Rejected - Higher variance in estimates; 10-fold better for small samples
- **Time-series CV**: Not applicable - Cross-sectional data, no temporal ordering

---

## R5: Feature Selection for High-Dimensional Data (288 Q-codes)

### Decision
Three-stage feature selection pipeline:
1. **Domain knowledge**: Pre-select theoretically motivated predictors from proposal (demographics, family values, gender attitudes, economic security)
2. **Univariate screening**: Correlation analysis + chi-square tests to filter variables with p>0.10
3. **LASSO regularization**: L1 penalty (α tuned via CV) to perform final feature selection

### Rationale
- **Curse of dimensionality**: 288 potential predictors >> 1,000-2,000 samples; overfitting risk
- **Theory-driven**: Constitution Principle IV emphasizes interpretability; start with research-motivated variables
- **Statistical screening**: Remove clearly uninformative variables before modeling
- **LASSO benefits**: Automatic feature selection + regularization; coefficients exactly zero for excluded features
- **Cross-validated α**: Prevents overfitting; picks optimal penalty strength

### Implementation
```python
# utils.py
from sklearn.linear_model import LassoCV

def select_features_lasso(X, y, cv=10, random_state=42):
    # 1. Domain knowledge: Pre-selected in notebook based on proposal
    # (This step is manual feature list creation)
    
    # 2. Univariate screening (example for continuous predictors)
    from scipy.stats import pearsonr
    correlations = {col: pearsonr(X[col], y)[1] for col in X.columns}  # p-values
    candidates = [col for col, pval in correlations.items() if pval < 0.10]
    
    # 3. LASSO with CV
    lasso = LassoCV(cv=cv, random_state=random_state, max_iter=10000)
    lasso.fit(X[candidates], y)
    
    # Extract non-zero coefficients
    selected = X[candidates].columns[lasso.coef_ != 0].tolist()
    
    return selected, lasso.alpha_, lasso.coef_
```

### Alternatives Considered
- **Stepwise regression**: Rejected - Greedy algorithm, high false positive rate in high-dimensional settings
- **Random Forest feature importance**: Considered - Useful for comparison but not primary method (non-parametric, harder to interpret)
- **Elastic Net**: Considered - LASSO (α=1) preferred for sparsity; Elastic Net if multicollinearity severe (would use α=0.5)

---

## R6: Langchain Architecture for LLM Integration

### Decision
Use **Langchain's ConversationChain** with custom prompt templates and **function calling** to extract WVS features from conversation, then invoke FastAPI `/predict` endpoint.

### Rationale
- **Langchain abstracts LLM APIs**: Unified interface for OpenAI/Anthropic, easier to swap providers
- **Conversation memory**: ConversationChain maintains chat history for context-aware responses
- **Function calling**: Modern LLM APIs (GPT-4, Claude 3) support function calling to structure outputs (e.g., extract {Q1: 1, Q260: 2, Q288: 6} from natural language)
- **Separation of concerns**: Langchain handles conversation, FastAPI serves model predictions (clean architecture)
- **Prototype focus**: No production hardening needed (per spec Out of Scope)

### Implementation
```python
# Modelling/LLMs/langchain_agent.py
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import requests

# Custom prompt for feature extraction
extraction_template = """You are a fertility survey assistant. Extract WVS features from user responses.

Conversation history:
{history}

User: {input}

Extract the following if mentioned:
- Q1 (family importance): 1=very important, 2=important, 3=not important, 4=not at all important
- Q260 (sex): 1=male, 2=female
- Q262 (age): numeric
- Q288 (income scale): 1-10

Return JSON format: {{"Q1": value, "Q260": value, ...}}
If information missing, return {{"status": "need_more_info", "missing": [list]}}
"""

prompt = PromptTemplate(template=extraction_template, input_variables=["history", "input"])
llm = ChatOpenAI(model="gpt-4", temperature=0)
chain = ConversationChain(llm=llm, prompt=prompt)

def chat_and_predict(user_input):
    # Extract features via Langchain
    response = chain.predict(input=user_input)
    features = parse_json(response)  # Parse LLM output
    
    # Call FastAPI prediction endpoint
    if features.get('status') != 'need_more_info':
        api_response = requests.post('http://localhost:8000/predict', json=features)
        prediction = api_response.json()
        return f"Predicted children: {prediction['predicted_children']:.1f}. Key drivers: {prediction['drivers']}"
    else:
        return f"I need more information: {features['missing']}"
```

### Alternatives Considered
- **Raw OpenAI API calls**: Rejected - More boilerplate code, no conversation memory management
- **LlamaIndex**: Rejected - Better for RAG (retrieval-augmented generation) over documents; overkill for structured feature extraction
- **Haystack**: Rejected - Similar to Langchain but less active development for LLM agents

---

## R7: FastAPI Endpoint Design

### Decision
Single `/predict` POST endpoint accepting JSON with WVS features, returning prediction + feature importance.

### Rationale
- **RESTful design**: POST for prediction requests (not idempotent, model inference = resource creation)
- **JSON schema validation**: Pydantic models ensure type safety, automatic API docs
- **Synchronous**: Prototype doesn't need async (single user, <2s response time per SC-014)
- **Stateless**: No session management; each request independent

### Implementation
```python
# Modelling/LLMs/api_service.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load trained model
model = joblib.load('../Outputs/models/linear_regression.pkl')
feature_names = ['Q1', 'Q260', 'Q262', 'Q288', ...]  # Full feature list

class PredictionRequest(BaseModel):
    Q1: int
    Q260: int
    Q262: int
    Q288: int
    # ... all required features

class PredictionResponse(BaseModel):
    predicted_children: float
    drivers: list[str]
    confidence_interval: list[float]

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Convert to feature array
    features = np.array([[request.Q1, request.Q260, request.Q262, request.Q288, ...]])
    
    # Predict
    pred = model.predict(features)[0]
    
    # Feature importance (top 3 by absolute coefficient)
    coefs = model.coef_
    top_indices = np.argsort(np.abs(coefs))[-3:]
    drivers = [feature_names[i] for i in top_indices]
    
    # Confidence interval (rough estimate: ±1.96 * RMSE)
    rmse = 0.8  # From model metadata
    ci = [pred - 1.96*rmse, pred + 1.96*rmse]
    
    return PredictionResponse(predicted_children=pred, drivers=drivers, confidence_interval=ci)
```

### Alternatives Considered
- **GraphQL**: Rejected - Overkill for single endpoint; REST simpler
- **gRPC**: Rejected - Binary protocol unnecessary for prototype; JSON human-readable for debugging
- **Multiple endpoints (/predict, /explain, /validate)**: Rejected - Single endpoint with comprehensive response cleaner for prototype

---

## R8: Visualization Best Practices for Academic Reports

### Decision
Use **Seaborn** for statistical plots with **colorblind-friendly palettes** (e.g., `colorblind` palette) and **consistent styling** via custom `sns.set_theme()`.

### Rationale
- **Seaborn strengths**: Built on matplotlib, designed for statistical visualization (regression plots, distribution plots, heatmaps)
- **Accessibility**: NFR-003 requires colorblind-friendly palettes; Seaborn includes validated options
- **Publication quality**: Academic reports need high-resolution, clearly labeled figures
- **Consistency**: Custom theme ensures uniform appearance across all notebooks

### Implementation
```python
# utils.py
import seaborn as sns
import matplotlib.pyplot as plt

def setup_plot_style():
    sns.set_theme(style="whitegrid", palette="colorblind", font_scale=1.2)
    plt.rcParams['figure.dpi'] = 300  # High resolution for reports
    plt.rcParams['savefig.bbox'] = 'tight'  # No clipping

# Example: Coefficient plot
def plot_coefficients(model, feature_names, save_path=None):
    coefs = pd.DataFrame({'feature': feature_names, 'coefficient': model.coef_})
    coefs = coefs.sort_values('coefficient')
    
    plt.figure(figsize=(8, 6))
    sns.barplot(data=coefs, x='coefficient', y='feature', palette='colorblind')
    plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
    plt.xlabel('Coefficient Estimate')
    plt.title('Feature Importance: Linear Regression')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
```

### Alternatives Considered
- **Plotly**: Rejected - Interactive plots nice but not needed for static PDF reports
- **Matplotlib only**: Rejected - More verbose for statistical plots; Seaborn higher-level API better for academic figures
- **Base R ggplot2**: Rejected - Project is Python-based; pandas + seaborn ecosystem integrated

---

## R9: Notebook Organization & Execution Order

### Decision
6 sequential notebooks with clear input/output contracts documented in README:

1. `01_data_loading_eda.ipynb`: Load WVS → Singapore subset → EDA visualizations → Output: `Data/02 Clean/singapore_raw.csv`
2. `02_data_cleaning.ipynb`: Input: `singapore_raw.csv` → Handle missing, outliers, filters → Output: `Data/02 Clean/singapore_clean.csv`, `exclusion_log.csv`
3. `03_feature_engineering.ipynb`: Input: `singapore_clean.csv` → Encode categoricals, create indices, interactions → Output: `Data/03 Transformed/features_train.csv`, `features_test.csv`, `feature_metadata.json`
4. `04_model_training_baseline.ipynb`: Input: `features_train.csv` → Train OLS, Poisson, LASSO → Output: `Modelling/Outputs/models/*.pkl`, `metrics/baseline_results.json`
5. `05_model_validation.ipynb`: Input: `features_test.csv`, `models/*.pkl` → Cross-validation, comparative analysis → Output: `metrics/cv_results.json`, `visualizations/*`
6. `06_llm_integration.ipynb`: Input: `models/*.pkl` → Test Langchain agent, FastAPI endpoints → Output: Demo conversation logs

### Rationale
- **Linear dependency**: Each notebook depends only on previous outputs (DAG structure)
- **Single responsibility**: Each notebook one phase (Constitution Principle V)
- **Testable**: Can run any notebook independently if inputs available
- **Reproducible**: Clear execution order in README (FR-029)

### Implementation
```markdown
# README.md execution section
## Running the Pipeline

Execute notebooks in order:
1. `Scripts/01_data_loading_eda.ipynb` - Requires: `Data/01 Raw/wvs_data_sample20rows.csv`
2. `Scripts/02_data_cleaning.ipynb` - Requires: `Data/02 Clean/singapore_raw.csv`
3. `Scripts/03_feature_engineering.ipynb` - Requires: `Data/02 Clean/singapore_clean.csv`
4. `Scripts/04_model_training_baseline.ipynb` - Requires: `Data/03 Transformed/features_train.csv`
5. `Scripts/05_model_validation.ipynb` - Requires: `Data/03 Transformed/features_test.csv`, models
6. `Scripts/06_llm_integration.ipynb` - Requires: Trained models, API keys (OPENAI_API_KEY)

Each notebook sources functions from `Scripts/utils.py`.
```

### Alternatives Considered
- **Single monolithic notebook**: Rejected - Violates Constitution Principle V, hard to debug
- **Python scripts instead of notebooks**: Rejected - Notebooks better for EDA, visualization, academic documentation (narrative + code)
- **Pipeline orchestration (Airflow, Prefect)**: Rejected - Overkill for academic project; manual execution sufficient

---

## R10: Testing Strategy for utils.py

### Decision
**Pytest** with fixtures for sample data, unit tests for each utility function, target coverage ≥80%.

### Rationale
- **Pytest standard**: De facto Python testing framework, simple syntax, rich plugin ecosystem
- **Fixtures**: Reusable sample WVS data for testing (avoid loading full CSV per test)
- **Unit tests**: Each function in utils.py independently tested (load_wvs, handle_missing, train_model, etc.)
- **Coverage target**: 80% balances thoroughness with pragmatism (100% hard for data science code with external dependencies)

### Implementation
```python
# tests/test_utils.py
import pytest
import pandas as pd
from Scripts.utils import load_wvs, handle_missing

@pytest.fixture
def sample_wvs():
    return pd.DataFrame({
        'B_COUNTRY_ALPHA': ['SGP', 'SGP', 'USA'],
        'Q262': [28, 35, 42],
        'Q274': [1, 2, None],
        'Q1': [1, None, 2]
    })

def test_load_wvs(tmp_path):
    # Create temporary CSV
    csv_path = tmp_path / "test.csv"
    sample = pd.DataFrame({'B_COUNTRY_ALPHA': ['SGP'], 'Q274': [2]})
    sample.to_csv(csv_path, index=False)
    
    df = load_wvs(csv_path, validate_schema=False)
    assert len(df) == 1
    assert 'Q274' in df.columns

def test_handle_missing(sample_wvs):
    cleaned, metadata = handle_missing(sample_wvs, target_col='Q274')
    
    # Should drop row with missing Q274
    assert len(cleaned) == 2
    
    # Should impute Q1 (low missingness)
    assert cleaned['Q1'].notna().all()
```

### Alternatives Considered
- **Unittest**: Rejected - Pytest syntax cleaner, better fixtures
- **Doctest**: Rejected - Good for simple examples but insufficient for complex data functions
- **Property-based testing (Hypothesis)**: Considered - Useful for edge cases but adds complexity; deferred to future

---

## Summary of Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Data loading** | pandas ≥1.3.0 | Standard, handles CSV edge cases |
| **Missing values** | MICE (sklearn.IterativeImputer) | Robust for moderate missingness |
| **Count models** | statsmodels (Poisson, NB) | Statistical inference, diagnostics |
| **Feature selection** | LASSO (sklearn.LassoCV) | Automatic selection, regularization |
| **Cross-validation** | StratifiedKFold (sklearn) | Maximizes data use, controls age distribution |
| **LLM framework** | Langchain ≥0.1.0 | Conversation memory, function calling |
| **API service** | FastAPI + Uvicorn | Fast, type-safe, auto-docs |
| **Visualization** | Seaborn + Matplotlib | Statistical plots, colorblind palettes |
| **Testing** | Pytest | Standard, clean syntax, fixtures |
| **Notebooks** | Jupyter (local or Colab) | Interactive, narrative + code |

---

## Resolved Questions from Technical Context

All "NEEDS CLARIFICATION" items from plan.md Technical Context now resolved:
- ✅ Language/Version: Python 3.8+ confirmed
- ✅ Dependencies: Full stack specified (pandas, scikit-learn, statsmodels, langchain, fastapi)
- ✅ Storage: CSV files in Data/ subfolders
- ✅ Testing: Pytest for utils.py, notebook execution tests
- ✅ Platform: Local Jupyter or Google Colab
- ✅ Performance: <30min pipeline, <2s API response
- ✅ Constraints: Singapore n ≥ 500, age 25-49, interpretable models
- ✅ Scale: ~97k global, ~1-2k Singapore, 30 FRs, 6 notebooks

**Phase 0 Complete - Proceed to Phase 1 (Design & Contracts)**
