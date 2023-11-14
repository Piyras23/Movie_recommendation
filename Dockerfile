#1. Python runtime as a parent image
FROM python:3.9-slim

# Working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Installing needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install streamlit

# Making port 5001 available to the world outside this container
EXPOSE 5001

# Defining environment variable
ENV FLASK_APP flask_app.py

# Runing Flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"docker run -p 5001:5001 -p 8501:8501]