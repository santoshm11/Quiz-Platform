from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import CustomUser,Student
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import UserQuiz, MCQQuestion, Result,Student
import json

COMMON_PASSWORD = "SMD@123"

@login_required(login_url="/login/")
def result_details(request, uucms_id):
    participant_answers = UserQuiz.objects.filter(uucms_id=uucms_id).select_related('question')
    
    data = []
    for index, answer in enumerate(participant_answers, start=1):
        if answer.status == "correct":
            row_color = "green-row"
        elif answer.status == "incorrect":
            row_color = "red-row"
        elif answer.status == "unanswered":
            row_color = "yellow-row"
        else:
            row_color = "pink-row"

        data.append({
            'sl_no': index,
            'question_text': answer.question.question_name,
            'correct_answer': answer.question.get_correct_answer_text(),
            'selected_answer': "Unanswered" if answer.answered_question == "No Response" else answer.answered_question,
            'status': row_color
        })
    
    return render(request, 'quiz/result_details.html', {
        'participant_id': uucms_id,
        'answers': data
    })

@login_required(login_url="/login/")
def get_quiz_results(request):
    if request.method == "GET":
        # 1️⃣ Get all active sessions (not expired)
        active_sessions = Session.objects.filter(expire_date__gte=now())

        # 2️⃣ Extract participant_user_id from each session
        logged_in_participant_ids = [
            session.get_decoded().get("participant_user_id") 
            for session in active_sessions 
            if session.get_decoded().get("participant_user_id")
        ]
        
        # 3️⃣ Get CustomUser objects matching these IDs
        participants = CustomUser.objects.filter(id__in=logged_in_participant_ids)

        # 4️⃣ Extract uucms_ids
        uucms_ids = participants.values_list("uucms_id", flat=True)

        # 5️⃣ Get Result records only for logged-in users
        results = Result.objects.filter(uucms_id__in=uucms_ids).order_by('-score')

        result_list = []
        for result in results:
            try:
                participant = Student.objects.get(uucms_id=result.uucms_id)
                name = participant.name  # Adjust based on actual field
            except Student.DoesNotExist:
                name = "Unknown"

            result_list.append({
                'uucms_id': result.uucms_id,
                'name': name,
                'score': result.score,
            })

        return JsonResponse({'success': True, 'results': result_list})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_participant_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        participant = request.user
        if participant.is_authenticated:
            uucms_id = participant.uucms_id  # Assuming participant is logged in
            latest_quiz = UserQuiz.objects.filter(uucms_id=uucms_id).order_by('-submitted_at').first()
            if latest_quiz:
                status = latest_quiz.status  # Correct, Incorrect, Unanswered
                print(status)
                return JsonResponse({'status': status})
            else:
                return JsonResponse({'status': 'unanswered'})
        else:
            return JsonResponse({'status': 'unauthorized'}, status=401)
    
    # 🚩 IMPORTANT: Always return something for non-POST requests
    return JsonResponse({'error': 'Invalid request'}, status=400) 

@csrf_exempt
@login_required(login_url="/login/")
def submit_answer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')
            selected_option = data.get('selected_option')
            participant = request.user

            question = MCQQuestion.objects.get(id=question_id)

            # Check correct or not
            correct_option = question.get_correct_answer_text()  # Assuming MCQQuestion has this
            #print(correct_option)
            #print(selected_option)
            if selected_option == 'No Response':
                status = 'unanswered'
                print(status)
            elif selected_option.strip().lower() == correct_option.strip().lower():
                status = 'correct'
                print(status)
            else:
                status = 'incorrect'
                print(status)
            print(f"{participant.uucms_id} submited the answer {selected_option} for {question} and status is {status}")
            # Save to UserQuiz
            UserQuiz.objects.update_or_create(
                uucms_id=participant.uucms_id,  # Assuming username is UUCMS_ID
                question=question,
                defaults={
                    'answered_question': selected_option,
                    'status': status,
                    'submitted_at': now(),
                }
            )
            if status == "correct":
                result, created = Result.objects.get_or_create(uucms_id=participant.uucms_id)
                result.score += 5
                result.save()
            
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid Request"})

