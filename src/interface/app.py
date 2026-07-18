import streamlit as st
from dotenv import load_dotenv
import sys
import os
import tempfile

# Asegurar que python encuentre el módulo 'src'
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

load_dotenv(override=True)

from src.generation.pinecone_assistant import PineconeAssistant


def init_page():
    st.set_page_config(
        page_title="Agente RAG Corporativo",
        page_icon="💼",
        layout="wide"
    )


@st.cache_resource(show_spinner=False)
def get_assistant() -> PineconeAssistant:
    """Inicializa y cachea el Asistente Pinecone (una sola vez por sesión del servidor)."""
    return PineconeAssistant()


def main():
    init_page()

    st.title("💼 Agente RAG Corporativo")
    st.markdown(
        "Bienvenido al asistente de conocimiento corporativo. "
        "Haz preguntas sobre los documentos internos de la empresa."
    )

    api_key = os.getenv("PINECONE_API_KEY", "")
    assistant_name = os.getenv("PINECONE_ASSISTANT_NAME", "victor")
    host = os.getenv("PINECONE_HOST", "")

    # ── Barra lateral ─────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Configuración")

        if not api_key:
            st.error("❌ PINECONE_API_KEY no configurada en el archivo .env")
        else:
            st.success("✅ Pinecone API Key detectada")

        st.markdown("---")
        st.subheader("🤖 Asistente Activo")
        st.info(
            f"**Nombre:** `{assistant_name}`\n\n"
            f"**Host:** `{host}`"
        )

        # ── Subida de documentos a Pinecone ───────────────────────────────────
        st.markdown("---")
        st.subheader("📁 Subir Documentos")
        st.caption("Los archivos se indexan directamente en el asistente Pinecone.")

        uploaded_files = st.file_uploader(
            "Selecciona archivos",
            accept_multiple_files=True,
            type=["pdf", "txt", "docx"],
            help="Los documentos se subirán al asistente Pinecone para indexación."
        )

        if st.button("⬆️ Subir a Pinecone", disabled=not uploaded_files):
            if api_key and uploaded_files:
                assistant = get_assistant()
                success_count = 0
                for uf in uploaded_files:
                    with st.spinner(f"Subiendo `{uf.name}`..."):
                        try:
                            # Guardar temporalmente el archivo para subirlo
                            suffix = os.path.splitext(uf.name)[1]
                            with tempfile.NamedTemporaryFile(
                                delete=False, suffix=suffix, prefix=uf.name + "_"
                            ) as tmp:
                                tmp.write(uf.read())
                                tmp_path = tmp.name

                            assistant.upload_file(tmp_path)
                            os.unlink(tmp_path)
                            success_count += 1
                            st.success(f"✅ `{uf.name}` subido correctamente")
                        except Exception as e:
                            st.error(f"❌ Error con `{uf.name}`: {str(e)}")
                if success_count:
                    st.info(f"{success_count} archivo(s) indexado(s) en el asistente.")

        st.markdown("---")
        if st.button("🗑️ Limpiar conversación"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.subheader("📊 Estado de Conexión")
        if api_key:
            try:
                assistant = get_assistant()
                if assistant.health_check():
                    st.success("✅ Asistente Pinecone en línea")
                else:
                    st.warning("⚠️ No se pudo verificar el asistente")
            except ValueError as e:
                st.error(str(e))

    # ── Interfaz de Chat ───────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        if not api_key:
            st.error("Configura tu PINECONE_API_KEY en el archivo `.env` para continuar.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                assistant = get_assistant()
                history = st.session_state.messages[:-1]

                # Respuesta con streaming
                response_placeholder = st.empty()
                full_response = ""

                for chunk in assistant.ask_stream(prompt, history=history):
                    # Los chunks del SDK de Pinecone son objetos; extraer texto
                    if hasattr(chunk, "delta") and hasattr(chunk.delta, "content"):
                        full_response += chunk.delta.content or ""
                    elif isinstance(chunk, str):
                        full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                response = full_response

            except ValueError as e:
                response = f"❌ Error de configuración: {str(e)}"
                st.markdown(response)
            except Exception as e:
                response = f"❌ Error inesperado: {str(e)}"
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
