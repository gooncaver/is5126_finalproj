<!--
Sync Impact Report (2025-11-01):
- Version: 0.0.0 → 1.0.0 (Initial constitution creation)
- Principles defined: 5 core research principles
- Sections added: Core Principles, Academic Standards, Governance
- Templates status:
  ✅ plan-template.md - aligns with research workflow
  ✅ spec-template.md - compatible with feature-based development
  ✅ tasks-template.md - supports phased implementation
- Follow-up: None required
-->

# IS5126 Fertility Prediction Project Constitution

## Core Principles

### I. Reproducibility First
All analysis, models, and results MUST be fully reproducible from raw data. Every notebook, script, and model pipeline includes clear documentation, fixed random seeds, environment specifications (requirements.txt, Python version), and step-by-step execution instructions. No "it works on my machine" - results must be verifiable by reviewers and stakeholders.

**Rationale**: Academic integrity and research credibility demand reproducible results. Final project deliverables will be evaluated on reproducibility.

### II. Simplicity Over Complexity
Choose interpretable models and simple methods unless complexity is justified by substantial performance gains. Linear regression, Poisson regression, and tree-based models preferred over deep learning. Code readability trumps cleverness - clear variable names, concise functions, minimal abstraction.

**Rationale**: Project focus is on understanding fertility drivers (feature importance), not chasing marginal accuracy gains. Stakeholders need interpretable insights for policy recommendations.

### III. Data Quality Gates (NON-NEGOTIABLE)
Every data processing step MUST document: input schema validation, missing value handling (with counts and strategy), outlier detection, and filter rationale. No silent data drops - every exclusion logged with justification. Singapore sample size and demographics compared against Census data for representativeness checks.

**Rationale**: Small Singapore sample (n≈1,000-2,000) demands rigorous quality control. Data issues can invalidate findings - they must be transparent and justified.

### IV. Limitation-Aware Interpretation
All findings presented with explicit caveats: cross-sectional limitations (no causality), temporal mismatch (2017-2021 data for 2025 analysis), sample constraints, and reverse causality risks. Model performance expectations realistic (R²≈0.20-0.40 acceptable for social science). No overclaiming - correlations are not causes.

**Rationale**: Constitution acknowledges study limitations documented in proposal Section 10. Findings inform policy exploration, not definitive prescriptions.

### V. Modular Notebooks
Notebooks organized by phase: (1) Data Loading & EDA, (2) Preprocessing & Feature Engineering, (3) Model Training, (4) Evaluation & Interpretation, (5) LLM Integration. Each notebook standalone executable with clear inputs/outputs. No monolithic 2000-line notebooks - split at logical boundaries.

**Rationale**: Phased workflow enables iterative development, easier debugging, and independent review of each analysis stage.

## Academic Standards

### Documentation Requirements
- **Proposal adherence**: Implementation follows refined_proposal.md scope and methodology
- **Code comments**: Explain WHY (rationale), not WHAT (obvious from code)
- **Jupyter narratives**: Markdown cells provide context, interpret outputs, link to research questions
- **README files**: Each subfolder (Data/, Modelling/, Notebooks/) has README explaining contents and workflow

### Model Development
- **Baseline first**: Start with simple baseline (e.g., mean predictor, univariate regression) before complex models
- **Cross-validation**: K-fold CV mandatory for Singapore subset; train-test split if sample permits
- **Feature selection**: Document selection rationale (domain knowledge, statistical methods like LASSO)
- **Hyperparameters**: Log all tuning decisions; avoid excessive grid search on small samples

### Testing & Validation
- **Data integrity tests**: Assert expected shapes, value ranges, no unexpected nulls
- **Model sanity checks**: Coefficients have sensible signs (e.g., family importance → positive effect on fertility)
- **Comparative validation**: Singapore model tested on comparable countries (HK, TW, KR) if feasible

## Governance

### Amendment Process
Constitution amendments require:
1. Documented rationale for change (what problem does it solve?)
2. Impact assessment on existing work (which notebooks/scripts need updates?)
3. Approval via commit to main branch with clear message

### Versioning
- **MAJOR** (X.0.0): Principle removal/redefinition, methodology pivot
- **MINOR** (1.X.0): New principle added, expanded guidance
- **PATCH** (1.0.X): Clarifications, wording fixes

### Compliance Review
- All notebooks checked against Principles I-V before milestone submissions
- Feature branches must reference applicable principles in commit messages
- Final project review includes constitution compliance checklist

### Development Guidance
For day-to-day development decisions not covered by this constitution, refer to:
- `Docs/refined_proposal.md` for research scope and methodology
- `.specify/templates/` for feature specification workflow
- Course rubric (Docs/final_group_project_2025.txt) for evaluation criteria

**Version**: 1.0.0 | **Ratified**: 2025-11-01 | **Last Amended**: 2025-11-01

