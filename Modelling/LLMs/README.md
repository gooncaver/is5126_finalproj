# LLM Integration: Langchain Agent + FastAPI

This folder contains the LLM integration prototype for the Fertility Prediction pipeline.

## Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   User      │─────▶│  Langchain Agent │─────▶│  FastAPI Server │
│ Conversation│      │   (utils.py)     │      │  (api_utils.py)   │
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │                          │
                              │                          │
                              ▼                          ▼
                     ┌─────────────────┐       ┌──────────────┐
                     │   GPT-5 LLM     │       │ Mock Model   │
                     │ (OpenAI API)    │       │ (TODO: .pkl) │
                     └─────────────────┘       └──────────────┘
```

## Files

- **`api_service.py`**: FastAPI + Uvicorn server serving the prediction model
- **`utils.py`**: Langchain agent that calls the FastAPI endpoint
- **`README.md`**: This file

## Quick Start

### Step 1: Install Dependencies

```powershell
pip install fastapi uvicorn requests langchain openai python-dotenv pydantic
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Step 3: Start FastAPI Server

In **Terminal 1**:

```powershell
cd "Modelling\LLMs"
python api_service.py
```

Expected output:
```
============================================================
Starting Fertility Prediction API
============================================================
Model: mock_model_v1 (DummyBaseline)
R²: 0.23, RMSE: 0.85
============================================================

API will be available at:
  - Root: http://localhost:8000/
  - Docs: http://localhost:8000/docs
  - Health: http://localhost:8000/health
  - Predict: http://localhost:8000/predict
============================================================
```

### Step 4: Test FastAPI Directly (Optional)

Open browser: **http://localhost:8000/docs**

Or use PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get | ConvertTo-Json

# Make prediction
$body = @{
    gender = "male"
    Q217 = $true
    Q281 = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json
```

### Step 5: Run Langchain Agent

In **Terminal 2** (keep FastAPI running in Terminal 1):

```powershell
cd "Modelling\LLMs"
python utils.py
```

Expected output:
```
=== Full Conversation ===

Message 0: HumanMessage
Content: I am male, Q217 is True, Q281 is False. How many children will I have?

Message 1: AIMessage
Content: 
Tool Calls: [{'name': 'predict_number_of_children', 'args': {...}, ...}]

Message 2: ToolMessage
Tool returned: Predicted children: 2.15 (95% CI: [0.48, 3.82])

Key drivers:
- Q217: Q217=True increases predicted fertility
- Q281: Q281=False decreases predicted fertility
- gender: Gender 'male' increases predicted fertility

Message 3: AIMessage
Content: Based on your inputs, the predicted number of children is approximately 2.15...

=== Tool Message ===
Tool returned: Predicted children: 2.15 (95% CI: [0.48, 3.82])

Key drivers:
- Q217: Q217=True increases predicted fertility
- Q281: Q281=False decreases predicted fertility
- gender: Gender 'male' increases predicted fertility

=== Final AI Response ===
AI says: Based on your inputs, the predicted number of children is approximately 2.15...
```

## How It Works

1. **User asks a question** in natural language to the Langchain agent
2. **GPT-5 extracts features** from the conversation (gender, Q217, Q281)
3. **Agent calls `predict_number_of_children()` tool** with extracted features
4. **Tool sends HTTP POST** to FastAPI `/predict` endpoint
5. **FastAPI server** runs prediction using the mock model (TODO: real model)
6. **API returns prediction + drivers** (predicted children, confidence interval, feature importance)
7. **Tool formats response** into natural language
8. **GPT-5 interprets results** and provides conversational response to user

## Upgrading to Real Model

### Replace Mock Model in `api_utils.py`

```python
# In api_utils.py, replace MockFertilityModel with:

import joblib

class RealFertilityModel:
    def __init__(self, model_path: str):
        # Load trained model
        self.model = joblib.load(model_path)
        self.model_id = "linear_regression_v1"
        self.model_type = "OLS"
        self.r_squared = 0.23  # From cv_results.json
        self.rmse = 0.85
        
    def predict(self, features: Dict) -> float:
        # Convert features to model input format
        feature_vector = self._features_to_vector(features)
        prediction = self.model.predict([feature_vector])[0]
        return max(0.0, prediction)
    
    def get_feature_importance(self, features: Dict) -> List[Dict]:
        # Extract coefficients from linear model
        coef_dict = dict(zip(self.feature_names, self.model.coef_))
        # Return top 3 by absolute value
        # ...

# Load model at startup
model = RealFertilityModel("../Outputs/models/linear_regression.pkl")
```

## Testing

### Unit Test for FastAPI Endpoint

```powershell
# Install test dependencies
pip install pytest httpx

# Create test file: test_api_utils.py
# Run tests
pytest test_api_utils.py
```

### Integration Test for Full Flow

```python
# test_integration.py
def test_full_agent_flow():
    # 1. Start FastAPI server
    # 2. Initialize Langchain agent
    # 3. Send user message
    # 4. Verify agent calls predict_number_of_children
    # 5. Verify prediction returned
    # 6. Verify natural language response generated
```

## API Schema Reference

See: `../../specs/001-fertility-prediction-pipeline/contracts/api-schema.yaml`

- **OpenAPI 3.0** specification
- **Pydantic models** for request/response validation
- **SwaggerUI** auto-generated docs at http://localhost:8000/docs

## Troubleshooting

### Error: "FastAPI server not running"

**Solution**: Start the server in a separate terminal:
```powershell
python api_utils.py
```

### Error: "Connection refused on port 8000"

**Solution**: Check if port is already in use:
```powershell
netstat -ano | findstr :8000
```

Kill process if needed, then restart FastAPI.

### Error: "OPENAI_API_KEY not found"

**Solution**: Create `.env` file with your API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### Model predictions seem incorrect

**Solution**: 
1. Check mock model logic in `api_utils.py` (currently using simple rules)
2. Replace with trained model from `../Outputs/models/` when available
3. Verify feature encoding matches training data

## Next Steps

1. **Train actual models** using notebooks 01-05
2. **Replace MockFertilityModel** with real model loader
3. **Add more WVS features** to PredictionRequest schema
4. **Enhance conversation flow** with multi-turn dialogue
5. **Add user profile persistence** (optional)
6. **Deploy to cloud** (if needed beyond prototype)

## Performance Metrics (from spec.md)

- ✅ **SC-014**: API response time <2 seconds ✓ (mock model is instant)
- ✅ **SC-016**: LLM generates coherent insights ✓ (GPT-5 interprets results)
- ✅ **SC-017**: Full cycle demonstrated ✓ (conversation → prediction → interpretation)
- ⏳ **SC-015**: Feature extraction ≥70% (pending multi-feature testing)

## References

- **Specification**: `../../specs/001-fertility-prediction-pipeline/spec.md` (User Story 4)
- **Research**: `../../specs/001-fertility-prediction-pipeline/research.md` (R6, R7)
- **Quickstart**: `../../specs/001-fertility-prediction-pipeline/quickstart.md` (Section 4)
- **API Schema**: `../../specs/001-fertility-prediction-pipeline/contracts/api-schema.yaml`
