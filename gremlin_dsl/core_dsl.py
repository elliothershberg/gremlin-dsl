from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import Column
from gremlin_python.process.traversal import Direction
from gremlin_python.process.traversal import Operator
from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import TextP
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions


def get_db_endpoint():
    return "ws://localhost:8182/gremlin"


def main():
    endpoint = get_db_endpoint()
    connection = DriverRemoteConnection(endpoint, "g")

    g = traversal().with_remote(connection)

    result = (
        g.V()
        .has_label("person")
        .has("age", P.gt(30))
        .order()
        .by("age", Order.desc)
        .to_list()
    )

    print(result)

    connection.close()


main()
