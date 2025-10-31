# Analysis Notebooks

This directory contains Jupyter notebooks for all analytical work in the IS5126 Final Project.

## Notebook Organization & Workflow

### Naming Convention
Use numbered prefixes for sequential workflow:
- `01_data_exploration.ipynb`
- `02_data_integration.ipynb`
- `03_feature_engineering.ipynb`
- `04_model_development.ipynb`
- `05_results_analysis.ipynb`
- `06_visualization_reports.ipynb`

## Recommended Notebook Structure

### 01_data_exploration.ipynb
**Purpose**: Initial data understanding and quality assessment
- Load and examine raw datasets (HES, Census, amenity data)
- Data quality assessment (missing values, outliers, distributions)
- Exploratory visualizations
- Cross-dataset consistency checks
- Initial hypothesis validation through descriptive statistics

### 02_data_integration.ipynb
**Purpose**: Implement ecological inference methodology
- HES expenditure data processing and categorization
- Census income distribution alignment by planning area
- Weighted average calculations for expenditure fusion
- LLM-assisted expenditure categorization (family vs. non-family)
- Temporal adjustment (CPI corrections 2020-2023)
- Integration validation and quality checks

### 03_feature_engineering.ipynb
**Purpose**: Create analysis-ready variables
- Distance calculations to amenities (childcare, schools, parks)
- Density metrics (facilities within radius)
- Housing characteristic standardization
- Demographic control variable creation
- Interaction term generation (income × amenity access)
- Feature correlation analysis and multicollinearity assessment

### 04_model_development.ipynb
**Purpose**: Regression model building and validation
- Model specification and variable selection
- Multiple regression implementation
- Model diagnostics and assumption testing
- Cross-validation and robustness checks
- Alternative model comparison (Ridge, Lasso)
- Influential observation analysis

### 05_results_analysis.ipynb
**Purpose**: Statistical interpretation and business insights
- Coefficient interpretation and significance testing
- Effect size calculations and practical significance
- Planning area predictions and rankings
- Sensitivity analysis (±15% HES variation)
- Subgroup analysis by income levels
- Geographic pattern identification

### 06_visualization_reports.ipynb
**Purpose**: Generate final visualizations and summaries
- Planning area maps with expenditure patterns
- Amenity-expenditure relationship charts
- Income interaction visualizations
- Policy recommendation visualizations
- LLM-generated insight summaries for stakeholders
- Export publication-ready figures

## Best Practices

### Code Organization
- Use clear markdown headers for each analysis section
- Include brief explanations before complex code blocks
- Comment statistical calculations and modeling decisions
- Display intermediate results for transparency

### Reproducibility Requirements
- Set random seeds for all stochastic operations
- Include library version specifications
- Document data file paths and access methods
- Validate calculations against known benchmarks

### LLM Integration Points
- **Expenditure Categorization**: Automated classification of HES spending categories
- **Quality Assurance**: LLM validation of categorization decisions
- **Insight Generation**: Automated business insight summaries
- **Stakeholder Communication**: Policy-relevant narrative generation

### Output Management
- Save key intermediate datasets to avoid re-computation
- Export final visualizations to `../Outputs/figures/`
- Generate summary statistics tables for report inclusion
- Create reproducible analysis pipeline documentation

## Technical Requirements
- **Python Environment**: Ensure pandas, numpy, scikit-learn, matplotlib, seaborn
- **Geospatial Libraries**: geopandas, folium for spatial analysis
- **Statistical Libraries**: statsmodels for regression diagnostics
- **LLM Integration**: openai or similar API for automated categorization