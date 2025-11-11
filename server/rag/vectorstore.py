from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Persistent ChromaDB folder
CHROMA_DIR = "./db"

_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_db = Chroma(persist_directory=CHROMA_DIR, embedding_function=_embeddings)

def get_retriever():
    '''
    Returns a retriever to retrieve from the db
    '''
    return _db.as_retriever()

def add_documents(docs):
    '''
    Adds embeddings of a list of docs to the db
    '''
    _db.add_texts(docs)
