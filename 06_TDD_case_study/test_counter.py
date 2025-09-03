"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
import status
from counter import app

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()
        
    def test_create_counter(self):
        response = self.client.post("/counters/test-counter")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.get_json()
        self.assertIn("test-counter", data)
        self.assertEqual(data["test-counter"], 1)

    def test_create_duplicate_counter(self):
        response = self.client.post("/counters/test-counter-1")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/counters/test-counter-1")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
    def test_update_counter(self):
        response = self.client.post("/counters/test-counter-2")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put("/counters/test-counter-2")  
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
        data = response.get_json()
        self.assertIn("test-counter-2", data)
        self.assertEqual(data["test-counter-2"], 2)
        
    def test_update_counter_failed(self):
        response = self.client.put("/counters/test-counter-3")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_read_counter(self):
        response = self.client.post("/counters/test-counter-4")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/counters/test-counter-4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.get_json()
        self.assertIn("test-counter-4", data)
        self.assertEqual(data["test-counter-4"], 1)
        
    def test_read_counter_failed(self):
        response = self.client.get("/counters/test-counter-5")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_counter(self):
        response = self.client.post("/counters/test-counter-6")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete("/counters/test-counter-6")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.get_json()
        self.assertEqual(data, {})
        
    def test_delete_counter_failed(self):
        response = self.client.delete("/counters/test-counter-7")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)