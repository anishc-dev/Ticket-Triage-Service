"""
    Ingest documents from a sitemap and store them in a vector database
"""

import chromadb
import logging
from ingestion.sitemap_parser import SitemapParser


class DocumentIngestion:
    def __init__(self):
        # Initalising the chromadb for vector database
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Creating a collection for the documents
        try:
            self.collection = self.client.get_collection("netskope_docs")
        except:
            # Create the collection if it doesn't exist
            self.collection = self.client.create_collection("netskope_docs")
        self.sitemap = "https://docs.netskope.com/docs-sitemap.xml"
    
    def ingest_from_sitemap(self):
        """
            Ingest documents from a sitemap and store them in a vector database
        """
        # Parse the sitemap and get the pages
        pages = SitemapParser(self.sitemap).get_pages()
        # iterate over the pages and add them to the chromadb collection
        for page in pages:
            self.ingest_page(page['url'], page['content'])

    def ingest_page(self, url, content):
        """
            Ingest a single page into the chromadb collection
        """
        self.collection.add(
            documents=[content],
            ids=[url]
        )
    
    def get_collection_stats(self):
        """
            Get the stats of the chromadb collection
        """
        return self.collection.count()


