# Flask High Court Case Scraper

A simple web application built with Flask and Playwright to scrape case details and order documents from the Delhi High Court website.

## Features

-   Search for cases by type, number, and year.
-   Displays case details including petitioner, respondent, and hearing dates.
-   Fetches and provides direct download links for all associated PDF order documents.
-   Clean, responsive, single-page user interface.

## Setup and Installation

Follow these steps to run the project locally.

### Prerequisites

-   Python 3.7+
-   pip

### Steps

1.  **Clone the repository:**

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright's browser dependencies:**
    ```bash
    python -m playwright install
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```

6.  Open your web browser and navigate to **`http://127.0.0.1:5001`**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
