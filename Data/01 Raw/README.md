# Raw Data Directory

This folder contains the original, unprocessed datasets downloaded directly from official sources.

## Data Sources

### Primary Sources
1. **Household Expenditure Survey (HES) 2023**
   - Source: Singapore Department of Statistics
   - URL: https://www.singstat.gov.sg/publications/households/household-expenditure-survey
   - Contains: Monthly household expenditure by category and income band

2. **Census of Population 2020 - Income Distribution**
   - Source: data.gov.sg
   - URL: https://data.gov.sg/datasets/d_2d6793de474551149c438ba349a108fd/view
   - Contains: Resident households by planning area and monthly household income

3. **HDB Dwelling Data (T8 Mapping)**
   - Source: SingStat TableBuilder
   - URL: https://tablebuilder.singstat.gov.sg/statistical-tables/downloadMultiple/sZDBhHEmyUYZNAjc3GJuSg
   - Contains: Mapping between HDB dwellings and monthly income groups

### Secondary Data (Housing & Amenities)
- Planning area boundaries
- School locations and proximity data
- Childcare center locations
- Park and recreational facility data
- Public transport accessibility metrics

## File Naming Convention
- Use ISO date format: YYYY-MM-DD
- Include source abbreviation: `HES_`, `CENSUS_`, `HDB_`
- Example: `2023-10-31_HES_expenditure_by_income.csv`

## Data Integrity
- All files should be in original format as downloaded
- No modifications or transformations
- Preserve original column names and data types
- Include metadata files with download timestamps and source URLs

## Important Notes
- Do not edit files in this directory
- Maintain original file structures
- Document any data collection assumptions
- Files here serve as the authoritative source for reproducibility