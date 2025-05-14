import uuid
from django.db import models
from django.contrib.auth.models import User

"""
Django modely pre aplikáciu Gamifikace.

Obsahuje definície kurzov, skóre, okruhov, otázok, odpovedí, komentárov a achievementov.
"""

class Course(models.Model):
    """
    Model reprezentujúci kurz.

    Attributes:
        name (str): Názov kurzu (krátky).
        full_name (str): Celý názov kurzu.
        visited_by (QuerySet[User]): Používatelia, ktorí navštívili tento kurz.
    """
    name = models.CharField(max_length=255, unique=True, default="")
    full_name = models.CharField(max_length=255, default="")
    visited_by = models.ManyToManyField(User)
    def __str__(self):
        """Vráti názov kurzu ako reťazec."""
        return self.name

class Score(models.Model):
    """
    Model reprezentujúci skóre používateľa v konkrétnom kurze.

    Attributes:
        id (UUID): Unikátne ID skóre.
        points (int): Počet získaných bodov.
        user (User): Používateľ, ktorý skóre dosiahol.
        course (Course): Kurz, ku ktorému skóre patrí.
    """   
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    points = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default="1")

class Okruh(models.Model):
    """
    Model reprezentujúci okruh v rámci kurzu.

    Attributes:
        name (str): Názov okruhu.
        description (str): Popis okruhu.
        available (bool): Označuje, či je okruh dostupný.
        course (Course): Kurz, ku ktorému okruh patrí.
        finished_by (QuerySet[User]): Používatelia, ktorí okruh dokončili.
    """
    name = models.CharField(max_length=255, unique=False, default="")
    description = models.CharField(max_length=255, unique=False, default="")
    available = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    finished_by = models.ManyToManyField(User, blank=True)
    def __str__(self):
        """Vráti názov okruhu ako reťazec."""
        return self.name


class Question(models.Model):
    """
    Model reprezentujúci otázku.

    Attributes:
        id (UUID): Unikátne ID otázky.
        name (str): Názov otázky.
        text (str): Text otázky.
        approved (bool): Schválená otázka.
        created_at (datetime): Dátum a čas vytvorenia.
        visible (bool): Viditeľnosť otázky.
        created_by (User): Autor otázky.
        likes (int): Počet lajkov.
        reported (bool): Nahlásená otázka.
        okruh (Okruh): Okruh, ku ktorému otázka patrí.
        is_text_question (bool): Označuje, či ide o textovú otázku.
        ai_context (str): AI generovaný kontext k otázke.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    text = models.TextField(default="")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    okruh = models.ForeignKey(Okruh, on_delete=models.CASCADE)
    is_text_question = models.BooleanField(default=False)
    ai_context = models.CharField(max_length=255, default="", blank="True")

    def __str__(self):
        """Vráti názov otázky ako reťazec."""
        return self.name


class Answer(models.Model):
    """
    Model reprezentujúci odpoveď na otázku.

    Attributes:
        id (UUID): Unikátne ID odpovede.
        answer_type (bool): Označuje správnosť odpovede (True = správna).
        text (str): Text odpovede.
        question (Question): Otázka, ku ktorej odpoveď patrí.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    answer_type = models.BooleanField(default=True)
    text = models.TextField(default="")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Model reprezentujúci komentár k otázke.

    Attributes:
        id (UUID): Unikátne ID komentára.
        text (str): Text komentára.
        created_at (datetime): Dátum a čas vytvorenia.
        created_by (User): Autor komentára.
        likes (int): Počet lajkov.
        question (Question): Otázka, ku ktorej komentár patrí.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class ChalangeQuestion(models.Model):
    """
    Model reprezentujúci priradenie otázky k výzve.

    Attributes:
        id (UUID): Unikátne ID.
        courseID (Course): Kurz, ku ktorému sa otázka viaže.
        question (Question): Otázka priradená k výzve.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Achievement(models.Model):
    """
    Model reprezentujúci achievement.

    Attributes:
        id (UUID): Unikátne ID achievementu.
        name (str): Názov achievementu.
        awarded_to (QuerySet[User]): Používatelia, ktorým bol achievement udelený.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.TextField(default="")
    awarded_to = models.ManyToManyField(User)
    
    def __str__(self):
        """Vráti názov achievementu ako reťazec."""
        return self.name
    
    def award_to_user(self, user):
        """
        Pridá achievement používateľovi, ak ho ešte nemá.

        Args:
            user (User): Používateľ, ktorému sa má achievement udeliť.

        Returns:
            bool: True, ak bol achievement pridaný, False ak už ho mal.
        """
        if user not in self.awarded_to.all():
            self.awarded_to.add(user)
            return True
        return False
