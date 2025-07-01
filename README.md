# FSE (Food Service Establishment) Rating System

This project provides a system to rate Food Service Establishments (FSEs) based on their compliance with food safety regulations. It uses a checklist to assess various aspects of an FSE's operations, calculates a total score, and assigns a star rating. An SMS notification (simulated) is then sent to the FSE owner/manager.

## Project Structure

```
.
├── fse_rating_system/
│   ├── __init__.py         # Makes the directory a Python package
│   ├── models.py           # Defines FSE and AssessmentChecklist data structures
│   ├── assessment.py       # Contains logic for scoring and star rating
│   └── notifications.py    # Handles formatting and sending (simulated) SMS
├── tests/
│   └── test_assessment_logic.py # Unit tests for scoring and star rating
├── main_cli.py             # Command-line interface to run the application
└── README.md               # This file
```

## Features

*   **FSE Data Management**: Stores basic information about the FSE.
*   **Checklist-Based Assessment**: Uses a 7-part checklist for scoring:
    *   Part 1: Background information (not scored)
    *   Part 2: Documentations (20 marks)
    *   Part 3: Personal Hygiene of Food handlers (20 marks)
    *   Part 4: Material sourcing (20 marks)
    *   Part 5: Water Sources and Storage (10 marks)
    *   Part 6: Waste Disposal (20 marks)
    *   Part 7: Cleaning (10 marks)
*   **Scoring and Star Rating**:
    *   Calculates a total score out of 100.
    *   Assigns a star rating:
        *   5 Stars: 90-100
        *   4 Stars: 80-89
        *   3 Stars: 70-79
        *   2 Stars: 60-69
        *   1 Star: Below 60
*   **SMS Notification**: Generates and simulates sending an SMS to the FSE owner/manager with the assessment results.
*   **Command-Line Interface**: Allows users to input FSE details and assessment scores interactively.
*   **Unit Tests**: Includes tests for the core scoring and rating logic.

## Prerequisites

*   Python 3.x

## How to Run

1.  **Clone the repository or download the files.**
2.  **Navigate to the project's root directory** (the directory containing `main_cli.py`).
3.  **Run the CLI application:**
    ```bash
    python main_cli.py
    ```
4.  **Follow the on-screen prompts** to:
    *   Enter FSE details (name, location, owner name, owner phone number).
    *   Enter assessment background information (date, assessor name).
    *   Enter scores for each part of the checklist.

The application will then display the total score, star rating, a breakdown of scores, and simulate sending an SMS notification to the provided phone number.

## How to Run Tests

1.  **Navigate to the project's root directory.**
2.  **Run the unit tests:**
    ```bash
    python -m unittest discover tests
    ```
    or specifically:
    ```bash
    python -m unittest tests.test_assessment_logic
    ```

    The tests for `AssessmentChecklist` might produce some print output for invalid score entries (e.g., "Error: Score for Part X must be between 0 and Y."). This is expected with the current implementation, but the tests themselves should still pass.

## Future Enhancements (Potential)

*   Integration with a real SMS gateway (e.g., Twilio, Vonage).
*   Persistent storage for FSE data and assessment results (e.g., database, CSV files).
*   A web-based interface instead of/in addition to the CLI.
*   More detailed reporting and analytics.
*   Configuration options for checklist items and scoring weights.
```
