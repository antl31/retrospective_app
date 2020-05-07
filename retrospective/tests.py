from graphene_django.utils.testing import GraphQLTestCase
import schema
import json
from django.contrib.auth.models import User


class MyFancyTestCase(GraphQLTestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="", username="", password="")

    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema.schema

    def test_token_auth(self):
        response = self.query(
            '''
           mutation{
  tokenAuth(username:"",password:""){
    token
  }
}
            ''',
            op_name='myModel'
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(content)
