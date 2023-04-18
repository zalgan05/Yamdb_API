from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "date_joined",
    )
    list_editable = ("role",)
    search_fields = ("username",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Title)
