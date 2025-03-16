from rest_framework import serializers

from mailings.models import Contact, Mailing, Message


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Contact

    def validate_number(self, value):
        if str(value)[0] != '7':
            raise serializers.ValidationError(
                'Enter the number in the format 7XXXXXXXXXX'
            )
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'send_time', 'status', 'mailing', 'contact'
        )
        model = Message


class MailinglistSerializer(serializers.ModelSerializer):
    send_messages = serializers.SerializerMethodField()
    not_send_messages = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'start_send_time', 'end_send_time',
            'text', 'tag', 'code', 'send_messages', 'not_send_messages'
        )
        model = Mailing

    def get_send_messages(self, obj):
        return obj.messages.filter(status='S').count()

    def get_not_send_messages(self, obj):
        return obj.messages.filter(status='N').count()


class MailingSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id', 'start_send_time', 'end_send_time',
            'text', 'tag', 'code', 'messages'
        )
        model = Mailing
