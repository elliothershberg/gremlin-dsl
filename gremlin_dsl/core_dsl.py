from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import TextP
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions
from gremlin_python.process.traversal import Bytecode
from gremlin_python.process.graph_traversal import __ as AnonymousTraversal
from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

def get_db_endpoint():
    """Provide the local connection URL"""
    return "ws://localhost:8182/gremlin"


class SocialTraversal(GraphTraversal):
    def knows(self, person_name):
        return self.out("knows").has_label("person").has("name", person_name)

    def youngest_friends_age(self):
        return self.out("knows").has_label("person").values("age").min()

    def created_at_least(self, number):
        return self.out_e("created").count().is_(P.gte(number))


class __(AnonymousTraversal):

    graph_traversal = SocialTraversal

    @classmethod
    def knows(cls, *args):
        return cls.graph_traversal(None, None, Bytecode()).knows(*args)

    @classmethod
    def youngest_friends_age(cls, *args):
        return cls.graph_traversal(None, None, Bytecode()).youngest_friends_age(*args)

    @classmethod
    def created_at_least(cls, *args):
        return cls.graph_traversal(None, None, Bytecode()).created_at_least(*args)


class SocialTraversalSource(GraphTraversalSource):
    def __init__(self, *args, **kwargs):
        super(SocialTraversalSource, self).__init__(*args, **kwargs)
        self.graph_traversal = SocialTraversal

    def persons(self, *args):
        traversal = self.get_graph_traversal()
        traversal.bytecode.add_step("V")
        traversal.bytecode.add_step("hasLabel", "person")

        if len(args) > 0:
            traversal.bytecode.add_step("has", "name", P.within(args))

        return traversal


def main():
    endpoint = get_db_endpoint()
    connection = DriverRemoteConnection(endpoint, "g")

    # g = traversal().with_remote(connection)

    # result = (
    #     g.V()
    #     .has_label("person")
    #     .has("age", P.gt(30))
    #     .order()
    #     .by("age", Order.desc)
    #     .to_list()
    # )

    # print(result)

    social = traversal(SocialTraversalSource).with_remote(endpoint)
    
    print(social.persons('marko').knows('josh'))

    connection.close()


main()
