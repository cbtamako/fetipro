# encoding=utf-8

from django.db import models



class Feti(models.Model):

    class Meta:
        verbose_name = "フェチ"
        verbose_name_plural = "フェチ"
        ordering = ("ordering", "id")

    ordering = models.IntegerField("表示順", default=100)
    created_at = models.DateTimeField("新規登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    slug = models.SlugField("スラッグ", max_length=50, unique=True)
    name = models.CharField("名称", max_length=100, unique=True)
    parent = models.ForeignKey("self", related_name="children", blank=True, null=True)
    icon = models.ImageField("アイコン", blank=True)

    class Status(object):
        Unauthorided = 0
        Authorized = 1
        Ignored = -1

    STATUS_CHOICES = (
                      (Status.Unauthorided, "未確認"),
                      (Status.Authorized, "OK"),
                      (Status.Ignored, "拒否")
                      )
    status = models.IntegerField("状態", choices=STATUS_CHOICES, default=Status.Unauthorided)

    created_by = models.ForeignKey("user.User", blank=True, null=True, related_name="+")
    authorized_by = models.ForeignKey("user.User", blank=True, null=True, related_name="+")

    def __str__(self):
        return self.name







