import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class RAGChain:
    def __init__(self, vector_store):
        """
        Inicializa la cadena RAG con Google Gemini.
        """
        self.vector_store = vector_store
        
        # Usamos Gemini 2.0 Flash como LLM (rápido, gratis con API de Google AI Studio)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3
        )
        
        self.system_prompt = (
            "Eres un asistente experto corporativo. Utiliza los siguientes fragmentos "
            "de contexto recuperado para responder a la pregunta. Si no sabes la respuesta, "
            "di que no la sabes basándote en los documentos disponibles. Trata de ser "
            "claro y conciso.\n\n"
            "Contexto:\n{context}"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
        ])
        
    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    def build_chain(self):
        """
        Construye la cadena de recuperación y generación utilizando LCEL.
        """
        store = self.vector_store.get_store()
        
        # Recuperador (retriever): busca los chunks más similares a la pregunta
        retriever = store.as_retriever(search_kwargs={"k": 4})
        
        # Cadena RAG con LCEL
        rag_chain = (
            {"context": retriever | self.format_docs, "input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain
        
    def ask(self, question: str):
        """
        Realiza una pregunta a la cadena RAG.
        
        Args:
            question (str): La pregunta del usuario.
            
        Returns:
            str: La respuesta generada por el agente.
        """
        try:
            chain = self.build_chain()
            response = chain.invoke(question)
            return response
        except Exception as e:
            return f"Hubo un error al generar la respuesta: {str(e)}"
