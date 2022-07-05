from django.urls import path

from blood_donation_app.views import HomeView, SignUpView, UserProfileView, AllRequestListView, RequestListView, \
    RequestCreateView, RequestDetailView, RequestUpdateView, RequestDeleteView, NotificationsView, UserDiseaseListView, \
    UserDiseaseCreateView, UserDiseaseDetailView, UserDiseaseUpdateView, UserDiseaseDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('request/', AllRequestListView.as_view(), name='all-request-list'),
    path('request/list/', RequestListView.as_view(), name='request-list'),
    path('request/create/', RequestCreateView.as_view(), name='request-create'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('request/<int:pk>/update/', RequestUpdateView.as_view(), name='request-update'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name='request-delete'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('user/disease/list/', UserDiseaseListView.as_view(), name='user-disease-list'),
    path('user/disease/create/', UserDiseaseCreateView.as_view(), name='user-disease-create'),
    path('user/disease/<int:pk>/', UserDiseaseDetailView.as_view(), name='user-disease-detail'),
    path('user/disease/<int:pk>/update/', UserDiseaseUpdateView.as_view(), name='user-disease-update'),
    path('user/disease/<int:pk>/delete/', UserDiseaseDeleteView.as_view(), name='user-disease-delete'),
]
