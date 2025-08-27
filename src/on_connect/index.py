# -----------------------------------------------------------
#    Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#    SPDX-License-Identifier: MIT-0
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy of this
#    software and associated documentation files (the "Software"), to deal in the Software
#    without restriction, including without limitation the rights to use, copy, modify,
#    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#    permit persons to whom the Software is furnished to do so.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------

import boto3
import os
import json
import traceback

connections_table = os.environ.get("CONNECTIONS_TABLE_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(connections_table)


def lambda_handler(event, context):
    try:
        print(event)
        event_body = json.loads(event["body"])
        executionArn = event_body["executionArn"]
        websocket_connectionId = event["requestContext"]["connectionId"]

        table.put_item(
            Item={"ExecutionArn": executionArn, "WsClientId": websocket_connectionId},
        )

    except Exception as e:
        err_msg = (
            "Error on connect, please check logs and ensure you have supplied valid body & executionArn parameters, error details:\n"
            + traceback.format_exc()
        )
        print(err_msg)
        return {
            "statusCode": 500,
            "body": err_msg,
        }

    return {"statusCode": 200, "body": "Connected"}
