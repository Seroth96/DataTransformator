from neo4j.v1 import GraphDatabase
import spacy
import time

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "localneo4j"))

listOfAcceptedTags = ['ADJ', 'ADV', 'VERB', 'NOUN', 'PROPN']

def get_raw_messages_analyzed(tx):
    nlp = spacy.load('en_core_web_sm')
    for record in tx.run("MATCH (a:MESSAGE:RAW)"
                         "RETURN a", ):
        # print(record["a"].properties['Text'])
        doc = nlp(record["a"].properties['text'])
        messageId = record["a"].properties['id']

        for token in doc:
            # print(token.text,token.pos_)
            if any(token.pos_ in tag for tag in listOfAcceptedTags):                
                kw = tx.run("MATCH (m:MESSAGE:RAW {id:{ID}}) "
                       "MERGE(kw:KEYWORD {value: {value}, type: {type}}) "
                       "MERGE (m)-[c:CONTAINS]->(kw) "
                       "RETURN kw ", { "value": token.text, "type": token.pos_, "ID": messageId }
                       )
                print(kw)

        tx.run("MATCH (m:MESSAGE:RAW {id:{ID}})"
               "SET m.processed = {timestamp}"
               "REMOVE m:RAW "
               "RETURN m", {"ID": messageId,"timestamp": time.time()} )

with driver.session() as session:
    session.read_transaction(get_raw_messages_analyzed)


    # localneo4j