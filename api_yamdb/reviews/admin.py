from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Genre, Title, GenreTitle, Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'is_active')
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
