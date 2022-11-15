#!/usr/bin/env python3
from aws_cdk import App, Environment
from aws_cdk.assertions import Template

from app import CognitoTudelftStack

app = App()
cognito_tudelft_stack = CognitoTudelftStack(
    app, "CognitoTudelftStack",
    env=Environment(
        account="123456789012", region="eu-central-1"
    )
)

# Prepare the stack for assertions.
template = Template.from_stack(cognito_tudelft_stack)


def test_synthesizes_properly():
    template.resource_count_is(type="AWS::Cognito::UserPool", count=1)
    template.resource_count_is(
        type="AWS::Cognito::UserPoolIdentityProvider", count=1
    )
    template.resource_count_is(type="AWS::Cognito::UserPoolClient", count=1)
    template.resource_count_is(type="AWS::Cognito::UserPoolDomain", count=1)
