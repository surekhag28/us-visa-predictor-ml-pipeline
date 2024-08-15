# Use a base Python image
FROM python:3.9-slim

# Install MLflow
RUN pip install mlflow

# Create directories for MLflow logs and artifacts
RUN mkdir -p /mlruns /mlartifacts

# Set environment variables for MLflow
ENV MLFLOW_TRACKING_URI=http://localhost:5000
ENV MLFLOW_DEFAULT_ARTIFACT_ROOT=/mlartifacts

# Expose the MLflow port
EXPOSE 5000

# Start MLflow server
CMD ["mlflow", "server", "--default-artifact-root", "/mlartifacts", "--host", "0.0.0.0"]
