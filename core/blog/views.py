from django.views.generic import TemplateView,RedirectView,ListView,DetailView,FormView,CreateView,UpdateView,DeleteView
from blog.models import Post
from blog.forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from accounts.models import Profile

# Create your views here.

# FBV for templateview
"""
def index_view(request):
    '''this is a function based view to show index view'''
    context = {"name":"ali"}
    return render(request,"blog/index.html",context)
"""

# CBV for TemolateView
class IndexView(TemplateView):
    """this is a class based view to show index view"""
    template_name = "blog/index.html"
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["name"] = "Mohammad"
        context["posts"] = Post.objects.all()
        return context

# FBV for redirectview
"""
def redirect_view(request):
    '''this is a function based views to show redirect view'''
    return redirect('https://google.com')
"""

# CBV for RedirectView
class RedirectView(RedirectView):
    """this is a class based view to show redirect view"""
    pattern_name = "blog:cbv-index"
    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)
    

# CBV for ListView
class PostListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    """this is a class based view for postslist"""
    permission_required = "blog.view_post"
    context_object_name = "posts"
    # model = Post
    queryset = Post.objects.filter(status=True)
    paginate_by = 2 
    ordering = "-published_date"
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts


# CBV for DetailView     
class DetalViewPost(LoginRequiredMixin,DetailView):
    """this is a class based view for postsdetails"""
    # model = Post
    queryset = Post.objects.filter(status=True)


# CBV for FormView
'''
class CreatePostView(FormView):
    """this is a class based view for creating posts"""
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = "/blog/posts/"
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)
'''

# CBV for CreateView
class CreatePostView(LoginRequiredMixin,CreateView):
    """this is a class based view for creating posts"""
    model = Post
    # fields = ["author","title","content","status"]
    form_class = PostForm
    success_url = "/blog/posts/"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# CBV for UpdateView
class UpdatePostView(LoginRequiredMixin,UpdateView):
    """this is a class based view for updating posts"""
    model = Post
    form_class = PostForm
    success_url = "/blog/posts/"

# CBV for DeleteView
class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = "/blog/posts/"

    
    
