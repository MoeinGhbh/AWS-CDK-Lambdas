from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway,
    aws_dynamodb as dynamodb,

    # aws_s3_notifications,
    #  aws_s3 as _s3,
)


class NexrshowParticipantsManagementsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = CodePipeline(self, "Pipeline",
                                pipeline_name="MyPipeline",
                                synth=ShellStep("Synth",
                                                # input=CodePipelineSource.connection("MoeinGh/nexrshow-participants-management", "master",
                                                #                                     connection_arn="arn:aws:codestar-connections:eu-central-1:597729917624:connection/dc6afc73-154f-40dd-b475-73f2e6fc6bd0"
                                                #                                     ),
                                                input=CodePipelineSource.connection("MoeinGh/nexrshow-participants-managements", "master",
                                                                                    connection_arn="arn:aws:codestar-connections:eu-central-1::connection/60098faed96c"
                                                                                    ),
                                                commands=[
                                                    "/root/.pyenv/versions/3.9.5/bin/python -m pip install --upgrade pip",
                                                    "npm install -g aws-cdk",
                                                    "python -m pip install -r requirements.txt",
                                                    "cdk synth"]
                                                )
                                )

        table = dynamodb.Table(self, "tbl_survey",
                               partition_key=dynamodb.Attribute(
                                   name="id", type=dynamodb.AttributeType.STRING)
                               )

      

        # # create lambda function
        function = _lambda.Function(self, "send_steamkey",
                                    runtime=_lambda.Runtime.PYTHON_3_9,
                                    handler="lambda_handler.main",
                                    code=_lambda.Code.asset("./send_steamkey"))

        # create s3 bucket
        # s3 = _s3.Bucket(self, "s3bucket")

        # # create s3 notification for lambda function
        # notification = aws_s3_notifications.LambdaDestination(function)

        # # assign notification for the s3 event type (ex: OBJECT_CREATED)
        # s3.add_event_notification(_s3.EventType.OBJECT_CREATED, notification)

        # create lambda function
        function2 = _lambda.Function(self, "resend_steamkey",
                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                     handler="lambda_handler.lambda_handler",
                                     code=_lambda.Code.asset("./resend_steam_key"))

        function3 = _lambda.Function(self, "sending_survey_invitation_email",
                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                     handler="lambda_handler.lambda_handler",
                                     code=_lambda.Code.asset("./sending_survey_invitation_email"))

        function6 = _lambda.Function(self, "send_patchkit",
                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                     handler="lambda_handler.lambda_handler",
                                     code=_lambda.Code.asset("./send_patchkit"))

        api_patchkit = aws_apigateway.LambdaRestApi(self, "API_Patchkit",
                                           handler=function6,
                                           proxy=False
                                           )
        intgration6 = aws_apigateway.LambdaIntegration(function6)

        items_patchkit = api_patchkit.root.add_resource("patchkit")
        items_patchkit.add_method("ANY", intgration6)  # ANY /items

        # Survey app
        # defining api gatway for send email address

        # function4 = _lambda.Function(self, "sending_survey_form",
        #                              runtime=_lambda.Runtime.PYTHON_3_9,
        #                              handler="lambda_handler.lambda_handler",
        #                              code=_lambda.Code.asset("./survey_url"))

        # function5 = _lambda.Function(self, "submit_survey_form",
        #                              runtime=_lambda.Runtime.PYTHON_3_9,
        #                              handler="lambda_handler.lambda_handler",
        #                              code=_lambda.Code.asset("./submit_survey"))

        # Survey app with API
        # defining api gatway for send email address

        function7 = _lambda.Function(self, "webpage_survey_form",
                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                     handler="lambda_handler.lambda_handler",
                                     code=_lambda.Code.asset("./survey_url"))

        function8 = _lambda.Function(self, "submit_survey_form",
                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                     handler="lambda_handler.lambda_handler",
                                     environment={ # ADD THIS, FILL IT FOR ACTUAL VALUE 
                                                    "TABLE_NAME": "NexrshowParticipantsManagementsStack-tblsurveyD52BC641-1S6QI8314TK2C"
                                                    #  "TABLE_NAME": table.fromTableName
                                                     },
                                     code=_lambda.Code.asset("./submit_survey"))

        api = aws_apigateway.LambdaRestApi(self, "API_survey",
                                           handler=function7,
                                           proxy=False
                                           )
        intgration7 = aws_apigateway.LambdaIntegration(function7)

        items = api.root.add_resource("newsurvey")
        items.add_method("ANY", intgration7)  # ANY /items

        intgration8 = aws_apigateway.LambdaIntegration(function8)

        items2 = api.root.add_resource("submitsurvey")
        items2.add_method("ANY", intgration8)  # ANY /items

        table.grant_read_write_data(function8)


        # send email per each signupp of participant

        function20 = _lambda.Function(self, "send_per_part-patchkit",
                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                     handler="lambda_handler.lambda_handler",
                                     code=_lambda.Code.asset("./send_per_part-patchkit"))

        api_per_part_patchkit = aws_apigateway.LambdaRestApi(self, "API_per_part_Patchkit",
                                           handler=function20,
                                           proxy=False
                                           )
        intgration20 = aws_apigateway.LambdaIntegration(function20)

        items_per_part_patchkit = api_per_part_patchkit.root.add_resource("per_part_patchkit")
        items_per_part_patchkit.add_method("ANY", intgration20)  # ANY /items