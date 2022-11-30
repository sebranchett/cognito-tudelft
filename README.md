# AWS Cognito User Pool with TU Delft federated identity provider sign-in

## Intended audience
This repository is intended for TU Delft researchers with a TU Delft AWS account, see [TU Delft Cloud4Research](https://tu-delft-ict-innovation.github.io/Cloud4Research/).

With this repository, you can configure a AWS Cognito User pool so that users can log in with their TU Delft NetId. Note that this is for the users of the services created in the AWS account, not for direct access to the AWS account itself.

## License
This work was inspired by part of the [Jupyter ECS Service CDK project](https://github.com/avishayil/jupyter-ecs-service), under an [Apache 2.0 License](https://github.com/avishayil/jupyter-ecs-service/blob/master/LICENSE.md).

This repository has an [Apache 2.0 License](./LICENSE).

## Pre-requisites
1) AWS account issued by the TU Delft Cloud4Research team. [Learn more here.](https://tu-delft-ict-innovation.github.io/Cloud4Research/)
2) Working Python AWS CDK environment. [Learn more here](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_prerequisites), and for running an AWS CDK app [learn more here](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html).
3) A domain name that you have control over, e.g. managed by AWS Route 53.
4) An 'empty' Cognito User Pool. See the helper stack, included in this repository, for an example. You will need to provide the User pool ID when you ask the TU Delft to act as your identity provider (IdP).


## Procedure to request TU Delft as Identity Provider
For background information [read this](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-configuring-federation-with-saml-2-0-idp.html).

Make a new request in the [TU Self Service Portal](https://tudelft.topdesk.net/), e.g. ICT services -> ICT malfunction or Service Request, category Service Request. Mention 'Cloud4Research', 'AWS Cognito' and 'TU Delft as Identity Provider (IdP)'.

Be sure to include the following information:
* your ‘assertion consumer endpoint'. If you are using a Cognito domain, then it will look something like this: `https://<yourDomainPrefix>-secure.auth.<region>.amazoncognito.com/saml2/idpresponse`
* your User pool ID, which looks like this: `<region>_<hash>`
* ask for these two attributes to be released:
    * 'mail'
    * 'eduPersonPrincipalName'

'mail' is the user's e-mail and will be mapped to 'email'. 'eduPersonPrincipalName' is the user's NetId and will be mapped to 'preferred_username'.

## How to include this repository in your own CDK Python code
Add this to your requirements file and build your (virtual) environment:
```
git+https://github.com/sebranchett/cognito-tudelft.git@main
```
You can then add this to your Python code:
```
from cognito_tudelft.tudelft_idp import CognitoTudelftStack
...
cognito_tudelft_stack = CognitoTudelftStack(
    self,
    "CognitoTudelftStack",
    base_name=base_name,
    application_domain_name=domain_name,
    cognito_user_pool_id=cognito_user_pool_id,
    user_group=optional_user_group_name,
    env=Environment(
        account=self.account,
        region=self.region
    ),
)
...
```
You need to provide suitable values for `base_name`, `domain_name`, `cognito_user_pool_id` and optionally `optional_user_group_name`.

This will take a pre-existing Cognito User pool and add:
* the TU Delft SAML identity provider
* a User pool client, that uses the TU Delft identity provider
* a User pool domain, called `<yourDomainPrefix>-secure`
* optionally a user group, which you can later configure, for example to empower allowed users.


A helper stack is included in this repository. This helper stack creates a Cognito User pool and then looks up its `IUserPool`.

## Testing
Clone this repository and move into it. Use the requirements file to create a virtual environment. Activate the virtual environment. Make sure you are at the root of this repository and type:
```
pytest
```
There should be no errors.
