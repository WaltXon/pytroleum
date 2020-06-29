import pytest
from pytroleum.decline import arps_hyperbolic_rate


def test_arps_hyperbolic_rate():
    assert round(
        arps_hyperbolic_rate(20000.0, .7, 1.2, 2), 2) == 8795.31