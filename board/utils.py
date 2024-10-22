
import hashlib
import datetime
import math
from django.utils import timezone

def create_id(ip_address):
    return hashlib.sha256((ip_address + str(datetime.date.today())).encode()).hexdigest()[:8]
def calculate_momentum(thread):
    # 勢いを計算するロジック（例：最後の投稿からの時間と投稿数に基づく）
    last_post = thread.post_set.last()
    if last_post:
        time_diff = (timezone.now() - last_post.created_at).total_seconds()
        post_count = thread.post_set.count()
        momentum = post_count / time_diff if time_diff > 0 else 0
        return momentum
    return 0

def get_momentum_label(momentum):
    points = math.floor(momentum * 1000)
    return points