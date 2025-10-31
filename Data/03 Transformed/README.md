# Transformed Data Directory

This folder contains the final, analysis-ready datasets with all transformations, aggregations, and feature engineering applied.

## Key Transformations Applied

### Ecological Inference Integration
- **Income-weighted expenditure fusion** combining HES 2023 and Census 2020 data
- **Formula applied**: Weighted average = Σ(Expenditure_by_income_band × Population_proportion_by_planning_area)
- **Example**: Jurong West education spending = (SGD 300 × 0.40) + (SGD 250 × 0.30) + ...

### Target Variable Creation
**Family-Oriented Expenditure per Member (SGD/month)**
- Aggregated from HES categories: education, healthcare, child recreation
- LLM-assisted classification of spending categories
- Planning area level aggregation
- Per-capita calculations based on household size

### Feature Engineering

#### Housing Characteristics
- Flat type encoding (1-room to Executive)
- Living space per person
- Housing age and condition metrics
- Ownership type (HDB vs. private)

#### Neighbourhood Amenities
- Distance to nearest childcare center (km)
- Number of schools within 1km radius
- Park accessibility index
- Public transport connectivity score
- Healthcare facility proximity

#### Demographic Controls
- Income distribution by planning area
- Population density
- Age structure (% families with children)
- Employment rate by planning area

### Data Adjustments
- **Temporal alignment**: CPI adjustment from 2017/18 HES base to 2020 equivalent
- **Inflation correction**: Education and healthcare costs standardized to 2020 SGD
- **Sample bias mitigation**: Weighting adjustments for under-represented demographics

## Final Dataset Structure

### Primary Analysis Dataset: `family_expenditure_by_planning_area.csv`
Key columns:
- `planning_area`: Geographic identifier
- `family_oriented_expenditure_per_member`: Target variable (SGD/month)
- `avg_distance_to_childcare`: Proximity metric (km)
- `schools_within_1km`: Amenity density count
- `median_household_income`: Income control (SGD/month)
- `pct_families_with_children`: Demographic control (%)

### Supporting Datasets
- `amenity_features_by_area.csv`: Detailed amenity characteristics
- `housing_features_by_area.csv`: Housing stock and characteristics
- `demographic_controls_by_area.csv`: Population and socioeconomic controls

## Validation & Quality Checks
- National totals match HES published figures
- Planning area coverage: 55 areas (100% of residential areas)
- Missing data rate: <5% across key variables
- Cross-validation with external benchmarks

## Usage Notes
- All monetary values in 2020-equivalent SGD
- Distance measurements in kilometers
- Percentages as decimals (0.42 = 42%)
- Ready for regression analysis and visualization