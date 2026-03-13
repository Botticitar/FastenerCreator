FROM mambaorg/micromamba:latest

USER root

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglu1-mesa && rm -rf /var/lib/apt/lists/*

USER micromamba
WORKDIR /app


RUN micromamba install -y -n base -c conda-forge -c cadquery \
    cadquery \
    fastapi \
    uvicorn \
    pandas \
    pydantic \
    && micromamba clean --all --yes

COPY --chown=micromamba:micromamba ./src /app/src

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

EXPOSE 8000


CMD ["micromamba", "run", "-n", "base", "uvicorn", "stepgen_app.main:app", "--host", "0.0.0.0", "--port", "8000"]