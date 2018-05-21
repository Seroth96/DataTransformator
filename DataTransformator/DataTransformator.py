from neo4j.v1 import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "1234"))

def print_friends_of(tx, name):
    for record in tx.run("MATCH (a:SOURCE)"
                         "RETURN a.Name", name=name):
        print(record["a.Name"])

with driver.session() as session:
    session.read_transaction(print_friends_of, "Alice")