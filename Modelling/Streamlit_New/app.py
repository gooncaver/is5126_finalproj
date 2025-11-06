
"""
Streamlit app for predicting with a pre-trained Random Forest pipeline.
This version does NOT require a CSV upload. Instead, it shows input fields for selected top features
listed in rf_top20.csv (first column). Remaining features are left blank and imputed by the pipeline.
It also introspects the saved model to ensure all required input columns exist, preventing 'columns are missing' errors.
"""

import json
import re
from collections import OrderedDict
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# Compatibility shim for pickled sklearn pipelines that reference private internals
try:
    # If available, this import will satisfy unpickling
    from sklearn.compose._column_transformer import _RemainderColsList  # type: ignore[attr-defined]
except Exception:
    # If import fails (version mismatch), inject a dummy into the module so pickle can resolve it
    try:
        import sklearn.compose._column_transformer as _ct  # type: ignore

        class _RemainderColsList(list):
            pass

        _ct._RemainderColsList = _RemainderColsList  # type: ignore[attr-defined]
    except Exception:
        # As a last resort, continue; joblib.load may still succeed for some artifacts
        pass

# Artifact paths (same folder as this script)
ARTIFACT_DIR = Path(__file__).parent
MODEL_PATH = ARTIFACT_DIR / "rf_pipeline.joblib"
META_PATH = ARTIFACT_DIR / "rf_meta.json"
TOP20_PATH = ARTIFACT_DIR / "rf_top20.csv"


def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        st.error(
            f"Failed to load model artifact '{MODEL_PATH.name}'. Ensure the file exists and sklearn versions are compatible. Details: {e}"
        )
        return None


def load_meta():
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Metadata is optional (only used for target column name); warn but continue
        st.warning(
            f"Could not load metadata file '{META_PATH.name}'. Using default target column name. Details: {e}"
        )
        return None


def load_top20_features():
    """
    Read rf_top20.csv directly: use the first column as feature names.
    Returns: list[str] of feature names (could be engineered/one-hot names).
    """
    try:
        df = pd.read_csv(TOP20_PATH)
        if df.empty:
            st.error(f"'{TOP20_PATH.name}' is empty.")
            return None
        # Use the first column directly as feature names
        features = df.iloc[:, 0].astype(str).dropna().tolist()
        if not features:
            st.error(f"No feature names found in '{TOP20_PATH.name}'.")
            return None
        return features
    except Exception as e:
        st.error(f"Failed to load top-20 features from '{TOP20_PATH.name}'. Details: {e}")
        return None


_NUMERIC_SUFFIX_RE = re.compile(r"^-?\d+(?:\.\d+)?$")

def to_base_feature_name(name: str) -> str:
    """
    Convert a possibly one-hot feature name like
      "Q273: Marital status_6.0" -> "Q273: Marital status"
    Heuristic: if there's an underscore and the last token looks numeric (code/category),
    drop the suffix. Otherwise, keep as-is.
    """
    if "_" in name:
        left, right = name.rsplit("_", 1)
        if _NUMERIC_SUFFIX_RE.match(right.strip()):
            return left.strip()
    return name.strip()

def derive_raw_features_from_top20(top20: list[str]) -> list[str]:
    """
    Derive raw/base column names expected in the uploaded CSV from top20 list.
    This collapses engineered one-hot names back to their source column names,
    preserving order and uniqueness.
    """
    seen = OrderedDict()
    for f in top20:
        base = to_base_feature_name(str(f))
        if base not in seen:
            seen[base] = True
    return list(seen.keys())

def is_probably_numeric(col_name: str) -> bool:
    hint = col_name.lower()
    patterns = [
        "age", "year", "number", "count", "latitude", "longitude", "income", "amount", "score", "height", "weight"
    ]
    return any(p in hint for p in patterns)

def coerce_value(name: str, s: str):
    s = (s or "").strip()
    if s == "":
        return None
    if is_probably_numeric(name):
        try:
            return float(s)
        except Exception:
            st.warning(f"Could not parse a numeric value for '{name}'. Treating as missing.")
            return None
    return s

def infer_required_input_columns(model) -> list[str] | None:
    """
    Try to infer the raw input column names the model expects when calling predict(X as DataFrame).
    Prefer the sklearn-wide attribute `feature_names_in_`. Fallback to common pipeline patterns.
    """
    # Primary: most sklearn estimators/pipelines expose feature_names_in_ after fit when trained on DataFrame
    cols = getattr(model, "feature_names_in_", None)
    if cols is not None:
        return list(cols)
    # Pipeline fallback: look for a 'pre' or 'preprocessor' step with feature_names_in_'
    pre = None
    for key in ("pre", "preprocessor"):
        try:
            pre = model.named_steps.get(key)  # type: ignore[attr-defined]
            if pre is not None:
                break
        except Exception:
            pass
    if pre is not None:
        cols = getattr(pre, "feature_names_in_", None)
        if cols is not None:
            return list(cols)
    return None

