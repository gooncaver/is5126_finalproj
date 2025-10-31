# Clean Data Directory

This folder contains processed datasets with basic cleaning and standardization applied, ready for transformation and analysis.

## Data Processing Applied

### Quality Assurance
- Missing value identification and handling
- Outlier detection and treatment
- Data type standardization
- Duplicate record removal

### Standardization
- Consistent column naming conventions (snake_case)
- Standardized planning area names
- Income band harmonization across datasets
- Date format standardization (YYYY-MM-DD)

### Data Integration Preparation
- Alignment of categorical variables across datasets
- Creation of common identifier keys for joining
- Validation of data ranges and constraints

## Key Datasets

### Expenditure Data (HES Cleaned)
- Standardized spending categories
- Income band alignment with Census data
- Family-oriented vs. non-family-oriented expenditure classification
- Missing expenditure estimates for incomplete survey responses

### Income Distribution Data (Census Cleaned)
- Planning area name standardization
- Income bracket consistency with HES categories  
- Population weight calculations
- Geographic boundary alignment

### Housing & Amenity Data (Cleaned)
- Geocoded facility locations
- Distance calculations to amenities
- Housing type standardization
- Planning area assignments

## Data Quality Metrics
- Completeness rates by dataset
- Value range validations
- Cross-dataset consistency checks
- Population coverage assessments

## Processing Log
Each cleaned dataset should include:
- Processing timestamp
- Cleaning steps applied
- Data quality flags
- Validation results

## File Format
- Primary format: CSV with UTF-8 encoding
- Backup format: Parquet for large datasets
- Metadata: JSON sidecar files with processing details