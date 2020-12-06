from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.slug


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)
    draft = models.BooleanField(_("Draft"), default=True, db_index=True)
    image = models.ImageField(_("Image"), upload_to='media/images')
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), related_name='posts', related_query_name='children',
                               on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['publish_time']

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']

    def __str__(self):
        return self.author.name+','+self.post


class CommentLike(models.Model):
    status = models.BooleanField(_("Status"), null=True, blank=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name=_("Comment"), related_name="comment_like",
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = [["user", "comment"]]
        verbose_name = _("Comment_Like")
        verbose_name_plural = _("Comment_Likes")

    def __str__(self):
        return str(self.status)


class PostLike(models.Model):
    status = models.BinaryField(_("Status"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Post_Like")
        verbose_name_plural = _("Post_Likes")

    def __str__(self):
        return self.updated_at


class PostSetting(models.Model):
    show_author_name = models.BooleanField(_("Show Author Name"), null=False, blank=False)
    show_publish_date = models.BooleanField(_("Show Publish Date"), null=False, blank=False)
    allow_discussion = models.BooleanField(_("Allow Discussion"), null=False, blank=False)
    save_draft = models.BooleanField(_("Save Draft"), null=False, blank=False)
    post = models.OneToOneField("Post", verbose_name=_("media"),related_name="post_setting",related_query_name="post_setting", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Post_Setting")
        verbose_name_plural = _("Post_settings")

    def __str__(self):
        return str(self.show_author_name) + "," + str(self.show_publish_date) + "," + str(
            self.allow_discussion) + "," + str(self.save_draft)