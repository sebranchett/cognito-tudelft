#!/usr/bin/env python3
import os
import aws_cdk as cdk
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
        application_domain_name = "my-service.my-domain.nl"

        new_cognito_user_pool = cognito.UserPool(
            self,
            f'{base_name}UserPool',
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False
        )

        # There are differences between class UserPool and IUserPool
        cognito_user_pool = cognito.UserPool.from_user_pool_id(
            self, "UserPoolID", new_cognito_user_pool.user_pool_id
        )

        # cognito_app_client = \
        configure_user_pool(
            self,
            base_name=base_name,
            application_domain_name=application_domain_name,
            cognito_user_pool=cognito_user_pool
        )


# These environment variables set based on your default AWS profile or
# the profile you specify the --profile option
default_env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)
app = cdk.App()

CognitoTudelftStack(
    app, "CognitoTudelftStack",
    env=default_env,
)

app.synth()
