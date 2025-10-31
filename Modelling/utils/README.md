# Utility Functions

This directory contains reusable Python modules and helper functions supporting the analysis pipeline.

## Module Organization

### Core Modules

#### `data_processing.py`
**Purpose**: Data cleaning, transformation, and integration utilities
- `load_hes_data()` - Standardized HES dataset loading with error handling
- `load_census_data()` - Census income distribution processing
- `ecological_inference()` - Weighted average calculation implementation
- `standardize_planning_areas()` - Geographic name harmonization
- `apply_cpi_adjustment()` - Temporal inflation correction (2020-2023)

#### `feature_engineering.py`
**Purpose**: Variable creation and transformation functions
- `calculate_distances()` - Euclidean distance computation to amenities
- `count_facilities_in_radius()` - Density metrics within specified radius
- `create_interaction_terms()` - Income × amenity interaction variables
- `encode_categorical_variables()` - Standardized encoding for housing types
- `validate_feature_ranges()` - Data quality checks for engineered features

#### `modeling_utils.py`
**Purpose**: Statistical modeling and validation support
- `run_regression_diagnostics()` - Assumption testing and residual analysis  
- `cross_validate_model()` - K-fold validation with performance metrics
- `sensitivity_analysis()` - Robustness testing with parameter variations
- `calculate_confidence_intervals()` - Bootstrap and analytical CI computation
- `detect_influential_observations()` - Outlier and leverage point identification

#### `visualization_helpers.py`
**Purpose**: Plotting and mapping functions
- `create_choropleth_map()` - Planning area spatial visualizations
- `plot_regression_diagnostics()` - Model validation visualizations
- `generate_scatter_with_regression()` - Expenditure-amenity relationship plots
- `create_interaction_plots()` - Income interaction effect visualization
- `format_publication_plots()` - Consistent styling and formatting

### LLM Integration

#### `llm_integration.py`
**Purpose**: Large Language Model workflow automation
- `classify_expenditure_categories()` - Automated family vs. non-family categorization
- `validate_classifications()` - Quality assurance for LLM outputs
- `generate_stakeholder_insights()` - Business-friendly interpretation generation
- `create_policy_summaries()` - Planning area analysis for policymakers
- `batch_process_categories()` - Efficient bulk classification processing

#### `llm_prompts.py`
**Purpose**: Standardized prompt templates and validation
- `EXPENDITURE_CLASSIFICATION_PROMPT` - Template for spending categorization
- `INSIGHT_GENERATION_PROMPT` - Template for business insight creation
- `VALIDATION_PROMPT` - Template for quality assurance checks
- `format_prompt_with_data()` - Data injection into prompt templates
- `parse_llm_responses()` - Structured output extraction from LLM responses

### Statistical Analysis

#### `statistical_tests.py`
**Purpose**: Hypothesis testing and statistical validation
- `test_normality_assumptions()` - Shapiro-Wilk and Anderson-Darling tests
- `test_heteroscedasticity()` - Breusch-Pagan and White tests
- `test_multicollinearity()` - VIF calculation and correlation analysis
- `test_spatial_autocorrelation()` - Moran's I for geographic patterns
- `bootstrap_confidence_intervals()` - Non-parametric CI estimation

#### `business_metrics.py`
**Purpose**: ROI calculation and business impact assessment
- `calculate_amenity_roi()` - Infrastructure investment return calculations
- `estimate_policy_impact()` - Predicted expenditure changes from interventions
- `rank_planning_areas()` - Priority scoring for investment decisions
- `generate_optimization_recommendations()` - Budget allocation optimization

### Data Validation

#### `quality_checks.py`
**Purpose**: Data integrity and validation functions
- `validate_data_completeness()` - Missing value assessment
- `check_value_ranges()` - Outlier and constraint validation
- `verify_cross_dataset_consistency()` - Integration quality checks
- `audit_calculation_accuracy()` - Mathematical operation verification
- `generate_data_quality_report()` - Comprehensive validation summary

## Usage Guidelines

### Import Convention
```python
from utils.data_processing import ecological_inference, load_hes_data
from utils.llm_integration import classify_expenditure_categories
from utils.modeling_utils import run_regression_diagnostics
```

### Configuration Management
- Use `config.py` for shared constants (file paths, API keys, parameters)
- Environment variables for sensitive information (API keys)
- Centralized parameter management for model specifications

### Error Handling
- All functions include comprehensive error handling and logging
- Input validation with descriptive error messages
- Graceful degradation for missing or malformed data

### Testing
- Unit tests for each utility function in `tests/` subdirectory
- Integration tests for data processing pipelines
- Validation against known benchmarks and expected outcomes

### Documentation
- Docstrings following NumPy style conventions
- Type hints for all function parameters and returns
- Usage examples in docstrings for complex functions