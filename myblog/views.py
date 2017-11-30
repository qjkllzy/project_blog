from django.shortcuts import render,redirect
from myblog.models import *
from django.db.models import Count
from myblog.article_comment import article_comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from django.contrib.auth.hashers import make_password
from myblog.forms import *
from django.contrib.auth import  login,logout, authenticate
from django.http import HttpResponse
import time

# Create your views here.
def global_settings(request):
    Cate_list = Category.objects.all()
    LLlist=Article.objects.all().order_by('-click_count')[:6]
    PLlist = Comment.objects.values('article').annotate(PLcount=Count('article')).order_by(
        '-PLcount')
    article_PLlist = [Article.objects.get(pk=comment['article']) for comment in PLlist]
    TJlist=Article.objects.filter(is_recommend='1')[:6]
    def result_date():
        result_date_list = []
        date_list = Article.objects.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m')
            if date not in result_date_list:
                result_date_list.append(date)
        return result_date_list
    result_date_list=result_date()
    return locals()

def getPage(request, article_list):
    paginator = Paginator(article_list, 8)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

def index(request):
    article_hascomment=article_comment()
    newest_list=getPage(request,article_hascomment)
    return render(request,'index.html',locals())

def category(request):
    cid=request.GET.get('cid',None)
    category=Category.objects.get(pk=cid)
    article_list=Article.objects.filter(category=category)
    article_hascomment=article_comment()
    last_list=[]
    for art in article_list:
        for t1 in article_hascomment:
            if t1['title']==art.title:
                last_list.append({'title':art.title,'count_comment':t1['count_comment']})
    newest_list=getPage(request,last_list)
    return render(request,'category.html',locals())


def article_xq(request):
    title=request.GET.get('title',None)
    article=Article.objects.filter(title=title)
    comments=Comment.objects.filter(article=article)
    comment_list=[]
    for comment in comments:
        for com in comment_list:
            if not hasattr(com,'children_comment'):
                setattr(com,'children_comment',[])
            if comment.pid==com:
                com.children_comment.append(comment)
        if comment.pid is None:
            comment_list.append(comment)


        #     return render(request, 'article_xq.html', locals())
        # else:
        #     return HttpResponse("内容不能为空!")

    # for art in article:
    #     if '<img src' in art.content:
    #         import re,os,shutil
    #         from django.conf import settings
    #         # regName=re.compile(r'.*?<img\ssrc="/uploads/kindeditor/\d+/\d+/(.*?)"')
    #         regPath = re.compile(r'.*?<img\ssrc="(.*?)"')
    #         # ImgNameList=regName.findall(art.content)
    #         regName=re.compile(r'/uploads/kindeditor/\d+/\d+/(.*?)')
    #         ppath_list = regPath.findall(art.content)
    #
    #         jpath = os.path.join(settings.BASE_DIR, 'myblog\static')
    #         path=os.path.join(jpath,'uploads')
    #         if not os.path.exists(path):
    #             os.makedirs(path)
    #         for ppath in ppath_list:
    #             imgName=ppath.replace(regName.search(ppath).group(0),'')
    #             newppath = ppath.replace('/', '\\')
    #             ImgPath=settings.BASE_DIR+newppath
    #             shutil.copy(ImgPath,path)
                # art.content=art.content.replace('img src="%s"'%ppath,'img src="{%% static \'uploads/%s \'%%}"'%imgName)
            # jpath=os.path.join(settings.BASE_DIR,'myblog\static')
            # path=os.path.join(jpath,'uploads')
            # if not os.path.exists(path):
            #     os.makedirs(path)
            # newppath=ppath.replace('/','\\')
            # ImgPath=settings.BASE_DIR+newppath
           # shutil.copy(ImgPath,path)
    return render(request,'article_xq.html',locals())

def wendang(request):
    date=request.GET.get('date')
    date_list=Article.objects.values('title','date_publish')
    last_list=[]
    for d in date_list:
        if str(d['date_publish'].year)+'/'+str(d['date_publish'].month)==date:
            last_list.append(d)
    return render(request,'wendang.html',locals())

def write_comment(request):
    if request.method=='GET':
        if request.user.is_authenticated():
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    elif request.method == 'POST':
        content = request.POST.get('comment_text')
        id = request.POST.get('art_id')
        if content != '':
            Comment.objects.create(content=content, username=request.user.username, date_publish=time.time(),
                                   article_id=id)
    return redirect(request.META['HTTP_REFERER'])

def answer_comment(request):
    pid=request.POST.get('answer_id')
    id=request.POST.get('art_id')
    content=request.POST.get('answer')
    if content!='':
       Comment.objects.create(content=content,username=request.user.username,date_publish=time.time(),
                              article_id=id,pid_id=pid)
    return redirect(request.META['HTTP_REFERER'])

def zhuce(request):

    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            # 注册
            user = User.objects.create(username=reg_form.cleaned_data["username"],
                                email=reg_form.cleaned_data["email"],

                                password=make_password(reg_form.cleaned_data["password"]),)
            user.save()

            # 登录
            user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
            login(request, user)
            return redirect(request.POST.get('source_url'))
        else:
            return render(request, 'failure.html'), #{'reason': reg_form.errors})
    else:
        reg_form = RegForm()
    return render(request, 'zhuce.html', locals())

def denglu(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 登录
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
            else:
                return render(request, 'failure.html', {'reason': '登录验证失败'})
            return redirect(request.POST.get('source_url'))
        else:
            return render(request, 'failure.html', {'reason': login_form.errors})
    else:
        login_form = LoginForm()


        return render(request, 'denglu.html', locals())

def zhuxiao(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])