from os import path

from freezegun import freeze_time
from nose.tools import assert_equals
from echelonpy.__main__ import generate_output


@freeze_time("2017-04-23T12:57:42Z")
def test_single_stage():
    _integration_test('single_stage')


@freeze_time("2017-04-23T12:59:00Z")
def test_multi_stage():
    _integration_test('multi_stage')


def _integration_test(fixture_name):
    input_path = path.join(path.dirname(__file__), 'fixtures', '{}.csv'.format(fixture_name))
    expected_output_path = path.join(path.dirname(__file__), 'fixtures', '{}.tcx'.format(fixture_name))

    actual_tcx = generate_output(input_path)

    with open(expected_output_path, "r") as expected_file:
        expected_tcx = expected_file.read()
        assert_equals(expected_tcx, actual_tcx)
