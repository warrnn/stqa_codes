"""
Test Cases for Mocking Lab
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

IMDB_DATA = {}

class TestIMDbDatabase(TestCase):
    """Tests Cases for IMDb Database"""

    @classmethod
    def setUpClass(cls):
        """ Load imdb responses needed by tests """
        global IMDB_DATA
        with open('tests/fixtures/imdb_responses.json') as json_data:
            IMDB_DATA = json.load(json_data)


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    @patch('models.imdb.requests.get')
    def test_search_by_title(self, mock):
        """Test searching by title"""
        mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["GOOD_SEARCH"])
        )
        
        imdb = IMDb("fake_valid_api_key")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertIsNone(results["errorMessage"])
        self.assertIsNotNone(results["results"])
        self.assertEqual(results["results"][0]["id"], "tt1375666")
        
    @patch('models.imdb.requests.get')
    def test_search_with_no_results(self, mock):
        """Test searching with no results"""
        mock.return_value = Mock(
            status_code=404,
        )
        
        imdb = IMDb("fake_valid_api_key")
        results = imdb.search_titles("Bambi")
        self.assertEqual(results, {})
        
    def test_search_by_title_failed(self):
        """Test searching by title failed"""
        with patch('models.imdb.requests.get') as mock:
            mock.return_value = Mock(
                spec=Response,
                status_code=200,
                json=Mock(return_value=IMDB_DATA["INVALID_API"])
            )
            imdb = IMDb("invalid_api_key")
            results = imdb.search_titles("Bambi")
            self.assertIsNotNone(results)
            self.assertEqual(results["errorMessage"], "Invalid API Key")
            
    @patch('models.imdb.requests.get')
    def test_movie_ratings(self, mock):
        """Test movie Ratings"""
        mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["GOOD_RATING"])
        )
        
        imdb = IMDb("fake_valid_api_key")
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["filmAffinity"], 3)
        self.assertEqual(results["rottenTomatoes"], 5)
        
    @patch('models.imdb.requests.get')
    def test_movie_ratings_with_no_results(self, mock):
        """Test movie Ratings"""
        mock.return_value = Mock(status_code=404)
        
        imdb = IMDb("fake_valid_api_key")
        results = imdb.movie_ratings("tt1375666")
        self.assertEqual(results, {})
        
    @patch('models.imdb.requests.get')
    def test_movie_reviews(self, mock):
        """Test movie Reviews"""
        mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["GOOD_REVIEW"])
        )
        
        imdb = IMDb("fake_valid_api_key")
        results = imdb.movie_reviews("tt1375666")
        self.assertIsNotNone(results)
        
    @patch('models.imdb.requests.get')
    def test_movie_reviews_with_no_results(self, mock):
        """Test movie Reviews"""
        mock.return_value = Mock(status_code=404)
        
        imdb = IMDb("fake_valid_api_key")
        results = imdb.movie_reviews("tt1375666")
        self.assertEqual(results, {})