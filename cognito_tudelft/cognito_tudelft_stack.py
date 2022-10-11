from aws_cdk import (
    Stack, RemovalPolicy,
    aws_cognito as cognito,
)
from constructs import Construct


class CognitoTudelftStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # User pool and user pool OAuth client
        base_name = "CogTUD"
        cognito.UserPool(
            self,
            f'{base_name}UserPool',
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False
        )
