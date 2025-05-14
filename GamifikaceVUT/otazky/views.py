from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
from rest_framework.permissions import AllowAny

class OtazkaView(generics.ListCreateAPIView):
    """
    API endpoint na získanie zoznamu všetkých otázok a pridanie novej otázky.

    - GET: Vráti zoznam všetkých otázok.
    - POST: Uloží novú otázku do databázy.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CommentView(generics.ListCreateAPIView):
    """
    API endpoint na získanie zoznamu komentárov a pridanie nového komentára.

    - GET: Vráti zoznam všetkých komentárov.
    - POST: Uloží nový komentár.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentsForQuestionView(generics.ListCreateAPIView):
    """
    API endpoint na získanie komentárov k danej otázke podľa parametra `questionID`.

    - GET: Vráti zoznam komentárov prislúchajúcich k danej otázke.
    """
    Model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Vráti queryset komentárov filtrovaných podľa `questionID`.

        Ak je parameter `questionID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba komentáre priradené
        k otázke s daným ID. Inak vráti všetky komentáre.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované komentáre.
        """
        queryset= Comment.objects.all()
        questionID = self.request.query_params.get('questionID')
        if questionID:
            queryset = queryset.filter(question=questionID)
        return queryset


class CourseView(generics.ListCreateAPIView):
    """
    API endpoint na získanie zoznamu kurzov a pridanie nového kurzu.

    - GET: Vráti zoznam všetkých kurzov.
    - POST: Uloží nový kurz.
    """
    Model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Vráti queryset všetkých kurzov.

        Returns:
            QuerySet: Django QuerySet obsahujúci všetky kurzy.
        """
        queryset= Course.objects.all()
        return queryset


class ScoreView(generics.ListCreateAPIView):
    """
    API endpoint na získanie zoznamu skóre pre zadaný kurz (`courseID`).

    - GET: Vráti skóre zoradené zostupne podľa bodov.
    """
    Model = Score
    serializer_class = ScoreSerializer

    def get_queryset(self):
        """
        Vráti queryset skóre filtrovaných podľa `courseID` a zoradených zostupne.

        Načíta `courseID` z query parametrov požiadavky, filtruje skóre
        pre daný kurz a zoradí výsledky zostupne podľa atribútu `points`.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované a zoradené skóre.
        """
        courseID = self.request.query_params.get('courseID')
        queryset = Score.objects.filter(course = courseID)
        queryset = queryset.order_by('-points')
        return queryset


class AnswersForQuestion(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating answers for a specific question.
    """
    Model = Answer
    serializer_class = AnswerSerializer

    def get_queryset(self):
        """
        Vráti queryset odpovedí filtrovaných podľa `questionID`.

        Ak je parameter `questionID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba odpovede priradené
        k otázke s daným ID. Inak vráti všetky odpovede.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované odpovede.
        """
        queryset= Answer.objects.all()
        questionID = self.request.query_params.get('questionID')
        if questionID:
            queryset = queryset.filter(question=questionID)
        return queryset


class OkruhsForCourse(generics.ListCreateAPIView):
    """
    API endpoint pre získanie zoznamu okruhov pre špecifický kurz
    a pre pridanie nového okruhu ku kurzu.

    - GET: Vráti zoznam okruhov pre daný kurz (`courseID`).
    - POST: Umožní vytvoriť nový okruh priradený ku kurzu.
    """
    Model = Okruh
    serializer_class = OkruhSerializer

    def get_queryset(self):
        """
        Vráti queryset okruhov filtrovaných podľa `courseID`.

        Ak je parameter `courseID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba okruhy priradené
        k danému kurzu. Inak vráti všetky okruhy.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované okruhy.
        """
        queryset= Okruh.objects.all()
        courseID = self.request.query_params.get('courseID')
        if courseID:
            queryset = queryset.filter(course=courseID)
        return queryset


class OkruhByID(generics.ListCreateAPIView):
    """
    API endpoint pre získanie okruhu (alebo zoznamu okruhov) podľa jeho ID.

    - GET: Vráti okruh (okruhy) filtrované podľa `okruhID`.
    - POST: Umožní vytvoriť nový okruh.
    """
    Model = Okruh
    serializer_class = OkruhSerializer

    def get_queryset(self):
        """
        Vráti queryset okruhov filtrovaných podľa `okruhID`.

        Ak je parameter `okruhID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba okruhy s daným ID.
        Inak vráti všetky okruhy.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované okruhy.
        """
        queryset= Okruh.objects.all()
        okruhID = self.request.query_params.get('okruhID')
        if okruhID:
            queryset = queryset.filter(id=okruhID)
        return queryset


class QuestionByID(generics.ListCreateAPIView):
    """
    API endpoint pre získanie otázky (alebo zoznamu otázok) podľa jej ID.

    - GET: Vráti otázku (otázky) filtrované podľa `questionID`.
    - POST: Umožní vytvoriť novú otázku.
    """
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Vráti queryset otázok filtrovaných podľa `questionID`.

        Ak je parameter `questionID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba otázky s daným ID.
        Inak vráti všetky otázky.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované otázky.
        """
        queryset= Question.objects.all()
        question_id = self.request.query_params.get('questionID')
        if question_id:
            queryset = queryset.filter(id=question_id)
        return queryset


