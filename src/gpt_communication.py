import json
from openai import OpenAI
import os
def extract_transformations_from_response(response):
    if isinstance(response, dict):
        return response.get("transformations", [])
    else:
        print("Invalid format of response")
        return []

def get_transformations_from_gpt(user_query: str) -> list[list[dict]]:
    key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=key)

    transformations_schema = {
        "name": "transformations_schema",
        "schema": {
            "type": "object",
            "properties": {
                "transformations": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "operation": {
                                    "type": "string",
                                    "description": "The operation to perform, e.g. 'filter' or 'select'."
                                },
                                "column": {
                                    "type": "string",
                                    "description": "Column name for filter operation"
                                },
                                "operator": {
                                    "type": "string",
                                    "description": "Operator for filter, e.g. ==, !=, >, <, >=, <="
                                },
                                "value": {
                                    "type": ["string", "number", "boolean"],
                                    "description": "Filter value (could be string, int, float, or boolean)"
                                },
                                "columns": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "List of column names for 'select' operation"
                                }
                            },
                            "required": ["operation"],
                            "additionalProperties": False
                        }
                    }
                }
            },
            "required": ["transformations"],
            "additionalProperties": False
        }
    }

    messages = [
        {
            "role": "developer",
            "content": (
                """You are a helpful assistant that returns a structured JSON array of arrays of transformations.

            We have a special format:
            - "transformations" is an array of sub-arrays.
            - Each sub-array can contain zero or more "filter" operations, combined with AND logic within that sub-array.
            - If the user's prompt implies multiple disjunctive conditions (logical OR), we should produce multiple sub-arrays, each sub-array containing the ANDed filters for one branch of the OR.
            - If the user requests a final set of columns, place a "select" operation in a separate sub-array (usually the last one) to pick only the requested columns. If the user does not specify columns to select, you may omit the "select" operation or return all columns.
            - Always output valid JSON that follows the transformations_schema, which is an array of arrays of transformation objects. Each transformation object must have an 'operation' field. For a filter operation, include 'column', 'operator', and 'value'. For a select operation, include 'columns'.

            Example:
            If the user says: "Show me rows where (age>30 AND salary>50000) OR department==\"HR\", then select columns [\"name\", \"department\"]",
            we should produce something like:
            {
            "transformations": [
                [
                {"operation": "filter", "column": "age", "operator": ">", "value": 30},
                {"operation": "filter", "column": "salary", "operator": ">", "value": 50000}
                ],
                [
                {"operation": "filter", "column": "department", "operator": "==", "value": "HR"}
                ],
                [
                {"operation": "select", "columns": ["name", "department"]}
                ]
            ]
            }

            If the user only gives AND filters with no mention of columns to select, you can put them all into a single sub-array of filters and return no 'select' sub-array. If the user states multiple conditions joined by OR, create multiple filter sub-arrays. If the user wants multiple columns, list them in a single 'select' operation or multiple if needed. 
            Always respond with well-formed JSON and no additional commentary.
                """
            )
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": transformations_schema
        }
    )
    
    print("Received transformations:")
    print(response.choices[0].message.content)
    print()
    
    js = json.loads(response.choices[0].message.content)
    transformations = extract_transformations_from_response(js)
    return transformations