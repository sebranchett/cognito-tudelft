#!/usr/bin/env python3
from aws_cdk import App, Environment
from aws_cdk.assertions import Template, Match, Capture

from cognito_tudelft.helper_stack import HelperStack
from cognito_tudelft.tudelft_idp import CognitoTudelftStack

app = App()
env = Environment(account="123456789012", region="eu-central-1")
base_name = "TU-Delft"
application_domain_name = "my-service.my-domain.nl"

helper_stack = HelperStack(
    app, "HelperStack",
    base_name=base_name,
    env=env,
)

cognito_tudelft_stack = CognitoTudelftStack(
    app,
    "CognitoTudelftStack",
    base_name=base_name,
    application_domain_name=application_domain_name,
    cognito_user_pool=helper_stack.user_pool,
    user_group="AllowedUsers",
    env=env,
)

groupless_cognito_tudelft_stack = CognitoTudelftStack(
    app,
    "GrouplessCognitoTudelftStack",
    base_name=base_name,
    application_domain_name=application_domain_name,
    cognito_user_pool=helper_stack.user_pool,
    env=env,
)

# Prepare the stack for assertions.
template = Template.from_stack(cognito_tudelft_stack)
groupless_template = Template.from_stack(groupless_cognito_tudelft_stack)


def test_synthesizes_properly():
    template.resource_count_is(
        type="AWS::Cognito::UserPoolIdentityProvider", count=1
    )
    template.resource_count_is(type="AWS::Cognito::UserPoolClient", count=1)
    template.resource_count_is(type="AWS::Cognito::UserPoolGroup", count=1)
    template.resource_count_is(type="AWS::Cognito::UserPoolDomain", count=1)


def test_identity_provider():
    template.has_resource_properties(
        "AWS::Cognito::UserPoolIdentityProvider",
        {"ProviderType": Match.string_like_regexp("SAML")}
    )

    template.has_resource_properties(
        "AWS::Cognito::UserPoolIdentityProvider",
        {"AttributeMapping": {
            "email": Match.string_like_regexp("mail")
        }}
    )

    template.has_resource_properties(
        "AWS::Cognito::UserPoolIdentityProvider",
        {"AttributeMapping": {
            "preferred_username": Match.string_like_regexp(
                "eduPersonPrincipalName"
            )
        }}
    )


def test_user_pool_client():
    template.has_resource_properties(
        "AWS::Cognito::UserPoolClient",
        {"UserPoolId": {
            "Fn::ImportValue": Match.string_like_regexp("HelperStack:*")
        }}
    )

    auth_flow_allowed = Capture()
    template.has_resource_properties(
        "AWS::Cognito::UserPoolClient",
        {"AllowedOAuthFlowsUserPoolClient": auth_flow_allowed}
    )
    assert auth_flow_allowed.as_boolean() is True

    template.has_resource_properties(
        "AWS::Cognito::UserPoolClient",
        {"CallbackURLs": [Match.string_like_regexp(
            "https://my-service.my-domain.nl/hub/oauth_callback"
        )]}
    )

    template.has_resource_properties(
        "AWS::Cognito::UserPoolClient",
        {"SupportedIdentityProviders": [
            "COGNITO",
            {"Ref": Match.string_like_regexp("TUDelftIdentityProvider*")}
        ]}
    )


def test_user_pool_domain():
    template.has_resource_properties(
        "AWS::Cognito::UserPoolDomain",
        {"Domain":  Match.string_like_regexp("my-service-secure")}
    )

    template.has_resource_properties(
        "AWS::Cognito::UserPoolDomain",
        {"UserPoolId": {
            "Fn::ImportValue": Match.string_like_regexp("HelperStack:*")
        }}
    )


def test_groupless_user_pool():
    groupless_template.resource_count_is(
        type="AWS::Cognito::UserPoolGroup", count=0
    )
