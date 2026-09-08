import os
import django
from faker import Faker
import pandas as pd

# Read Excel file
df = pd.read_excel('/home/santosh/Downloads/bcadata.xlsx')  # You can specify sheet name if needed

uucms_id = list(df['Regisration No'])

name = list(df['Student Name'])

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_event.settings")
django.setup()

from quiz.models import Student, CustomUser,Result

fake = Faker()
COMMON_PASSWORD = "SMD@123"

def populate_students_and_users():
    for i,j in zip(uucms_id, name):
        email = i+'@gmail.com'

        # Create Student record
        student = Student.objects.create(
            uucms_id=i,
            name=j,
        )

        # Create CustomUser linked by uucms_id
        user, created = CustomUser.objects.get_or_create(
            uucms_id=i,
            defaults={
                "email": email
            }
        )
        user.set_password(COMMON_PASSWORD)
        user.save()

        # ✅ Create Result record with default score 0
        result, created = Result.objects.get_or_create(
            uucms_id=i,
            defaults={
                "score": 0
            }
        )

        print(f"Created Student & User: {j} | UUCMS_ID: {i}")

if __name__ == "__main__":
    #student_count = 1  # Change count as needed
    populate_students_and_users()
    print(f"\n✅ Populated students and users with password: {COMMON_PASSWORD}")
