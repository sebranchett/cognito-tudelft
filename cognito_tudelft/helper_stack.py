#!/usr/bin/env python3
from aws_cdk import (
    Stack, RemovalPolicy,
    aws_cognito as cognito,
)
from constructs import Construct


class HelperStack(Stack):
    """
    Helper stack class for creating a Cognito user pool

    There are differences between class UserPool and IUserPool.
    This class creates a UserPool and looks up its IUserPool.
    ...

    Attributes
    ----------
    user_pool : IUserPool
        the IUserPool interface of the newly created Cognito user pool
    """
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

        self.user_pool_id = new_cognito_user_pool.user_pool_id
