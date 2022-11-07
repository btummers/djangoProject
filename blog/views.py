from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from .forms import PostCreateForm
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.edit import UpdateView

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

    resp = requests.get('https://tst-rugtc.poweredbymentor.nl/api/modules_api/catalog/')
    # print(resp.json())

    return render(request, 'blog/post_list.html', {'posts': posts, 'mentor_data': resp.json(), 'range': range(1, 4)})


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
        return super(PostUpdateView, self).post( request, *args, **kwargs)

    def form_invalid(self, form):
        return super(PostUpdateView, self).form_invalid(form)
    def form_valid(self, form):
        return super(PostUpdateView, self).form_valid(form)


class ApiView(View):
    template_name = 'blog/api.html'
    success_url = reverse_lazy('blog-list')
    resp = requests.get('https://tst-rugtc.poweredbymentor.nl/api/modules_api/catalog/')

    def get(self, request, *args, **kwargs):
        context = {'hallo': '',
                   'mentor_data': self.resp.json()}

        return render(request, self.template_name, context)
