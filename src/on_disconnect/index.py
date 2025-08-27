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
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

execution_table = os.environ.get("CONNECTIONS_TABLE_NAME")

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(execution_table)


class DatabaseException(Exception):
    pass


def lambda_handler(event, context):
    print(event)

    websocket_connectionId = event["requestContext"]["connectionId"]
    websocket_connection_index_name = table.global_secondary_indexes[0]["IndexName"]

    try:
        connection_query_resp = table.query(
            IndexName=websocket_connection_index_name,
            KeyConditionExpression=Key("WsClientId").eq(websocket_connectionId),
        )

        print("query_results", connection_query_resp)

        if connection_query_resp.get("Items"):
            item = connection_query_resp["Items"][0]
            print(item)
            execution_id = item["ExecutionArn"]
            table.delete_item(Key={"ExecutionArn": execution_id})
    except ClientError as error:
        raise DatabaseException from error
    else:
        return
