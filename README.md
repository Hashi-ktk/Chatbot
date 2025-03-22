# Chatbot Project

This project is a Flask-based chatbot application.

## Overview

The application utilizes Flask for creating a web API and Flask-CORS to handle Cross-Origin Resource Sharing (CORS). It's structured with blueprints for different functionalities: `faq_bp` and `noor_bp`.

## File Structure

*   `app.py`: The main application file.
*   `blueprints/faq_bp.py`: Blueprint for FAQ-related functionalities.
*   `blueprints/noor_bp.py`: Blueprint for Noor-related functionalities.

## Functionality

*   **CORS Enabled**: The application allows requests from any origin using `flask-cors`.
*   **Blueprints**: The application is structured using Flask blueprints for modularity.
    *   `faq_bp`: Handles FAQ-related endpoints.
    *   `noor_bp`: Handles Noor-related endpoints.
*   **Run Configuration**: The application runs in debug mode and listens on all available network interfaces (`host="0.0.0.0"`).

## Usage

To run the application:

1.  Install the required dependencies:

    ```bash
    pip install Flask flask-cors
    ```

2.  Run the `app.py` file:

    ```bash
    python app.py
    ```

The application will be accessible at `http://0.0.0.0:5000` (or the port Flask defaults to).

## Deployment

The application is configured to be deployed to platforms like AWS by setting the host to `0.0.0.0`.

## Blueprints Details

More details on each blueprint (`faq_bp`, `noor_bp`) should be added here, including the routes they handle and the data they process.  *(This information is not available from the provided `app.py` and should be filled in based on the contents of those files.)*