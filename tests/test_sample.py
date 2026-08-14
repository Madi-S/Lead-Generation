"""Sample test module for py_lead_generation."""


def test_meaning_of_life() -> None:
    """Test that the meaning of life is 42."""
    meaning = 42
    assert meaning == 42


def test_package_imports() -> None:
    """Test that the package can be imported."""
    from py_lead_generation import GoogleMapsEngine, YelpEngine

    assert GoogleMapsEngine is not None
    assert YelpEngine is not None
