# from rest_framework import serializers
# from rest_framework_gis.serializers import GeoFeatureModelSerializer
# from .models import Activity
#
#
# class ActivitySerializer(GeoFeatureModelSerializer):
#
#     datetime = serializers.DateTimeField()
#     post_type = serializers.CharField(max_length=255)
#     image = serializers.ImageField()
#     video = serializers.FileField()
#     body = serializers.CharField(max_length=255)
#     location =
#
#
#     class Meta:
#         model = Activity
#         fields = ('user', 'datetime', 'post_type', 'image', 'video', 'body', 'location')
#         read_only_fields = ('datetime', 'user')
#         extra_kwargs = {'datetime': {'write_only': True} }
#
#
# class CreateActivitySerializer(serializers.ModelSerializer):
#
#     def create(self, validated_data):
#         # call create_user on user object. Without this
#         # the password will be stored in plain text.
#         activity = Activity.objects.create(**validated_data)
#         return activity
#
#     class Meta:
#         model = Activity
#         fields = ('user', 'datetime', 'post_type', 'image', 'video', 'body', 'location')
#         read_only_fields = ('datetime',)
#         extra_kwargs = {'datetime': {'write_only': True},
#                         'user': {'write_only': True}
#                         }
