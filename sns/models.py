from django.db import models
from django.utils import timezone


#カテゴリ(1)
class Category(models.Model):

    # id(連番)
    name    = models.CharField(verbose_name="名前", max_length=100)
    icon    = models.ImageField(verbose_name="カテゴリアイコン",upload_to="sns/category/icon/")

    #TODO:ここにカテゴリのIDを文字列に直すモデルクラスのメソッドを追加する。
    def str_id(self):
        return str(self.id)

    def __str__(self):
        return self.name


#タグ(多)
class Tag(models.Model):

    #公園の特性(遊具がある、池があるなど)
    name    = models.CharField(verbose_name="名前", max_length=100)

    def __str__(self):
        return self.name

#公園(多)
class Park(models.Model):

    #id (連番)

    #このcategoryはCategoryのidが記録される。
    category    = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.PROTECT)

    #TODO:タグとのManyToManyFieldを作る
    #タグの未指定を許す場合、ここでblank=Trueを書く
    tag         = models.ManyToManyField(Tag,verbose_name="タグ",blank=True)

    name        = models.CharField(verbose_name="名前",max_length=100)
    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    lat         = models.DecimalField(verbose_name="緯度",max_digits=9, decimal_places=6)
    lon         = models.DecimalField(verbose_name="経度",max_digits=9, decimal_places=6)


    # 中間テーブルのモデルを使用する仕様に書き換え(throughを指定する。)
    #tag         = models.ManyToManyField(Tag,verbose_name="タグ",through="ParkTag",blank=True)


    def __str__(self):
        return self.name

#TODO:ここに中間テーブルを作る(タグ検索でAND検索をするため)←タグのAND検索は中間テーブルのモデルは不要
#https://noauto-nolife.com/post/django-m2m-through/
"""
class ParkTag(models.Model)

    park        = models.ForeignKey(Park,verbose_name="公園",on_delete=models.CASCADE)
    tag         = models.ForeignKey(Tag,verbose_name="タグ",on_delete=models.CASCADE)

    #ここに公園にタグが追加された日時を記録
"""





