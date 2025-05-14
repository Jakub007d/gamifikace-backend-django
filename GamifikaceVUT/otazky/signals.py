"""
Signály pre aplikáciu Gamifikace.

Obsahuje logiku pre automatické udeľovanie achievementov po dokončení všetkých okruhov v kurze.
"""

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Okruh, Achievement, User

@receiver(m2m_changed, sender=Okruh.finished_by.through)
def check_all_lectures_completed(sender, instance, action, pk_set, **kwargs):
    """
    Skontroluje, či používateľ dokončil všetky okruhy v rámci kurzu.

    Ak áno, priradí mu príslušný achievement.

    Tento signál sa spustí pri zmene ManyToManyField `finished_by` na modeli Okruh.

    Args:
        sender: Trieda modelu, ktorá vyvolala signál.
        instance: Inštancia Okruh, ktorej sa zmena týka.
        action: Typ akcie na ManyToManyField (napr. 'post_add').
        pk_set: Sada primárnych kľúčov používateľov, ktorých sa zmena týka.
        **kwargs: Ďalšie voliteľné argumenty.
    """
    if action == "post_add":  # Ak sa pridali noví používatelia
        # Získa všetky okruhy prislúchajúce ku kurzu
        course_okruhy = Okruh.objects.filter(course=instance.course)

        # Prechádza používateľov pridaných do finished_by
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)

            # Skontroluje, či používateľ dokončil všetky okruhy v danom kurze
            if all(user in okruh.finished_by.all() for okruh in course_okruhy):
                achievement_name = f"Dokončené všetky okruhy v {instance.course.name}"

                # Vytvorí alebo nájde achievement pre tento kurz
                achievement, created = Achievement.objects.get_or_create(name=achievement_name)

                if created:
                    print(f"New achievement created: {achievement_name}")

                # Priradí achievement používateľovi (ak ho ešte nemá)
                achievement.award_to_user(user)
