import graphene
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker
from graphql_relay import from_global_id

from retrospective.queries import UserNode, TeamNode, CardNode, RetroNode
from retrospective.models import Teams, Retros, Cards


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        last_name = graphene.String(required=False)
        first_name = graphene.String(required=False)

    def mutate(self, info, password, email, last_name='', first_name=''):
            user = get_user_model()(
                username=email,
                email=email,
                last_name=last_name,
                first_name=first_name
            )
            user.set_password(password)
            user.save()

            return CreateUser(user=user)


class ForgotPassword(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        user = User.objects.get(username=email)
        user.set_password('1234')
        user.save()

        return ForgotPassword(user=user)


class CreateTeam(graphene.Mutation):
    team = graphene.Field(TeamNode)

    class Arguments:
        team_name = graphene.String(required=True)
        team_members = graphene.List(graphene.String)

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, team_name, team_members):
        list_ids_members = []
        for member in team_members:
            user = User.objects.get(email=member)
            if user:
                list_ids_members.append(user.id)
        team = Teams.objects.create(name=team_name, members=list_ids_members)

        return CreateTeam(team=team)


class CreateRetro(graphene.Mutation):
    retro = graphene.Field(RetroNode)

    class Arguments:
        retro_name = graphene.String(required=True)
        retro_date = graphene.Date()
        retro_time = graphene.Time()
        retro_format = graphene.String(required=True)
        retro_fk_team = graphene.String(required=True)

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, retro_name, retro_date, retro_time, retro_format, retro_fk_team):
        id = from_global_id(retro_fk_team)[1]
        team = Teams.objects.get(pk=id)
        if team:
            retro = Retros.objects.create(name=retro_name, date=retro_date, time=retro_time,
                                          meeting_format=retro_format, fk_team=team)

            return CreateRetro(retro=retro)


class CreateCard(graphene.Mutation):
    card = graphene.Field(CardNode)

    class Arguments:
        card_description = graphene.String()
        card_type = graphene.String()
        card_author = graphene.String()
        card_anonymus = graphene.Boolean()
        card_retro = graphene.String()
        card_tags = graphene.List(graphene.String)
        card_status = graphene.String()
        card_priority = graphene.String()
        card_asignee = graphene.List(graphene.String)
        card_likes = graphene.Int()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, card_description, card_author, card_anonymus, card_likes, card_priority, card_type,
               card_retro, card_tags, card_asignee, card_status):
        author_id = from_global_id(card_author)[1]
        user = User.objects.get(id=author_id)
        retro_id = from_global_id(card_retro)[1]
        retro = Retros.objects.get(id=retro_id)
        ids_asignee = []
        for assignee in card_asignee:
            id = from_global_id(assignee)[1]
            ids_asignee.append(id)
        card = Cards.objects.create(description=card_description, type=card_type, author=user, priority=card_priority,
                                    retro_fk=retro, is_anonymus=card_anonymus, tags=card_tags, likes=card_likes,
                                    asignee=ids_asignee, status=card_status)
        return CreateCard(card=card)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    forgot_password = ForgotPassword.Field()
    create_team = CreateTeam.Field()
    create_retro = CreateRetro.Field()
    create_card = CreateCard.Field()