def pretty_label(eng_name: str, raw_name: str) -> str:
    """
    Make a human-friendly label. Special-case marital status to 'Marital Status'.
    Otherwise: strip leading 'Q123: ' and remove trailing encoded suffix from engineered name.
    """
    low = eng_name.lower()
    if "marital status" in low:
        return "Marital Status"
    # generic cleanup
    label = eng_name
    if ":" in label:
        label = label.split(":", 1)[1].strip()
    if "_" in label:
        label = label.rsplit("_", 1)[0]
    return label or raw_name

def main():
    st.set_page_config(page_title="Expected No. of Children – Predictor", page_icon="👶", layout="wide")

    # Global CSS to polish look & feel
    st.markdown(
        """
        <style>
        .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1, h2, h3 { font-weight: 700; }
        .stSelectbox label, .stTextInput label { font-weight: 600; }
        .stButton>button {
            background: #4f46e5; color: #ffffff;
            padding: 0.6rem 1rem; border-radius: 8px; border: 1px solid transparent;
        }
        .stButton>button:hover { background: #4338ca; }
        .metric-card {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            border: 1px solid #e5e7eb; border-radius: 16px; padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .metric-value {
            font-size: 56px; font-weight: 800; line-height: 1; color: #111827;
        }
        .metric-sub { color: #6b7280; margin-bottom: 6px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("👶 Expected No. of Children – Predictor")
    st.caption("Enter values for a few of the most important features.")

    # Sidebar with quick info
    with st.sidebar:
        st.header("About")
        st.markdown(
            "This app uses a pre-trained Random Forest pipeline and the top features from rf_top20.csv to make a prediction."
        )
        st.divider()
        st.subheader("Artifacts")
        for p in (MODEL_PATH, TOP20_PATH, META_PATH):
            exists = p.exists()
            emoji = "✅" if exists else "❌"
            st.write(f"{emoji} {p.name}")

    model = load_model()
    meta = load_meta()  # optional

    if model is None:
        st.stop()

    # Load top-20 features from CSV (post-encoding names are possible)
    top20_features = load_top20_features()
    if not top20_features:
        st.stop()

    # Exclude engineered features we don't want in the UI (case-insensitive)
    excluded_phrases = ["year of birth"]
    filtered_engineered = [f for f in top20_features if all(p not in f.lower() for p in excluded_phrases)]
    # Pick top-5 after exclusion (backfill with next features)
    top_engineered = filtered_engineered[:5]

    # Derive full raw feature list from the top-20 (for display; may be narrower or wider than model's actual requirement)
    raw_features_from_top20 = derive_raw_features_from_top20(top20_features)

    # Infer the model's required raw input columns (best-effort)
    required_cols = infer_required_input_columns(model)
    if required_cols is None:
        # Fallback: assume raw columns are those derived from top-20 (may still fail if model expects more)
        required_cols = raw_features_from_top20
        # Hidden info message previously shown to user is now suppressed.


    # Map engineered -> raw for the selected inputs
    mapping = {eng: to_base_feature_name(eng) for eng in top_engineered}

    # Decide target column name from metadata if available (kept for internal reference),
    # but display the prediction as 'Expected No. of Children'.
    if isinstance(meta, dict):
        target_column = meta.get("target_column", "prediction")
    else:
        target_column = "prediction"
    display_label = "Expected No. of Children"

    st.subheader("Input values")
    with st.form("predict_form"):
        inputs_raw = {}
        display_labels = {}
        cols = st.columns(min(3, len(mapping)) or 1)
        for idx, (eng, raw) in enumerate(mapping.items()):
            col = cols[idx % len(cols)]
            with col:
                label = pretty_label(eng, raw)
                display_labels[raw] = label
                low_eng = eng.lower()
                low_raw = raw.lower()
                if "marital status" in low_eng:
                    # Labeled dropdown for marital status while storing numeric code
                    options = [
                        (1, "Married"),
                        (2, "Living together as married"),
                        (3, "Divorced"),
                        (4, "Separated"),
                        (5, "Widowed"),
                        (6, "Single"),
                    ]
                    sel = st.selectbox(
                        label,
                        options=options,
                        index=None,
                        placeholder="Select marital status",
                        format_func=lambda x: f"{x[0]}. {x[1]}"
                    )
                    inputs_raw[raw] = float(sel[0]) if sel is not None else None
                elif ("live with your parents" in low_eng) or ("live with your parents" in low_raw) or (("live with" in low_eng and "parent" in low_eng) or ("live with" in low_raw and "parent" in low_raw)):
                    # Labeled dropdown for 'Do you live with your parents?' mapping to numeric code
                    options = [
                        (1, "No"),
                        (2, "Yes, own parent(s)"),
                        (3, "Yes, parent(s) in law"),
                        (4, "Yes, both own parent(s) and parent(s) in law"),
                    ]
                    sel = st.selectbox(
                        label,
                        options=options,
                        index=None,
                        placeholder="Select an option",
                        format_func=lambda x: f"{x[0]}. {x[1]}"
                    )
                    inputs_raw[raw] = float(sel[0]) if sel is not None else None
                elif ("sex before marriage" in low_eng) or ("sex before marriage" in low_raw) or (("justifiable" in low_eng and "sex" in low_eng) or ("justifiable" in low_raw and "sex" in low_raw)):
                    # Labeled dropdown for 'Justifiable sex before marriage' on a 1–10 scale with explicit labels
                    options = [
                        (1, "1.- Never justifiable"),
                        (2, "2.- 2"),
                        (3, "3.- 3"),
                        (4, "4.- 4"),
                        (5, "5.- 5"),
                        (6, "6.- 6"),
                        (7, "7.- 7"),
                        (8, "8.- 8"),
                        (9, "9.- 9"),
                        (10, "10.- Always justifiable"),
                    ]
                    sel = st.selectbox(
                        "Justifiable Sex Before Marriage",
                        options=options,
                        index=None,
                        placeholder="Select a value 1–10",
                        format_func=lambda x: x[1]
                    )
                    inputs_raw[raw] = float(sel[0]) if sel is not None else None
                elif ("number of people in household" in low_eng) or ("number of people in household" in low_raw) or (("household" in low_eng and "people" in low_eng) or ("household" in low_raw and "people" in low_raw)) or ("household size" in low_eng) or ("household size" in low_raw):
                    # Labeled dropdown for 'Number of people in household'
                    options = [
                        (1, "1 Person"),
                        (2, "2 Persons"),
                        (3, "3 Persons"),
                        (4, "4 Persons"),
                        (5, "5 Persons"),
                        (6, "6 Persons"),
                        (7, "7 Persons or more"),
                    ]
                    sel = st.selectbox(
                        label,
                        options=options,
                        index=None,
                        placeholder="Select household size",
                        format_func=lambda x: f"{x[0]}. {x[1]}"
                    )
                    inputs_raw[raw] = float(sel[0]) if sel is not None else None
                elif ("age" in low_eng) or ("age" in low_raw):
                    # Age selection: allow choosing from 20 to 49
                    sel = st.selectbox(label, options=list(range(20, 50)), index=None, placeholder="Select age 20-49")
                    inputs_raw[raw] = float(sel) if sel is not None else None
                else:
                    placeholder = "Leave blank to let model impute"
                    if eng != raw:
                        placeholder += f" (enter category/code for '{raw}')"
                    val_str = st.text_input(label, placeholder=placeholder)
                    inputs_raw[raw] = coerce_value(raw, val_str)

        submitted = st.form_submit_button("Predict")

    if submitted:
        # Validate: prompt user if any fields are blank
        missing = [display_labels.get(raw, raw) for raw, val in inputs_raw.items() if (val is None or (isinstance(val, str) and str(val).strip() == ""))]
        if missing:
            st.warning("Some inputs are missing. Please fill all fields before predicting.")
            st.markdown("\n".join([f"- {m}" for m in missing]))
            st.stop()

        # Build a single-row input with ALL columns the model expects, default to None
        row = {col_name: None for col_name in required_cols}
        # Fill provided inputs (only where the raw column exists)
        for raw, val in inputs_raw.items():
            if raw in row:
                row[raw] = val
        X = pd.DataFrame([row], columns=required_cols)

        # Predict. If model is a full sklearn Pipeline, it will handle preprocessing internally.
        try:
            predictions = model.predict(X)
        except Exception as e:
            st.error(
                "Prediction failed. The saved artifact may not be a full preprocessing pipeline, ",
                "or it expects columns that cannot be imputed. ",
            )
            st.exception(e)
            return

        # Present the prediction in a styled, centered card
        try:
            pred_value = float(predictions[0])
        except Exception:
            pred_value = float(pd.Series(predictions).iloc[0])
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.markdown(
                f"""
                <div class='metric-card' style='text-align:center;'>
                    <div class='metric-sub'>{display_label}</div>
                    <div class='metric-value'>{pred_value:.1f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
