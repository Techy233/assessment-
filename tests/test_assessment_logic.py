import unittest
from fse_rating_system.models import AssessmentChecklist
from fse_rating_system.assessment import calculate_star_rating

class TestAssessmentChecklist(unittest.TestCase):

    def setUp(self):
        self.checklist = AssessmentChecklist()

    def test_initial_scores(self):
        """Test that all scores are initially 0."""
        for part_name in self.checklist.parts:
            self.assertEqual(self.checklist.parts[part_name]["score"], 0)
        self.assertEqual(self.checklist.get_total_score(), 0)

    def test_set_valid_score(self):
        """Test setting a valid score for a part."""
        self.assertTrue(self.checklist.set_score("Part 2: Documentations", 15))
        self.assertEqual(self.checklist.parts["Part 2: Documentations"]["score"], 15)
        self.assertEqual(self.checklist.get_total_score(), 15)

    def test_set_score_too_high(self):
        """Test setting a score higher than max_score."""
        self.assertFalse(self.checklist.set_score("Part 2: Documentations", 25))
        self.assertEqual(self.checklist.parts["Part 2: Documentations"]["score"], 0) # Should remain unchanged

    def test_set_score_negative(self):
        """Test setting a negative score."""
        self.assertFalse(self.checklist.set_score("Part 3: Personal Hygiene of Food handlers", -5))
        self.assertEqual(self.checklist.parts["Part 3: Personal Hygiene of Food handlers"]["score"], 0)

    def test_set_score_invalid_part(self):
        """Test setting a score for an invalid part name."""
        self.assertFalse(self.checklist.set_score("Invalid Part Name", 10))

    def test_get_total_score(self):
        """Test calculation of total score with multiple parts."""
        self.checklist.set_score("Part 2: Documentations", 20)
        self.checklist.set_score("Part 3: Personal Hygiene of Food handlers", 10)
        self.checklist.set_score("Part 5: Water Sources and Storage", 5)
        self.assertEqual(self.checklist.get_total_score(), 35)

    def test_get_max_total_score(self):
        """Test that max total score is correct."""
        # (20+20+20+10+20+10) = 100
        self.assertEqual(self.checklist.get_max_total_score(), 100)

    def test_set_background_info(self):
        """Test setting and retrieving background info."""
        info = {"Date": "2024-01-01", "Assessor": "Test User"}
        self.checklist.set_background_info(info)
        self.assertEqual(self.checklist.background_info, info)


class TestStarRating(unittest.TestCase):

    def test_star_ratings_boundaries(self):
        """Test star ratings at various score boundaries (assuming max score of 100)."""
        max_score = 100
        self.assertEqual(calculate_star_rating(100, max_score), 5, "Score 100 should be 5 stars")
        self.assertEqual(calculate_star_rating(90, max_score), 5, "Score 90 should be 5 stars")
        self.assertEqual(calculate_star_rating(89, max_score), 4, "Score 89 should be 4 stars")
        self.assertEqual(calculate_star_rating(80, max_score), 4, "Score 80 should be 4 stars")
        self.assertEqual(calculate_star_rating(79, max_score), 3, "Score 79 should be 3 stars")
        self.assertEqual(calculate_star_rating(70, max_score), 3, "Score 70 should be 3 stars")
        self.assertEqual(calculate_star_rating(69, max_score), 2, "Score 69 should be 2 stars")
        self.assertEqual(calculate_star_rating(60, max_score), 2, "Score 60 should be 2 stars")
        self.assertEqual(calculate_star_rating(59, max_score), 1, "Score 59 should be 1 star")
        self.assertEqual(calculate_star_rating(0, max_score), 1, "Score 0 should be 1 star")

    def test_star_rating_various_max_scores(self):
        """Test star ratings with a different max_score."""
        # Example: Max score of 200
        max_score = 200
        # 90% of 200 = 180
        self.assertEqual(calculate_star_rating(180, max_score), 5)
        # 80% of 200 = 160
        self.assertEqual(calculate_star_rating(160, max_score), 4)
        # 70% of 200 = 140
        self.assertEqual(calculate_star_rating(140, max_score), 3)
        # 60% of 200 = 120
        self.assertEqual(calculate_star_rating(120, max_score), 2)
        # <60% of 200 (e.g., 119)
        self.assertEqual(calculate_star_rating(119, max_score), 1)

    def test_star_rating_zero_max_score(self):
        """Test star rating when max_score is zero to prevent division by zero."""
        self.assertEqual(calculate_star_rating(50, 0), 0) # Expect 0 or some indicator of error
        self.assertEqual(calculate_star_rating(0, 0), 0)

    def test_star_rating_negative_score(self):
        """Test star rating with a negative score."""
        self.assertEqual(calculate_star_rating(-10, 100), 0) # Or specific error indicator

if __name__ == '__main__':
    # This setup is to allow running tests directly from this file,
    # ensuring that the fse_rating_system package is discoverable.
    import os
    import sys
    # Add the parent directory (project root) to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.insert(0, project_root)

    unittest.main()
