from django.contrib import admin
from blog.models import Post, Category


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    empty_value_display = "-empty-"
    list_display = (
        "author",
        "title",
        "status",
        "created_date",
        "published_date",
    )


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
