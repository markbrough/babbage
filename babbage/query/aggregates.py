from babbage.query.parser import Parser
from babbage.model.binding import Binding
from babbage.exc import QueryException
import six
import datetime
from babbage.api import map_is_class

class Aggregates(Parser):
    """ Handle parser output for aggregate/drilldown specifications. """
    start = "aggregates"
    rollups = None

    def aggregate(self, ast):
        refs = [a.ref for a in self.cube.model.aggregates]
        if ast not in refs:
            raise QueryException('Invalid aggregate: %r' % ast)
        self.results.append(ast)


    def _check_type(self, ref, value):
        """
        Checks whether the type of the cut value matches the type of the
        concept being cut, and raises a QueryException if it doesn't match
        """
        if isinstance(value, list):
            return [self._check_type(ref, val) for val in value]

        model_type = self.cube.model[ref].datatype
        if model_type is None:
            return
        query_type = self._api_type(value)
        if query_type == model_type:
            return
        else:
            raise QueryException("Invalid value %r parsed as type '%s' "
                                 "for cut %s of type '%s'"
                                 % (value, query_type, ref, model_type))

    def _api_type(self, value):
        """
        Returns the API type of the given value based on its python type.

        """
        if isinstance(value, six.string_types):
            return 'string'
        elif isinstance(value, six.integer_types):
            return 'integer'
        elif type(value) is datetime.datetime:
            return 'date'


    def rollup(self, ast):
        value = ast[2]
        if isinstance(value, six.string_types) and len(value.strip()) == 0:
            value = None
        # TODO: can you filter measures or aggregates?
        if ast[0] not in self.cube.model:
            raise QueryException('Invalid rollup: %r' % ast[0])
        self.results.append((ast[0], ast[1], value))


    def apply(self, q, bindings, aggregates, rollup=None):
        info = []

        self.start = "rollup"
        if rollup is not None:
            for (ref, operator, value) in self.parse(rollup):
                if map_is_class and isinstance(value, map):
                    value = list(value)
                self._check_type(ref, value)
                table, column = self.cube.model[ref].bind(self.cube)
                self.rollups = (table, column, value[0])
            self.results = []

        self.start = "aggregates"
        for aggregate in self.parse(aggregates):
            info.append(aggregate)
            table, columns = self.cube.model[aggregate].bind(self.cube, self.rollups)
            bindings.append(Binding(table, aggregate))
            for column in columns:
                q = q.column(column)

        if not len(self.results):
            # If no aggregates are specified, aggregate on all.
            for aggregate in self.cube.model.aggregates:
                info.append(aggregate.ref)
                table, column = aggregate.bind(self.cube)
                bindings.append(Binding(table, aggregate.ref))
                q = q.column(column)
        return info, q, bindings
