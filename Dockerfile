# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y gcc

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Streamlit
RUN pip install streamlit

# Make ports 5001 and 8501 available to the world outside this container
EXPOSE 5001
EXPOSE 8501

# Define environment variable
ENV FLASK_APP flask_app.py

# Run Streamlit app when the container launches
CMD ["streamlit", "run", "streamlit_app.py"]