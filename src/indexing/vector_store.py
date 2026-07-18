import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Inicializa el almacén de vectores.
        
        Args:
            persist_directory (str): Nombre del directorio donde se guardará Chroma.
        """
        base_dir = Path(__file__).parent.parent.parent
        self.persist_dir = str(base_dir / persist_directory)
        
        # Usamos HuggingFace para embeddings locales gratuitos, ya que Groq no provee embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
    def get_store(self):
        """
        Obtiene la instancia de Chroma.
        
        Returns:
            Chroma: Instancia configurada de la base de datos vectorial.
        """
        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )
        
    def add_documents(self, documents):
        """
        Añade documentos (chunks) a la base de datos vectorial.
        
        Args:
            documents (list): Lista de documentos a indexar.
        """
        if not documents:
            return
            
        store = self.get_store()
        store.add_documents(documents)
        print(f"Indexados {len(documents)} chunks de texto en {self.persist_dir}.")
