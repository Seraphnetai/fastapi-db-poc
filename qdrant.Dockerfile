FROM qdrant/qdrant:latest

RUN apt-get update -yq && apt-get install -yqq curl