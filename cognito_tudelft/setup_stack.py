from aws_cdk import (
    Stack, RemovalPolicy,
    aws_cognito as cognito,
)
from constructs import Construct


class SetupStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str,
        base_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cognito_user_pool = cognito.UserPool(
            self,
            f'{base_name}UserPool',
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False
        )

        self.cognito_user_pool = cognito_user_pool
