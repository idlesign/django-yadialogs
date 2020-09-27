from django.urls import path, include


urlpatterns = [
    path('dialogs/', include('yadialogs.urls'))
]
