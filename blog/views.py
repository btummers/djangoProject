import urllib.parse

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, BadHeaderError
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import ListView
from .forms import PostCreateForm
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.edit import UpdateView

from .forms import RegisterForm

import requests


def post_list(request):
    sorting = request.GET.get('s', None)

    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    )

    if sorting:
        posts = posts.order_by(sorting)
    else:
        posts = posts.order_by('-published_date', '-pk')

    subject_id = request.GET.get('subject_id', '')

    resp = requests.get(f'https://tst-rugtc.poweredbymentor.nl/api/modules_api/catalog/?subject_id={subject_id}')
    thema = requests.get('https://tst-rugtc.poweredbymentor.nl/api/modules_api/subjects/')

    try:
        mentor_data = resp.json()
        thema_data = thema.json()
    except:
        mentor_data = []
        thema_data = []
    # print(resp.json())

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'mentor_data': mentor_data,
        'themas': thema_data,
        'parameters': urllib.parse.urlencode(request.GET)
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# def my_django_view(request):
#     if request.method == 'POST':
#         r = requests.post('https://www.somedomain.com/some/url/save', params=request.POST)
#     else:
#         r = requests.get('https://www.somedomain.com/some/url/save', params=request.GET)
#     if r.status_code == 200:
#         return HttpResponse('Yay, it worked')
#     return HttpResponse('Could not save data')

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    # image = CreateView.ImageField(upload_to='images/')
    success_url = reverse_lazy("post_list")

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.user = self.request.user
    #     obj.save
    #     return HttpResponseRedirect(self.success_url)
    def get_initial(self):
        initial = super(PostCreateView, self).get_initial()
        if self.request.user.is_authenticated:
            initial.update({'author': self.request.user})
        return initial


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('pk')
        return context

    def post(self, request, *args, **kwargs):
        return super(PostUpdateView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return super(PostUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        return super(PostUpdateView, self).form_valid(form)


class ApiView(View):
    template_name = 'blog/api.html'
    success_url = reverse_lazy('blog-list')

    def get(self, request, *args, **kwargs):

        cursus_id = self.kwargs.get('cursus_id')
        try:
            resp = requests.get(f'https://tst-rugtc.poweredbymentor.nl/api/modules_api/catalog/{cursus_id}/')
            resp = resp.json()
        except:
            resp = []

        context = {'hallo': '',
                   'cursus': resp}

        return render(request, self.template_name, context)


class TestView(ListView):
    model = Post
    template_name = 'blog/test.html'
    success_url = reverse_lazy('post_list')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="passwords/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # import pdb;pdb.set_trace() n = volgende c = doorlopen l = zien waar je bent
            user = form.save(commit=False)
            user.username = user.username.lower()

            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'registration/register.html', {'form': form})
