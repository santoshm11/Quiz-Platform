from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, uucms_id, email, password=None, **extra_fields):
        if not uucms_id:
            raise ValueError("The UUCMS_ID must be set")
        email = self.normalize_email(email)
        user = self.model(uucms_id=uucms_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uucms_id, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(uucms_id, email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    uucms_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    username = None  # Remove default username field
    USERNAME_FIELD = "uucms_id"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.uucms_id

class Student(models.Model):
    uucms_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class MCQQuestion(models.Model):
    question_name = models.TextField()  # Stores the question text
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    CATEGORY_CHOICES = [
        ("programming", "Programming"),
        ("data_structures", "Data Structures"),
        ("algorithms", "Algorithms"),
        ("databases", "Databases"),
        ("networking", "Networking"),
        ("cybersecurity", "Cybersecurity"),
        ("operating_systems", "Operating Systems"),
        ("ai_ml", "AI & Machine Learning"),
        ("cloud_computing", "Cloud Computing"),
        ("software_engineering", "Software Engineering"),
        ("general","General")
    ]
    # The correct answer should be one of the 4 options
    CORRECT_ANSWER_CHOICES = [
        ("option1", "Option 1"),
        ("option2", "Option 2"),
        ("option3", "Option 3"),
        ("option4", "Option 4"),
    ]
    correct_answer = models.CharField(max_length=10, choices=CORRECT_ANSWER_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # ✅ New field (Category)
    duration = models.PositiveIntegerField(default=30)  # ✅ New field (Duration in seconds)

    def get_correct_answer_text(self):
        """Return the actual text of the correct answer instead of option1, option2, etc."""
        correct_option = getattr(self, self.correct_answer, None)
        return correct_option if correct_option else "Not Set"

    def __str__(self):
        return self.question_name

class UserQuiz(models.Model):
    STATUS_CHOICES = [
        ("correct", "Correct"),
        ("incorrect", "Incorrect"),
        ("unanswered", "Unanswered"),
    ]
    uucms_id = models.CharField(max_length=20)  # Store participant's UUCMS_ID
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE)
    answered_question = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="unanswered")
    submitted_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"Participant {self.uucms_id} - {self.question.question_name[:50]}"

class Result(models.Model):
    uucms_id = models.CharField(max_length=20, unique=True)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Participant {self.uucms_id} - Score: {self.score}"
