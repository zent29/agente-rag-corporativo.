from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Inicializa el divisor de texto.
        
        Args:
            chunk_size (int): Tamaño máximo de cada chunk en caracteres.
            chunk_overlap (int): Cantidad de caracteres superpuestos entre chunks adyacentes.
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        
    def split_documents(self, documents):
        """
        Divide una lista de objetos Document en chunks más pequeños.
        
        Args:
            documents (list): Lista de documentos cargados por LangChain.
            
        Returns:
            list: Lista de documentos divididos (chunks).
        """
        if not documents:
            return []
            
        return self.splitter.split_documents(documents)
