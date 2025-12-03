from django.contrib import admin
from django.template.response import TemplateResponse
from .models import Blog, Category, Comment
import json
from assignments.models import About,SocialLink

# ------------- Custom AdminSite -------------
class MyAdminSite(admin.AdminSite):
    site_header = "My Dashboard Admin"
    change_list_template = "admin/index.html"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Prepare chart data
        categories = Category.objects.all()
        labels = [cat.category_name for cat in categories]
        data = [Blog.objects.filter(category=cat).count() for cat in categories]

        extra_context['chart_labels'] = json.dumps(labels)
        extra_context['chart_data'] = json.dumps(data)
          # <-- Add this

        extra_context['total_blogs'] = Blog.objects.count()
        extra_context['total_categories'] = Category.objects.count()
        extra_context['total_comments'] = Comment.objects.count()


        # Call parent index to include default context (app_list, log_entries, etc.)
        return super().index(request, extra_context=extra_context)

# Create custom admin instance
my_admin_site = MyAdminSite(name='myadmin')

# ------------- BlogAdmin -------------
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured',)

# Register models
my_admin_site.register(Category)
my_admin_site.register(Blog, BlogAdmin)
my_admin_site.register(Comment)
my_admin_site.register(About)
my_admin_site.register(SocialLink)
