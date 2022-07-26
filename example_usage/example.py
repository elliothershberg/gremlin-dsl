from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

from gremlin_dsl.core_dsl import get_db_endpoint
from gremlin_dsl.core_dsl import SocialTraversalSource

def main():
    endpoint = get_db_endpoint()
    connection = DriverRemoteConnection(endpoint, "g")

    social = traversal(SocialTraversalSource).with_remote(endpoint)

    print(social.persons("marko").knows("josh"))

    connection.close()

if __name__ == "__main__":
  main()
