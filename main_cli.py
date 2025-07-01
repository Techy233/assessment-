from fse_rating_system.models import FSE, AssessmentChecklist
from fse_rating_system.assessment import perform_assessment
from fse_rating_system.notifications import format_assessment_sms, send_sms

def get_valid_score(prompt: str, max_score: int) -> int:
    """Gets a valid integer score from the user."""
    while True:
        try:
            score = int(input(prompt))
            if 0 <= score <= max_score:
                return score
            else:
                print(f"Invalid score. Please enter a value between 0 and {max_score}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_cli():
    """Runs the command-line interface for FSE assessment."""
    print("Welcome to the FSE Rating System CLI")
    print("------------------------------------")

    # 1. Get FSE Background Information (Part 1 - not scored, but FSE details)
    print("\n--- FSE Details ---")
    fse_name = input("Enter FSE Name: ")
    fse_location = input("Enter FSE Location: ")
    owner_name = input("Enter Owner/Manager Name: ")
    owner_contact = input("Enter Owner/Manager Phone Number (for SMS): ")

    fse_instance = FSE(name=fse_name, location=fse_location, owner_name=owner_name, owner_contact=owner_contact)

    # Part 1: Background information for the checklist (optional, can be extended)
    print("\n--- Assessment Background (Part 1 - Not Scored) ---")
    date_of_assessment = input("Enter Date of Assessment (e.g., YYYY-MM-DD): ")
    assessor_name = input("Enter Assessor Name: ")
    # Add any other relevant background fields here
    assessment_bg_info = {
        "Date of Assessment": date_of_assessment,
        "Assessor Name": assessor_name,
        # "FSE Type": input("Enter FSE Type (e.g., Restaurant, Kiosk): ") # Example of another field
    }

    # 2. Get scores for each part of the checklist
    print("\n--- Enter Assessment Scores ---")
    checklist = AssessmentChecklist() # Used here to access part names and max scores
    checklist_scores_input = {}

    for part_name, details in checklist.parts.items():
        prompt_message = f"Score for {part_name} (Max {details['max_score']}): "
        score = get_valid_score(prompt_message, details['max_score'])
        checklist_scores_input[part_name] = score

    # 3. Perform Assessment
    print("\n--- Processing Assessment ---")
    total_score, star_rating = perform_assessment(fse_instance, checklist_scores_input, assessment_bg_info)

    if total_score is not None and star_rating is not None:
        print("\n--- Assessment Results ---")
        print(f"FSE Name: {fse_instance.name}")
        print(f"Total Score: {fse_instance.total_score} / {checklist.get_max_total_score()}")
        print(f"Star Rating: {fse_instance.star_rating} Stars")

        print("\n--- Score Breakdown ---")
        for part_name, score_value in fse_instance.assessment_scores.items():
            max_s = checklist.parts[part_name]['max_score']
            print(f"  {part_name}: {score_value}/{max_s}")

        # 4. Generate and "Send" SMS
        print("\n--- SMS Notification ---")
        sms_message = format_assessment_sms(fse_instance)
        if fse_instance.owner_contact:
            send_sms(fse_instance.owner_contact, sms_message)
        else:
            print("No owner contact provided, SMS not sent.")
            print(f"Message content would have been:\n{sms_message}")
    else:
        print("Assessment could not be completed due to errors in score input.")

    print("\n------------------------------------")
    print("Thank you for using the FSE Rating System.")

if __name__ == "__main__":
    # Create the package directory if it doesn't exist, for imports to work when run directly
    import os
    if not os.path.exists("fse_rating_system"):
        os.makedirs("fse_rating_system")
    # Create an __init__.py if it doesn't exist for the same reason
    if not os.path.exists("fse_rating_system/__init__.py"):
        with open("fse_rating_system/__init__.py", "w") as f:
            pass # Empty file is fine for a simple package marker

    run_cli()
