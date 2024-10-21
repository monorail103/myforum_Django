from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from .utils import create_id
import re
import datetime
from .models import Thread, Post
from .forms import ThreadForm, PostForm

# スレ一覧を表示a66y77
def thread_list(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        # スレッドを作成
        if form.is_valid():
            ip_address = request.META.get('REMOTE_ADDR')

            thread, post = form.save(commit=True, ip_address=ip_address)
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ThreadForm()
    
    threads = Thread.objects.filter(is_archived=0).order_by('-created_at')
    thread_data = []

    # 表示用スレッドデータを作成
    for thread in threads:
        if thread.is_archived == 0:
            thread_data.append({
                'thread': thread,
                'post_count': thread.post_set.count(),
                'last_post': thread.post_set.last().created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': thread.user_id
            })
    cache.set('thread_data', thread_data, 60)
    return render(request, 'board/thread_list.html', {'form': form, 'thread_data': thread_data})

# スレ内を表示
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    # POSTメソッドの場合は新規投稿を受け付ける
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # 対象スレッド
            post.thread = thread
            post.created_at = datetime.datetime.now()

            ip_address = request.META.get('REMOTE_ADDR')
            # 投稿者のIPアドレス
            post.ip_address = ip_address
            # 日をまたいだら変わるIDを生成
            post.user_id = create_id(ip_address)
            post.save()

            if thread.post_set.count() >= 1000:
                thread.is_archived = 1
                thread.save()
            
            return redirect('thread_detail', pk=pk)
    else:
        # 過去ログの場合はスレッド一覧にリダイレクト
        if thread.is_archived != 1:
            form = PostForm()

    posts = thread.post_set.all() 

    post_data = []

    for i, post in enumerate(posts):
        # URLをリンクに変換
        post.content = re.sub(r'(https?://[a-zA-Z0-9.-]*)', r'<a href="\1">\1</a>', post.content)
        # >>1のようなレス番号をリンクに変換
        post.content = re.sub(r'>>(\d+)', r'<a href="#post-\1">>>\1</a>', post.content)
        # 投稿に付番したい
        post_data.append({
            'post': post,
            'post_number': i + 1,
            'user_id': post.user_id,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'content' : post.content
        })

    return render(request, 'board/thread_detail.html', {'form': form, 'thread': thread, 'post_data': post_data})

