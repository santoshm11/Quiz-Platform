import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_event.settings")
django.setup()

from quiz.models import Student, Result

def create_results_for_existing_students():
    students = Student.objects.all()
    created_count = 0

    for student in students:
        # Check if Result already exists to avoid duplicates
        result, created = Result.objects.get_or_create(
            uucms_id=student.uucms_id,
            defaults={
                "score": 0
            }
        )
        if created:
            created_count += 1
            print(f"✅ Created Result for UUCMS_ID: {student.uucms_id}")
        else:
            print(f"⚠️ Result already exists for UUCMS_ID: {student.uucms_id}")

    print(f"\n🎉 Done! Total new results created: {created_count}")

if __name__ == "__main__":
    create_results_for_existing_students()
