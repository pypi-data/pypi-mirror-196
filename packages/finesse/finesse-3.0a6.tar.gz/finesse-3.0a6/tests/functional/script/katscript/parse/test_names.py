"""Element name tests."""

from hypothesis import given, assume, settings
from finesse.script import parse
from testutils.text import dedent_multiline
from testutils.fuzzing import DEADLINE, kat_name


@given(name=kat_name())
@settings(deadline=DEADLINE)
def test_component_name_fuzzing(name):
    parse(f"mirror {name}")


@given(name=kat_name())
@settings(deadline=DEADLINE)
def test_analysis_name_fuzzing(name):
    assume(name != "m1")
    parse(
        dedent_multiline(
            f"""
            mirror m1
            xaxis(m1.phi, lin, 0, 90, 100, name='{name}')
            """
        )
    )
