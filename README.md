# Unstaffed Freelance Platform

Unstaffed is a web application designed to connect freelancers with potential clients. It provides user management, profile creation, search functionality, and contract handling features.

## Features

- **User Authentication**: Login and signup functionality for both freelancers and clients.
- **User Profiles**: Separate profiles for freelancers and clients, including customizable details like skills, location, and salary.
- **Freelancer Search**: Search freelancers by location, skills, and desired salary.
- **Contracts**: Allow clients to hire freelancers and manage contracts.
- **Feedback System**: Post and like feedback posts to enhance engagement within the platform.
- **Dashboard Navigation**: Personalized dashboards for freelancers and clients.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, and Flask templates
- **Session Management**: Flask sessions
- **Hosting**: Local development

## Installation

### Prerequisites

- Python 3.x
- MySQL Server
- Virtual environment (optional)

### Steps

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd unstaffed
    ```

2. Set up a virtual environment (optional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ``` bash
    pip install flask flask-mysqldb
    ```

4. Configure the MySQL database:
- Create a MySQL database named unstaffeddb.
- Update the app.config values for MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DB in app.py to match your local MySQL configuration.
- Run the SQL script to set up the database schema (not included in this README).

5. Run the application:
    ```bash
    python app.py
    ```

6. Open your web browser and navigate to http://127.0.0.1:5000.