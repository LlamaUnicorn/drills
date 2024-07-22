# TODO use clickable urls

## Drill 1: api_view endpoint
# Create an endpoint for Person model using @api_view
# urls: views.list_people > views: @api_view(['GET'])

# sandbox/people/models.py
from django.models import models


class Person(models.Model):
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    title = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'People'


# sandbox/people/admin.py
# list_display Can be a list or a tuple
from django.contrib import admin
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['first', 'last', 'title']


# sanbox/people/serializers.py
from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
        class Meta:
            model = Person
            fields = ['id', 'first', 'last', 'title']


# sandbox/people/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer


@api_view(['GET'])
def list_people(request):
        people = Person.objects.all()
        serializer = PersonSerializer(people, many=True)
        content = {
                'people': serializer.data
        }

        return Response(content)


# sanbox/people/urls.py
from django.urls import path
from . import views


urlpatterns = [
        path('list_people/', views.list_people),
    ]


# sandbox/sandbox/settings.py
# ALLOWED_HOSTS
# INSTALLED_APPS

# sandbox/sandbox/urls.py
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
        path('admin/', admin.site.urls),
        path('people/', include('people.urls')),
]


# Part Two ViewSets
    # ViewSets allow you to get the REST methods: List, Retrieve, Create, Update, Update Partial, Delete
# Routers define all the URL mappings for ViewSets
# Get List
curl -s http://127.0.0.1:8000/artifacts/artifacts/ | python -m json.tool

# Get Detail
curl -s http://127.0.0.1:8000/artifacts/artifacts/1/ | python -m json.tool

# POST
curl -s -X POST -d 'name=Ark of the Covenant' -d 'shiny=True' http://127.0.0.1:8000/artifacts/artifacts/

# PUT
curl -s -X PUT -d 'name=Golden Idol' -d 'shiny=True' http://127.0.0.1:8000/artifacts/artifacts/1/

# PATCH
curl -s -X PATCH -d 'shiny=False' http://127.0.0.1:8000/artifacts/artifacts/1/

# DELETE
curl -s -X DELETE http://127.0.0.1:8000/artifacts/artifacts/1/

## Drill 2: ViewSets
# Create a ViewSet for Artifact model with the default_router.

# sandbox/artifacts/apps.py
class ArtifactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artifacts'


# sandbox/artifacts/models.py
from django.db import models


class Artifact(models.Model):
    name = CharField(max_length=100)
    shiny = BooleanField()


# sandbox/artifacts/admin.py
from django.contrib import admin

from .models import Artifact


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ('name', 'shiny')


# sandbox/artifacts/serializers.py
from rest_framework import serializers

from .models import Artifact


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = '__all__'
        

# sandbox/artifacts/views.py
from rest_framework import viewsets

from .models import Artifact
from .serializers import ArtifactSerializer


class ArtifactViewSet(viewsets.ModelViewSet):
    serializer_class = ArtifactSerializer

    def get_queryset(self):
         return Artifact.objects.all()


# sandbox/artifacts/urls.py
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'artifacts', views.ArtifactViewSet, 'artifact')

urlpatterns = [
        path('', include('router.urls')),
]


# sandbox/sandbox/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
        path('admin/', admin.site.urls),
        path('list_people/', include('people.urls')),
        path('artifacts/', include('artifacts.urls')),
]


# Drill 3: Setting up Web interface.
# Setting global renderers
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASS': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # degrades performance by downloading all possible choices. Good for debugging, disable on production
    ]
}


# Local renderer with a decorator
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_count_view(request, format=None):
    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)


# or within APIView set:
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserCountView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)


# browser
http://127.0.0.1:8000/artifacts/artifacts/

# edit entry
http://127.0.0.1:8000/artifacts/artifacts/1/


## Drill 4: Set up permissions

# create templates folder on the same level as the manage.py
mkdir
templates
mkdir
templates / registration

# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],

        LOGIN_REDIRECT_URL = '/books/library/'

# urls.py
path('accounts/', include('django.contrib.auth.urls')),

# templates/registration/login.html

< !-- templates / registration / login.html -->
< html >
  < base >
  < h2 > Login < / h2 >

                   < form
method = "post" >
         { % csrf_token %}
{{form.as_p}}
< input
type = "submit"
value = "login" >
        < / form >
            < / base >
                < / html >

# create 2 users

# Permissions part 2
python manage.py startapp books

# update installed apps

# update urls.py

path('books/', include('books.urls')),

# books/models.py
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    restricted = models.BooleanField()


# books/serializers.py
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# books/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, 'book')

urlpatterns = [
    path('', include(router.urls)),
    path('library/', views.library),
]

# books/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission

