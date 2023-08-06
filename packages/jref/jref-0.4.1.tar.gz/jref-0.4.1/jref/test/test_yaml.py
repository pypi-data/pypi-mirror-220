from __future__ import absolute_import

import textwrap
import unittest

from io import BytesIO

from jref.yaml import Loader

from . import test_data


__metaclass__ = type


class _TestContext:
    def __init__(self, name):
        self.base_uri = 'data:' + name
        self.data = getattr(test_data, name)

    def open_uri(self, uri):
        return BytesIO(self.data)

    def parse_reference(self, ref):
        return _TestReference(ref)


class _TestReference(str):
    pass


class TestYamlLoader(unittest.TestCase):
    def test_it_loads_json_documents_properly(self):
        ctx = _TestContext('JSON_DATA')
        with Loader(ctx) as loader:
            self.assertEqual(
                test_data.JSON_DOCUMENT,
                loader.get_single_data())

    def test_it_loads_yaml_documents_properly(self):
        ctx = _TestContext('YAML_DATA')
        with Loader(ctx) as loader:
            self.assertEqual(
                test_data.YAML_DOCUMENT,
                loader.get_single_data())

    def assertIsTestReference(self, value, reference):
        self.assertIsInstance(value, _TestReference)
        self.assertEqual(value, reference)

    def test_it_processes_reference_objects_using_the_context(self):
        good_ref = '#/value'
        not_a_ref = 'Not a reference'

        ctx = _TestContext('REFERENCES_DATA')
        with Loader(ctx) as loader:
            doc = loader.get_single_data()

        self.assertIsTestReference(
            doc['reference-in-object']['object'], good_ref)
        self.assertIsTestReference(
            doc['reference-in-explicit-map']['object'], good_ref)
        self.assertIsTestReference(doc['reference-in-array'][1], good_ref)
        self.assertIsTestReference(doc['reference-in-omap'][0][1], good_ref)
        self.assertIsTestReference(doc['reference-in-pairs'][1][1], good_ref)
        self.assertIsTestReference(doc['reference-cycle'], '#/reference-cycle')
        self.assertIsTestReference(
            doc['indirect-reference-cycle'], '#/indirect-reference-cycle-loop')
        self.assertIsTestReference(
            doc['indirect-reference-cycle-loop'], '#/indirect-reference-cycle')

    def test_it_supports_references_in_a_set(self):
        good_ref = '#/value'
        not_a_ref = 'Not a reference'

        ctx = _TestContext('REFERENCE_IN_SET_DATA')
        with Loader(ctx) as loader:
            doc = loader.get_single_data()

        self.assertIsInstance(doc, set)
        self.assertEqual(doc, set((good_ref, not_a_ref)))

        for v in doc:
            self.assertTrue(
                isinstance(v, _TestReference)
                or v == not_a_ref)


if __name__ == '__main__':
    unittest.main()
