from .models import FSE, AssessmentChecklist

def calculate_star_rating(total_score: int, max_total_score: int) -> int:
    """
    Assigns a star rating based on the total score.

    Args:
        total_score: The FSE's total score from the assessment.
        max_total_score: The maximum possible score for the assessment.

    Returns:
        An integer from 1 to 5 representing the star rating.
    """
    if max_total_score <= 0:
        return 0 # Avoid division by zero, indicate error or no rating

    percentage_score = (total_score / max_total_score) * 100

    if percentage_score >= 90:
        return 5
    elif percentage_score >= 80:
        return 4
    elif percentage_score >= 70:
        return 3
    elif percentage_score >= 60:
        return 2
    elif percentage_score < 60 and percentage_score >= 0: # Ensure score is not negative
        return 1
    else: # Handles scores below 0 or other unexpected cases
        return 0 # Or raise an error, or return a specific indicator for invalid scores


def perform_assessment(fse: FSE, checklist_scores: dict, background_info: dict = None) -> tuple[int, int]:
    """
    Performs an assessment for a given FSE.

    Args:
        fse: The Food Service Establishment object.
        checklist_scores: A dictionary where keys are part names (e.g., "Part 2: Documentations")
                          and values are the scores for those parts.
        background_info: Optional dictionary for Part 1 background information.

    Returns:
        A tuple containing the total score and the star rating.
        Returns (None, None) if checklist_scores are invalid.
    """
    assessment = AssessmentChecklist()

    if background_info:
        assessment.set_background_info(background_info)

    all_scores_valid = True
    for part_name, score in checklist_scores.items():
        if not assessment.set_score(part_name, score):
            all_scores_valid = False
            print(f"Failed to set score for {part_name}. Aborting assessment.")
            return None, None # Indicate failure

    if not all_scores_valid:
        return None, None

    total_score = assessment.get_total_score()
    max_score = assessment.get_max_total_score()
    star_rating = calculate_star_rating(total_score, max_score)

    # Update the FSE object with assessment results
    fse.assessment_scores = {part: data["score"] for part, data in assessment.parts.items()}
    fse.total_score = total_score
    fse.star_rating = star_rating

    # Store background info in FSE object if needed, or handle it separately
    # For now, it's part of the AssessmentChecklist instance which could be stored or logged.

    return total_score, star_rating

# Example Usage (for testing purposes, will be moved or integrated into main app flow)
if __name__ == "__main__":
    # Create an FSE instance
    my_fse = FSE(name="The Test Kitchen",
                 location="456 Test Ave",
                 owner_name="Alice Tester",
                 owner_contact="555-5678")

    # Define scores for the assessment
    scores_input = {
        "Part 2: Documentations": 18,
        "Part 3: Personal Hygiene of Food handlers": 20,
        "Part 4: Material sourcing": 15,
        "Part 5: Water Sources and Storage": 7,
        "Part 6: Waste Disposal": 18,
        "Part 7: Cleaning": 9,
    }

    # Define background info
    bg_info = {
        "Date of Assessment": "2024-07-31",
        "Assessor ID": "A001",
        "FSE Type": "Restaurant"
    }

    print(f"Performing assessment for: {my_fse.name}")
    total_score, stars = perform_assessment(my_fse, scores_input, bg_info)

    if total_score is not None:
        print(f"Assessment Complete for {my_fse.name}:")
        print(f"  Total Score: {my_fse.total_score} / {AssessmentChecklist().get_max_total_score()}")
        print(f"  Star Rating: {my_fse.star_rating} Stars")
        print(f"  Breakdown: {my_fse.assessment_scores}")

        # Test star rating function directly
        print("\nTesting star rating boundaries:")
        test_scores = [59, 60, 69, 70, 79, 80, 89, 90, 100]
        max_total = AssessmentChecklist().get_max_total_score() # Assuming 100
        for score in test_scores:
            rating = calculate_star_rating(score, max_total)
            print(f"Score {score}/{max_total} -> {rating} Stars")

        rating_at_zero = calculate_star_rating(0, max_total)
        print(f"Score 0/{max_total} -> {rating_at_zero} Stars")

        rating_below_zero = calculate_star_rating(-10, max_total)
        print(f"Score -10/{max_total} -> {rating_below_zero} Stars (expected 0 or error indicator)")

    # Test with invalid score input
    print("\nTesting with invalid score:")
    invalid_scores_input = {
        "Part 2: Documentations": 25, # Invalid score
        "Part 3: Personal Hygiene of Food handlers": 15,
    }
    result = perform_assessment(my_fse, invalid_scores_input, bg_info)
    if result == (None, None):
        print("Assessment failed as expected due to invalid score.")

    print("\nTesting with invalid part name:")
    invalid_part_name_scores = {
        "Part X: Imaginary Section": 10,
        "Part 2: Documentations": 15
    }
    result = perform_assessment(my_fse, invalid_part_name_scores, bg_info)
    if result == (None, None):
        print("Assessment failed as expected due to invalid part name.")
