from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Post


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
        posts_list = list(posts.values('id', 'title', 'text', 'publish_date'))
        return JsonResponse(posts_list, safe=False)
    else:
        try:
            data = json.loads(request.body)
            title = data.get('title')
            text = data.get('text')
            if not title or not text:
                return JsonResponse({'success': 'false', 'desc': f'title 和 text不能为空'}, status=400)
            
            post = Post.objects.create(
                title=title, text=text, author=request.user,
                publish_date=timezone.now()
            )
            return JsonResponse({'success': 'true', 'id': post.id, 'decs': f'已成功新建{post.pk}'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': 'false', 'desc': '无效的JSON'}, status=400)

@csrf_exempt    
@require_http_methods(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'success': 'false', 'desc': f'没有找到id为{pk}的文章'}, status=400)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': post.id, 'title': post.title,
            'text': post.text, 'publish_date': post.publish_date
        })
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            post.title = data.get('title', post.title)
            post.text = data.get('text', post.text)
            post.save()
            return JsonResponse({'success': 'true', 'desc': f'已更新 {post.id}'})
        except json.JSONDecodeError:
            return JsonResponse({'success': 'false', 'desc': '无效的JSON'}, status=400)
    elif request.method == 'DELETE':
        post.delete()
        return JsonResponse({'success': 'true', 'desc': f'已删除{pk}'}, status=204)