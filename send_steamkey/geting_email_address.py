# from botocore.exceptions import ClientError
import json
import boto3
import datetime


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def get_emails_address_cognito():
    client = boto3.client('cognito-idp')
    response = client.list_users(
        # the PanPot Cognito
        UserPoolId='eu-central-1_dTsWQlTS9',
        # Limit=1,
        # Filter='given_name^=\"Xavier\"'
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response['Users'],
                           sort_keys=True,
                           indent=1,
                           default=default)
    }


def update_emailaddress_db(steamkeyId, emailAddress, table):
    response = table.update_item(
        Key={
            'steamkeysId': steamkeyId
        },
        UpdateExpression="set email=:email, steamkeyStatus=:steamkeyStatus",
        ExpressionAttributeValues={
            ':email': emailAddress,
            ':steamkeyStatus': True
        },
        ReturnValues="UPDATED_NEW"
    )


def all_email_address():
    emails_address = []
    user = get_emails_address_cognito()
    for s in user.items():
        if s[1] != 200:
            for d in json.loads(s[1]):
                for k, v in d.items():
                    if k == "Attributes":
                        for a, b in v[4].items():
                            if b[:] != "email":
                                emails_address.append(b[:])
    return emails_address
