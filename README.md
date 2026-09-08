# Quiz Event Management System

A real-time online quiz application built with **Django** and **Django Channels**. The system allows participants to register, log in using their UUCMS ID, attend timed MCQ quizzes, and view their results. Administrators can monitor participants and control the quiz.

## Features

* Participant registration and login
* UUCMS ID-based authentication
* Admin dashboard
* Real-time quiz using WebSockets
* Countdown before each question
* Timed MCQ questions
* Automatic answer submission
* Automatic answer evaluation
* Score calculation
* Participant result tracking
* Detailed question-wise results
* Admin can view and logout active participants

## Technologies Used

* Python
* Django 4.2
* Django Channels
* Daphne
* SQLite
* HTML
* CSS
* JavaScript
* WebSockets

The project uses Django Channels and WebSocket routes for both participants and administrators.

## Project Structure

```text
quiz_event/
│
├── manage.py
├── requirements.txt
│
├── quiz_event/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── ...
│
├── quiz/
│   ├── models.py
│   ├── views.py
│   ├── consumers.py
│   ├── routing.py
│   ├── middleware.py
│   ├── admin.py
│   └── ...
│
├── templates/
├── static/
│
├── populate.py
├── populateresult.py
└── quizpopulate.py
```

## Installation

Clone the project and create a virtual environment:

```bash
git clone <repository-url>
cd quiz_event

python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

## Main URLs

```text
/register/              Participant registration
/login/                 Participant login
/team-dashboard/        Participant dashboard
/admin-dashboard/       Admin dashboard
/quiz/                   Quiz page
/countdown/              Quiz countdown
/result/                 Result page
/admin/                  Django admin
```

The application also exposes WebSocket endpoints for participants and administrators.

## Quiz Flow

```text
Participant Registration
          ↓
       Login
          ↓
   Participant Dashboard
          ↓
      Countdown
          ↓
     Quiz Questions
          ↓
    Answer Submission
          ↓
    Answer Evaluation
          ↓
       Score
          ↓
       Results
```

The admin can start the quiz through the WebSocket connection, which broadcasts quiz events to connected participants.

## Database Models

The main models are:

* `CustomUser` – participant authentication
* `Student` – participant information
* `MCQQuestion` – quiz questions and options
* `UserQuiz` – participant answers and status
* `Result` – participant score

MCQ questions support categories such as Programming, Data Structures, Algorithms, Databases, Networking, AI/ML, Cloud Computing, and others.

## Data Population

The project includes scripts for populating students, results, and sample quiz questions:

```bash
python populate.py
python populateresult.py
python quizpopulate.py
```

`populate.py` can import student information from an Excel file and create corresponding student/user/result records.

## License

This project is developed for educational/event purposes.
