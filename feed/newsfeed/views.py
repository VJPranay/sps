from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Activity, Like, Comment
from feed.users.models import User
from friendship.models import Friend, FriendshipRequest
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D


@api_view(['GET', 'POST'])
def post_activity(request):
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        video = request.FILES.get('video', None)
        body = request.POST.get('body', None)
        post_type = request.POST.get('ptype', None)
        location = request.POST.get('location', None)
        if image == None and video == None and body == None:
            return Response("Your post cant be empty")
        elif post_type == 'NB' and location == None:
            return Response("Location must be sent")
        else:
            new_activity = Activity(
                user=request.user,
                post_type=post_type,
                image=image,
                video=video,
                body=body,
                location=location
            )
            new_activity.save()
            return Response("Posted")


@api_view(['GET'])
def near_by_posts(request):
    user_details = User.objects.get(id=request.user.id)
    user_location = GEOSGeometry(request.user.location)
    print(request.user.id)
    posts = Activity.objects.filter(post_type='NB', location__distance_lte=(user_details.location, D(m=16093)))[:20]
    temp_posts = []
    for post in posts:
        post_comments = []
        posted_user = User.objects.get(id=post.user_id)
        likes = Like.objects.filter(post_id=post.id)
        comments = Comment.objects.filter(post_id=post.id)
        for comment in comments:
            commented_user_details = User.objects.get(id=comment.user_id)
            temp_comment = {
                'user': commented_user_details.username,
                'comment': comment.body
            }
            post_comments.append(temp_comment)
        temp_user_like = Like.objects.filter(post_id=post.id, user_id=request.user.id)
        post_location = GEOSGeometry(post.location)

        if not post.image:
            if not post.video:
                temp_post = {
                    'post_id': post.id,
                    'user': posted_user.username,
                    'first_name': posted_user.first_name,
                    'last_name': posted_user.last_name,
                    'profile_pic': None if not posted_user.profile_picture else posted_user.profile_picture.url,
                    'datetime': post.datetime,
                    'body': post.body,
                    'distance': user_location.distance(post_location) * 100000,
                    'likes': len(likes),
                    'user_liked': False if len(temp_user_like) == 0 else True,
                    'comments': post_comments[0:2],
                }
                temp_posts.append(temp_post)
            elif post.video:
                temp_post = {
                    'user': posted_user.username,
                    'id': post.id,
                    'first_name': posted_user.first_name,
                    'last_name': posted_user.last_name,
                    'profile_pic': None if not posted_user.profile_picture else posted_user.profile_picture.url,
                    'datetime': post.datetime,
                    'body': post.body,
                    'video': None if not post.video else post.video.url,
                    'distance': user_location.distance(post_location) * 100000,
                    'likes': len(likes),
                    'user_liked': False if len(temp_user_like) == 0 else True,
                    'comments': post_comments[0:2],
                }
                temp_posts.append(temp_post)
            # else:
            #     temp_post = {
            #         'user': friend.username,
            #         'profile_pic': None if not friend.profile_picture else friend.profile_picture.url,
            #         'datetime': activity.datetime,
            #         'body': activity.body,
            #         'video' : activity.video.url,
            #     }
            #     friend_posts.append(temp_post)
        elif post.image:
            temp_post = {
                'user': post.user_id,
                'id': post.id,
                'first_name': posted_user.first_name,
                'last_name': posted_user.last_name,
                'profile_pic': None if not posted_user.profile_picture else posted_user.profile_picture.url,
                'datetime': post.datetime,
                'body': post.body,
                'image': None if not post.image else post.image.url,
                'distance': user_location.distance(post_location) * 100000,
                'likes': len(likes),
                'user_liked': False if len(temp_user_like) == 0 else True,
                'comments': post_comments[0:2],
            }
            temp_posts.append(temp_post)
        else:
            temp_post = {
                'user': posted_user.username,
                'id': post.id,
                'first_name': posted_user.first_name,
                'last_name': posted_user.last_name,
                'profile_pic': None if not posted_user.profile_picture else posted_user.profile_picture.url,
                'datetime': post.datetime,
                'body': post.body,
                'image': None if not post.image else post.image.url,
                'video': None if not post.video else post.video.url,
                'distance': user_location.distance(post_location) * 100000,
                'likes': len(likes),
                'user_liked': False if len(temp_user_like) == 0 else True,
                'comments': post_comments[0:2],
            }
            temp_posts.append(temp_post)
    return Response(temp_posts)


