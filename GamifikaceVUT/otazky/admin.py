from django.contrib import admin
from .models import Achievement, Question, Answer, Comment, Course, Okruh, Score,ChalangeQuestion


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'approved','reported','visible')


    def __str__(self):
        return self.name



admin.site.register(Question, QuestionAdmin)


# Register your models here.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text')


    def __str__(self):
        return self.text


admin.site.register(Answer, AnswerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by')
    


admin.site.register(Comment, CommentAdmin)


class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('visited_by',)
    list_display = ('name','full_name')
    def __str__(self):
        return self.name


admin.site.register(Course, CourseAdmin)


class OkruhAdmin(admin.ModelAdmin):
    filter_horizontal = ('finished_by',)
    list_display = ('name', 'course', 'available')
    def __str__(self):
        return self.name


admin.site.register(Okruh, OkruhAdmin)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'points', 'user')
    def __str__(self):
        return self.user


admin.site.register(Score, ScoreAdmin)

class ChallangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'courseID', 'question')

admin.site.register(ChalangeQuestion, ChallangeAdmin)

class AchievementAdmin(admin.ModelAdmin):
    filter_horizontal = ('awarded_to',)
    list_display = ('id', 'name')

admin.site.register(Achievement, AchievementAdmin)

