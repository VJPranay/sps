from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet, UserSearch,\
    send_friend_request, remove_friend,friend_requests,friends,accept_friend

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/user_search/', UserSearch.as_view(), name='user_search'),
    path('api/v1/send_friend_request/', send_friend_request, name='send_friend_request'),
    path('api/v1/friend_requests/', friend_requests, name='friend_requests'),
    path('api/v1/accept_friend/', accept_friend, name='accept_friend'),
    path('api/v1/friends/', friends, name='friends'),
    path('api/v1/remove_friend/', remove_friend, name='remove_friend'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
