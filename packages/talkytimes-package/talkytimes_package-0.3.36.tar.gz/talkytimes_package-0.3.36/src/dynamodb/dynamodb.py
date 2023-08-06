import json
from datetime import datetime
from typing import Any, Optional

from dynamodb.base import AbstractDynamoDB


class DynamoDB(AbstractDynamoDB):
    def get_user(self, *, external_id: str, profile: str) -> Any:
        data = {"id": external_id, "profile": profile}
        print(data)
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
        status: bool,
    ) -> Any:
        created_at = datetime.now().isoformat()
        data = dict(
            id=external_id,
            profile=profile,
            created_at=created_at,
            user_info=dict(user_status=status)
        )
        self.put_item(data=data)

    def update_user(
        self,
        *,
        profile: str,
        external_id: str,
        status: Optional[bool] = None,
        messages: Optional[int] = None,
        emails: Optional[int] = None
    ) -> None:
        updated_at = datetime.now().isoformat()
        set_expression = "SET "
        set_expression_list = []
        if status is not None:
            set_expression_list.append("user_info.user_status = :user_status")
        if messages is not None:
            set_expression_list.append("user_info.messages = :messages")
        if emails is not None:
            set_expression_list.append("user_info.emails = :emails")
        set_expression_list.append("updated_at = :updated_at")
        set_expression += ", ".join(set_expression_list)
        attribute_values = {
            ":user_status": status,
            ":messages": messages,
            ":emails": emails,
            ":updated_at": updated_at
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
        status: bool,
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
