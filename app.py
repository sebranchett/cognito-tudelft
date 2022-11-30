#!/usr/bin/env python3
import os
import aws_cdk as cdk

from cognito_tudelft.helper_stack import HelperStack
from cognito_tudelft.tudelft_idp import CognitoTudelftStack

# These environment variables set based on your default AWS profile or
# the profile you specify the --profile option
default_env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)

app = cdk.App()

base_name = "TU-Delft"
application_domain_name = "my-service.my-domain.nl"

# There are differences between class UserPool and IUserPool
# The helper stack creates an empty UserPool and finds its IUserPool
helper_stack = HelperStack(
    app, "HelperStack",
    base_name=base_name,
    env=default_env,
)

CognitoTudelftStack(
    app,
    "CognitoTudelftStack",
    base_name=base_name,
    application_domain_name=application_domain_name,
    cognito_user_pool_id=helper_stack.user_pool_id,
    user_group="AllowedUsers",
    env=default_env,
)

app.synth()
