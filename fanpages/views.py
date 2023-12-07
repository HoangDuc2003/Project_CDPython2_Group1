from django.shortcuts import render

# Create your views here.
def form_Fanpage(request):
    return render(request,'fanpage/form_fanpage.html')

def fanpage(request,page_id):
    custom_user = request.user
    fanpage = Fanpage.objects.get(id=page_id)
    posts = Post_Fanpage.objects.filter(fanpage=fanpage).order_by('-created_at')
    comments = CommentFanpage.objects.order_by('-created_at')
    reply_comment_post = ReplyCommentFanpage.objects.order_by('-created_at')
    for post_id in posts.all():
            post = posts.get(id=post_id.id)
            if custom_user in post.likes.all():
                post.liked = True
            else:
                post.liked = False
            post.save()
    context = {
         'user':custom_user,
         'fanpage':fanpage,
         'posts':posts,
         'comments':comments,
         'reply_comment_post':reply_comment_post,

         }
    return render(request,'fanpage/fanpage.html',context)

def create_fanpage(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
                author = request.user
                name = request.POST['name']
                description = request.POST['description']
                fanpage = Fanpage(author=author,name=name,description=description)
                if 'img_fanpage' in request.FILES:
                    fanpage.imgFanpage = request.FILES['img_fanpage']
                else:
                    fanpage.imgFanpage = 'fanpage/f1.webp'
                if 'img_cover_fanpage' in request.FILES:
                    fanpage.imgFanpageCover = request.FILES['img_cover_fanpage']
                fanpage.save()
                
        return HttpResponseRedirect(reverse('app_social:profile'))
    else:
        return redirect('app_social:login')

def create_post_fanpage(request):
    page_id = request.POST['page_id']
    fanpage = Fanpage.objects.get(id=page_id)
    if fanpage.author.username == request.POST['user']:
        if request.method == 'POST':
            if request.POST['content'] or request.FILES.getlist('images') or  request.FILES.getlist('videos'):
                content = request.POST['content'] 
                
                post = Post_Fanpage(fanpage=fanpage, content=content)
                post.save()
                if request.FILES.getlist('images'):
                    images_page = request.FILES.getlist('images')
                    for image_page in images_page:
                        new_image = ImageFanpage(image=image_page)
                        new_image.save()
                        post.images.add(new_image)
                if request.FILES.getlist('videos'):
                    videos = request.FILES.getlist('videos')
                    for video in videos:
                        new_video = VideoFanpage(video=video)
                        new_video.save()
                        post.video.add(new_video)
            else:
                messages.error(request, "Cần có hình, video hoặc nội dung bài viết!")
        
        return redirect('app_social:fanpage',page_id=page_id)
    else:
        return redirect('app_social:login')

def edit_fanpage(request):
    if request.POST['page_id']:
        page_id = request.POST['page_id']
        fanpage = Fanpage.objects.get(id=page_id)
        if request.method == 'POST':
            fanpage.name = request.POST['name_fanpage']
            fanpage.description = request.POST['description_fanpage']
            if request.FILES.get('image_fanpage'):
                fanpage.imgFanpage = request.FILES['image_fanpage'] 
            if request.FILES.get('img_cover_fanpage') is not None:
                fanpage.imgFanpageCover = request.FILES['img_cover_fanpage'] 
            fanpage.save()
            return redirect('app_social:fanpage',page_id=page_id)
    return redirect('app_social:index')

def delete_fanpage(request,page_id):
    fanpage = Fanpage.objects.get(id=page_id)
    fanpage.delete()
    return redirect('app_social:profile')

def edit_post_fanpage(request,post_id):
    post = get_object_or_404(Post_Fanpage, id=post_id)
    page_id = request.POST['page_id']
    if request.method == 'POST':
        if request.POST.get('content') or request.FILES.getlist('videos') or request.FILES.getlist('images'):
                post.content = request.POST['content']
                if request.FILES.getlist('images'):
                    images_p_f = request.FILES.getlist('images')
                    for old_image in post.images.all():
                        old_image.delete()
                    for image in images_p_f:
                        new_image = ImageFanpage(image=image)  
                        new_image.save()
                        post.images.add(new_image)
                
                if request.FILES.getlist('videos'):
                    videos = request.FILES.getlist('videos')
                    for old_video in post.video.all():
                        old_video.delete()
                    for video in videos:
                        new_video = VideoFanpage(video=video)  
                        new_video.save() 
                        post.video.add(new_video)
                post.save()
                
    return redirect('app_social:fanpage',page_id=page_id)

def delete_post_fanpage(request,post_id):
    post = get_object_or_404(Post_Fanpage, id=post_id)
    page_id = request.GET.get('page_id')
    post.delete()
    return redirect('app_social:fanpage',page_id=page_id)
def like_post_fanpage(request, post_id):
    page_id = request.GET.get('page_id')
    if request.user.is_authenticated: 
        post = get_object_or_404(Post_Fanpage, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            
        post.save()

        return redirect('app_social:fanpage',page_id=page_id)
    else:
        return redirect('app_social:login')

def join_fanpage(request,page_id):
    fanpage = Fanpage.objects.get(id=page_id)
    fanpage.members.add(request.user)
    return redirect('app_social:fanpage',page_id=page_id)

def like_fanpage(request,page_id):
    fanpage = Fanpage.objects.get(id=page_id)
    fanpage.likes.add(request.user)
    return redirect('app_social:fanpage',page_id=page_id)

def unlike_fanpage(request,page_id):
    fanpage = Fanpage.objects.get(id=page_id)
    fanpage.likes.remove(request.user)
    return redirect('app_social:fanpage',page_id=page_id)
    

def leave_fanpage(request, page_id):
    fanpage = Fanpage.objects.get(id=page_id)
    fanpage.members.remove(request.user)
    return redirect('app_social:fanpage',page_id=page_id)