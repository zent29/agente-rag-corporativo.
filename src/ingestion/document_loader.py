import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

class DocumentLoader:
    def __init__(self, raw_data_dir: str = "data/raw"):
        """
        Inicializa el cargador de documentos.
        """
        base_dir = Path(__file__).parent.parent.parent
        self.raw_data_dir = base_dir / raw_data_dir
        
        if not self.raw_data_dir.exists():
            self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_available_files(self):
        """Lista los archivos disponibles en el directorio raw."""
        files = []
        for file_path in self.raw_data_dir.glob("**/*.*"):
            if file_path.is_file() and file_path.suffix in [".pdf", ".txt", ".docx"]:
                files.append(file_path)
        return files

    def load_documents(self):
        """
        Carga y procesa todos los documentos soportados del directorio.
        
        Returns:
            list: Una lista de objetos Document de LangChain.
        """
        files = self.get_available_files()
        documents = []
        
        for file_path in files:
            file_path_str = str(file_path)
            try:
                if file_path.suffix == ".pdf":
                    loader = PyPDFLoader(file_path_str)
                elif file_path.suffix == ".txt":
                    loader = TextLoader(file_path_str, encoding="utf-8")
                elif file_path.suffix == ".docx":
                    loader = Docx2txtLoader(file_path_str)
                else:
                    continue
                
                docs = loader.load()
                documents.extend(docs)
                print(f"Cargado exitosamente: {file_path.name} ({len(docs)} páginas/secciones)")
            except Exception as e:
                print(f"Error al cargar {file_path.name}: {str(e)}")
                
        return documents

    def save_uploaded_file(self, uploaded_file):
        """
        Guarda un archivo subido a través de Streamlit en el directorio raw_data_dir.
        
        Args:
            uploaded_file: El archivo subido (objeto de Streamlit).
        Returns:
            str: Ruta donde se guardó el archivo.
        """
        file_path = self.raw_data_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(file_path)
