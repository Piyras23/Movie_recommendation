Prequesite:
python:3.9

#1 Run python recommendation engine in bash
bash-python recommendation.py 

#2 Run Dockerfile:
bash- docker build -t movie_recommendatiom .

#3 Asign port and image:
bash- docker run -p 5001:5001 -p 8501:8501 

#3 