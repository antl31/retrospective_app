import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from django_graphene_permissions import PermissionDjangoObjectType
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated

from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from retrospective.models import Teams, Retros, Cards


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        filter_fields = ['last_name', 'first_name']


class UserNode(PermissionDjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        filter_fields = ['last_name', 'first_name']
        interfaces = (relay.Node,)

    @staticmethod
    def permission_classes():
        return [IsAuthenticated]


class TeamType(DjangoObjectType):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'members', 'tags')
        filter_fields = ['name']


class TeamNode(PermissionDjangoObjectType):
    class Meta:
        model = Teams
        fields = ('id', 'name', 'members', 'tags')
        filter_fields = ['name']
        interfaces = (relay.Node,)

    @staticmethod
    def permission_classes():
        return [IsAuthenticated]


class RetroType(DjangoObjectType):
    class Meta:
        model = Retros
        fields = ('id', 'name', 'date', 'time', 'meeting_format', 'fk_team')
        filter_fields = ['name']


class RetroNode(PermissionDjangoObjectType):
    class Meta:
        model = Retros
        fields = ('id', 'name', 'date', 'time', 'meeting_format', 'fk_team')
        filter_fields = ['name']
        interfaces = (relay.Node,)

    @staticmethod
    def permission_classes():
        return [IsAuthenticated]


class CardType(DjangoObjectType):
    class Meta:
        model = Cards
        filter_fields = ['id']


class CardNode(PermissionDjangoObjectType):
    class Meta:
        model = Cards
        filter_fields = ['id']
        interfaces = (relay.Node,)

    @staticmethod
    def permission_classes():
        return [IsAuthenticated]


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    @permissions_checker([IsAuthenticated])
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    team = relay.Node.Field(TeamNode)
    teams = graphene.List(TeamType)
    all_teams = DjangoFilterConnectionField(TeamNode)

    @permissions_checker([IsAuthenticated])
    def resolve_teams(self, info, **kwargs):
        return Teams.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_all_teams(self, info, **kwargs):
        return Teams.objects.all()

    retro = relay.Node.Field(RetroNode)
    retros = graphene.List(RetroType)
    all_retros = DjangoFilterConnectionField(RetroNode)

    @permissions_checker([IsAuthenticated])
    def resolve_retros(self, info, **kwargs):
        return Retros.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_all_retros(self, info, **kwargs):
        return Retros.objects.all()

    card = relay.Node.Field(CardNode)
    cards = graphene.List(CardType)
    all_cards = DjangoFilterConnectionField(CardNode)

    @permissions_checker([IsAuthenticated])
    def resolve_cards(self, info, **kwargs):
        return Cards.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_all_cards(self, info, **kwargs):
        return Cards.objects.all()
