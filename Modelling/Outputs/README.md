# Model Outputs

This directory stores all generated results, visualizations, and model artifacts from the analysis pipeline.

## Output Organization

### File Structure
```
Outputs/
├── figures/           # Publication-ready visualizations
├── tables/           # Statistical summaries and results tables
├── models/           # Saved model objects and coefficients
├── predictions/      # Planning area predictions and rankings
└── reports/          # Automated LLM-generated insights
```

## Output Categories

### figures/
**Spatial Visualizations**
- `planning_area_expenditure_map.png` - Choropleth map of family expenditure by area
- `amenity_accessibility_maps.png` - Facility proximity and density visualizations
- `income_expenditure_spatial.png` - Geographic patterns of income-expenditure relationships

**Statistical Charts**
- `expenditure_vs_amenity_distance.png` - Scatter plots with regression lines
- `income_interaction_effects.png` - Interaction term visualizations
- `model_diagnostics.png` - Residual plots and validation metrics

**Business Insights**
- `roi_by_planning_area.png` - Infrastructure investment return calculations
- `policy_recommendations_chart.png` - Target area prioritization visualization

### tables/
**Statistical Results**
- `regression_coefficients.csv` - Model parameters with confidence intervals
- `model_performance_metrics.csv` - R², RMSE, validation statistics
- `planning_area_predictions.csv` - Predicted expenditure by area with uncertainty

**Descriptive Statistics**
- `expenditure_summary_by_area.csv` - Planning area expenditure descriptives
- `amenity_accessibility_stats.csv` - Distance and density summary statistics
- `demographic_controls_summary.csv` - Population and housing characteristics

### models/
**Saved Model Objects**
- `final_regression_model.pkl` - Primary analysis model (pickle format)
- `ridge_regression_model.pkl` - Alternative model for comparison
- `model_coefficients.json` - Model parameters in readable format

**Validation Results**
- `cross_validation_results.json` - CV performance metrics
- `sensitivity_analysis_results.json` - Robustness test outcomes

### predictions/
**Planning Area Analysis**
- `area_rankings_by_expenditure.csv` - Sorted planning areas with predictions
- `amenity_optimization_targets.csv` - Areas with highest improvement potential
- `policy_priority_matrix.csv` - Investment recommendation rankings

**Scenario Analysis**
- `amenity_improvement_scenarios.csv` - Predicted impacts of infrastructure changes
- `budget_allocation_optimization.csv` - ROI-based investment recommendations

### reports/
**LLM-Generated Insights**
- `automated_findings_summary.md` - Key insights for stakeholder communication
- `planning_area_insights/` - Individual area analysis summaries
- `policy_recommendations.md` - Actionable business recommendations
- `methodology_explanation.md` - Technical approach for non-technical stakeholders

## File Naming Conventions
- Use ISO date format: `YYYY-MM-DD_description.ext`
- Include model version: `v1_`, `v2_` for iterations
- Specify audience: `_technical`, `_stakeholder`, `_public`

## Quality Assurance
- All outputs include metadata with generation timestamp
- Statistical results include confidence intervals and significance levels
- Visualizations include proper labeling, legends, and source citations
- LLM-generated content includes confidence scores and validation flags

## Reproducibility
- Output generation scripts documented in `../Notebooks/`
- Data lineage tracked from raw data through transformations
- Model versioning with performance comparison tables
- Environment specifications for output recreation

## Usage Guidelines
- Figures are publication-ready with appropriate resolution (300 DPI)
- Tables formatted for direct inclusion in reports
- Model objects can be loaded for additional analysis or deployment
- Reports provide stakeholder-friendly interpretations of technical results