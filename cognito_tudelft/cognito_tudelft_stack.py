from aws_cdk import (
    Stack, RemovalPolicy, CfnOutput,
    aws_cognito as cognito,
    custom_resources as cr,
)
from constructs import Construct


class CognitoTudelftStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO these variables will become input parameters
        base_name = "CogTUD"
        domain_name = "my-service.my-domain.nl"
        domain_prefix = "my-service-secure"

        # User pool and user pool OAuth client
        cognito_user_pool = cognito.UserPool(
            self,
            f'{base_name}UserPool',
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False
        )

        # Output Cognito user pool id for future reference
        CfnOutput(
            self,
            f'{base_name}UserPoolID',
            value=cognito_user_pool.user_pool_id
        )

        cognito_app_client = cognito.UserPoolClient(
            self,
            f'{base_name}UserPoolClient',
            user_pool=cognito_user_pool,
            generate_secret=True,
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO],
            prevent_user_existence_errors=True,
            o_auth=cognito.OAuthSettings(
                callback_urls=[
                    'https://' + domain_name +
                    '/hub/oauth_callback'
                ],
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=True
                ),
                scopes=[cognito.OAuthScope.PROFILE, cognito.OAuthScope.OPENID]
            )
        )

        describe_cognito_user_pool_client = cr.AwsCustomResource(
            self,
            f'{base_name}UserPoolClientIDResource',
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE),
            on_create=cr.AwsSdkCall(
                service='CognitoIdentityServiceProvider',
                action='describeUserPoolClient',
                parameters={
                    'UserPoolId': cognito_user_pool.user_pool_id,
                    'ClientId': cognito_app_client.user_pool_client_id
                },
                physical_resource_id=cr.PhysicalResourceId.of(
                    cognito_app_client.user_pool_client_id)
            )
        )

        # cognito_user_pool_client_secret = \
        describe_cognito_user_pool_client.get_response_field(
            'UserPoolClient.ClientSecret'
        )

        # domain_prefix=application_prefix + '-' + suffix
        # cognito_user_pool_domain = \
        cognito.UserPoolDomain(
            self,
            f'{base_name}UserPoolDomain',
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=domain_prefix
            ),
            user_pool=cognito_user_pool
        )

        # tudelft_identity_provider = \
        cognito.UserPoolIdentityProviderSaml(
            self, "TUDelftIdentityProvider",
            metadata=cognito.UserPoolIdentityProviderSamlMetadata.url(
                "https://login.tudelft.nl/sso/saml2/idp/metadata.php"
            ),
            user_pool=cognito_user_pool,
            attribute_mapping=cognito.AttributeMapping(
                email=cognito.ProviderAttribute.other("mail"),
                preferred_username=cognito.ProviderAttribute.other(
                    "eduPersonPrincipalName"
                ),
            ),
            idp_signout=False,
            name="TU-Delft-IdP"
        )
