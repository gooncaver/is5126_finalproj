# Data Directory

This directory contains all datasets used in the IS5126 Final Project analyzing the influence of housing characteristics and neighbourhood amenities on family-oriented household expenditures in Singapore.

## Project Context
Our analysis combines data from:
- Household Expenditure Survey (HES) 2023 Report
- Singapore Department of Statistics Report on income distributions within Household Planning Areas
- Housing and amenity data for ecological inference techniques

## Data Processing Pipeline
The data flows through three main stages:

### 01 Raw/
- Contains original, unprocessed datasets
- Direct downloads from SingStat and data.gov.sg
- No modifications or transformations applied

### 02 Clean/
- Processed datasets with basic cleaning applied
- Missing values handled
- Data quality issues resolved
- Standardized formats and naming conventions

### 03 Transformed/
- Final datasets ready for analysis
- Income-weighted fusion applied using ecological inference
- Family-oriented expenditure categories aggregated
- Planning area level aggregations completed

## Target Variable
Average monthly family-oriented household expenditure per member (SGD), derived from HES categories including:
- Education expenses
- Healthcare costs
- Child-related recreation spending

## Data Integration Method
Uses ecological inference to combine:
1. HES expenditure data (aggregated by income band)
2. Census 2020 income distribution by planning area
3. Weighted average calculation: E.g., (SGD 300 × 0.40) + (SGD 250 × 0.30) + ...

## Important Notes
- All expenditure data adjusted to 2020-equivalent SGD using CPI
- Temporal alignment considerations between HES 2023 and Census 2020 data
- Sampling bias mitigation strategies implemented for urban/employment representation