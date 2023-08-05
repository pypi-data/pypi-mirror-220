import json
from typing import Any, Optional

from dynamodb.base import AbstractDynamoDB


class DynamoDB(AbstractDynamoDB):
    def get_user(self, *, external_id: str, profile: str) -> Any:
        data = {"id": external_id, "profile": profile}
        return self.get_item(key=data)

    def get_users(self) -> dict[str, Any]:
        response = self.table.scan()
        print(response)
        data = response.get("Items")

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data

    def create_user(
        self,
        *,
        profile: str,
        external_id: str,
        status: str,
    ) -> Any:
        data = dict(
            id=external_id,
            profile=profile,
            user_info=dict(status=status)
        )
        self.put_item(data=data)

    def update_user(
        self,
        *,
        profile: str,
        external_id: str,
        status: Optional[str] = None,
        messages: Optional[str] = None,
        emails: Optional[str] = None
    ) -> None:
        set_expression = ""
        if status:
            set_expression += "user_info.status = :status"
        if messages:
            set_expression += ", user_info.messages = :messages"
        if emails:
            set_expression += ", user_info.emails = :emails"

        attribute_values = {
            ":status": status,
            ":messages": messages,
            ":emails": emails
        }
        attribute_values = {k: v for k, v in attribute_values.items() if v is not None}
        self.table.update_item(
            Key={"id": external_id, "profile": profile},
            UpdateExpression=set_expression,
            ExpressionAttributeValues=attribute_values
        )

    def create_or_update(
        self,
        *,
        profile: str,
        external_id: str,
        status: str,
        messages: Optional[str] = None,
        emails: Optional[str] = None
    ):
        user = self.get_user(external_id=external_id, profile=profile)
        if not user:
            self.create_user(external_id=external_id, profile=profile, status=status)
        else:
            self.update_user(
                external_id=external_id,
                profile=profile,
                status=status,
                messages=messages,
                emails=emails
            )
