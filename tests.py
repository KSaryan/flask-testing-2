import unittest

from party import app
from model import db, example_data, connect_to_db
from party import session


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Stuff to do before test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """testing homepage"""

        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """testing homepage for non-rsvped guest"""

        result = self.client.get("/")
        self.assertIn('Please RSVP', result.data)
        self.assertNotIn('Party Details', result.data)

    def test_rsvp(self):
        """testing homepage for rsvped guest"""

        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        result = self.client.get("/")
        self.assertNotIn('Please RSVP', result.data)
        self.assertIn('Party Details', result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        #Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        #Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        """testing game page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        result = self.client.get("/games")
        self.assertIn('Leave Me Alone', result.data)
        self.assertIn('nap', result.data)
        self.assertIn('Eat', result.data)
        self.assertNotIn('Socialization', result.data)
        self.assertNotIn('Small talk', result.data)

    def test_games(self):
        """testing game page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        result = self.client.post("/add_game",
                                  data={"name": "Kristine",
                                        "description": "Be Kristine"},
                                  follow_redirects=True)
        result = self.client.get("/games", follow_redirects=True)
        self.assertIn('Kristine', result.data)
        self.assertIn('Be Kristine', result.data)



if __name__ == "__main__":
    unittest.main()
