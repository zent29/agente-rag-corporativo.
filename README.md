# Agente RAG Corporativo

Agente de inteligencia artificial basado en RAG (Retrieval-Augmented Generation) que permite a los colaboradores de una empresa consultar, en lenguaje natural, información contenida en los documentos internos (RH, Financiero, Legal, Operacional, etc.), obteniendo respuestas confiables y siempre citando la fuente original.

## 🎯 Objetivo del proyecto

Centralizar el acceso al conocimiento interno de la empresa a través de un agente conversacional que:

- Responde preguntas basándose **únicamente** en los documentos oficiales indexados.
- Cita siempre la fuente (archivo, sección o página) de cada respuesta.
- Informa claramente cuando no encuentra la información, en lugar de inventar una respuesta.

## 🧱 Stack tecnológico

| Capa | Tecnología |
|---|---|
| **Lenguaje** | Python 3 |
| **Base de datos vectorial / RAG** | [Pinecone Assistant](https://docs.pinecone.io/guides/assistant/understanding-assistant) (gestionado en la nube) |
| **Interfaz** | Streamlit |
| **Procesamiento de documentos** | pypdf, python-docx, openpyxl, python-pptx |
| **Variables de entorno** | python-dotenv |

> El proyecto utiliza **Pinecone Assistant** como motor RAG gestionado, lo que delega el chunking, la indexación vectorial y el retrieval semántico directamente al servicio de Pinecone, simplificando la arquitectura.

## 🗺️ Arquitectura del pipeline

```
Usuario
   │
   ▼
Interfaz Streamlit (src/interface/app.py)
   │
   ▼
PineconeAssistant (src/generation/pinecone_assistant.py)
   │  · chat() con soporte multi-turno
   │  · ask_stream() con respuesta en streaming
   │  · upload_file() para indexar documentos
   │  · health_check() para verificar estado
   │
   ▼
Pinecone Assistant API (RAG gestionado en la nube)
   │  · Chunking automático
   │  · Embeddings + búsqueda vectorial
   │  · Generación de respuesta con citación de fuentes
```

## 📂 Estructura del repositorio

```
agente-rag-corporativo/
├── src/
│   ├── generation/      # Cliente PineconeAssistant (ask, stream, upload)
│   ├── interface/       # Aplicación Streamlit (app.py)
│   ├── ingestion/       # (Reservado) colecta y organización de documentos
│   ├── processing/      # (Reservado) extracción y limpieza de contenido
│   ├── indexing/        # (Reservado) pipeline de indexación alternativo
│   ├── retrieval/       # (Reservado) capa de retrieval personalizado
│   └── logging/         # (Reservado) registro de ejecución
├── data/
│   ├── raw/             # Documentos originales
│   └── processed/       # Documentos procesados
├── docs/                # Documentación adicional, capturas, diagramas
├── logs/                # Logs de ejecución
├── tests/               # Pruebas
├── run.py               # Script de arranque de la aplicación
├── requirements.txt
├── .env.example         # Plantilla de variables de entorno
└── README.md
```

## 🚀 Estado del proyecto

- [x] Configuración inicial del repositorio
- [x] Integración con Pinecone Assistant (SDK oficial)
- [x] Módulo de generación con soporte multi-turno y streaming
- [x] Subida de documentos desde la interfaz (PDF, TXT, DOCX)
- [x] Interfaz de chat con Streamlit
- [x] Health check del asistente en la barra lateral
- [ ] Pruebas automatizadas
- [ ] Logging y trazabilidad de consultas
- [ ] Despliegue en producción (OCI / Streamlit Cloud)

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd agente-rag-corporativo
```

### 2. Crear y activar el entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

Edita el archivo `.env`:

```env
PINECONE_API_KEY=tu_clave_api_de_pinecone
PINECONE_ASSISTANT_NAME=nombre_de_tu_asistente
PINECONE_HOST=host_de_tu_asistente  # opcional
```

> Puedes obtener tu API key y el nombre del asistente desde la [consola de Pinecone](https://app.pinecone.io/).

### 5. Ejecutar la aplicación

```bash
python run.py
```

O directamente con Streamlit:

```bash
streamlit run src/interface/app.py
```

## 🖥️ Uso

1. Abre la aplicación en tu navegador (por defecto `http://localhost:8501`).
2. Verifica que la API Key esté configurada correctamente en la barra lateral.
3. (Opcional) Sube documentos internos desde la barra lateral para indexarlos en Pinecone.
4. Haz preguntas en el chat sobre los documentos indexados.

## 📄 Licencia

Proyecto desarrollado como parte de un desafío de formación — Alura Latam / Oracle Next Education (ONE).
