# Imagen de la GUI Streamlit del modelo de Bohr.
# El paquete no depende de Streamlit; aquí sí se instala el extra [gui].
#
# Construir:
#   docker build -t andresperez3/bohr-h-andresdperezc:0.1.0 .
# Ejecutar:
#   docker run --rm -p 8501:8501 andresperez3/bohr-h-andresdperezc:0.1.0
# Luego abrir http://localhost:8501

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY streamlit_app.py ./

RUN pip install --upgrade pip \
    && pip install ".[gui]"

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=8s --start-period=25s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
