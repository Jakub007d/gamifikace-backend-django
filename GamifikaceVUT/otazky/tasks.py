"""
Celery úloha pre týždenné generovanie výzvy v aplikácii Gamifikace.

Obsahuje logiku pre:
- Ocenenie najlepších hráčov achievementom.
- Resetovanie skóre.
- Generovanie novej sady otázok pre výzvu.
"""

import random
from celery import shared_task
from otazky.models import Achievement, Course, Okruh, Question, ChalangeQuestion, Score, User

@shared_task
def generate_weekly_challenge():
    """
    Vygeneruje týždennú výzvu a ocení najlepších hráčov v každom kurze.

    Funkcionalita:
    1. Vyhodnotí najlepších hráčov (1. miesto) podľa skóre v každom kurze a priradí im achievement.
    2. Vymaže existujúce skóre a predošlé výzvy.
    3. Pre každý dostupný okruh náhodne vyberie max. 5 otázok a vytvorí nové záznamy výzvy (ChalangeQuestion).

    Logika:
    - Hráči s rovnakým skóre na 1. mieste dostanú rovnaký achievement.
    - Výzvy sa regenerujú každým spustením tasku (raz týždenne cez Celery Beat).

    Returns:
        None
    """
    print("🛠️ Dávam achivment najlepsim hráčom")

    scores = Score.objects.select_related('course').all().order_by('course__name')
    top_scores_by_course = {}

    # Nájdeme najlepších hráčov pre každý kurz
    for score in scores:
        course_id = score.course.id
        if course_id not in top_scores_by_course:
            top_scores_by_course[course_id] = {
                'users': [score.user],
                'course': score.course,
                'points': score.points
            }
        elif score.points == top_scores_by_course[course_id]['points']:
            top_scores_by_course[course_id]['users'].append(score.user)

    # Ocenenie najlepších hráčov
    for data in top_scores_by_course.values():
        users = data['users']
        course = data['course']
        if course:
            achievement_name = f"Dosiahnuté 1. miesto v {course.name}"
            achievement, created = Achievement.objects.get_or_create(name=achievement_name)
            if created:
                print(f"New achievement created: {achievement_name}")
            for user in users:
                achievement.award_to_user(user)

    print("🚀 Generujem týždennú výzvu...")

    # Resetovanie predošlých výziev a skóre
    ChalangeQuestion.objects.all().delete()
    Score.objects.all().delete()
    print("🧹 Skóre bolo vymazané.")

    # Výber otázok pre novú výzvu
    okruhy = Okruh.objects.filter(available=True)

    for okruh in okruhy:
        course = okruh.course
        questions = Question.objects.filter(okruh=okruh, visible=True, approved=True)

        if questions.exists():
            selected_questions = random.sample(
                list(questions),
                k=min(5, questions.count())
            )
            for question in selected_questions:
                ChalangeQuestion.objects.create(courseID=course, question=question)

    print("✅ Výzva vygenerovaná a skóre zresetované.")
