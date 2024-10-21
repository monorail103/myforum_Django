from django.db import models

# Create your models here.
class Thread(models.Model):
    # スレタイ
    title = models.CharField(max_length=100)
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 個人を識別するためのID
    user_id = models.CharField(max_length=100, null=True)
    # 過去ログかどうか
    is_archived = models.BooleanField(default=False)
    # IPアドレス
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    # タイムスタンプ
    timestamp = models.DateTimeField(auto_now_add=True)

    # 表示するときにタイトルを返す
    def __str__(self):
        return self.title

class Post(models.Model):
    # どのスレに対する投稿か
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    # 投稿者名前
    author = models.CharField(max_length=100, default='nnssdsd')
    # mail
    mail = models.EmailField(null=True, blank=True)
    # 表示用日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 投稿本文
    content = models.TextField()
    # 個人を識別するためのID
    user_id = models.CharField(max_length=100, null=True)
    # タイムスタンプ
    timestamp = models.DateTimeField(auto_now_add=True)
    # 投稿者のIPアドレス
    ip_address = models.GenericIPAddressField(null=True, blank=True)


    # 表示するときにタイトルを返す
    def __str__(self):
        return f'{self.author}: {self.content[:30]}'