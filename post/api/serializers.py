
from post.models import Comment, Like, Post
from rest_framework import serializers

from user_app.api.serializers import AccountSerializer

class LikesSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"

        extra_kwargs = {"author": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

        extra_kwargs = {"author": {"read_only": True}}


class PostSerializer(serializers.ModelSerializer):
    #user=AccountSerializer(read_only=True)
    
    # def validate(self, attrs):
    #     attrs['user'] = self.context['request'].user
    #     return attrs
    likes = LikesSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_amount = serializers.SerializerMethodField("get_likes_amount")
    comments_amount = serializers.SerializerMethodField("get_comments_amount")
    is_liked = serializers.SerializerMethodField(source="get_is_liked")
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Post
        fields = [
            "title",
            "description",
            "post_image",
            "author",
            "is_liked",
            "likes",
            "likes_amount",
            "comments",
            "comments_amount",
        ]
        extra_kwargs = {
            "is_liked": {"read_only": True},
        }
    @staticmethod
    def get_likes_amount(obj):
        return obj.likes.count()

    @staticmethod
    def get_comments_amount(obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        print (user)
        if user and not user.is_anonymous:
            return bool(obj.likes.filter(author=user))
        return None
class LikesDetailedSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}
       
        # read_only_fields = ['user']
# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=4000)
#     post_image=serializers.ImageField()
#     author_id = serializers.IntegerField()
#     post_date=serializers.DateField()

#     def create(self, validated_data):
#         return Post.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.author_id = validated_data.get('author_id', instance.author_id)
#         instance.post_image=validated_data.get('post_image', instance.post_image)
#         instance.post_date = validated_data.get('post_date', instance.post_date)
#         instance.save()
#         return instance
    