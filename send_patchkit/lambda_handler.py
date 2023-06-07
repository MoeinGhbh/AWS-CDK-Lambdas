from botocore.exceptions import ClientError
import json,boto3,datetime
from geting_email_address import get_emails_address_cognito, all_email_address 


def lambda_handler(event, context):
    
    # lst_sent_email_address = sent_emails_address()

    # this two below code remove the email address from the list that got the steam key
    emails_address = all_email_address()
    # emails_address = set(emails_address)-set(lst_sent_email_address)

            
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
    for reciver in emails_address:
        # Try to send the email.
        try:
                    # new_steamKey,steamkeysId = valid_steam_key()
                    # print(new_steamKey,steamkeysId)
                    # The HTML body of the email.
                    with open("index.html", "r") as f:
                        webpage = f.read()
                    BODY_HTML = webpage
                    # print(reciver)
                    # Provide the contents of the email.
                    response = client.send_email(
                                                    Destination={
                                                        'ToAddresses': [
                                                            reciver,
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
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print('send email successfully')

    return {
        'statusCode': 200,
        'body': event
    }