@login_required(login_url="/login/")
def get_logged_in_participants(request):
    active_sessions = Session.objects.filter(expire_date__gte=now())

    logged_in_participant_ids = [
        session.get_decoded().get("participant_user_id") 
        for session in active_sessions 
        if session.get_decoded().get("participant_user_id")
    ]
    
    participants = CustomUser.objects.filter(id__in=logged_in_participant_ids)

    uucms_ids = participants.values_list("uucms_id", flat=True)

    students = Student.objects.filter(uucms_id__in=uucms_ids)
    
    participants_data = []
    for index, student in enumerate(students, start=1):
        participants_data.append({
        "serialNo": index,
        "uucms_id": student.uucms_id,
        "name": student.name,
    })

    return JsonResponse(participants_data, safe=False)

def is_admin(user):
    return user.is_staff or user.is_superuser 

@login_required(login_url="/admin/")
@user_passes_test(is_admin, login_url="/admin/")
def admin_dashboard(request):
    return render(request, "quiz/admin_dashboard.html",)

@login_required(login_url="/login/")
def team_dashboard(request):
    return render(request, "quiz/individual_dashboard.html")

@login_required(login_url="/admin/")
@user_passes_test(is_admin, login_url="/admin/")
def admin_logout_participant(request, uucms_id):
    """Allows admin to force logout a specific participant"""
    try:
        # Get the participant user
        participant = CustomUser.objects.get(uucms_id=uucms_id)

        # Find and delete session linked to this participant
        active_sessions = Session.objects.filter(expire_date__gte=now())
        for session in active_sessions:
            data = session.get_decoded()
            if data.get("participant_user_id") == participant.id:
                session.delete()  # ❌ Force logout the participant

        return JsonResponse({"success": True, "message": f"Participant {uucms_id} has been logged out."})
    except CustomUser.DoesNotExist:
        return JsonResponse({"success": False, "error": "Participant not found."}, status=404)
    
@csrf_protect
def register_individual(request):
    if request.method == "POST":
        uucms_id = request.POST.get("uucms_id")
        name = request.POST.get("name")
        email = uucms_id+'@gmail.com'

        if CustomUser.objects.filter(uucms_id=uucms_id).exists():
            return JsonResponse({"success": False, "error": "UUCMS ID already exists."}, status=400)

         # 1️⃣ Create Student
        student = Student.objects.create(
            uucms_id=uucms_id,
            name=name,
        )

        # 2️⃣ Create CustomUser linked by UUCMS_ID (No need for ForeignKey!)
        user, created = CustomUser.objects.get_or_create(
            uucms_id=uucms_id,
            defaults={
                "email": email
            }
        )
        user.set_password(COMMON_PASSWORD)
        user.save()

        return JsonResponse({"success": True, "message": "Registration successful.","uucms_id": uucms_id, "password": COMMON_PASSWORD})

    return render(request, "quiz/register.html")

@csrf_protect
def individual_login(request):
    if request.method == "POST":
        uucms_id = request.POST.get("uucms_id")
        password = request.POST.get("password")
        user = authenticate(request, uucms_id=uucms_id, password=password)
        if user is not None:
            # ✅ Check if the participant is already logged in
            existing_sessions = Session.objects.filter(expire_date__gte=now())
            for session in existing_sessions:
                data = session.get_decoded()
                if data.get("participant_user_id") == user.id:
                    session.delete()  # ❌ Logout previous session (only one active login)

            # ✅ Flush session (prevent interference with admin session)
            request.session.flush()

            # ✅ Set participant-specific session key
            request.session["participant_user_id"] = user.id
            request.session.create()
            request.session.save()

            response = redirect("team_dashboard")  # Redirect to participant dashboard

            # ✅ Set unique session cookie for this participant
            response.set_cookie(f"participant_sessionid_{user.uucms_id}", request.session.session_key)

            login(request, user)
            #notify_admin_dashboard()  
            return redirect("team_dashboard")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('individual_login')
        
    return render(request, "quiz/login.html")

@csrf_protect
def reset_password(request):
    if request.method == "POST":
        uucms_id = request.POST.get("uucms_id")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        try:
            user = CustomUser.objects.get(uucms_id=uucms_id)
            user.set_password(COMMON_PASSWORD)  # Reset to common password
            user.save()

            return redirect('individual_login')

        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid UUCMS ID or Email."}, status=400)

    return render(request, "quiz/reset_password.html")
