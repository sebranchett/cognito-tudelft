import aws_cdk as core
import aws_cdk.assertions as assertions

from cognito_tudelft.cognito_tudelft_stack import CognitoTudelftStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cognito_tudelft/cognito_tudelft_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CognitoTudelftStack(app, "cognito-tudelft")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
