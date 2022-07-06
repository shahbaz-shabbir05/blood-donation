from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blood_donation_app.forms import UserForm
from blood_donation_app.models import Request, UserDisease


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "index.html"


class SignUpView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = "registration/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['notifications'] = Request.objects.select_related('requester').filter(
            Q(required_blood_group=self.request.user.blood_group) & ~Q(requester__username=self.request.user.username))
        return context


@method_decorator(login_required, name='dispatch')
class AllRequestListView(ListView):
    model = Request
    template_name = 'request/all-request-list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(AllRequestListView, self).get_queryset()
        queryset = queryset.select_related('requester').all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllRequestListView, self).get_context_data(**kwargs)
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


@method_decorator(login_required, name='dispatch')
class RequestListView(ListView):
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


@method_decorator(login_required, name='dispatch')
class RequestCreateView(CreateView):
    model = Request
    template_name = 'request/request-create.html'
    fields = ('required_blood_group', 'deadline',)
    success_url = reverse_lazy('all-request-list')

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super(RequestCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class RequestDetailView(DetailView):
    model = Request
    template_name = 'request/request-detail.html'
    context_object_name = 'request'


@method_decorator(login_required, name='dispatch')
class RequestUpdateView(UpdateView):
    model = Request
    template_name = 'request/request-update.html'
    context_object_name = 'request'
    fields = ('required_blood_group', 'deadline',)
    success_url = reverse_lazy('request-list')


@method_decorator(login_required, name='dispatch')
class RequestDeleteView(DeleteView):
    model = Request
    template_name = 'request/request-delete.html'
    success_url = reverse_lazy('all-request-list')


@method_decorator(login_required, name='dispatch')
class NotificationsView(ListView):
    model = Request
    template_name = 'notifications.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super(NotificationsView, self).get_queryset()
        queryset = queryset.select_related('requester').filter(
            Q(required_blood_group=self.request.user.blood_group) & ~Q(requester__username=self.request.user.username))
        return queryset


@method_decorator(login_required, name='dispatch')
class UserDiseaseListView(ListView):
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


@method_decorator(login_required, name='dispatch')
class UserDiseaseCreateView(CreateView):
    model = UserDisease
    template_name = 'user_disease/user-disease-create.html'
    fields = ('disease', 'start_date', 'end_date')
    success_url = reverse_lazy('user-disease-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserDiseaseCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserDiseaseDetailView(DetailView):
    model = UserDisease
    template_name = 'user_disease/user-disease-detail.html'
    context_object_name = 'disease'


@method_decorator(login_required, name='dispatch')
class UserDiseaseUpdateView(UpdateView):
    model = UserDisease
    template_name = 'user_disease/user-disease-update.html'
    context_object_name = 'disease'
    fields = ('disease', 'start_date', 'end_date')
    success_url = reverse_lazy('user-disease-list')


@method_decorator(login_required, name='dispatch')
class UserDiseaseDeleteView(DeleteView):
    model = UserDisease
    template_name = 'user_disease/user-disease-delete.html'
    success_url = reverse_lazy('user-disease-list')
