# Data Model: Fertility Prediction Pipeline

**Feature**: Fertility Prediction Data Science Pipeline  
**Date**: 2025-11-01  
**Phase**: 1 (Design)

## Purpose

Define entities, relationships, validation rules, and state transitions for the fertility prediction pipeline. Extracted from feature specification requirements.

---

## Core Entities

### Entity 1: WVS Respondent

**Description**: Individual survey participant representing a single row in the WVS dataset.

**Attributes**:
- `B_COUNTRY_ALPHA` (string): ISO3 country code (e.g., "SGP" for Singapore)
- `Q262` (integer): Age in years (range: 18-99, filtered to 25-49 for analysis)
- `Q260` (integer): Sex (1=Male, 2=Female)
- `Q274` (integer): **TARGET VARIABLE** - Number of children (0 to n, non-negative)
- `Q1-Q288` (mixed): Survey responses across 288 questions
  - Categorical (e.g., Q1-Q6: 1-4 scale for importance)
  - Ordinal (e.g., Q288: 1-10 income scale)
  - Continuous (rare, mostly ordinal/categorical)
- Missing value codes: -1 (Don't know), -2 (No answer), -3 (Not applicable), -5 (Missing)

**Validation Rules** (enforced in `02_data_cleaning.ipynb`):
- `B_COUNTRY_ALPHA == 'SGP'` for Singapore subset (FR-002)
- `25 <= Q262 <= 49` for age filter (FR-003)
- `Q274 >= 0` and `Q274.notna()` for valid target (FR-007)
- Missing values in [-1, -2, -3, -5] handled per strategy (FR-004)
- Outlier detection: Z-score > 3 flagged for review (SC-003)

**Relationships**:
- Belongs to **Country** (via B_COUNTRY_ALPHA)
- Belongs to **Age Cohort** (derived: 25-29, 30-34, 35-39, 40-44, 45-49)
- Has many **Feature Values** (Q1-Q288 responses)
- Generates one **Feature Vector** (post-engineering)

**State Transitions**:
```
Raw Respondent (from CSV)
  → [Filter: Singapore + Age 25-49]
  → Eligible Respondent
  → [Handle missing values]
  → Clean Respondent
  → [Feature engineering]
  → Model-Ready Respondent
```

---

### Entity 2: Feature Set

**Description**: Processed predictor variables derived from WVS responses, ready for model training.

**Attributes**:
- `feature_name` (string): Descriptive name (e.g., "family_importance_Q1", "age_Q262", "income_scale_Q288")
- `source_q_code` (string): Original WVS question code (e.g., "Q1", "Q262", "Q288")
- `data_type` (enum): ['continuous', 'categorical', 'ordinal', 'binary', 'composite_index']
- `encoding_method` (enum): ['none', 'one_hot', 'ordinal', 'pca', 'interaction']
- `value_range` (object): Min/max for continuous, categories for categorical
- `missingness_pct` (float): Percentage of missing values pre-imputation (0.00 to 1.00)
- `importance_score` (float): LASSO coefficient magnitude (populated post-training)

**Validation Rules** (enforced in `03_feature_engineering.ipynb`):
- Feature names unique and descriptive (no "feat_1", "feat_2")
- Categorical encodings preserve interpretability (one-hot for nominal, ordinal for ordered)
- Composite indices documented with formula (e.g., "mean(Q1, Q2, Q3)")
- All features mapped back to source Q-codes in `feature_metadata.json` (FR-011)

**Relationships**:
- Derived from **WVS Respondent** (many features per respondent)
- Used by **Model** (X matrix in training)
- Linked to **Feature Importance** (post-training)

**State Transitions**:
```
Raw Q-code Value
  → [Encoding: one-hot/ordinal/interaction]
  → Encoded Feature
  → [Scaling: standardization if needed]
  → Model-Ready Feature
  → [Feature selection: LASSO]
  → Selected Feature (non-zero coefficient)
```

---

### Entity 3: Model

**Description**: Trained statistical or machine learning model for predicting Q274 (number of children).

**Attributes**:
- `model_id` (string): Unique identifier (e.g., "linear_regression_v1", "poisson_baseline")
- `model_type` (enum): ['linear_regression', 'poisson', 'negative_binomial', 'lasso', 'random_forest', 'xgboost', 'lightgbm']
- `hyperparameters` (dict): Model-specific parameters (e.g., `{"alpha": 0.01, "max_iter": 1000}` for LASSO)
- `training_date` (datetime): Timestamp when model was trained
- `training_sample_size` (integer): Number of respondents in training set
- `feature_names` (list): Ordered list of features used (must match Feature Set)
- `coefficients` (array): Model weights (for linear models) or feature importance scores
- `performance_metrics` (dict): `{"r2": 0.23, "rmse": 0.85, "mae": 0.67}`
- `cv_metrics` (dict): Cross-validation results `{"mean_r2": 0.21, "std_r2": 0.03, "folds": 10}`
- `file_path` (string): Serialized model location (e.g., "Modelling/Outputs/models/linear_regression.pkl")

**Validation Rules** (enforced in `04_model_training_baseline.ipynb`, `05_model_validation.ipynb`):
- Model type must be in allowed list (FR-012 to FR-015)
- Hyperparameters logged for reproducibility (NFR-006)
- Performance metrics computed on same test set for fair comparison (SC-009)
- Cross-validation uses 10 folds with stratified sampling (FR-017)
- Serialized models include metadata (version, date, hyperparams) (NFR-006)

**Relationships**:
- Trained on **Feature Set** (X matrix)
- Predicts **Target Variable** (Q274)
- Generates **Predictions** (via inference)
- Produces **Feature Importance** rankings
- Compared with other **Models** in model comparison table

**State Transitions**:
```
Untrained Model (algorithm selected)
  → [Training: fit on X_train, y_train]
  → Trained Model
  → [Validation: cross-validation]
  → Validated Model
  → [Serialization: save to .pkl]
  → Persisted Model
  → [Deployment: load in FastAPI]
  → Serving Model
```

---

### Entity 4: Prediction

**Description**: Model output for a specific respondent or hypothetical feature vector.

**Attributes**:
- `prediction_id` (string): Unique identifier (UUID or timestamp-based)
- `model_id` (string): Reference to Model used for prediction
- `input_features` (dict): Feature values provided (e.g., `{"Q1": 1, "Q262": 28, "Q288": 6}`)
- `predicted_children` (float): Predicted number of children (continuous, rounded for interpretation)
- `confidence_interval` (tuple): 95% CI `[lower_bound, upper_bound]`
- `feature_importance` (dict): Top 3-5 drivers `{"Q1": 0.45, "Q288": 0.32, "Q262": 0.18}`
- `timestamp` (datetime): When prediction was made
- `source` (enum): ['model_validation', 'llm_chatbot', 'manual_test']

**Validation Rules** (enforced in `06_llm_integration.ipynb`, API service):
- Input features must match model's expected feature set (schema validation)
- Predicted children cannot be negative (clip at 0 if model predicts negative)
- Confidence interval computed using model RMSE (rough estimate for prototype)
- Feature importance sorted by absolute coefficient value

**Relationships**:
- Generated by **Model** (via `model.predict()`)
- Linked to **Respondent** (if predicting on test set) or hypothetical input (if LLM chatbot)
- Used by **LLM Interpretation** layer for natural language insights

**State Transitions**:
```
Feature Input (from chatbot or test set)
  → [Validation: schema check]
  → Valid Input
  → [Model inference: predict()]
  → Raw Prediction (continuous float)
  → [Post-processing: clip, round, CI]
  → Final Prediction
  → [Interpretation: LLM generates insights]
  → Explained Prediction
```

---

## Supporting Entities

### Entity 5: Data Quality Report

**Description**: Metadata tracking data transformations and quality metrics.

**Attributes**:
- `report_id` (string): Unique identifier (e.g., "dq_report_2025_11_01")
- `sample_size_raw` (integer): Initial WVS respondents before filters
- `sample_size_filtered` (integer): After Singapore + age filter
- `sample_size_clean` (integer): After missing value handling
- `exclusion_log` (list): `[{"step": "age_filter", "excluded": 523, "reason": "Q262 < 25 or > 49"}, ...]`
- `missingness_summary` (dict): `{"Q1": 0.03, "Q274": 0.01, "Q288": 0.12}`
- `outlier_flags` (dict): `{"Q262": ["resp_123", "resp_456"], "Q288": ["resp_789"]}`
- `file_path` (string): `Data/02 Clean/data_quality_report.csv`

**Validation Rules** (FR-005):
- All exclusion steps logged with counts
- Missingness percentages sum to total missing values
- Outlier detection uses Z-score > 3 or domain-specific rules

**Relationships**:
- Documents transformations on **WVS Respondent**
- Referenced in notebooks for transparency (Constitution Principle III)

---

### Entity 6: HES Spending Data (Optional/Supplementary)

**Description**: Household Expenditure Survey data mapped to WVS income deciles.

**Attributes**:
- `income_decile` (integer): 1-10 (mapped from WVS Q288)
- `family_oriented_spending_pct` (float): Percentage of income spent on family items (education, childcare, family recreation)
- `education_spending_per_capita` (float): Education expenses / household size
- `childcare_intensity` (float): Childcare expenses / total income

**Validation Rules**:
- Income decile must map to Q288 values (1-10)
- Spending percentages between 0-100
- Acknowledge ecological fallacy in interpretation (Limitation 10.4.1)

**Relationships**:
- Joined to **WVS Respondent** via Q288 (income scale)
- Optional enrichment for Model training (FR-002 supplementary)

**State**: 
- **Status**: Out of scope for initial implementation (per refined proposal Section 10.4)
- **Future consideration**: If HES data successfully mapped, add as supplementary features

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Raw WVS CSV                                 │
│                    (97k respondents, 288 Q-codes)                   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  01_data_loading_eda    │
                    │  - Load CSV             │
                    │  - Filter SGP           │
                    │  - EDA visualizations   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Singapore Raw Subset    │
                    │ (n ≈ 1,000-2,000)       │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  02_data_cleaning       │
                    │  - Age filter 25-49     │
                    │  - Handle missing       │
                    │  - Outlier detection    │
                    │  - Generate DQ report   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Singapore Clean Dataset │
                    │ (n ≥ 500)               │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  03_feature_engineering │
                    │  - Encode categoricals  │
                    │  - Create indices       │
                    │  - Train/test split     │
                    │  - Feature metadata     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Engineered Feature Sets │
                    │ (train.csv, test.csv)   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  04_model_training      │
                    │  - OLS, Poisson, LASSO  │
                    │  - Hyperparameter tuning│
                    │  - Save models (.pkl)   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Trained Models +        │
                    │ Performance Metrics     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  05_model_validation    │
                    │  - 10-fold CV           │
                    │  - Model comparison     │
                    │  - Diagnostic plots     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Validation Results +    │
                    │ Model Selection         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  06_llm_integration     │
                    │  - FastAPI service      │
                    │  - Langchain chatbot    │
                    │  - Demo conversations   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Predictions +           │
                    │ LLM Insights            │
                    └─────────────────────────┘
```

---

## Schema Validation Rules

### Input Validation (01_data_loading_eda.ipynb)

```python
def validate_wvs_schema(df):
    required_cols = ['B_COUNTRY_ALPHA', 'Q262', 'Q260', 'Q274'] + [f'Q{i}' for i in range(1, 289)]
    missing = set(required_cols) - set(df.columns)
    assert len(missing) == 0, f"Missing columns: {missing}"
    
    # Check data types
    assert df['Q262'].dtype in ['int64', 'float64'], "Q262 (age) must be numeric"
    assert df['Q274'].dtype in ['int64', 'float64'], "Q274 (children) must be numeric"
```

### Data Quality Validation (02_data_cleaning.ipynb)

```python
def validate_clean_data(df):
    # Age filter enforcement
    assert (df['Q262'] >= 25).all() and (df['Q262'] <= 49).all(), "Age filter violated"
    
    # No missing target variable
    assert df['Q274'].notna().all(), "Q274 has missing values after cleaning"
    
    # Non-negative children
    assert (df['Q274'] >= 0).all(), "Q274 has negative values"
    
    # Sample size check
    assert len(df) >= 500, f"Sample size {len(df)} below minimum 500 (SC-001)"
```

### Feature Validation (03_feature_engineering.ipynb)

```python
def validate_features(X_train, X_test, feature_metadata):
    # Train/test have same columns
    assert set(X_train.columns) == set(X_test.columns), "Train/test feature mismatch"
    
    # All features in metadata
    for col in X_train.columns:
        assert col in feature_metadata, f"Feature {col} not documented in metadata"
    
    # No missing values (post-imputation)
    assert X_train.notna().all().all(), "Train set has missing values"
    assert X_test.notna().all().all(), "Test set has missing values"
```

### Model Validation (04_model_training_baseline.ipynb)

```python
def validate_model(model, X_train, y_train):
    # Model can make predictions
    y_pred = model.predict(X_train)
    assert len(y_pred) == len(y_train), "Prediction length mismatch"
    
    # For linear models, check coefficients
    if hasattr(model, 'coef_'):
        assert len(model.coef_) == X_train.shape[1], "Coefficient count mismatch"
        
        # Sensible signs (example: family importance positive)
        # This is domain-specific validation
```

---

## State Management

### Pipeline State Tracking

Track progress through notebooks using metadata files:

```json
// Data/pipeline_state.json
{
  "last_updated": "2025-11-01T14:30:00",
  "completed_notebooks": [
    "01_data_loading_eda",
    "02_data_cleaning",
    "03_feature_engineering"
  ],
  "current_stage": "04_model_training",
  "datasets": {
    "singapore_raw": {
      "path": "Data/02 Clean/singapore_raw.csv",
      "rows": 1523,
      "created": "2025-11-01T12:00:00"
    },
    "singapore_clean": {
      "path": "Data/02 Clean/singapore_clean.csv",
      "rows": 1342,
      "created": "2025-11-01T12:30:00"
    },
    "features_train": {
      "path": "Data/03 Transformed/features_train.csv",
      "rows": 939,
      "columns": 45,
      "created": "2025-11-01T13:15:00"
    }
  },
  "models_trained": ["linear_regression_v1", "poisson_baseline"],
  "next_action": "Train LASSO model in 04_model_training_baseline.ipynb"
}
```

---

## Summary

**Entities Defined**: 6 (WVS Respondent, Feature Set, Model, Prediction, Data Quality Report, HES Spending Data)

**Key Relationships**:
- Respondent → Feature Set (1:many features)
- Feature Set → Model (many features:many models)
- Model → Prediction (1:many predictions)
- Data Quality Report → Respondent (documents transformations)

**Validation Rules**: Schema checks, age/Singapore filters, sample size thresholds, feature encoding standards

**State Transitions**: Raw → Filtered → Clean → Engineered → Trained → Validated → Serving

**Data Flow**: Linear pipeline through 6 notebooks with clear input/output contracts

**Next Phase**: Generate API contracts (contracts/api-schema.yaml) and quickstart guide
