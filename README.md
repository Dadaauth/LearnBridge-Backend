# LearnBridge

A tutorial application for kwasu students. LearnBridge means a bridge of learning between students

## Table Of Contents

- [Requirements](#requirements)
- [How to Install](#how-to-install)
- [Project Structure](#project-structure)

## Requirements

- [ffmpeg](https://www.ffmpeg.org/) program must be installed on the target machine running the flask server.
- python packages requirements are listed in the requirements.txt file
- Python

## How to Install

Clone to your local machine

```shell
git clone <repo_url>
```

change working directory

```shell
cd <project directory>
```

create a virtual environment

```shell
python -m venv .env
```

activate the virtual environment

for windows:

```shell
source .env/scripts/activate
```

for linux

```shell

```

Install Dependencies

```shell
pip install -r requirements.txt
```

Run flask server for development

```shell
flask --app main run --debug
```

## Project Structure

```text
.
|—— models                              # Database Models
|   |—— engine                          # storage engine
|—— static                              # static files
|—— tests                               # tests
|—— utils                               # utilities functions
|—— views                               # flask API routes
|—— __init__.py
|—— create_app.py                       # initialize flask app
|—— main.py                             # program entry point
|—— populate_db.py
|—— pytest.ini                          # pytest config file
|—— README.md                           # Readme documentation
|__ requirements.txt                    # python requirements
```

## > Features to Implement

- Students should be able to upload documents then they can ask a reasoning engine questions. Ths will be a feature like when chatGPT is trained on web content and then the propmpters can ask it a lot of questions based on what it has been trained on. A RAG - (Retrieval Augmented Generation), a combination of a generative and retrieval model.
- You should probably implement your own streaming protocol directly from your servers instead of using cloud storage which has the extra cost of storing your files. If your cloud compute has enough space you can store your videos on it.
- Add automated practice section where students can practice what they have learned. It can be an automated marker using a complicated algorithm to mark the answers maybe using OCR image recognition or it can just be an objectives based question. There should be a variety of randomly generated questions. There should also be rankings for questions solved that can be displayed on the student's profile. This can motivate students to solve more questions and effectively become better students overall.
- Concerning the automated checking of questions. For something like calculus for examle, there should be a form of visualization that will make you see the result of your work in real time. If you fail in your calculations you should be able to see it, resolve your questions, input your values and check if it will work. It should be like programming where you get instant feedback. The main thing is that it must portray real life scenerios while complementing the lack of real-life scenerious in the education system. For example you might be given a question to solve how to balance a system. THere shouldf be a graphics where you can input your result then the graphics will show the result of your work, e.g. in a building, for civil engineers, if the building will collapse or stand.

## API DOCUMENTATION
