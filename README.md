# Agente RAG Corporativo

Agente de inteligencia artificial basado en RAG (Retrieval-Augmented Generation) que permite a los colaboradores de una empresa consultar, en lenguaje natural, información contenida en los documentos internos (RH, Financiero, Legal, Operacional, etc.), obteniendo respuestas confiables y siempre citando la fuente original.

## 🎯 Objetivo del proyecto

Centralizar el acceso al conocimiento interno de la empresa a través de un agente conversacional que:

- Responde preguntas basándose **únicamente** en los documentos oficiales indexados.
- Cita siempre la fuente (archivo, sección o página) de cada respuesta.
- Informa claramente cuando no encuentra la información, en lugar de inventar una respuesta.

## 🧱 Stack tecnológico

- **Lenguaje / Framework RAG:** Python + LangChain
- **Interfaz:** Streamlit
- **Base de datos vectorial:** Chroma (desarrollo local) — evaluando migración a Oracle Autonomous Database para producción
- **Despliegue:** Oracle Cloud Infrastructure (OCI)

## 🗺️ Arquitectura del pipeline

El proyecto está organizado en las siguientes etapas:

1. **Colecta y organización de documentos** — mapeo de fuentes, categorización, curaduría y definición de responsables.
2. **Procesamiento y extracción de contenido** — extracción por formato (PDF, Word, Excel, PowerPoint, etc.), limpieza y chunking.
3. **Indexación vectorial** — generación de embeddings y almacenamiento en base de datos vectorial.
4. **Capa de recuperación (retrieval)** — búsqueda semántica, filtrado por metadatos y reranking.
5. **Generación de respuesta** — generación de la respuesta final con citación de fuentes y control de alucinación.
6. **Interfaz** — chat web construido con Streamlit.
7. **Despliegue** — publicación en Oracle Cloud Infrastructure (OCI).
8. **Registro de ejecución** — logging y trazabilidad de las consultas realizadas.

## 📂 Estructura del repositorio

```
agente-rag-corporativo/
├── src/
│   ├── ingestion/       # Colecta y organización de documentos
│   ├── processing/      # Extracción y limpieza de contenido, chunking
│   ├── indexing/        # Generación de embeddings e indexación vectorial
│   ├── retrieval/       # Búsqueda semántica, filtros y reranking
│   ├── generation/      # Generación de respuestas con el LLM
│   ├── interface/       # Interfaz Streamlit
│   └── logging/         # Registro de ejecución (logs)
├── data/
│   ├── raw/              # Documentos originales
│   └── processed/        # Documentos procesados/chunked
├── docs/                 # Documentación adicional, capturas, diagramas
├── logs/                 # Logs de ejecución
├── tests/                # Pruebas
├── requirements.txt
└── README.md
```

## 🚀 Estado del proyecto

🔧 En desarrollo. Este README se irá actualizando a medida que avancen las etapas del proyecto.

- [x] Configuración inicial del repositorio
- [ ] Colecta y organización de documentos
- [ ] Procesamiento y extracción de contenido
- [ ] Indexación vectorial
- [ ] Capa de recuperación
- [ ] Generación de respuesta con citación de fuentes
- [ ] Interfaz (Streamlit)
- [ ] Despliegue en Oracle Cloud Infrastructure (OCI)
- [ ] Registro de ejecución en la nube

## ⚙️ Instalación (en construcción)

```bash
git clone <url-del-repositorio>
cd agente-rag-corporativo
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📄 Licencia

Proyecto desarrollado como parte de un desafío de formación (Alura Latam / Oracle Next Education).
# agente-rag-corporativo.
