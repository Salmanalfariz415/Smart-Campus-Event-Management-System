# Smart-Campus-Event-Management-System

## Overview

The Smart Campus Event Management System is a full-stack web application designed to streamline event organization and discovery on a university campus. It provides a centralized platform for organizers to create and manage events, and for students to browse, search, and book their attendance.

The backend is built with Python and Flask, utilizing Supabase as an all-in-one Backend-as-a-Service (BaaS) for the database, user authentication, and file storage. The frontend is crafted with HTML, JavaScript, and styled with Tailwind CSS to deliver a modern and responsive user experience.

## Features

-   **Dual User Roles**: Separate registration flows and profiles for regular users (attendees) and event organizers.
-   **Secure Authentication**: JWT-based authentication for secure access to user-specific features, with password hashing handled by bcrypt.
-   **Comprehensive Event Creation**: Organizers can create detailed event listings with titles, descriptions, dates, times, locations, capacity limits, and registration fees.
-   **Event Image Uploads**: A seamless interface for organizers to upload event posters and images to Supabase Storage.
-   **Interactive Event Discovery**: A dynamic and visually engaging page where users can browse all upcoming events, with powerful search functionality.
-   **Detailed Event View**: A modal overlay provides comprehensive details for each event, including organizer info, location, date/time, and booking options.
-   **Effortless Booking System**: Users can book their spots for an event through a simple form, and organizers can view all bookings associated with their events.
-   **User Profile Dashboard**: Authenticated users have a personal dashboard to view their account details, manage their event bookings, and change their password.
-   **Organizer Profile Management**: Organizers can view and edit their organization's details directly from their profile page.

## Technology Stack

-   **Backend**: Python, Flask
-   **Database & BaaS**: Supabase (PostgreSQL, Auth, Storage)
-   **Frontend**: HTML, JavaScript, Tailwind CSS
-   **Key Python Libraries**: `supabase-py`, `Flask`, `Flask-CORS`, `PyJWT`, `bcrypt`
-   **Key JavaScript Libraries**: `anime.js`, `GSAP`, `split-type`

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Salmanalfariz415/Smart-Campus-Event-Management-System.git
cd Smart-Campus-Event-Management-System
```

### 2. Set Up Supabase

1.  Go to [supabase.com](https://supabase.com/) and create a new project.
2.  In your Supabase project, navigate to **Project Settings** > **API**. You will need the **Project URL** and the `service_role` **Key**.
3.  Navigate to **Project Settings** > **Database**. Under **Connection string**, copy the **URI**.

### 3. Configure Environment Variables

1.  Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and populate it with your Supabase credentials from the previous step. You also need to add a strong secret key for JWT signing.

    ```env
    SUPABASE_URL=your_supabase_project_url_here
    SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
    SUPABASE_DATABASE_URL=your_supabase_database_connection_uri_here
    SECRET_KEY=your_strong_jwt_secret_key_here
    ```

### 4. Install Dependencies

1.  **Backend (Python)**: It is recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install Python packages
    pip install Flask Flask-Cors supabase python-dotenv PyJWT bcrypt requests
    ```

2.  **Frontend (Node.js)**:
    ```bash
    npm install
    ```

### 5. Set Up Database

1.  **Create Tables**: Run the provided script to automatically create the necessary tables in your Supabase database.
    ```bash
    python create_supabase_tables.py
    ```
    If this script fails, you can copy the SQL commands from `setup_supabase.py` and run them manually in the **SQL Editor** in your Supabase project dashboard.

2.  **Create Storage Bucket**: In the Supabase dashboard, go to **Storage** and create a new public bucket named `event-images`. This is where event posters will be stored.

### 6. Run the Application

1.  **Start the Backend Server**:
    ```bash
    python run.py
    ```
    The backend API will be running on `http://127.0.0.1:5000`.

2.  **View the Frontend**:
    Open the HTML files from the `app/templates/` directory in your browser. For full functionality (to allow the frontend to make API calls to the backend), it's recommended to use a live server extension (like VS Code's Live Server) which will serve the files. The backend is configured to accept requests from ports `5500`, `5501`, and `63342`.

## Project Structure

The core application logic is contained within the `app/` directory, which is organized as follows:

```
app/
├── dao/              # Data Access Objects for database interactions
├── routes/           # Flask API endpoint definitions
├── static/           # CSS, JavaScript, and image assets
├── templates/        # HTML files for the frontend
├── supabase_client.py # Initializes the Supabase client
└── __init__.py       # Flask application factory
```

## API Endpoints

The application provides a RESTful API to handle all operations.

| Method | Endpoint                      | Description                                   |
| :----- | :---------------------------- | :-------------------------------------------- |
| `POST` | `/auth/register`              | Register a new user.                          |
| `POST` | `/auth/login`                 | Log in a user and receive a JWT.              |
| `POST` | `/auth/register_organizer`    | Register a new organizer account.             |
| `GET`  | `/auth/profile`               | Get the profile of the authenticated user.    |
| `GET`  | `/auth/my-bookings`           | Get all bookings for the authenticated user.  |
| `POST` | `/auth/profile/update`        | Update an organizer's profile details.        |
| `POST` | `/auth/change-password`       | Change the user's password.                   |
| `POST` | `/event/submit`               | Submit a new event (organizer only).          |
| `GET`  | `/event/add_card`             | Get a list of all available events.           |
| `POST` | `/event/image_upload`         | Upload an image for an event.                 |
| `POST` | `/booking/create`             | Create a new booking for an event.            |
| `GET`  | `/booking/lookup/<ref>`       | Look up a booking by its reference number.    |
| `POST` | `/booking/cancel`             | Cancel an existing booking.                   |
| `GET`  | `/booking/event/<id>`         | Get all bookings for a specific event.        |

## Testing

The repository includes several scripts to help with setup, verification, and testing:

-   `test_supabase_connection.py`: Verifies that the `.env` configuration is correct and that the application can successfully connect to your Supabase instance.
-   `test_api_endpoints.py`: Runs a series of automated requests against the live Flask server to test critical endpoints like user registration and login.
-   `create_supabase_tables.py`: Tests for the existence of database tables and creates them if they are missing.
