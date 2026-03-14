import pytest
from stepgen_app.validator import ScrewRequest, WasherRequest, AssemblyRequest

def test_screw_diameter_validation():
    # Valid data
    assert ScrewRequest(diameter=10.0, length=50.0)
    # Invalid diameter (7.3 is not in ISO table)
    with pytest.raises(ValueError):
        ScrewRequest(diameter=7.3, length=50.0)

def test_screw_shanktooshort_validation():
    # Valid data
    assert ScrewRequest(diameter=5.0, length=15.0)
    # Too short shank length (for M5 minimum is 10 millimeters)
    with pytest.raises(ValueError):
        ScrewRequest(diameter=5.0, length=1.0)

def test_screw_shanktoolong_validation():
    # Valid data
    assert ScrewRequest(diameter=8.0, length=75.0)
    # Too great shank length (for M8 maximum is 80 millieters)
    with pytest.raises(ValueError):
        ScrewRequest(diameter=8.0, length=94.0)

def test_washer_diameters_validation():
    # Valid data
    assert WasherRequest(inner_diameter=4.0, outer_diameter=8.0, thickness=2)
    # Inner diameter is greater than outer diameter
    with pytest.raises(ValueError):
        WasherRequest(inner_diameter=8.0, outer_diameter=4.0, thickness=2)

def test_assembly_mismatch():
    # Attempting to put an M12 screw in an M8 washer hole
    payload = {
        "screw": {"diameter": 12, "length": 50},
        "washer": {"inner_diameter": 8, "outer_diameter": 20, "thickness": 2}
    }
    with pytest.raises(ValueError, match="Washer inner diameter is smaller"):
        AssemblyRequest(**payload)