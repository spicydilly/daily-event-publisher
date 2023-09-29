FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python code into the Docker image
COPY src/ src/
COPY pyproject.toml .
COPY credentials.json .

RUN pip install poetry

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

# Command to run the script
CMD ["python", "src/main.py"]
