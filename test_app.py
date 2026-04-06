import unittest
import json
from app import app

class CalculatorTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Welcome to Calculator API')
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_addition(self):
        response = self.app.post('/add', 
                                 json={'a': 5, 'b': 3})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 8)
    
    def test_subtraction(self):
        response = self.app.post('/subtract', 
                                 json={'a': 10, 'b': 4})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 6)
    
    def test_multiplication(self):
        response = self.app.post('/multiply', 
                                 json={'a': 6, 'b': 7})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 42)
    
    def test_division(self):
        response = self.app.post('/divide', 
                                 json={'a': 15, 'b': 3})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 5)
    
    def test_division_by_zero(self):
        response = self.app.post('/divide', 
                                 json={'a': 10, 'b': 0})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_missing_parameters(self):
        response = self.app.post('/add', 
                                 json={'a': 5})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_invalid_json(self):
        response = self.app.post('/add', 
                                 data='invalid json',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
