#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cognito_tudelft.cognito_tudelft_stack import CognitoTudelftStack

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
