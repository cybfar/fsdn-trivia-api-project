# TRIVIA API : Development and Documentation Final Project

## Trivia App

Trivia API is a game in which players can test their knowledge in different categories by answering trivia questions.

In Trivia App, we can:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
### Pre-requisites and Local Development

The project is divided into two parts.
A backend part made in Flask and a frontend part made in React.
Developers using this project should already have Python3, pip and node installed on their local machines.
### Frontend

The [frontend](./frontend/) directory contains a complete React frontend to consume the data from the Flask server.
To start the frontend, run the following commands from the frontend folder:
    
    npm install //To install dependencies
    npm start //To run the frontend
By default, the frontend will run on localhost:3000


### Backend

The [backend](./backend) directory contains a Flask and SQLAlchemy server.
To setup the Trivia API, install the required dependencies by navigating to the `/backend` directory and run:

```bash
pip install -r requirements.txt
```

#### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

#### Run the application
To run the application run the following commands:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=On
flask run
```
The `FLASK_DEBUG=On` will detect file changes and restart the server automatically.
The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.


## Running Tests

All test are in the `test_flaskr.py` file in the `backend` folder and use the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

## API Reference
### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": False,
  "error": 422,
  "message": "unprocessable",
}
```

The API will return three error types when requests fail (The message is sent with a specific description of the error):

  - 400: Bad Request
  - 404: Resource Not Found
  - 422: Not Processable

### Endpoints

#### Get all categories

```http
GET /categories
```

- General :
    - Fetch all categories
    - Returns a list of categories object,total categories and success value: 
- Sample : `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

#### Get all questions

```http
GET /questions
```

- General :
    - Returns a list of questions objects, success value, total questions and all categories
    - Results are paginated and questions are 10 per page
- Sample : `curl http://127.0.0.1:5000/questions`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 26
}
```


#### Get all questions based on category

```http
GET /categories/{id}/questions
```

- General :
    - Get all questions based on category
    - Returns a list of the questions, current category, total questions on this category and success value
- Sample : `curl http://127.0.0.1:5000/categories/5/questions`

```json
{
  "current_category": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### Create a new question
```http
POST /questions
```
- General :
    - Create a new question using `question`, `answer`, `category`, `difficulty`
    - Returns the id of the created question and success value
- Sample : `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is CURL ?", "answer":"client URL", "category": 1, "difficulty":3}'`

```json
{
  "created": 10,
  "success": true
}
```


#### Search questions
```http
POST /questions/search
```
- General :
    - Search questions using `searchTerm`
    - Return any questions for whom the search term is a substring of the question.
    - Returns total questions and success value
- Sample : `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`

```json
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### Delete question
```http
DELETE /questions/{id}
```
- General :
    - Deletes the question of the given ID if it exists
    - Returns the id of the deleted question and success value
- Sample : `curl -X DELETE http://127.0.0.1:5000/questions/1`

```json
{
  "deleted": 1,
  "success": true
}

```


#### Play the quiz game

```http
POST /quizzes
```
- General :
    - Start the quiz game
    - JSON Request should have `previous_questions` which is a list of previous questions and `quiz_category`, the current category
    - Return JSON object with a new random question which in not in previous questions
- Sample : `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3], "quiz_category": {"id": 1, "type": "Science"} }'`

```json
{
  "question": {
    "answer": "client URL",
    "category": 1,
    "difficulty": 3,
    "id": 10,
    "question": "What is CURL ?"
  },
  "success": true
}
```

## Authors

- [@cybfar](https://github.com/cybfar) for editing some files in the project
- All project files were created by [Udacity](https://github.com/udacity) as a template for the Development and Documentation Final Project.
