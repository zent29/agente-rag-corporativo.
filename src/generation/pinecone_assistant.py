import os
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message


class PineconeAssistant:
    """
    Cliente para el Asistente Pinecone v9.x usando el SDK oficial.

    En la versión 9.x del SDK, el asistente se accede a través de
    `pc.assistant._assistants` y los métodos reciben `assistant_name`
    como parámetro en cada llamada.
    """

    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY", "")
        self.assistant_name = os.getenv("PINECONE_ASSISTANT_NAME", "victor")

        if not self.api_key:
            raise ValueError(
                "PINECONE_API_KEY no encontrada. Configúrala en el archivo .env"
            )

        self._pc = Pinecone(api_key=self.api_key)
        # En SDK v9.x el acceso correcto es pc.assistant._assistants
        self._client = self._pc.assistant._assistants

    def ask(self, question: str, history: list = None) -> str:
        """
        Envía una pregunta al asistente con historial de conversación multi-turno.

        Args:
            question (str): La pregunta del usuario.
            history (list): Historial previo en formato
                [{"role": "user"/"assistant", "content": "..."}]

        Returns:
            str: Respuesta del asistente.
        """
        messages = []

        # Incluir historial previo para conversación multi-turno
        if history:
            for msg in history:
                messages.append(Message(content=msg["content"], role=msg["role"]))

        # Agregar la pregunta actual del usuario
        messages.append(Message(content=question, role="user"))

        try:
            resp = self._client.chat(
                assistant_name=self.assistant_name,
                messages=messages
            )
            return resp["message"]["content"]
        except Exception as e:
            return f"❌ Error al consultar el asistente: {str(e)}"

    def ask_stream(self, question: str, history: list = None):
        """
        Envía una pregunta al asistente con respuesta en streaming.

        Yields:
            str: Fragmentos de texto de la respuesta.
        """
        messages = []

        if history:
            for msg in history:
                messages.append(Message(content=msg["content"], role=msg["role"]))

        messages.append(Message(content=question, role="user"))

        try:
            chunks = self._client.chat(
                assistant_name=self.assistant_name,
                messages=messages,
                stream=True
            )
            for chunk in chunks:
                if chunk:
                    # Extraer texto según el tipo de chunk del SDK
                    if hasattr(chunk, "delta") and hasattr(chunk.delta, "content"):
                        text = chunk.delta.content
                        if text:
                            yield text
                    elif isinstance(chunk, dict):
                        text = chunk.get("delta", {}).get("content", "")
                        if text:
                            yield text
                    elif isinstance(chunk, str):
                        yield chunk
        except Exception as e:
            yield f"❌ Error en streaming: {str(e)}"

    def upload_file(self, file_path: str) -> dict:
        """
        Sube un archivo al asistente Pinecone para indexarlo.

        Args:
            file_path (str): Ruta absoluta al archivo a subir.

        Returns:
            dict: Respuesta con información del archivo subido.
        """
        try:
            response = self._client.upload_file(
                assistant_name=self.assistant_name,
                file_path=file_path,
                timeout=None
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Error al subir el archivo: {str(e)}")

    def health_check(self) -> bool:
        """
        Verifica que el asistente esté accesible y en estado 'Ready'.

        Returns:
            bool: True si el asistente está Ready.
        """
        try:
            info = self._client.describe_assistant(
                assistant_name=self.assistant_name
            )
            return getattr(info, "status", "").lower() == "ready"
        except Exception:
            return False
