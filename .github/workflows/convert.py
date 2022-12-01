#!/usr/bin/env python3
# substitute the UserPoolId in a CloudFormation template with the text
# "<my_user_pool_id_here>", to make the template easier to reuse
import json

with open('./cdk.out/CognitoTudelftStack.template.json') as f:
    data = json.load(f)

for resource in data["Resources"]:
    if "UserPoolId" in data["Resources"][resource]["Properties"]:
        data["Resources"][resource]["Properties"]["UserPoolId"] = \
            "my-user-pool-id"
        print(data["Resources"][resource]["Properties"]["UserPoolId"])

with open('./cdk.out/Dummy.CognitoTudelftStack.template.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
