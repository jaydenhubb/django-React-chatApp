from rest_framework import serializers
from .models import Room, Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Channel
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_room = ChannelSerializer(many=True)
    class Meta :
        model = Room
        exclude = ("member",)
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data

