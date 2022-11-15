#!/usr/bin/env python3
from aws_cdk import App, Environment
from aws_cdk.assertions import Template, Match, Capture

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
            "Ref": Match.string_like_regexp("TUDelftUserPool*")
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
            "Ref": Match.string_like_regexp("TUDelftUserPool*")
        }}
    )
