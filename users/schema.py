# users/schema.py
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        try:
            user = get_user_model()(username=username, email=email)
            user.set_password(password)
            user.save()
            return CreateUser(user=user)
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
