from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Blog, Category #Series
from .forms import BlogForm
# Create your views here.



###################### SERIES RELATED #####################
class SeriesCreate(LoginRequiredMixin, CreateView):
    model       =   Series
    fields      =   ['title']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class SeriesDetail(DetailView):
    model       =   Series


class BlogCreate(LoginRequiredMixin, CreateView):
    form_class  =   BlogForm
    template_name   =   "blog/blog_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    



class BlogList(ListView):
    model       =   Blog
    paginate_by =   15
    ordering    =   '-date_stamp'
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series'] = Series.objects.all()[:8]
        context['categories'] = Category.objects.all()[:10]
        return context


class BlogCategory(ListView):
    template_name   = "blog/blog_category.html"
    paginate_by     =   15
   

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return  Blog.objects.filter(category=self.category)


    def get_context_data(self, **kwargs):
        context = super(BlogCategory, self).get_context_data(**kwargs)
        context['category_list']  = Category.objects.all()
        return context


class BlogDetail(DetailView):
    model       =       Blog

    def get_object(self):
        obj = super(BlogDetail, self).get_object()
        obj.view +=1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        is_liked    = False
        is_disliked = False
        if obj.like.filter(id = self.request.user.pk).exists():
            is_liked = True
        if obj.dislike.filter(id = self.request.user.pk).exists():
            is_disliked = True

        context['is_liked']     = is_liked
        context['is_disliked']  = is_disliked
        return context




class BlogUpdate(UpdateView):
    model       =   Blog
    #form_class  =   BlogForm
    fields      =   ['title','content','category']

    def form_valid(self, form):
        form.instance.edited == True
        form.save()
        return super().form_valid(form)


def blogDelete(request, pk):
    blog    =   get_object_or_404(Blog, pk=pk)
    if blog.author == request.user or request.user.is_superuser:
        blog.delete()
        messages.success(request, f"Post Deleted")
        return redirect('blog_list')
    else:
        messages.warning(request, f"you don't have the permission for the operation!!!")
        return redirect(blog.get_absolute_url())

@login_required
def likeBlog(request, pk):
    obj = get_object_or_404(Blog, pk=pk)
    if obj.dislike.filter(id=request.user.id).exists():
        obj.dislike.remove(request.user.id)
        obj.like.add(request.user.id)
        #obj.author.points -= 1  # Reduce Authors Points by one if user dislikes the blog
    elif obj.like.filter(id=request.user.id).exists():
        obj.like.remove(request.user.id)
    else:
        obj.like.add(request.user.id)
        obj.author.points += 1  # Increase Authors Points by one if user likes the blog
    return redirect(obj.get_absolute_url())

def disLikeBlog(request, pk):
    obj = get_object_or_404(Blog, pk=pk)
    print(obj.author.points)
    if obj.like.filter(id=request.user.id).exists():
        obj.like.remove(request.user.id)
        obj.dislike.add(request.user.id)
    elif obj.dislike.filter(id=request.user.id).exists():
        obj.dislike.remove(request.user.id)
    else:
        obj.dislike.add(request.user.id)
    return redirect(obj.get_absolute_url())