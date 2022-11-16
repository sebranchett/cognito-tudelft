# AWS Cognito User Pool with TU Delft federated identity provider sign-in

## Intended audience
This repo is intended for TU Delft researchers with a TU Delft AWS account, see [TU Delft Cloud4Research](https://tu-delft-ict-innovation.github.io/Cloud4Research/).

With this repo, an AWS Cognito user pool can be configured to work, such that users can log in with their TU Delft NetId. Note that this is for the users of the services created in the AWS account, not for direct access to the AWS account itself.

## Pre-requisites
1) AWS account issued by the TU Delft Cloud4Research team. [Learn more here.](https://tu-delft-ict-innovation.github.io/Cloud4Research/)
2) Working Python AWS CDK environment. [Learn more here](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_prerequisites) and for running an AWS CDK app [learn more here](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html).