from sqlalchemy import func
from sqlalchemy.sql.expression import select

from babbage.query.cuts import Cuts  # noqa
from babbage.query.fields import Fields  # noqa
from babbage.query.drilldowns import Drilldowns  # noqa
from babbage.query.aggregates import Aggregates  # noqa
from babbage.query.ordering import Ordering  # noqa
from babbage.query.pagination import Pagination  # noqa


def count_results(cube, q):
    """ Get the count of records matching the query. """
    with cube.engine.connect() as connection:
        q = select(*[func.count(True)]).select_from(q.alias())
        results = connection.execute(q).scalar()
    return results


def generate_results(cube, q):
    """ Generate the resulting records for this query, applying pagination.
    Values will be returned by their reference. """
    if q._limit is not None and q._limit < 1:
        return
    with cube.engine.connect() as connection:
        rp = connection.execute(q)
    while True:
        row = rp.fetchone()
        if row is None:
            return
        yield dict(row._mapping.items())


def first_result(cube, q):
    for row in generate_results(cube, q):
        return row
