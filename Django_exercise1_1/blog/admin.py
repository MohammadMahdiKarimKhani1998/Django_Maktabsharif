from django.contrib import admin
from .models import Post, Category, Comment, PostSetting, CommentLike
from django.utils.translation import ngettext
from django.contrib import messages


class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = ("title", "slug")
    extra = 1
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "parent")
    search_fields = ("slug", "title")
    list_filter = ("parent",)
    inlines = [ChildrenItemInline, ]


class PostSettingAdmin(admin.StackedInline):
    model = PostSetting


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at", "created_at", "category", "author", "draft")
    search_fields = ("title",)
    list_filter = ("author", "category")
    date_hierarchy = "publish_time"
    list_editable = ("draft",)

    def make_draft(self, request, queryset):
        updated = queryset.update(draft=True)
        self.message_user(request, ngettext(
            '%d story was successfully marked as drafted.',
            '%d stories were successfully marked as drafted.',
            updated,
        ) % updated, messages.SUCCESS)

    make_draft.short_description = "True draft"
    inlines = [PostSettingAdmin]
    actions = [make_draft]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at", "updated_at")
    search_fields = ("author",)
    list_filter = ("author", "updated_at")
    date_hierarchy = "updated_at"


admin.site.register(Category, CategoryAdmin)
admin.site.register(CommentLike)
