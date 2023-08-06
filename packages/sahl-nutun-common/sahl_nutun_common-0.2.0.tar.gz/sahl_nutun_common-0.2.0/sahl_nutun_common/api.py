""" Authentifi API class
"""

from attrs import define
from dotenv import load_dotenv
import httpx
import jwt
from rich import print

import base64
from datetime import datetime, timedelta
import os

import constants

load_dotenv()

API_VERSION = "1.13"
CBI_USECASES = [14]
CBI_DEFAULT_MESSAGE_TEMPLATE = 101
DEFAULT_FILENAME = "download.zip"


@define
class CBiClientInteractionReply:
    link: str
    request_id: str
    reference: str


@define
class CBiClientInteractionData:
    """Data required to initiate a CBi client interaction session"""

    customer_id_number: int
    customer_name: str
    customer_phone_number: str
    reference: str
    customer_id_type: constants.IDType = constants.IDType.IDNumber
    purpose: constants.CBiPurpose = constants.CBiPurpose.AffordabilityAssessment
    engagement_method: constants.EngagementMethod = (
        constants.EngagementMethod.CallCenter
    )
    message_template: int = CBI_DEFAULT_MESSAGE_TEMPLATE
    services: [constants.CBIService] = [
        constants.CBIService.TransactionHistory90,
        constants.CBIService.BankStatement90,
        constants.CBIService.Beneficiaries,
        constants.CBIService.AccountInfo,
        constants.CBIService.PersonalInfo,
        constants.CBIService.ContactInfo,
        constants.CBIService.Address,
    ]
    data_insight_services: [constants.CBiInsight] = [
        constants.CBiInsight.Affordability,
        constants.CBiInsight.DebitOrder,
        constants.CBiInsight.IncomeVerification,
        constants.CBiInsight.StrikeDate,
    ]

    def get_dict(self):
        return {
            "Request": {
                "CustomerReference": data.reference,
                "Surname": data.customer_name,
                "IdentityType": data.customer_id_type.value,
                "IdentityNumber": data.customer_id_number,
                "MobileNumber": data.customer_phone_number,
                "PurposeId": data.purpose.value,
                "EngagedCustomer": 1,
                "EngagementMethodId": data.engagement_method.value,
                "MessageTemplateId": data.message_template,
                "CBiServices": ",".join([f"{c.value}" for c in data.services]),
                "CBiDataInsightServices": ",".join(
                    [f"{c.value}" for c in data.data_insight_services]
                ),
                "UseCases": CBI_USECASES,
            },
        }


@define
class CBiClientInteractionResult:
    status: str
    file_written: bool = False
    file_name: str = None


@define(slots=False)
class AuthentifiAPI:
    username: str = os.getenv("API_USERNAME")
    password: str = os.getenv("API_PASSWORD")
    base_url: str = os.getenv("API_BASE_URL")
    usercode: str = os.getenv("API_USERCODE")
    debug: bool = False

    def __attrs_post_init__(self):
        self.token = None
        self.client = httpx.Client()
        self.client.headers = {
            "X-Version": API_VERSION,
        }
        self.authenticate()

    def authenticate(self):
        """Acquire a new token if the current token is None
        or will expire in less than 10 minutes
        """
        if self.token is None or (
            datetime.now()
            > (
                datetime.fromtimestamp(
                    jwt.decode(self.token, options={"verify_signature": False})["exp"]
                )
                - timedelta(minutes=10)
            )
        ):
            if self.debug:
                print("Token expiring soon or not set, renewing")
            data = {
                "username": self.username,
                "password": self.password,
                "accepttnc": 1,
            }
            res = self.client.post(
                f"{self.base_url}/user/authenticate",
                json=data,
            )
            self.token = res.json()["token"]
        else:
            if self.debug:
                print("Token not expiring soon, not renewing")

        if self.debug:
            print(f"Authentication Token: {self.token}")
        self.client.headers["Authorization"] = f"Bearer {self.token}"

    def initiate_client_interaction_whatsapp(
        self, data: CBiClientInteractionData
    ) -> str:
        self.authenticate()
        d = data.get_dict()
        d["Usercode"] = self.usercode
        d["Request"]["DeliveryMethod"] = constants.DeliveryMethod.WhatsApp.value

        res = self.client.post(
            f"{self.base_url}/Request/Process/",
            json=d,
            timeout=20,
        )
        res.raise_for_status()
        j = res.json()
        if self.debug:
            print(j)

        return CBiClientInteractionReply(
            link=j["cBi"]["landingPageURL"],
            request_id=j["requestId"],
            reference=j["customerReference"],
        )

    def retrieve_client_interaction_results(self, request_id, fn=None):
        self.authenticate()
        res = self.client.get(f"{self.base_url}/Request/View/{request_id}")
        res.raise_for_status()
        j = res.json()
        if self.debug:
            print(j)

        result = CBiClientInteractionResult(status=j["cBi"]["status"])
        if result.status == "FilesReady":
            # use the reference for the file name, or a fallback if that isn't given
            if fn is None:
                if j["customerReference"]:
                    fn = f'{j["customerReference"].lower().replace(" ", "").replace("-","")}.zip'
                else:
                    fn = DEFAULT_FILENAME
                result.file_name = fn
            with open(fn, "wb") as fh:
                fh.write(base64.b64decode(j["cBi"]["resultFile"]["file"]))
                result.file_written = True
        return result


if __name__ == "__main__":
    api = AuthentifiAPI(debug=True)

    if 0:
        data = CBiClientInteractionData(
            customer_id_number="8712195262086",
            customer_name="Kim van Wyk",
            customer_phone_number="0833844260",
            reference="test1",
        )
        res = api.initiate_client_interaction_whatsapp(data)
    if 1:
        res = api.retrieve_client_interaction_results(
            "0401f151-cc23-4c15-b20f-7be6aed5d0cf"
        )
    print(res)
