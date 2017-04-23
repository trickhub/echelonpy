from os import path

from freezegun import freeze_time
from lxml import etree
from nose.tools import assert_equals
from echelonpy import reader
from echelonpy import tcx


@freeze_time("2017-04-23T12:57:42Z")
def test_single_stage():
    _integration_test('single_stage')


@freeze_time("2017-04-23T12:59:00Z")
def test_multi_stage():
    _integration_test('multi_stage')


def _integration_test(fixture_name):
    input_path = path.join(path.dirname(__file__), 'fixtures', '{}.csv'.format(fixture_name))
    expected_output_path = path.join(path.dirname(__file__), 'fixtures', '{}.tcx'.format(fixture_name))

    laps = reader.read(input_path)
    doc = etree.tostring(tcx.from_laps(laps), xml_declaration=True, encoding="utf-8", pretty_print=True)

    with open(expected_output_path, "r") as expected_file:
        expected_lines = expected_file.read()
        assert_equals(doc, expected_lines)
