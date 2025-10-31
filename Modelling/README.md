# Modelling Directory

This directory contains all analytical code, model development, and output generation materials for the IS5126 Final Project.

## Project Modeling Approach

### Core Analysis Framework
**Regression Problem**: Predicting average monthly family-oriented household expenditure per member (SGD) based on housing characteristics and neighborhood amenities.

**Target Variable**: Family-oriented expenditure per member, derived from HES categories (education, healthcare, child recreation)

**Key Predictors**:
- Housing characteristics (flat type, size, age)
- Neighborhood amenities (childcare distance, school density, park access)
- Demographic controls (income, family composition, population density)

## Directory Structure

### Notebooks/
Jupyter notebooks containing:
- Data exploration and visualization
- Ecological inference implementation
- Feature engineering pipelines
- Model development and validation
- Results interpretation and visualization

### Outputs/
Generated results including:
- Model performance metrics and validation results
- Regression coefficients and statistical summaries
- Visualizations (plots, maps, charts)
- Prediction outputs by planning area
- Business insight summaries

### utils/
Supporting utility functions:
- Data preprocessing modules
- Statistical analysis helpers
- Visualization functions
- LLM integration utilities
- Validation and testing functions

## Modeling Strategy

### 1. Data Integration (Ecological Inference)
- **Method**: Income-weighted fusion of HES expenditure and Census income distribution
- **Formula**: E(planning_area) = Σ(Expenditure_income_band × Population_proportion)
- **Validation**: National totals verification against HES published figures

### 2. Feature Engineering
- **Distance Metrics**: Euclidean distances to key amenities
- **Density Measures**: Count of facilities within 1km radius
- **Interaction Terms**: Income × amenity access interactions
- **Categorical Encoding**: Planning area, housing type standardization

### 3. Model Development
- **Primary Model**: Multiple linear regression with robust standard errors
- **Alternative Models**: Ridge regression for multicollinearity handling
- **Validation**: Cross-validation and holdout testing
- **Diagnostics**: Residual analysis, influential observation detection

### 4. LLM Integration Points
- **Automated Categorization**: Family vs. non-family expenditure classification
- **Insight Generation**: Automated stakeholder communication summaries
- **Quality Assurance**: Validation of categorization decisions

## Key Analysis Questions
1. How do amenities affect family spending across income levels?
2. Which planning areas show optimal amenity-expenditure relationships?
3. What is the ROI of infrastructure investment in middle-income areas?
4. How do high-income areas differ in amenity sensitivity?

## Model Validation & Robustness
- **Sensitivity Analysis**: ±15% variation in HES bin averages
- **Temporal Adjustment**: CPI correction for 2020-2023 alignment
- **Sample Bias Correction**: Employment status weighting adjustments
- **Geographic Validation**: Spatial autocorrelation testing

## Expected Outcomes
- Planning area rankings by family investment efficiency
- Amenity impact quantification (SGD/month per km reduction)
- Policy recommendations with ROI calculations
- Spatial visualization of optimization opportunities