@api_view(['GET'])
def posts(request):
    temp = []
    page = int(request.GET['page'])
    friends = Friend.objects.friends(request.user)
    user_location = GEOSGeometry(request.user.location)
    friend_posts = []
    for friend in friends:
        activities = Activity.objects.filter(user_id=friend.id, post_type='FR').order_by('-id')[
                     page * 20:(page + 1) * 20]
        for activity in activities:
            post_comments = []
            likes = Like.objects.filter(post_id=activity.id)
            temp_user_like = Like.objects.filter(post_id=activity.id, user_id=request.user.id)
            comments = Comment.objects.filter(post_id=activity.id)
            for comment in comments:
                commented_user_details = User.objects.get(id=comment.user_id)
                temp_comment = {
                    'user': commented_user_details.username,
                    'comment': comment.body
                }
                post_comments.append(temp_comment)
            if not activity.image:
                if not activity.video:
                    temp_post = {
                        'user': friend.username,
                        'post_id': activity.id,
                        'first_name': friend.first_name,
                        'last_name': friend.last_name,
                        'profile_pic': None if not friend.profile_picture else friend.profile_picture.url,
                        'datetime': activity.datetime,
                        'body': activity.body,
                        'likes': len(likes),
                        'user_liked': False if len(temp_user_like) == 0 else True,
                        'comments': post_comments[0:2],
                    }
                    friend_posts.append(temp_post)
                elif activity.video:
                    temp_post = {
                        'user': friend.username,
                        'post_id': activity.id,
                        'first_name': friend.first_name,
                        'last_name': friend.last_name,
                        'profile_pic': None if not friend.profile_picture else friend.profile_picture.url,
                        'datetime': activity.datetime,
                        'body': activity.body,
                        'video': activity.video.url,
                        'likes': len(likes),
                        'user_liked': False if len(temp_user_like) == 0 else True,
                        'comments': post_comments[0:2],
                    }
                    friend_posts.append(temp_post)
            elif activity.image:
                temp_post = {
                    'user': friend.username,
                    'post_id': activity.id,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name,
                    'profile_pic': None if not friend.profile_picture else friend.profile_picture.url,
                    'datetime': activity.datetime,
                    'body': activity.body,
                    'image': activity.image.url,
                    'likes': len(likes),
                    'user_liked': False if len(temp_user_like) == 0 else True,
                    'comments': post_comments[0:2],
                }
                friend_posts.append(temp_post)
            else:
                temp_post = {
                    'user': friend.username,
                    'post_id': activity.id,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name,
                    'profile_pic': None if not friend.profile_picture else friend.profile_picture.url,
                    'datetime': activity.datetime,
                    'body': activity.body,
                    'image': activity.image.url,
                    'video': activity.video.url,
                    'likes': len(likes),
                    'user_liked': False if len(temp_user_like) == 0 else True,
                    'comments': post_comments[0:2],
                }
                friend_posts.append(temp_post)
    return Response(friend_posts)


@api_view(['POST'])
def post_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        likes = Like.objects.filter(user_id=request.user.id, post_id=post_id)
        if len(likes) == 0:
            like = Like.objects.create(user_id=request.user.id, post_id=post_id)
            like.save()
            content = {'status': 'success', 'message': 'liked post'}
            return Response(content)
        else:
            content = {'status': 'error', 'message': 'already liked'}
            return Response(content)


@api_view(['POST'])
def post_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        body = request.POST.get('body')
        comment = Comment.objects.create(user_id=request.user.id, post_id=post_id,body=body)
        comment.save()
        content = {'status': 'success', 'message': 'commented on post'}
        return Response(content)


@api_view(['POST'])
def get_comments(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comments = Comment.objects.filter(post_id=post_id)
        final_comments = []
        for comment in comments:
            commented_user_details = User.objects.get(id=comment.user_id)
            if not commented_user_details.profile_picture:
                temp_comment = {
                    'user': None,
                    'profile_pic': commented_user_details.profile_picture.url,
                    'comment': comment.body
                }
                final_comments.append(temp_comment)
            else:
                temp_comment = {
                    'user': commented_user_details.username,
                    'profile_pic': commented_user_details.profile_picture.url,
                    'comment': comment.body
                }
                final_comments.append(temp_comment)
        return Response(final_comments)
