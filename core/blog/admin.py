from django.contrib import admin
from blog.models import Post,Category

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    empty_value_display = '-empty-'
    fields = ('author','image','title','content','category','published_date')
    list_display = ('author','title','content')


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)