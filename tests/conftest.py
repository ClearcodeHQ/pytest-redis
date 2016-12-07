"""Tests main conftest file."""
import warnings

warnings.filterwarnings(
    "error",
    category=DeprecationWarning,
    module='(_pytest|pytest|redis|path|mirakuru).*'
)
