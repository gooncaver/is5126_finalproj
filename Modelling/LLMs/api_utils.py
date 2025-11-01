"""
FastAPI service for fertility prediction.
Serves trained model via REST API for Langchain agent integration.

Based on specs/001-fertility-prediction-pipeline/contracts/api-schema.yaml
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
import numpy as np
from datetime import datetime

app = FastAPI(
    title="Fertility Prediction API",
    description="Predict number of children based on WVS features",
    version="1.0.0"
)


# ============================================================================
# Pydantic Models (Request/Response Schemas)
# ============================================================================

class PredictionRequest(BaseModel):
    """Request schema for /predict endpoint"""
    gender: str = Field(..., description="Gender: 'male' or 'female'")
    Q217: bool = Field(..., description="Q217 WVS feature (placeholder)")
    Q281: bool = Field(..., description="Q281 WVS feature (placeholder)")
    
    # Optional: Add more WVS features as needed
    Q1: Optional[int] = Field(None, ge=1, le=4, description="Importance of family (1-4)")
    Q262: Optional[int] = Field(None, ge=25, le=49, description="Age in years")
    Q288: Optional[int] = Field(None, ge=1, le=10, description="Income scale (1-10)")

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "male",
                "Q217": True,
                "Q281": False,
                "Q1": 1,
                "Q262": 28,
                "Q288": 6
            }
        }


class FeatureImportance(BaseModel):
    """Feature importance/driver information"""
    name: str
    coefficient: float
    interpretation: str


class ModelMetadata(BaseModel):
    """Model metadata"""
    model_id: str
    model_type: str
    r_squared: Optional[float] = None
    rmse: Optional[float] = None


class PredictionResponse(BaseModel):
    """Response schema for /predict endpoint"""
    predicted_children: float = Field(..., description="Predicted number of children")
    confidence_interval: List[float] = Field(..., description="95% CI [lower, upper]")
    drivers: List[FeatureImportance] = Field(..., description="Top predictive features")
    metadata: ModelMetadata


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_id: Optional[str] = None
    uptime_seconds: Optional[int] = None


# ============================================================================
# Mock Model (Replace with actual trained model)
# ============================================================================

class MockFertilityModel:
    """
    Mock model for demonstration.
    TODO: Replace with actual trained model loaded from .pkl file
    """
    
    def __init__(self):
        self.model_id = "mock_model_v1"
        self.model_type = "DummyBaseline"
        self.r_squared = 0.23
        self.rmse = 0.85
        
        # Mock coefficients for feature importance
        self.feature_importance = {
            "gender": 0.15,
            "Q217": 0.35,
            "Q281": -0.22,
            "Q1": 0.45,
            "Q262": 0.18,
            "Q288": 0.32
        }
    
    def predict(self, features: Dict) -> float:
        """
        Mock prediction logic.
        TODO: Replace with model.predict(feature_vector)
        """
        # Simple rule-based logic for demo
        base_prediction = 1.5
        
        if features.get("gender") == "female":
            base_prediction += 0.3
        
        if features.get("Q217"):
            base_prediction += 0.5
        
        if features.get("Q281"):
            base_prediction -= 0.3
        
        # Add effect of optional features
        if features.get("Q1"):
            # Family importance: lower value = higher importance = more children
            base_prediction += (5 - features["Q1"]) * 0.2
        
        if features.get("Q262"):
            # Age effect: slight positive (completed fertility)
            base_prediction += (features["Q262"] - 25) * 0.01
        
        if features.get("Q288"):
            # Income effect: higher income = more children
            base_prediction += features["Q288"] * 0.05
        
        # Ensure non-negative
        return max(0.0, base_prediction)
    
    def get_feature_importance(self, features: Dict) -> List[Dict]:
        """
        Get top 3 feature drivers.
        TODO: Replace with actual feature importance from trained model
        """
        # Calculate which features were most influential
        drivers = []
        
        for feature, coef in sorted(
            self.feature_importance.items(), 
            key=lambda x: abs(x[1]), 
            reverse=True
        )[:3]:
            if feature in features:
                interpretation = self._interpret_feature(feature, features[feature], coef)
                drivers.append({
                    "name": feature,
                    "coefficient": coef,
                    "interpretation": interpretation
                })
        
        return drivers
    
    def _interpret_feature(self, feature: str, value, coefficient: float) -> str:
        """Generate human-readable interpretation"""
        direction = "increases" if coefficient > 0 else "decreases"
        
        interpretations = {
            "gender": f"Gender '{value}' {direction} predicted fertility",
            "Q217": f"Q217={value} {direction} predicted fertility",
            "Q281": f"Q281={value} {direction} predicted fertility",
            "Q1": f"Family importance (Q1={value}) {direction} predicted fertility",
            "Q262": f"Age {value} years {direction} predicted fertility (completed fertility)",
            "Q288": f"Income level {value}/10 {direction} predicted fertility"
        }
        
        return interpretations.get(feature, f"{feature}={value} {direction} predicted fertility")


# ============================================================================
# Global Model Instance
# ============================================================================

# Initialize model at startup
# TODO: Load actual trained model from Modelling/Outputs/models/
model = MockFertilityModel()
startup_time = datetime.now()


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Fertility Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict (POST)"
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint.
    Returns API status and model information.
    """
    uptime = (datetime.now() - startup_time).total_seconds()
    
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        model_id=model.model_id if model else None,
        uptime_seconds=int(uptime)
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_fertility(request: PredictionRequest):
    """
    Predict number of children based on WVS features.
    
    This endpoint is called by the Langchain agent's predict_number_of_children tool.
    """
    try:
        # Convert request to feature dict
        features = {
            "gender": request.gender,
            "Q217": request.Q217,
            "Q281": request.Q281
        }
        
        # Add optional features if provided
        if request.Q1 is not None:
            features["Q1"] = request.Q1
        if request.Q262 is not None:
            features["Q262"] = request.Q262
        if request.Q288 is not None:
            features["Q288"] = request.Q288
        
        # Make prediction
        predicted_children = model.predict(features)
        
        # Calculate confidence interval (rough estimate using RMSE)
        ci_lower = max(0.0, predicted_children - 1.96 * model.rmse)
        ci_upper = predicted_children + 1.96 * model.rmse
        
        # Get feature importance
        drivers_raw = model.get_feature_importance(features)
        drivers = [
            FeatureImportance(**driver) 
            for driver in drivers_raw
        ]
        
        # Build metadata
        metadata = ModelMetadata(
            model_id=model.model_id,
            model_type=model.model_type,
            r_squared=model.r_squared,
            rmse=model.rmse
        )
        
        # Return response
        return PredictionResponse(
            predicted_children=round(predicted_children, 2),
            confidence_interval=[round(ci_lower, 2), round(ci_upper, 2)],
            drivers=drivers,
            metadata=metadata
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/models", tags=["Models"])
async def list_models():
    """
    List available models.
    TODO: Implement model registry when multiple models available.
    """
    return {
        "models": [
            {
                "model_id": model.model_id,
                "model_type": model.model_type,
                "status": "active",
                "performance": {
                    "r_squared": model.r_squared,
                    "rmse": model.rmse
                }
            }
        ]
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    """
    Run the FastAPI server with Uvicorn.
    
    Usage:
        python fastapi.py
        
    Or with hot reload:
        uvicorn fastapi:app --reload --port 8000
    """
    print("=" * 60)
    print("Starting Fertility Prediction API")
    print("=" * 60)
    print(f"Model: {model.model_id} ({model.model_type})")
    print(f"R²: {model.r_squared}, RMSE: {model.rmse}")
    print("=" * 60)
    print("\nAPI will be available at:")
    print("  - Root: http://localhost:8000/")
    print("  - Docs: http://localhost:8000/docs")
    print("  - Health: http://localhost:8000/health")
    print("  - Predict: http://localhost:8000/predict")
    print("=" * 60)
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
