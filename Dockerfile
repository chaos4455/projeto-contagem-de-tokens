# Use a slim base image to reduce image size
FROM python:3.9-slim-buster AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Build the final image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /app/requirements.txt .
COPY --from=builder /app/api_vectors_fastapi.py .
COPY --from=builder /app/vector_server.py .
COPY --from=builder /app/vector_client.py .
COPY --from=builder /app/tool.analyzer.token_counter_interface_THOTH.py .
COPY --from=builder /app/tool.automation.file_organization_manager_ATLAS.py .
COPY --from=builder /app/tool.backup.project_version_controller_JANUS.py .
COPY --from=builder /app/tool.backup.restoration_controller_CHRONOS.py .
COPY --from=builder /app/tool.backup.version_recovery_system_MNEMOSYNE.py .
COPY --from=builder /app/tool.tester.api_vector_validator_APOLLO_v2.py .
COPY --from=builder /app/tool.tester.api_vector_validator_APOLLO.py .
COPY --from=builder /app/tool.tester.vector_database_validator_HEPHAESTUS.py .
COPY --from=builder /app/util.cleaner.advanced_duplicate_remover_PERSEUS.py .
COPY --from=builder /app/util.cleaner.duplicate_file_handler_HERCULES.py .
COPY --from=builder /app/util.compression.yaml_archiver_VULCAN.py .
COPY --from=builder /app/vector_analyzer_extended.py .
COPY --from=builder /app/vector_analyzer.py .
COPY --from=builder /app/versionador.py .
COPY --from=builder /app/processor.db.incremental_vector_parser_THESEUS.py .
COPY --from=builder /app/processor.vector.continuous_embedding_engine_PROMETHEUS.py .
COPY --from=builder /app/processor.vector.yaml_vectorization_engine_DAEDALUS.py .
COPY --from=builder /app/processor.yaml.context_stream_engine_ATHENA.py .
COPY --from=builder /app/processor.yaml.dictionary_text_generator_CALLIOPE.py .
COPY --from=builder /app/processor.yaml.embedding_core_system_APOLLO.py .
COPY --from=builder /app/processor.yaml.prompt_embedding_generator_ORPHEUS.py .
COPY --from=builder /app/processor.yaml.wordlist_stream_processor_ISIS.py .
COPY --from=builder /app/db.manager.token_database_controller_HERMES.py .
COPY --from=builder /app/api.vector.continuous_service_HERMES.py .
COPY --from=builder /app/analytics.visualization.vector_metrics_ATLAS.py .
COPY --from=builder /app/adicionar_nomes_mitologicos_v2.py .
COPY --from=builder /app/adicionar_nomes_mitologicos.py .
COPY --from=builder /app/database-structure-export-v1.py .
COPY --from=builder /app/evolucao_framework.py .
COPY --from=builder /app/extract_vectors.py .
COPY --from=builder /app/generator.docs.ai_documentation_engine_MINERVA.py .
COPY --from=builder /app/generator.docs.project_documentation_builder_CLIO.py .
COPY --from=builder /app/gerador_vetorizador_continuo_PROMETHEUS-work--revision-0001.py .
COPY --from=builder /app/limparootv1.py .
COPY --from=builder /app/renomeador_nomenclatura_tecnica_profissional_v2.py .
COPY --from=builder /app/renomeador_nomenclatura_tecnica_profissional.py .
COPY --from=builder /app/test_vector_api.py .
COPY --from=builder /app/teste_framework.py .
COPY --from=builder /app/util.cleaner.advanced_duplicate_remover_PERSEUS.py .
COPY --from=builder /app/util.cleaner.duplicate_file_handler_HERCULES.py .
COPY --from=builder /app/util.compression.yaml_archiver_VULCAN.py .


# Set the entrypoint
CMD ["python", "vector_server.py"]
