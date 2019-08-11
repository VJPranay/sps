from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Activity
from feed.users.models import User
from friendship.models import Friend,FriendshipRequest
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
                user = request.user,
                post_type = post_type,
                image = image,
                video = video,
                body = body,
                location = location
            )
            new_activity.save()
            return Response("Posted")

@api_view(['GET'])
def near_by_posts(request):
    user_details = User.objects.get(id=request.user.id)
    user_location = GEOSGeometry(request.user.location)
    print(request.user.id)
    posts = Activity.objects.filter(post_type='NB',location__distance_lte=(user_details.location, D(m=16093)))[:20]
    temp_posts = []
    for post in posts:
            posted_user = User.objects.get(id=post.user_id)
            post_location = GEOSGeometry(post.location)
            if not post.image:
                if not post.video:
                    temp_post = {
                        'user' : posted_user.username,
                        'first_name' : posted_user.first_name,
                        'second_name' : posted_user.last_name,
                        'profile_pic' : posted_user.profile_picture.url,
                        'datetime' : post.datetime,
                        'body' : post.body,
                        'distance': user_location.distance(post_location) * 100000
                    }
                    temp_posts.append(temp_post)
                elif post.video:
                    temp_post = {
                        'user': posted_user.username,
                        'first_name': posted_user.first_name,
                        'second_name': posted_user.last_name,
                        'profile_pic': posted_user.profile_picture.url,
                        'datetime': post.datetime,
                        'body': post.body,
                        'video': post.video.url,
                        'distance': user_location.distance(post_location) * 100000
                    }
                    temp_posts.append(temp_post)
                # else:
                #     temp_post = {
                #         'user': friend.username,
                #         'profile_pic': friend.profile_picture.url,
                #         'datetime': activity.datetime,
                #         'body': activity.body,
                #         'video' : activity.video.url,
                #     }
                #     friend_posts.append(temp_post)
            elif post.image:
                temp_post = {
                    'user': post.user_id,
                    'first_name': posted_user.first_name,
                    'second_name': posted_user.last_name,
                    'profile_pic': posted_user.profile_picture.url,
                    'datetime': post.datetime,
                    'body': post.body,
                'image' :post.image.url,
                    'distance': user_location.distance(post_location) * 100000
                }
                temp_posts.append(temp_post)
            else:
                temp_post = {
                    'user': posted_user.username,
                    'first_name': posted_user.first_name,
                    'second_name': posted_user.last_name,
                    'profile_pic': posted_user.profile_picture.url,
                    'datetime': post.datetime,
                    'body': post.body,
                    'image': post.image.url,
                    'video': post.video.url,
                    'distance': user_location.distance(post_location) * 100000
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
        activities = Activity.objects.filter(user_id=friend.id,post_type='FR').order_by('-id')[page*20:(page+1)*20]
        for activity in activities:
            if not activity.image:
                if not activity.video:
                    temp_post = {
                        'user' : friend.username,
                        'first_name' : friend.first_name,
                        'second_name' : friend.second_name,
                        'profile_pic' : friend.profile_picture.url,
                        'datetime' : activity.datetime,
                        'body' : activity.body,
                    }
                    friend_posts.append(temp_post)
                elif activity.video:
                    temp_post = {
                        'user': friend.username,
                        'first_name': friend.first_name,
                        'second_name': friend.second_name,
                        'profile_pic': friend.profile_picture.url,
                        'datetime': activity.datetime,
                        'body': activity.body,
                        'video': activity.video.url,
                    }
                    friend_posts.append(temp_post)
            elif activity.image:
                temp_post = {
                'user': friend.username,
                'first_name': friend.first_name,
                'second_name': friend.second_name,
                'profile_pic': friend.profile_picture.url,
                'datetime': activity.datetime,
                'body': activity.body,
                'image' :activity.image.url
                }
                friend_posts.append(temp_post)
            else:
                temp_post = {
                    'user': friend.username,
                    'first_name': friend.first_name,
                    'second_name': friend.second_name,
                    'profile_pic': friend.profile_picture.url,
                    'datetime': activity.datetime,
                    'body': activity.body,
                    'image': activity.image.url,
                    'video': activity.video.url,
                }
                friend_posts.append(temp_post)
    return Response(friend_posts)