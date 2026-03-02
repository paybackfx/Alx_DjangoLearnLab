from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_content_type',
                  'target_object_id', 'timestamp', 'is_read']
        read_only_fields = ['recipient', 'actor', 'verb', 'target_content_type',
                            'target_object_id', 'timestamp']
