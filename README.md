# Movie Recommendation System

Movie Recommendation System project! This repository contains the code for building and deploying a movie recommendation system using Python, Flask, and Streamlit. 

## Overview

The project consists of the following components:

1. **Initial Setup**: Setting up the environment, installing dependencies, and preparing the data.

2. **Python Scripts**: Python scripts for processing JSON data, analyzing profitability, and implementing recommendation algorithms.

3. **Flask Application**: A Flask web application for serving movie recommendations.

4. **Streamlit Dashboard**: A Streamlit dashboard for interactive exploration of the recommendation system.

5. **Docker Configuration**: Docker files for containerization and easy deployment.

## Initial Setup

To get started with the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/Piyras23/movie_recommendation.git
    cd movie_recommendation
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    .\venv\Scripts\activate   # For Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Python Scripts
The `python_scripts` directory contains Python scripts for processing JSON data, analyzing profitability, and implementing recommendation algorithms


## Flask Application
The `flask_app.py` file contains the Flask application that serves movie recommendations. Run the Flask app using the following command:

```bash
pyhton run flask_app.py

streamlit run streamlit_app.py

```bash
docker build -t movie_recommendation .

docker run -p 5001:5001 -p 8501:8501 movie_recommendation
# Expected url : http://localhost:5001/user_recommendations?user_id=1

# Expected output: [{"estimated_rating":5.0,"title":"English Vinglish (2012)"},{"estimated_rating":5.0,"title":"Mother (Madeo) (2009)"},{"estimated_rating":5.0,"title":"Voices from the List (2004)"},{"estimated_rating":5.0,"title":"Siam Sunset (1999)"},{"estimated_rating":5.0,"title":"Boy Eats Girl (2005)"}]