from .models import Book
from .serializers import BookSerializer


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsIndy(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.restricted:
            return True

        return request.user.username == "indy"


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # permission_classes = [IsAdminUser]
    # permission_classes = [IsSuperUser]
    # permission_classes = [IsIndy | IsSuperUser]

    def get_queryset(self):
        return Book.objects.all()
        # if self.request.user.is_staff:
        #    return Book.objects.all()

        # return Book.objects.filter(restricted=False)


@login_required
def library(request):
    output = f"""
        <html>
            <body>
                <h2>Library</h2>
                <p>{request.user.username}</p>
                <a href="/books/books/">Books API</a>
                <br/>
                <a href="/accounts/logout/">Logout</a>
            </body>
        </html>
    """
    return HttpResponse(output)


# make migrations

# http://127.0.0.1:8000/books/library/
# logout errors due to Django 5 rejecting GET during Logout. Downgrading to 4 solved the issue.


# Serializers
# create vehicles app and register it

# vehicles/models/tools.py
class Tool:
    def __init__(self, name, make):
        self.name = name
        self.make = make


# in order for tools to work init the tool
# vehicles/models/__init__.py
from .tools import Tool

# vehicles/serializers/tools.py
from rest_framework import serializers


class ToolSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    make = serializers.CharField(max_length=50)


# vehicle/views/tools.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

from vehicles.models import Tool
from vehicles.serializers.tools import ToolSerializer


@api_view(['GET'])
def list_tools(request):
    tools = [
        Tool('hammer', 'Mastercraft'),
        Tool('wrench', 'Husky'),
    ]

    serializer = ToolSerializer(tools, many=True)
    content = {
        'tools': serializer.data,
    }

    return Response(content)


# vehicle/urls.py

from django.urls import path

from .views import tools

urlpatterns = [
    path('list_tools/', tools.list_tools),
]

## Drill 5: Nested serializers

# vehicles/models/vehicles.py

from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=100)


class Part(models.Model):
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)


# vehicles/models/__init__.py
from .tools import Tool
from .vehicles import Vehicle, Part

# vehicles/serializers/vehicles.py
from rest_framework import serializers
from vehicles.models import Vehicle, Part


class SerialNumberField(serializers.Field):
    def to_representation(self, value):
        code = value.make[:3].upper()
        return f"{code}-{value.id}"


class PartSerializer(serializers.ModelSerializer):
    serial_no = SerialNumberField(source="*")

    class Meta:
        model = Part
        fields = ["url", "name", "vehicle", "serial_no"]


class VehicleSerializer(serializers.ModelSerializer):
    part_set = PartSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ["url", "name", "part_set"]


# vehicle/views/vehicles.py
from rest_framework import viewsets
from rest_framework.response import Response

from vehicles.models import Vehicle, Part
from vehicles.serializers.vehicles import VehicleSerializer, PartSerializer


class PartViewSet(viewsets.ModelViewSet):
    serializer_class = PartSerializer
    queryset = Part.objects.all()


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return Vehicle.objects.all()


# vehicles/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import tools, vehicles

router = DefaultRouter()
router.register(r"vehicles", vehicles.VehicleViewSet, "vehicle")
router.register(r"parts", vehicles.PartViewSet, "part")

urlpatterns = [
    path("", include(router.urls)),
    path("list_tools/", tools.list_tools),
]


## Drill 6: Nested complex serialization
# python manage.py startapp
# register in installed_apps
# include api.urls

# api/views.py
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from artifacts.models import Artifact
from people.models import Person
from vehicles.models import Vehicle
from people.serializers import PersonSerializer
from vehicles.serializers.vehicles import VehicleSerializer


@api_view(["GET"])
def listing(request):
    doctors = Person.objects.filter(title="Dr.")
    vehicles = Vehicle.objects.all()

    context = {
        "request": request,
    }
    vehicle_serializer = VehicleSerializer(vehicles, many=True, context=context)

    results = {
        "doctors": PersonSerializer(doctors, many=True).data,
        "vehicles": vehicle_serializer.data,
    }

    return Response(results)


# apis/urls.py
# Without routers you won't get the discovery within the web api in the root listing
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path("v1/listing/", views.listing),
]


curl -s http://127.0.0.1:8000/api/v1/listing/ | python -m json.tool


# Add new viewset
# api/views.py
class DoctorsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    def list(self, request):
        doctors = Person.objects.filter(title="Dr.")
        results = {
            "doctors": PersonSerializer(doctors, many=True).data,
        }

        return Response(results)


# updated api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"doctors", views.DoctorsViewSet, "doctor")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/listing/", views.listing),
]


# custom mass delete action api/views.py
class MassDeleteArtifactsViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    @action(detail=False, methods=["delete"])
    def mass_delete(self, request, pk=None):
        for artifact_id in request.POST["ids"].split(","):
            Artifact.objects.get(id=artifact_id).delete()

        return Response()


# updated urls.py
# apis/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"doctors", views.DoctorsViewSet, "doctor")
router.register(r"mass_delete", views.MassDeleteArtifactsViewSet, "mass_delete")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/listing/", views.listing),
]

