import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, data):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in data]
    
    return questions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/flaskr/*": {"origins": '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    
    @app.route('/categories')
    def index_categories():
        categories = Category.query.all()
        
        return jsonify({
            "success" : True,
            "categories" : {category.id:category.type for category in categories},
            "total_categories" : len(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def index_paginated_questions():
        questions = Question.query.all()
        paginated_questions = paginate_questions(request, questions)
        
        if len(paginated_questions) == 0:
            abort(404, 'No questions found')
        
        categories = Category.query.all()
        
        return jsonify({
            "success" : True,
            "questions" : paginated_questions,
            "total_questions" : len(questions),
            "categories" : {category.id:category.type for category in categories},
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            
            return jsonify({
                "success" : True,
                "deleted" : question_id,
            })
            
        except:
            abort(404, 'This question is not found')
            
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        
        request_data = request.get_json()
        
        question = request_data.get("question", None)
        answer = request_data.get("answer", None)
        difficulty = request_data.get("difficulty", None)
        category = request_data.get("category", None)
        
        if ("question" and "answer" and "difficulty" and "category") not in request_data:
            abort(400, 'Missing Field')
        
        try:
            #
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            
            new_question.insert()
            
            return jsonify({
                "success" : True,
                "created" : new_question.id,
            })
            
            
        except:
            abort(422, 'Question cannot be created')
        

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        
        request_data = request.get_json()
        search_term = request_data.get("searchTerm")
        
        search = f'%{search_term}%'
        query = Question.query.filter(Question.question.ilike(search))
        
        questions = [question.format() for question in query]
        
        
        return jsonify({
            "success" : True,
            "questions" : questions,
            "total_questions" : len(questions)
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        
        try:
            query = Question.query.filter(Question.category == category_id)
            if query.count() == 0:
                abort(404, 'No questions found for this category')
                
            questions = [question.format() for question in query]
            
            return jsonify({
                "success" : True,
                "questions" : questions,
                "total_questions" : len(questions),
                "current_category" : category_id
            })
        
        except:
            abort(422, 'Cannot load questions for this category')
        

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=["POST"])
    def quiz():
        request_data = request.get_json()
        
        if ("previous_questions" and "quiz_category") not in request_data:
            abort(400, 'Quiz category and previous questions  is required')
        
        previous_questions = request_data.get("previous_questions")
        quiz_category = request_data.get("quiz_category")
  
        category_id = int(quiz_category.get("id"))
        query = Question.query.filter(Question.category == category_id)
        
        remaining_questions = [question.format() for question in query if question.id not in previous_questions]
        
        if len(remaining_questions) != 0:
            next_question = remaining_questions[random.randint(0, len(remaining_questions) - 1)]
        else:
            return jsonify({})
        
        return jsonify({
            "success": True,
            "question" : next_question
        })
        
        

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": f'not found : {error.description}'
            }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, 
                "error": 422, 
                "message": f'unprocessable : {error.description}'
            }),
            422,
        )
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, 
                "error": 400, 
                "message": f'bad request : {error.description}'
            }),
            400,
        )
    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, 
                "error": 405, 
                "message": f'method not allowed : {error.description}'
            }),
            405,
        )
    return app

