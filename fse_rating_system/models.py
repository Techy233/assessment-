class FSE:
    """Represents a Food Service Establishment."""
    def __init__(self, name: str, location: str, owner_name: str, owner_contact: str):
        self.name = name
        self.location = location
        self.owner_name = owner_name
        self.owner_contact = owner_contact
        self.assessment_scores = {}
        self.total_score = 0
        self.star_rating = 0

    def __str__(self):
        return f"FSE: {self.name} at {self.location}, Owner: {self.owner_name} ({self.owner_contact})"

class AssessmentChecklist:
    """Represents the assessment checklist and its parts."""
    def __init__(self):
        self.parts = {
            "Part 2: Documentations": {"max_score": 20, "score": 0},
            "Part 3: Personal Hygiene of Food handlers": {"max_score": 20, "score": 0},
            "Part 4: Material sourcing": {"max_score": 20, "score": 0},
            "Part 5: Water Sources and Storage": {"max_score": 10, "score": 0},
            "Part 6: Waste Disposal": {"max_score": 20, "score": 0},
            "Part 7: Cleaning": {"max_score": 10, "score": 0},
        }
        self.background_info = {} # Part 1, not scored

    def set_background_info(self, info: dict):
        """Sets the background information for the assessment."""
        self.background_info = info

    def set_score(self, part_name: str, score: int) -> bool:
        """Sets the score for a specific part of the checklist.
        Returns True if successful, False if part_name is invalid or score is out of bounds.
        """
        if part_name in self.parts:
            max_score = self.parts[part_name]["max_score"]
            if 0 <= score <= max_score:
                self.parts[part_name]["score"] = score
                return True
            else:
                print(f"Error: Score for {part_name} must be between 0 and {max_score}.")
                return False
        else:
            print(f"Error: Invalid part name '{part_name}'.")
            return False

    def get_total_score(self) -> int:
        """Calculates the total score for the assessment."""
        total = 0
        for part_name in self.parts:
            total += self.parts[part_name]["score"]
        return total

    def get_max_total_score(self) -> int:
        """Calculates the maximum possible total score for the assessment."""
        max_total = 0
        for part_name in self.parts:
            max_total += self.parts[part_name]["max_score"]
        return max_total

    def __str__(self):
        details = "Assessment Checklist:\n"
        if self.background_info:
            details += "Part 1: Background Information\n"
            for key, value in self.background_info.items():
                details += f"  {key}: {value}\n"
        for part_name, data in self.parts.items():
            details += f"{part_name}: Score {data['score']}/{data['max_score']}\n"
        details += f"Total Score: {self.get_total_score()}/{self.get_max_total_score()}\n"
        return details

# Example Usage (for testing purposes, will be removed or moved later)
if __name__ == "__main__":
    # Create an FSE instance
    my_fse = FSE(name="The Good Eatery",
                 location="123 Food Street",
                 owner_name="John Owner",
                 owner_contact="555-1234")
    print(my_fse)

    # Create an AssessmentChecklist instance
    checklist = AssessmentChecklist()

    # Set background info
    checklist.set_background_info({
        "Date of Assessment": "2024-07-30",
        "Assessor Name": "Jane Doe"
    })

    # Set scores for each part
    checklist.set_score("Part 2: Documentations", 18)
    checklist.set_score("Part 3: Personal Hygiene of Food handlers", 15)
    checklist.set_score("Part 4: Material sourcing", 19)
    checklist.set_score("Part 5: Water Sources and Storage", 8)
    checklist.set_score("Part 6: Waste Disposal", 17)
    checklist.set_score("Part 7: Cleaning", 9)

    # Try setting an invalid score
    checklist.set_score("Part 7: Cleaning", 15) # Should print error
    checklist.set_score("Invalid Part", 5)   # Should print error

    print(checklist)

    # Store assessment results in FSE object (will be done by main application logic)
    my_fse.assessment_scores = {part: data["score"] for part, data in checklist.parts.items()}
    my_fse.total_score = checklist.get_total_score()

    print(f"\nFSE '{my_fse.name}' Total Score: {my_fse.total_score}")