class QuestionForOkruh(generics.ListCreateAPIView):
    """
    API endpoint pre získanie zoznamu otázok pre špecifický okruh
    a pre pridanie novej otázky k okruhu.

    - GET: Vráti zoznam otázok pre daný okruh (`okruhID`).
    - POST: Umožní vytvoriť novú otázku priradenú k okruhu.
    """
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Vráti queryset otázok filtrovaných podľa `okruhID`.

        Ak je parameter `okruhID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba otázky priradené
        k danému okruhu. Inak vráti všetky otázky.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrované otázky.
        """
        queryset= Question.objects.all()
        okruhID = self.request.query_params.get('okruhID')
        if okruhID:
            queryset = queryset.filter(okruh=okruhID)
        return queryset


class ReportedQuestionsForLecture(generics.ListCreateAPIView):
    """
    API endpoint pre získanie zoznamu nahlásených otázok pre špecifickú prednášku (okruh).

    - GET: Vráti zoznam nahlásených otázok pre danú prednášku (`lectureID`).
    - POST: Umožní vytvoriť novú otázku (potenciálne nahlásenú, podľa dát).
    """
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Vráti queryset nahlásených otázok pre danú prednášku (okruh).

        Filtruje otázky na základe `lectureID` (ID okruhu) z query parametrov
        a zároveň na základe atribútu `reported=True`.

        Returns:
            QuerySet: Django QuerySet obsahujúci nahlásené otázky pre danú prednášku.
                      Ak `lectureID` nie je poskytnutý, vráti prázdny queryset.
        """
        lectureID = self.request.query_params.get('lectureID')
        if lectureID:
            queryset = Question.objects.all()
            queryset = queryset.filter(okruh=lectureID)
            queryset = queryset.filter(reported=True)
            return queryset
        return Question.objects.none() 


class CallangeQuestions(generics.ListCreateAPIView):
    """
    API endpoint pre získanie zoznamu "challenge" otázok pre daný kurz.

    - GET: Vráti zoznam "challenge" otázok na základe `courseID`.
    - POST: Umožní vytvoriť novú "challenge" otázku (prostredníctvom serializéra).
    """
    Model = Question
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Vráti queryset "challenge" otázok pre špecifikovaný kurz.

        Načíta `courseID` z query parametrov. Následne získa objekty `ChalangeQuestion`
        asociované s týmto kurzom a na základe nich vyfiltruje príslušné objekty `Question`.

        Returns:
            QuerySet: Django QuerySet obsahujúci "challenge" otázky pre daný kurz.
                      Vráti `None` alebo prázdny queryset, ak sa vyskytne chyba alebo nie sú nájdené žiadne otázky.
        """
        print(self.request.query_params.get('courseID'))
        challange_questions= ChalangeQuestion.objects.filter(courseID=self.request.query_params.get('courseID'))
        queryset= None
        for chalange_question in challange_questions:
            print(chalange_question.id)
            if queryset is None :
                queryset = Question.objects.filter(id = chalange_question.question.id)
                print(queryset.values_list())
            else:
                queryset = queryset | Question.objects.filter(id = chalange_question.question.id)
        return queryset


class Username(APIView):
    """
    API endpoint na získanie používateľského mena na základe prístupového tokenu.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na získanie používateľského mena.

        Očakáva `access_token` v tele požiadavky. Na základe tokenu dekóduje
        ID používateľa, načíta používateľa z databázy a vráti jeho reťazcovú reprezentáciu.

        Args:
            request (Request): Objekt HTTP požiadavky.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Odpoveď obsahujúca používateľské meno ako string,
                      alebo HttpResponse s chybou 401, ak je token neplatný.
        """
        try:
            access_token_obj = AccessToken(request.data["access_token"])
        except:
            return HttpResponse('Unauthorized', status=401)
        user_id=access_token_obj['user_id']

        user = User.objects.get(id=user_id)
        print(user)
        return Response(str(user))


class UsernameID(APIView):
    """
    API endpoint na získanie ID používateľa na základe prístupového tokenu.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na získanie ID používateľa.

        Očakáva `access_token` v tele požiadavky. Na základe tokenu dekóduje
        ID používateľa a vráti ho.

        Args:
            request (Request): Objekt HTTP požiadavky.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Odpoveď obsahujúca ID používateľa ako string,
                      alebo HttpResponse s chybou 401, ak je token neplatný.
        """
        try:
            access_token_obj = AccessToken(request.data["access_token"])
        except:
            return HttpResponse('Unauthorized', status=401)
        user_id=access_token_obj['user_id']
        return Response(str(user_id))


class NewQuestion(APIView):
    """
    API endpoint pre vytvorenie novej otázky.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na vytvorenie novej otázky.

        Očakáva dáta novej otázky v tele požiadavky vrátane `created_by` (ID používateľa)
        a `okruh` (ID okruhu). Vytvorí nový objekt `Question` a uloží ho.

        Args:
            request (Request): Objekt HTTP požiadavky s dátami otázky.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Odpoveď obsahujúca ID novovytvorenej otázky.
        """
        user = User.objects.filter(id=request.data["created_by"])
        okruh = Okruh.objects.filter(id=request.data["okruh"])
        newQuestion=Question.objects.create(name=request.data["name"],text=request.data["text"],approved=request.data["approved"],visible=request.data["visible"],created_by=user[0],is_text_question=request.data["is_text_question"],likes=0,okruh=okruh[0])
        print(newQuestion.id)
        return Response(newQuestion.id)


class NewComment(APIView):
    """
    API endpoint pre vytvorenie nového komentára.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na vytvorenie nového komentára.

        Očakáva dáta nového komentára v tele požiadavky vrátane `user_id` (ID používateľa),
        `text` komentára a `question_id` (ID otázky). Vytvorí nový objekt `Comment`.

        Args:
            request (Request): Objekt HTTP požiadavky s dátami komentára.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            HttpResponse: HTTP odpoveď so statusom 200 pri úspešnom vytvorení.
        """
        user = User.objects.filter(id=request.data["user_id"])
        text = request.data["text"]
        question = Question.objects.filter(id=request.data["question_id"])
        comment = Comment.objects.create(text=text,created_by=user[0],question=question[0])
        return HttpResponse(200)


class ScoreEntry(APIView):
    """
    API endpoint pre pridanie alebo aktualizáciu záznamu skóre používateľa v kurze.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na vytvorenie alebo aktualizáciu skóre.

        Očakáva `user_id`, `courseID` a `point` v tele požiadavky.
        Ak záznam pre daného používateľa a kurz už existuje, aktualizuje jeho body.
        Inak vytvorí nový záznam o skóre.

        Args:
            request (Request): Objekt HTTP požiadavky s dátami skóre.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Odpoveď so statusom 200 pri úspešnom spracovaní.
        """
        user = User.objects.filter(id=request.data["user_id"])
        course = Course.objects.filter(id=request.data["courseID"])
        points =request.data["point"]
        querry = Score.objects.filter(course=request.data["courseID"],user=request.data["user_id"])
        if not querry:
            score = Score.objects.create(user=user[0],course=course[0],points=points)
        else:
            for score in querry:
                score.points=points
                score.save()
        return Response(status=200)


class NewAnswers(APIView):
    """
    API endpoint pre pridanie viacerých nových odpovedí k jednej otázke.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na vytvorenie viacerých nových odpovedí.

        Očakáva zoznam dát odpovedí v tele požiadavky (`request.data`).
        Každá položka v zozname by mala obsahovať `question` (ID otázky,
        stačí v prvej položke), `text` odpovede a `answer_type`.
        Vytvorí nové objekty `Answer` pre každú položku.

        Args:
            request (Request): Objekt HTTP požiadavky so zoznamom dát odpovedí.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            HttpResponse: HTTP odpoveď so statusom 200 pri úspešnom vytvorení.
        """
        question=Question.objects.filter(id=request.data[0]["question"])
        for answer in request.data:
            new_answer = Answer.objects.create(text=answer["text"],answer_type=answer["answer_type"],question=question[0])
        return HttpResponse(200)


class UserForID(generics.ListCreateAPIView):
    """
    API endpoint pre získanie (a potenciálne vytvorenie) používateľa podľa ID.

    - GET: Vráti používateľa filtrovaného podľa `user_id`.
    - POST: Umožní vytvoriť nového používateľa.
    """
    model = User
    serializer_class = UserSerializer
    def get_queryset(self):
        """
        Vráti queryset používateľov filtrovaný podľa `user_id`.

        Metóda načíta `user_id` z query parametrov. Ak je `user_id` poskytnuté,
        pokúsi sa získať používateľa s daným ID.
        Poznámka: `User.objects.get()` vráti jeden objekt, nie queryset, čo môže byť
        neočakávané pre `ListCreateAPIView`, ak nie je správne ošetrené v serializéri
        alebo ak sa očakáva zoznam.

        Returns:
            User: Objekt používateľa, ak je `user_id` nájdené.
                  Správanie, ak `user_id` nie je nájdené, závisí od `User.objects.get()`.
        """
        user = User.objects.get(id=self.request.query_params.get('user_id'))
        return user


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint pre registráciu nového používateľa.

    Umožňuje komukoľvek (povolenie `AllowAny`) vytvoriť nový používateľský účet
    prostredníctvom POST požiadavky s registračnými dátami.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserForID(generics.ListCreateAPIView): 
    """
    API endpoint pre získanie zoznamu používateľov filtrovaných podľa ID
    a pre pridanie nového používateľa.

    - GET: Vráti zoznam používateľov (zvyčajne jedného) filtrovaných podľa `user_id`.
    - POST: Umožní vytvoriť nového používateľa.
    """
    Model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Vráti queryset používateľov filtrovaných podľa `userID`.

        Ak je parameter `userID` prítomný v query parametroch požiadavky,
        queryset je filtrovaný tak, aby obsahoval iba používateľov s daným ID.
        Inak vráti všetkých používateľov.

        Returns:
            QuerySet: Django QuerySet obsahujúci filtrovaných používateľov.
        """
        queryset= User.objects.all()
        userID = self.request.query_params.get('user_id')
        if userID:
            queryset = queryset.filter(id=userID)
        return queryset


def HomeView(request):
    """
    Jednoduchý view, ktorý vráti uvítaciu správu pre backend aplikácie.

    Args:
        request (HttpRequest): Objekt HTTP požiadavky.

    Returns:
        HttpResponse: HTTP odpoveď s textom "Vytaj na backende aplikacie Gamifikace".
    """
    return HttpResponse("Vytaj na backende aplikacie Gamifikace")


class LogoutView(APIView):
    """
    API endpoint pre odhlásenie používateľa.

    Vyžaduje, aby bol používateľ autentifikovaný.
    Pri POST požiadavke očakáva `refresh_token` v tele, ktorý bude pridaný na blacklist.
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        Spracuje POST požiadavku na odhlásenie používateľa.

        Načíta `refresh_token` z tela požiadavky, vytvorí z neho objekt
        `RefreshToken` a pridá ho na blacklist, čím ho zneplatní.

        Args:
            request (Request): Objekt HTTP požiadavky.

        Returns:
            Response: Odpoveď so statusom 205 (Reset Content) pri úspešnom odhlásení,
                      alebo so statusom 400 (Bad Request) v prípade chyby.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddUserToCourse(APIView):
    """
    API endpoint pre pridanie používateľa do kurzu.
    """
    def post(self, request, format=None):
        """
        Spracuje POST požiadavku na pridanie používateľa do kurzu.

        Očakáva `userID` a `courseID` v tele požiadavky. Validuje vstupy,
        načíta príslušný kurz a používateľa, skontroluje, či používateľ už nie je
        v kurze, a ak nie, pridá ho.

        Args:
            request (Request): Objekt HTTP požiadavky.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Správa o úspechu alebo chybe s príslušným HTTP status kódom.
        """
        user_id = request.data.get("userID")
        course_id = request.data.get("courseID")

        # Validácia používateľa a kurzu
        if not user_id or not course_id:
            return Response({"message": "userID and courseID are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Načítanie kurzu z databázy
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        # Kontrola, či používateľ už navštevuje kurz
        if course.visited_by.filter(id=user_id).exists():
            return Response({"message": "User is already enrolled in the course."}, status=status.HTTP_400_BAD_REQUEST)

        # Pridanie používateľa do kurzu
        course.visited_by.add(user_id)
        return Response({"message": "User added to the course."}, status=status.HTTP_200_OK)


class RemoveUserFomCourse(APIView):
    """
    API endpoint pre odstránenie používateľa z kurzu.
    """
    def post(self,request, format=None):
        """
        Spracuje POST požiadavku na odstránenie používateľa z kurzu.

        Očakáva `userID` a `courseID` v tele požiadavky. Validuje vstupy,
        načíta príslušný kurz, skontroluje, či používateľ kurz navštevuje,
        a ak áno, odstráni ho.

        Args:
            request (Request): Objekt HTTP požiadavky.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Správa o úspechu alebo chybe s príslušným HTTP status kódom.
        """
        user_id = request.data.get("userID")
        course_id = request.data.get("courseID")

        #Validacia pouzivatela a kurzu
        if not user_id or not course_id:
            return Response({"message": "userID and courseID are required."}, status=status.HTTP_400_BAD_REQUEST)
        #Nacitanie kurzu z databaze
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        #Kontrola ci uzivatel navstevuje kurz
        if course.visited_by.filter(id=user_id).exists():
            course.visited_by.remove(user_id)
            return Response({"message": "User removed from course."}, status=status.HTTP_200_OK) # Malo by byť status.HTTP_200_OK
        else:
            return Response({"message": "User not found in course."},status=status.HTTP_404_NOT_FOUND)


class CoursesForUSer(generics.ListCreateAPIView):
    """
    API endpoint pre získanie zoznamu kurzov pre špecifického používateľa
    a pre pridanie nového kurzu.

    - GET: Vráti zoznam kurzov, ktoré navštevuje daný používateľ (`user_id`).
    - POST: Umožní vytvoriť nový kurz.
    """
    Model = Course
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Vráti zoznam kurzov, ktoré navštevuje špecifikovaný používateľ.

        Načíta `user_id` z query parametrov. Iteruje cez všetky kurzy a pre každý
        kurz iteruje cez všetkých používateľov, ktorí ho navštevujú. Ak nájde
        zhodu s poskytnutým `user_id`, pridá kurz do výsledného zoznamu.

        Returns:
            list: Zoznam objektov `Course`, ktoré navštevuje daný používateľ.
        """
        queryset= Course.objects.all()
        queryset2 = []
        userID = self.request.query_params.get('user_id')
        print(userID)
        found = False
        for course in queryset:
            visited_by = course.visited_by
            for user in visited_by.all():
                if userID == str(user.id):
                    print(userID)
                    found = True
            if found:
                queryset2.append(course)
            found = False
        return queryset2


class CompleteLecture(APIView):
    """
    API endpoint pre označenie okruhu (prednášky) ako dokončeného pre prihláseného používateľa.

    Vyžaduje JWT autentifikáciu a ID okruhu v URL.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, okruh_id):
        """
        Označí špecifikovaný okruh ako dokončený pre aktuálne prihláseného používateľa.

        Načíta okruh podľa `okruh_id`. Skontroluje, či používateľ už okruh nedokončil.
        Ak nie, pridá používateľa do zoznamu `finished_by` pre daný okruh.

        Args:
            request (Request): Objekt HTTP požiadavky.
            okruh_id: ID okruhu, ktorý má byť označený ako dokončený.

        Returns:
            Response: Správa o úspechu alebo chybe s príslušným HTTP status kódom.
        """
        okruh = get_object_or_404(Okruh, id=okruh_id)

        # Skontroluje, či používateľ už dokončil okruh
        if request.user in okruh.finished_by.all():
            return Response({'status': 'error', 'message': 'Already marked as completed.'}, status=400)

        # Označí okruh ako dokončený pre používateľa
        okruh.finished_by.add(request.user)
        return Response({'status': 'success', 'message': f'Okruh {okruh.name} marked as completed.'}, status=200)


class AchievementView(APIView):
    """
    API endpoint pre získanie achievementov (úspechov) pre používateľa.
    """
    def get(self, request, user_id):
        """
        Vráti achievementy pre používateľa na základe jeho ID

        Args:
            request (Request): Objekt HTTP požiadavky.
            user_id: ID používateľa, pre ktorého sa majú získať achievementy.

        Returns:
            Response: Serializované dáta achievementov používateľa so statusom 200,
                      alebo 404 ak používateľ neexistuje.
        """
        user = get_object_or_404(User, id=user_id)
        achievements = Achievement.objects.filter(awarded_to=user)
        serializer = AchievementSerializer(achievements, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCourseCompletionView(APIView):
    """
    API endpoint, ktorý vráti percento dokončenia kurzov pre prihláseného používateľa.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Vypočíta a vráti zoznam kurzov s percentuálnym dokončením pre aktuálneho používateľa.

        Pre každý kurz v systéme vypočíta percento okruhov, ktoré prihlásený
        používateľ dokončil.

        Args:
            request (Request): Objekt HTTP požiadavky.

        Returns:
            Response: JSON so zoznamom kurzov a ich percentuálnym dokončením.
        """
        user = request.user
        course_completion_data = []

        courses = Course.objects.all()

        for course in courses:
            total_okruhs = Okruh.objects.filter(course=course).count()
            completed_okruhs = Okruh.objects.filter(course=course, finished_by=user).count()

            completion_percentage = (
                (completed_okruhs / total_okruhs) * 100 if total_okruhs > 0 else 0
            )

            course_completion_data.append({
                "course": course.name,
                "completion_percentage": round(completion_percentage, 2)
            })

        return Response(course_completion_data)


class ReportQuestion(APIView):
    """
    API endpoint, ktorý umožňuje nahlásiť otázku.
    """
    def patch(self,request, format=None):
        """
        Nahlási otázku podľa jej ID. Nastaví jej stav `reported=True` a `approved=False`.

        Parameters:
            request (Request): Obsahuje `questionID` v tele requestu.
            format (str, optional): Formát odpovede. Defaults to None.

        Returns:
            Response: Správa o úspešnosti alebo chybe.
        """
        question_id = request.data.get("questionID")
        if not question_id:
            return Response({"error": "questionID je povinné"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Otázka nenájdená"}, status=status.HTTP_404_NOT_FOUND)
        question.reported = True
        question.approved = False
        question.save()
        return Response({"message": "Otázka úspešne nahlásená."}, status=status.HTTP_200_OK)


class UpdateAIContextView(APIView):
    """
    API endpoint pre aktualizáciu hodnoty `ai_context` otázky.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] # Overenie, že používateľ je prihlásený

    def patch(self, request, question_id):
        """
        Aktualizuje `ai_context` pre otázku podľa jej ID.

        Parameters:
            request (Request): Obsahuje nový `ai_context` v tele requestu.
            question_id (UUID): ID otázky.

        Returns:
            Response: Aktualizovaná otázka alebo chybové hlásenie.
        """
        try:

            question = Question.objects.get(id=question_id)
            ai_context = request.data.get('ai_context')
            if not ai_context:
                return Response({"error": "ai_context je povinný parameter."}, status=status.HTTP_400_BAD_REQUEST)
            question.ai_context = ai_context
            question.save()
            return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)

        except Question.DoesNotExist:
            return Response({"error": "Otázka s týmto ID neexistuje."}, status=status.HTTP_404_NOT_FOUND)