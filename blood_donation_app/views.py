from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blood_donation_app.forms import UserForm, RequestForm
from blood_donation_app.models import Request, UserDisease, Disease, User
from blood_donation_app.serializers import ProfileSerializer, UserSerializer, RequestSerializer


class HomeView(LoginRequiredMixin, ListView):
    model = Request
    template_name = "index.html"
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(HomeView, self).get_queryset()
        queryset = queryset.select_related('requester').all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        requests = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(requests, self.paginate_by)
        try:
            requests = paginator.page(page)
        except PageNotAnInteger:
            requests = paginator.page(1)
        except EmptyPage:
            requests = paginator.page(paginator.num_pages)
        context['requests'] = requests
        return context


class SignUpView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['notifications'] = Request.objects.select_related('requester').filter(
            Q(required_blood_group=self.request.user.blood_group) & ~Q(requester__username=self.request.user.username))
        return context


class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'request/request-list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(RequestListView, self).get_queryset()
        queryset = queryset.select_related('requester').filter(requester=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)
        requests = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(requests, self.paginate_by)
        try:
            requests = paginator.page(page)
        except PageNotAnInteger:
            requests = paginator.page(1)
        except EmptyPage:
            requests = paginator.page(paginator.num_pages)
        context['requests'] = requests
        return context


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    template_name = 'request/request-create.html'
    success_url = reverse_lazy('request-list')
    form_class = RequestForm

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super(RequestCreateView, self).form_valid(form)


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'request/request-detail.html'
    context_object_name = 'requests'


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    template_name = 'request/request-update.html'
    context_object_name = 'request'
    fields = ('required_blood_group', 'deadline',)
    success_url = reverse_lazy('request-list')


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'request/request-delete.html'
    success_url = reverse_lazy('request-list')


class NotificationsView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'notifications.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(NotificationsView, self).get_queryset()
        queryset = queryset.select_related('requester').filter(
            Q(required_blood_group=self.request.user.blood_group) & ~Q(requester__username=self.request.user.username))
        return queryset


class UserDiseaseListView(LoginRequiredMixin, ListView):
    model = UserDisease
    template_name = 'user_disease/user-disease-list.html'
    context_object_name = 'diseases'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(UserDiseaseListView, self).get_queryset()
        queryset = queryset.select_related('user', 'disease').filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserDiseaseListView, self).get_context_data(**kwargs)
        requests = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(requests, self.paginate_by)
        try:
            requests = paginator.page(page)
        except PageNotAnInteger:
            requests = paginator.page(1)
        except EmptyPage:
            requests = paginator.page(paginator.num_pages)
        context['requests'] = requests
        return context


class UserDiseaseCreateView(LoginRequiredMixin, CreateView):
    model = UserDisease
    template_name = 'user_disease/user-disease-create.html'
    fields = ('disease', 'start_date', 'end_date')
    success_url = reverse_lazy('user-disease-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserDiseaseCreateView, self).form_valid(form)


class UserDiseaseDetailView(LoginRequiredMixin, DetailView):
    model = UserDisease
    template_name = 'user_disease/user-disease-detail.html'
    context_object_name = 'disease'


class UserDiseaseUpdateView(LoginRequiredMixin, UpdateView):
    model = UserDisease
    template_name = 'user_disease/user-disease-update.html'
    context_object_name = 'disease'
    fields = ('disease', 'start_date', 'end_date')
    success_url = reverse_lazy('user-disease-list')


class UserDiseaseDeleteView(LoginRequiredMixin, DeleteView):
    model = UserDisease
    template_name = 'user_disease/user-disease-delete.html'
    success_url = reverse_lazy('user-disease-list')


class DiseaseCreateView(LoginRequiredMixin, CreateView):
    model = Disease
    template_name = 'user_disease/disease-create.html'
    fields = ('name',)
    success_url = reverse_lazy('disease-create')


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist as error:
            return Response({'detail': error.args[0]}, status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist as error:
            return Response({'detail': error.args[0]}, status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super(RequestViewSet, self).get_queryset()
        queryset = queryset.filter(requester=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
