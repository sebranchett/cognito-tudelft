from os import path
from aws_cdk import (
    aws_cognito as cognito,
    aws_lambda as lambda_,
)


def configure_user_pool(
    self,
    base_name: str,
    domain_name: str,
    cognito_user_pool: cognito.UserPool
):

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

    cognito_user_pool.add_trigger(
        cognito.UserPoolOperation.PRE_TOKEN_GENERATION, lambda_.Function(
            self, "TidyUsernameFn",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="tidy_username_lambda.lambda_handler",
            code=lambda_.Code.from_asset(
                path.join(
                    path.dirname(path.abspath(__file__)),
                    "tidy_username_lambda"
                )
            )
        )
    )
    return cognito_app_client
