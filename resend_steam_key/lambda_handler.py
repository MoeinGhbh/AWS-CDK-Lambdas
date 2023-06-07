from botocore.exceptions import ClientError
import json
import boto3
import datetime
# from steam_email_template import email_termplte


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SteamKeys')


def List_participants_resend_steamkey_email():
    lst_steam_key = []
    response = table.scan()
    for h in response['Items']:
        if h['steamkeyStatus'] == False:
            if 'email' in h.keys():
                if h['email'] != '':
                    # lst_steam_key.append(h['email'])
                    lst_steam_key.append(
                        [h['email'], h['steamkeyValue'], h['steamkeysId']])
    return lst_steam_key


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


def lambda_handler(event, context):

    emails_address = List_participants_resend_steamkey_email()
    print('aaaaaaaa', emails_address)

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "inxspace@nexr-technologies.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-central-1"

    # The subject line for the email.
    SUBJECT = "NexR Show Invitation"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("This is a Nexr Show\r\n"
                 "This email was sent to handover your steam key "
                 "and you will get the newaletter from us."
                 )

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    print(type(emails_address))
    for reciver in emails_address:
        # Try to send the email.
        try:
            new_steamKey = reciver[1]
            steamkeysId = reciver[2]
            # print(new_steamKey,steamkeysId)
            # The HTML body of the email.
            with open("index.html", "r") as f:
                webpage = f.read()
            BODY_HTML = webpage.replace('Participant_steam_key', new_steamKey)
            # print(reciver)
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        reciver[0],
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
            update_emailaddress_db(steamkeysId, reciver[0], table)
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print('send email successfully')

    return {
        'statusCode': 200,
        'body': json.dumps('email send')
    }
