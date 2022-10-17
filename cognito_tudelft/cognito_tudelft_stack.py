from aws_cdk import (
    Stack, RemovalPolicy,
    aws_cognito as cognito,
)
from constructs import Construct

from cognito_tudelft.tudelft_idp import configure_user_pool


class CognitoTudelftStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        base_name = "TU-Delft"
        domain_name = "my-service.my-domain.nl"

        cognito_user_pool = cognito.UserPool(
            self,
            f'{base_name}UserPool',
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False
        )

        cognito_app_client = configure_user_pool(
            self,
            base_name=base_name,
            domain_name=domain_name,
            cognito_user_pool=cognito_user_pool
        )
