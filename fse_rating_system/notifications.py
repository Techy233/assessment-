from .models import FSE

def format_assessment_sms(fse: FSE) -> str:
    """
    Formats a text message summarizing the assessment outcome.

    Args:
        fse: The Food Service Establishment object, which should have
             total_score and star_rating attributes populated.

    Returns:
        A string formatted as an SMS message.
    """
    # Need to import AssessmentChecklist to get the max score.
    # This assumes the default checklist is always used for max score calculation.
    from .models import AssessmentChecklist

    if fse.total_score is None or fse.star_rating is None:
        return "Assessment data for SMS is incomplete. Cannot generate message."

    # Get the maximum possible score from a default checklist instance
    # This is a simplification; in a more complex system, the specific checklist
    # used for the assessment (or its max score) might need to be passed around or retrieved.
    max_score = AssessmentChecklist().get_max_total_score()

    message = (
        f"Dear {fse.owner_name},\n"
        f"The food safety assessment for '{fse.name}' is complete.\n"
        f"Final Score: {fse.total_score}/{max_score}.\n"
        f"Star Rating: {fse.star_rating} Star(s).\n"
        f"Thank you."
    )
    return message

def send_sms(phone_number: str, message: str):
    """
    Simulates sending an SMS message.
    In a real application, this would integrate with an SMS gateway API.

    Args:
        phone_number: The recipient's phone number.
        message: The text message to send.
    """
    print(f"--- Simulating SMS to {phone_number} ---")
    print(message)
    print("--- SMS Sent (Simulation) ---")

# Example Usage (for testing purposes)
if __name__ == "__main__":
    from .models import AssessmentChecklist # Required for the format_assessment_sms example

    # Create a dummy FSE with assessment results
    sample_fse = FSE(name="The Corner Cafe",
                     location="789 Main St",
                     owner_name="Sarah Owner",
                     owner_contact="555-8765")
    sample_fse.total_score = 85
    sample_fse.star_rating = 4 # Assuming 85 is 4 stars

    # Format the SMS
    sms_message = format_assessment_sms(sample_fse)
    print("Formatted SMS:\n", sms_message)

    # Simulate sending the SMS
    if sample_fse.owner_contact:
        send_sms(sample_fse.owner_contact, sms_message)
    else:
        print("Owner contact not available to send SMS.")

    # Test with incomplete data
    incomplete_fse = FSE(name="No Score Cafe", location="N/A", owner_name="Nobody", owner_contact="N/A")
    # total_score and star_rating are not set
    error_sms = format_assessment_sms(incomplete_fse)
    print("\nFormatted SMS (Incomplete Data):\n", error_sms)
