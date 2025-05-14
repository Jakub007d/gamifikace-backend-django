"""
URL configuration for gamifikace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from otazky import views
from django.conf.urls import *
from otazky.views import *
from rest_framework_simplejwt import views as jwt_views
router = routers.DefaultRouter()
router.register(r'otazky',views.OtazkaView,'otazka')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('',HomeView,name='otazka'),
        path('courses/',CourseView.as_view(),name='courses'),
        path('comment/',CommentView.as_view(),name='comment'),
        path('score/',ScoreView.as_view(),name='score'),
        path('comment/query',CommentsForQuestionView.as_view(),name='comment-specific'),
        path('answer/query',AnswersForQuestion.as_view(),name='answer-specific'),
        path('lectures/query',OkruhsForCourse.as_view(),name='okruhs-specific'),
        path('lectures/byID',OkruhByID.as_view(),name='okruhs-specific-id'),
        path('question/query',QuestionForOkruh.as_view(),name='questions-specific'),
        path('question/reported/query',ReportedQuestionsForLecture.as_view(), name='questions-reported-specific'),
        path('user/',Username.as_view(),name='user-specific'),
        path('newQuestion/',NewQuestion.as_view(),name='new-question'),
        path('newAnswers/',NewAnswers.as_view(),name='new-answers'),
        path('userID/',UsernameID.as_view(),name='user-ID'),
        path('challange/query',CallangeQuestions.as_view(),name="výzva"),
        path('token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
        path('token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
        path('home/', views.HomeView, name ='home'),
        path('logout/', views.LogoutView.as_view(), name ='logout'),
        path('user/query',UserForID.as_view(),name="user_id-specific"),
        path('score/entry',ScoreEntry.as_view(),name="score-entry"),
        path('question/specific',QuestionByID.as_view(),name="question-by-id"),
        path('comment/add',NewComment.as_view(),name="add-comment"),
        path('visited/add',AddUserToCourse.as_view(),name="add-visited"),
        path('visited/remove',RemoveUserFomCourse.as_view(),name="remove-visited"),
        path('courses/visited',CoursesForUSer.as_view(),name="courses-visited"),
        path('lecture/<int:okruh_id>/complete/', CompleteLecture.as_view(), name='complete_lecture'),
        path('user/<int:user_id>/achievements/', AchievementView.as_view(), name='user-achievements'),
        path('user/completion/', UserCourseCompletionView.as_view(), name='user-course-completion'),
        path('questions/<uuid:question_id>/update-ai-context/', UpdateAIContextView.as_view(), name='update_ai_context'),
        path('register/', UserRegistrationView.as_view(), name='user-register'),
        path('report-question/', ReportQuestion.as_view(), name='report-question'),
    ])),
]
