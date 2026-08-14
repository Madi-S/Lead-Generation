"""Tests for engine classes."""

import pytest


def test_google_maps_engine_import() -> None:
    """Test that GoogleMapsEngine can be imported."""
    from py_lead_generation import GoogleMapsEngine

    assert GoogleMapsEngine is not None


def test_yelp_engine_import() -> None:
    """Test that YelpEngine can be imported."""
    from py_lead_generation import YelpEngine

    assert YelpEngine is not None


def test_twogis_engine_import() -> None:
    """Test that TwoGisEngine can be imported."""
    from py_lead_generation import TwoGisEngine

    assert TwoGisEngine is not None


def test_google_maps_engine_instantiation() -> None:
    """Test that GoogleMapsEngine can be instantiated."""
    from py_lead_generation import GoogleMapsEngine

    engine = GoogleMapsEngine("test", "Paris")
    assert engine.query == "test"
    assert engine.location == "Paris"


def test_yelp_engine_instantiation() -> None:
    """Test that YelpEngine can be instantiated."""
    from py_lead_generation import YelpEngine

    engine = YelpEngine("test", "Paris")
    assert engine.query == "test"
    assert engine.location == "Paris"


def test_twogis_engine_instantiation() -> None:
    """Test that TwoGisEngine can be instantiated."""
    from py_lead_generation import TwoGisEngine

    engine = TwoGisEngine("test", "Almaty")
    assert engine.query == "test"
    assert engine.location == "Almaty"


def test_twogis_engine_not_implemented() -> None:
    """Test that TwoGisEngine raises NotImplementedError for unimplemented methods."""
    from py_lead_generation import TwoGisEngine

    engine = TwoGisEngine("test", "Almaty")

    with pytest.raises(NotImplementedError):
        engine._parse_data_with_soup("<html></html>")
