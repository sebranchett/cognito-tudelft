#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cognito_tudelft.setup_stack import SetupStack
from cognito_tudelft.cognito_tudelft_stack import CognitoTudelftStack

default_env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)
app = cdk.App()

base_name = "TU-Delft"
setup_stack = SetupStack(
    app, "SetupStack",
    base_name=base_name,
    env=default_env
)

CognitoTudelftStack(
    app, "CognitoTudelftStack",
    base_name=base_name,
    domain_name="my-service.my-domain.nl",
    cognito_user_pool=setup_stack.cognito_user_pool,
    env=default_env,
)

app.synth()
