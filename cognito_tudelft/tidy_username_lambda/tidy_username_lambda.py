# Inspired by:
# https://aws.amazon.com/blogs/mobile/how-to-use-cognito-pre-token-generators-to-customize-claims-in-id-tokens/
# and:
# https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html

def lambda_handler(event, context):
    """
    This function handles adding a custom claim to the cognito ID token.
    """

    # find the preferred_username that will contain '@' and '.' characters
    nickname = event['request']['userAttributes']['preferred_username']

    # get rid of problematic characters
    nickname = nickname.replace('@', '_').replace('.', '_')

    # "claimsToAddOrOverride" allows us to override claims in the id token
    event["claimsOverrideDetails"] = {
        "claimsToAddOrOverride": {
            "nickname": nickname
        }
    }

    # return modified ID token to Amazon Cognito
    return event
