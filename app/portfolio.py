import chromadb
import pandas as pd
import uuid

class Portfolio:
    def __init__(self):
        self.file_path="my_portfolio.csv"
        self.data = pd.read_csv(self.file_path)
        self.chromaClient = chromadb.PersistentClient('vectorstore')
        self.collection = self.chromaClient.get_or_create_collection(name='portfolio')

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in my_portfolio.iterrows():
                self.collection.add(documents = row["Techstack"],
                            metadatas = {"links": row["Links"]},
                            ids=[str(uuid.uuid4())])

    def query_links(self, techstack):
        return self.collection.query(query_texts=techstack, n_results=2).get("metadatas", [])