from django.urls import path

from blood_donation_app.views import HomeView, SignUpView, UserProfileView, AllRequestListView, RequestListView, \
    RequestCreateView, RequestDetailView, RequestUpdateView, RequestDeleteView, NotificationsView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('request/', AllRequestListView.as_view(), name='all-request-list'),
    path('request/list/', RequestListView.as_view(), name='request-list'),
    path('request/create/', RequestCreateView.as_view(), name='request-create'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('request/<int:pk>/update/', RequestUpdateView.as_view(), name='request-update'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name='request-delete'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
]
