import json
import jsonschema
from jsonschema import validate

def load_schema(path):
    with open(path, 'r') as f:
        return json.load(f)

def test_schema(name, schema_path, valid_payload, invalid_payload):
    print(f"Testing {name}...")
    schema = load_schema(schema_path)
    
    # Test valid
    try:
        validate(instance=valid_payload, schema=schema)
        print(f"  [PASS] Valid payload")
    except jsonschema.exceptions.ValidationError as e:
        print(f"  [FAIL] Valid payload rejected: {e.message}")
        return False

    # Test invalid
    try:
        validate(instance=invalid_payload, schema=schema)
        print(f"  [FAIL] Invalid payload accepted")
        return False
    except jsonschema.exceptions.ValidationError:
        print(f"  [PASS] Invalid payload rejected")
    
    return True

# 1. OHLCVBar
ohlcv_valid = {
    "time": "2026-07-20T14:00:00Z",
    "open": 1.1025,
    "high": 1.1050,
    "low": 1.1010,
    "close": 1.1035,
    "volume": 2450,
    "timeframe": "H1"
}
ohlcv_invalid = { "open": 1.1 } # Missing fields

# 2. SessionLiquidity
session_valid = {
    "instrument_id": "EUR/USD",
    "session_liquidity_score": 0.87,
    "is_fallback": False
}
session_invalid = { "session_liquidity_score": 1.5 } # Out of range

# 3. BeliefState
belief_valid = {
    "instrument_id": "EUR/USD",
    "timeframe": "H1",
    "timestamp": "2026-07-20T14:00:00Z",
    "belief_vector": [0.45, 0.05, 0.40, 0.07, 0.03, 0.00],
    "entropy": 1.45,
    "regime_label": "UPTREND",
    "confidence": 0.72
}
belief_invalid = { "belief_vector": [0.5, 0.5] } # Wrong length

# Run tests
results = []
results.append(test_schema("OHLCVBar", "../../06_Interfaces/OHLCVBar.schema", ohlcv_valid, ohlcv_invalid))
results.append(test_schema("SessionLiquidity", "../../06_Interfaces/SessionLiquidity.schema", session_valid, session_invalid))
results.append(test_schema("BeliefState", "../../06_Interfaces/BeliefState.schema", belief_valid, belief_invalid))

if all(results):
    print("\nALL CONTRACTS VALIDATED: PASS")
else:
    print("\nCONTRACT VALIDATION: FAILED")
