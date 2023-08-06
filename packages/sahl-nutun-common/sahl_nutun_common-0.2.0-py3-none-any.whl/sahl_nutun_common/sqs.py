from attrs import define
import boto3
from dotenv import load_dotenv
from rich import print

import json
import os


load_dotenv()


@define(slots=False)
class SQS:
    message_group_id: str
    access_key: str = os.getenv("AWS_ACCESS_KEY")
    secret_key: str = os.getenv("AWS_SECRET_KEY")
    queue_url: str = os.getenv("AWS_INITIATION_QUEUE_URL")
    region: str = os.getenv("AWS_REGION", "af-south-1")
    test: bool = False
    debug: bool = False

    def __attrs_post_init__(self):
        self.session = boto3.Session(
            aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key
        )
        self.sqs = self.session.resource(
            "sqs",
            region_name=self.region,
        )

        self.queue = self.sqs.Queue(self.queue_url)

    def send_data(self, data: dict):
        d = json.dumps(data)
        if self.test:
            print("Test enabled, will not send this data to sqs")
            print(d)
        else:
            response = self.queue.send_message(
                MessageBody=d,
                MessageGroupId=self.message_group_id,
            )

    def read_data(self, max_number_of_messages=10, timeout=5):
        results = self.queue.receive_messages(
            AttributeNames=["All"],
            MaxNumberOfMessages=max_number_of_messages,
            WaitTimeSeconds=timeout,
        )
        for r in results:
            r.delete()
        return [r.body for r in results]


if __name__ == "__main__":
    s = SQS(message_group_id="client-interaction-initiation")
    msgs = s.read_data(max_number_of_messages=5, timeout=5)
    print(msgs)
