FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python code into the Docker image
COPY src/ src/
COPY pyproject.toml .

RUN pip install --no-cache-dir poetry

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

# Set the entrypoint to Python interpreter
ENTRYPOINT ["python"]

# Set the default command to run the script with default arguments
CMD ["src/main.py", "--range-type", "month"]
