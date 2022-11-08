from django.urls import path
from knox import views as knox_views

from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register("user", views.UserViewSet, basename='user')
router.register("client", views.ClientViewSet, basename='client')
router.register("project", views.ProjectViewSet, basename='project')

urlpatterns = router.urls + [
    path("login/", views.LoginAPI.as_view(), name='login'),
    path("logout/",knox_views.LogoutView.as_view(), name='logout'),
    path('client/<int:id>/project/', views.ClientViewSet.as_view({"post": "project_post"})),
]