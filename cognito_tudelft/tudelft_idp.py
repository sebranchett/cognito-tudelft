from aws_cdk import (
    aws_cognito as cognito,
    Stack
)
from constructs import Construct


class CognitoTudelftStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str,
        base_name: str,
        application_domain_name: str,
        cognito_user_pool: cognito.UserPool,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        tudelft_identity_provider = cognito.UserPoolIdentityProviderSaml(
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
            name=f'{base_name}'
        )

        cognito_app_client = cognito.UserPoolClient(
            self,
            f'{base_name}UserPoolClient',
            user_pool=cognito_user_pool,
            generate_secret=True,
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO,
                cognito.UserPoolClientIdentityProvider.custom(
                    tudelft_identity_provider.provider_name
                )
            ],
            prevent_user_existence_errors=True,
            o_auth=cognito.OAuthSettings(
                callback_urls=[
                    'https://' + application_domain_name +
                    '/hub/oauth_callback'
                ],
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=True
                ),
                scopes=[cognito.OAuthScope.PROFILE, cognito.OAuthScope.OPENID]
            )
        )

        # allowed_users_group = \
        cognito.CfnUserPoolGroup(
            self,
            id=f'{base_name}AllowedUsersGroup',
            user_pool_id=cognito_user_pool.user_pool_id,
            group_name="AllowedUsers",
            precedence=10
        )
        #     role_arn=""
        # )

        suffix = "-secure"
        cognito.UserPoolDomain(
            self,
            f'{base_name}UserPoolDomain',
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=application_domain_name.split(".")[0] + suffix
            ),
            user_pool=cognito_user_pool
        )

        self.app_client = cognito_app_client
