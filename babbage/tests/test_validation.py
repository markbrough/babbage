from jsonschema import ValidationError
from nose.tools import raises

from babbage.tests.util import TestCase, load_json_fixture

from babbage.validation import validate_model


class ValidationTestCase(TestCase):

    def setUp(self):
        super(ValidationTestCase, self).setUp()
        self.simple_model = load_json_fixture('simple_model.json')

    def test_simple_model(self):
        validate_model(self.simple_model)

    @raises(ValidationError)
    def test_invalid_base_key(self):
        model = self.simple_model.copy()
        model['foo'] = 'bar'
        validate_model(model)

    @raises(ValidationError)
    def test_invalid_dimension_name(self):
        model = self.simple_model.copy()
        model['dimensions']['goo fdj.'] = {'label': 'bar'}
        validate_model(model)

    @raises(ValidationError)
    def test_invalid_measure_name(self):
        model = self.simple_model.copy()
        model['measures']['goo fdj.'] = {'label': 'bar'}
        validate_model(model)

    @raises(ValidationError)
    def test_no_measure(self):
        model = self.simple_model.copy()
        model['measures'] = {}
        validate_model(model)

    @raises(ValidationError)
    def test_no_measure_label(self):
        model = self.simple_model.copy()
        model['measures']['amount'] = {}
        validate_model(model)