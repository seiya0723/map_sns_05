from django.shortcuts import render,redirect
from django.views import View

from .models import Park,Category,Tag
from .forms import ParkForm,CategorySearchForm,TagSearchForm

from django.db.models import Q
from django.db.models import Count


class IndexView(View):


    #重複を除去する。(モデルオブジェクトから重複を取り除く)
    def distinct(self,obj):
        id_list     = [] # モデルオブエジェクトのidを記録する
        new_obj     = [] # 重複を除去した新しいモデルオブジェクトのリスト

        #モデルオブジェクトのリストから1つ取り出す。
        for o in obj:
            # idがid_listに含まれている場合
            if o.id in id_list:
                #次のループに行く(for文で使える構文、この命令を実行すると以降の処理はスキップして次のループに行く)
                continue

            #モデルオブジェクトのidを記録する
            id_list.append(o.id)
            #モデルオブジェクトを新しいリストに入れる
            new_obj.append(o)

        return new_obj

    def get(self, request, *args, **kwargs):

        context = {}
        context["categories"]   = Category.objects.all()
        context["tags"]         = Tag.objects.all()

        #TODO:ここで公園を検索するバリデーションを行う。

        #公園名の検索
        query   = Q()


        #パラメータの中にsearchがあるかどうかをチェック
        if "search" in request.GET:
            #searchを取り出す
            search      = request.GET["search"]

            raw_words   = search.replace("　"," ").split(" ")
            words       = [ w for w in raw_words if w != "" ]

            for w in words:
                query &= Q(name__contains=w)


        #カテゴリの検索
        form    = CategorySearchForm(request.GET)

        #カテゴリ検索を実現するには、入力値が数値であること、Categoryモデルに存在するidであることを確認する必要がある
        if form.is_valid():
            cleaned = form.clean()
            query &= Q(category=cleaned["category"].id)



        #多対多の検索
        form    = TagSearchForm(request.GET)

        if form.is_valid():
            cleaned         = form.clean()
            selected_tags   = cleaned["tag"] 
            

            """
            #タグ未指定による検索を除外する
            if selected_tags:
                # 指定したタグのいずれかを含む検索(重複あり)
                query &= Q(tag__in=selected_tags)
            """

            parks       = Park.objects.filter(query).order_by("-dt")

            #タグ検索をする(中間テーブル未使用、指定したタグを全て含む)
            for tag in selected_tags:
                new_parks   = []

                for park in parks:
                    if tag in park.tag.all():
                        new_parks.append(park)

                parks       = new_parks

            print(parks)

            """
            中間テーブルを使用する方法(概要)

            1、中間テーブルのモデルでタグ検索
            2、Parkモデルでqueryを使って検索
            3、1と2を突き合わせる

            このやり方ではかえって難しいため、今回はあえて見送った。
            今回のやり方はループを繰り返すだけで実現でき、distinctも不要なので更にシンプルに実現できる
            """

            context["parks"]    = parks
        else:

            #ここでループしてモデルオブジェクト比較し、重複除去をする。
            context["parks"]    = self.distinct( Park.objects.filter(query).order_by("-dt") )

        return render(request, "sns/index.html", context)

    def post(self, request, *args, **kwargs):

        form    = ParkForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("sns:index")

index   = IndexView.as_view()
