## Description

[Recommender] project repository.

## Installation
```python
Python version 3.8.3
```
```bash
$ pip install -r requirements.txt
```
# Step by step to run
## 1 Running the app

```bash
# development
$ python -m app

```

## 2 Train model

```bash
GET http://localhost:5000/train
```

## 3 Load movies to sqlite

```bash
GET http://localhost:5000/load-movies
```

## 4 Prepare predict scores 

```bash
GET http://localhost:5000/prepare
```

<b style="color:red;">note *</b>: Steps 1 to 4 are run only when you run the application for the first time

## 5 Predict score by userID

```bash
POST http://localhost:5000/predict
content-type: application/json

{
    "userId": "A268XZJ063VKTW"
}
```
