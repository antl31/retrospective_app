from rest_framework import serializers
from retrospective.models import Teams, MEETINGS


class TeamsSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    members = serializers.ListField(serializers.IntegerField())

    class Meta:
        model = Teams
        fields = ['id', 'name', 'members', 'tags']


class RetrosSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    date = serializers.DateField()
    time = serializers.TimeField()
    meeting_format = serializers.ChoiceField(choices=MEETINGS)
    fk_team = TeamsSerializer()
