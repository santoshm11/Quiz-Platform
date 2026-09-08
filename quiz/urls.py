from django.urls import path
from quiz import views
from django.shortcuts import render

urlpatterns = [
    path('register/', views.register_individual, name='register_individual'),
    path('login/', views.individual_login, name='individual_login'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path("team-dashboard/", views.team_dashboard, name="team_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("api/get-logged-in-participants/",views.get_logged_in_participants,name="get-logged-in-participants"),
    path("logout-participant/<str:uucms_id>/", views.admin_logout_participant, name="admin_logout_participant"),
    path('countdown/', lambda request: render(request, 'quiz/countdown.html')),
    path('quiz/',lambda request: render(request, 'quiz/quiz_page.html')),
    path('holding/',lambda request: render(request, 'quiz/holding.html')),
    path('result/',lambda request: render(request, 'quiz/result.html'),name='result'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('status/',views.get_participant_status,name='status'),
    path('get-quiz-results/',views.get_quiz_results,name='get_quiz_results'),
    path('result-details/<str:uucms_id>/',views.result_details,name="result_details"),
]
