import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_index_categories(self):
        req = self.client().get('/categories')
        res = json.loads(req.data)
        query = Category.query.all()
        
        self.assertEqual(req.status_code, 200)
        self.assertTrue(res["success"])
        self.assertEqual(res["total_categories"], len(query))
        
    def test_get_index_paginated_questions(self):
        req = self.client().get('/questions')
        res = json.loads(req.data)
        query = Question.query.all()
        
        self.assertEqual(req.status_code, 200)
        self.assertTrue(res["success"])
        self.assertEqual(res["total_questions"], len(query))
        
    def test_404_get_index_paginated_questions_page_not_exist(self):
        req = self.client().get(f'/questions?page={5000}')
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 404)
        self.assertEqual(res["success"], False)
        
    def test_delete_question(self):
        new_question = Question(question='Is it a test question ?', answer='Yes',difficulty=1 , category=1)
        new_question.insert()
        req = self.client().delete(f'/questions/{new_question.id}')
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res["success"], True)
        self.assertEqual(res["deleted"], new_question.id)
        
    def test_404_delete_question_not_found(self):
        req = self.client().delete(f'/questions/{5000}')
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 404)
        self.assertEqual(res["success"], False)
        
    def test_add_new_question(self):
        req = self.client().post('/questions', json={"question": "Is it a test question ?","answer": "Yes","difficulty": 1 , "category": 1 })
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res["success"], True)
        self.assertTrue(res["created"])
        
    def test_400_add_new_question_error(self):
        req = self.client().post('/questions', json={"question": "Is it a test question ?"})
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 400)
        self.assertEqual(res["success"], False)
        
    def test_search_question(self):
        req = self.client().post('/questions/search', json={"searchTerm": "title"})
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res["success"], True)
        self.assertGreater(res["total_questions"], 0)
        
    def test_search_question_with_no_results(self):
        req = self.client().post('/questions/search', json={"searchTerm": "no result"})
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res["success"], True)
        self.assertEqual(res["total_questions"], 0)
        
    def test_get_questions_by_category(self):
        category_id = 1
        query = Question.query.filter(Question.category == category_id)
        count = query.count()
        req = self.client().get(f'/categories/{category_id}/questions')
        res = json.loads(req.data)
        
        self.assertEqual(req.status_code, 200)
        self.assertTrue(res["success"])
        self.assertTrue(res["questions"])
        self.assertEqual(res["current_category"], category_id)
        self.assertEqual(res["total_questions"], count)
    
    def test_422_get_questions_by_category_questions_fail(self):
        category_id = 100
        req = self.client().get(f'/categories/{category_id}/questions')
        res = json.loads(req.data)
        
        self.assertEqual(req.status_code, 422)
        self.assertEqual(res["success"], False)
    
    def test_get_quiz_questions(self):
        req = self.client().post('/quizzes', json={
            'previous_questions': [2, 3, 4, 5, 9],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 200)
        self.assertEqual(res["success"], True)
        self.assertTrue(res["question"])
    
    def test_400_get_quiz_questions_fail_request_field_is_required(self):
        req = self.client().post('/quizzes', json={})
        res = json.loads(req.data)
       
        self.assertEqual(req.status_code, 400)
        self.assertEqual(res["success"], False)
        
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()