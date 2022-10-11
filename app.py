#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cognito_tudelft.cognito_tudelft_stack import CognitoTudelftStack


app = cdk.App()
CognitoTudelftStack(
    app, "CognitoTudelftStack",

    # AWS Account and Region are implied by the current CLI configuration.
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

app.synth()
