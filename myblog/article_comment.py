from myblog.models import *
from django.db.models import Count


def article_comment():
    article_list = Article.objects.all()
    comment_list = Comment.objects.values('article').annotate(comment_count=Count('article'))
    new_list = []
    t_list = []
    co_list = []
    for co in comment_list:
        title = Article.objects.filter(pk=co['article']).values('title')
        for t in title:
            t1 = t['title']
            count_comment = co['comment_count']
            co_list.append({'title': t1, 'count_comment': count_comment})
            t_list.append(t1)
    for article in article_list:
        if article.title not in t_list:
            new_list.append({'title': article.title, 'count_comment': 0})
        else:
            for co in co_list:
                if article.title == co['title']:
                    new_list.append({'title': article.title, 'count_comment': co['count_comment']})
    return new_list