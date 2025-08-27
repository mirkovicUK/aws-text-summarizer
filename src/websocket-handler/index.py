# -----------------------------------------------------------
#    Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#    SPDX-License-Identifier: MIT-0

#    Permission is hereby granted, free of charge, to any person obtaining a copy of this
#    software and associated documentation files (the "Software"), to deal in the Software
#    without restriction, including without limitation the rights to use, copy, modify,
#    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#    permit persons to whom the Software is furnished to do so.

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
from decimal import Decimal
from botocore.exceptions import ClientError
from boto3 import dynamodb

CONNECTIONS_TABLE_NAME = os.environ.get("CONNECTIONS_TABLE_NAME")
RESULTS_TABLE_NAME = os.environ.get("RESULTS_TABLE_NAME")
API_REGION = os.environ.get("API_REGION")
API_ENDPOINT_URL = os.environ.get("WEBSOCKET_CALLBACK_URL")

ddb = boto3.resource("dynamodb")

apiManagement = boto3.client(
    "apigatewaymanagementapi", region_name=API_REGION, endpoint_url=API_ENDPOINT_URL
)

connections_table = ddb.Table(CONNECTIONS_TABLE_NAME)
results_table = ddb.Table(RESULTS_TABLE_NAME)


class UnableToAccessDatabaseException(Exception):
    pass


class NoAvailableResultsException(Exception):
    pass


def get_database_item(table, key):
    """Retrieve an item from a DynamoDB table using the provided key."""
    try:
        ddb_response = table.get_item(Key=key)
    except ClientError as error:
        msg = error.response["Error"]["Message"]
        print(msg)
        raise UnableToAccessDatabaseException(msg) from error
    return ddb_response


def lambda_handler(event, context):
    print("event:", event)
    currentExecutionArn = event.get("executionArn")
    database_key = {"ExecutionArn": currentExecutionArn}

    # implement a direct message to WebSocket connection function for initial skeleton implementation
    msg_override = event.get("msgOverride")

    if msg_override:
        result_item = {"message": msg_override}
    else:
        results_response = get_database_item(results_table, database_key)
        if not results_response.get("Item"):
            raise NoAvailableResultsException

        result_item = results_response["Item"]

    connections_response = get_database_item(connections_table, database_key)

    # no item indicates no WebSocket connection has been opened to send the result back to
    # this is an optional task and not an error condition, the workflow should continue.
    if not connections_response.get("Item"):
        print(
            "No WebSocket connection found for executionArn: ",
            connections_response,
        )
        return {"result_item": result_item, "sent_item": False}

    execution_websocket_connection = connections_response["Item"]["WsClientId"]
    # Convert Decimal to int for JSON serialization
    def decimal_converter(obj):
        if isinstance(obj, Decimal):
            return int(obj)
        raise TypeError
    
    result_item_json = json.dumps(result_item, default=decimal_converter)

    ws_response = apiManagement.post_to_connection(
        ConnectionId=execution_websocket_connection, Data=result_item_json
    )
    return {"result_item": result_item, "sent_item": True}
