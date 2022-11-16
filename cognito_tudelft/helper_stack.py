#!/usr/bin/env python3
from aws_cdk import (
    Stack, RemovalPolicy,
    aws_cognito as cognito,
)
from constructs import Construct


class HelperStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str,
        base_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

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

        self.user_pool = cognito_user_pool
