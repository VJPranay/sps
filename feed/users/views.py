from rest_framework import viewsets, mixins, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from friendship.models import Friend,FriendshipRequest
from friendship.exceptions import AlreadyExistsError
from django.contrib.gis.geos import GEOSGeometry


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UserSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


@api_view(['POST'])
def send_friend_request(request):
    if request.method == 'POST':
        try:
            req_user_info = User.objects.get(pk=request.POST['pk'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            Friend.objects.add_friend(request.user, req_user_info, message=request.POST['message'])
            content = {'message': 'Request sent successfully'}
            return Response(content)
        except AlreadyExistsError:
            return Response(str({'message': 'Already Friends'}))


@api_view(['GET'])
def friend_requests(request):
    temp = []
    friend_requests = FriendshipRequest.objects.filter(to_user=request.user.id)
    for friend_request in friend_requests:
        temp_data = {
            'from_user' : friend_request.from_user.username,
            'from_user_id' : friend_request.from_user_id,
            'message' : friend_request.message,
        }
        temp.append(temp_data)
    data = {
        'friend_requests' : temp
    }
    return Response(data)


@api_view(['POST'])
def accept_friend(request):
    friend_requests = FriendshipRequest.objects.filter(to_user=request.POST['id'])
    for friend_request in friend_requests:
        friend_request.accept()
    data = {
         'status': 'success', 'message': 'accepted successfully'
    }
    return Response(data)


@api_view(['GET'])
def friends(request):
    temp = []
    friends = Friend.objects.friends(request.user)
    user_location = GEOSGeometry(request.user.location)
    for friend in friends:
        friend_location = GEOSGeometry(friend.location)
        temp_data = {
            'id' : friend.id ,
            'username' : friend.username ,
            'profile_pic' : friend.profile_picture.url ,
            'latitude' : friend.location.x,
            'longitude' : friend.location.y,
            'distance' :  user_location.distance(friend_location) * 100
        }
        temp.append(temp_data)
    data = {
        'friends' : temp
    }
    return Response(data)


@api_view(['POST'])
def remove_friend(request):
    if request.method == 'POST':
        try:
            req_user_info = User.objects.get(pk=request.POST['pk'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            Friend.objects.remove_friend(request.user, req_user_info)
            content = {'status': 'success', 'message': 'Removed successfully'}
            return Response(content)
        except AlreadyExistsError:
            return Response(str({'status': 'failed', 'message': 'Already Friends'}))