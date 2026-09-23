"""Live transfer for the GP booking call's Immediate tier (D-42).

`fake` returns the configured demo number and no token; the browser shows the
number, offers a tel: link, and records acknowledgement. `acs` issues an Azure
Communication Services user token so the browser's calling SDK can dial the duty
GP's number over PSTN with the patient still connected. The ACS path needs an ACS
resource and a purchased caller-id number; it is coded but untested without them.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class TransferSetup:
    provider: str
    transfer_number: str | None
    caller_id: str | None
    token: str | None
    user_id: str | None
    expires_on: str | None


class FakeTelephony:
    name = "fake"

    def setup(self) -> TransferSetup:
        return TransferSetup("fake", os.getenv("DEMO_TRANSFER_NUMBER") or None, None, None, None, None)


class AcsTelephony:
    name = "acs"

    def __init__(self) -> None:
        self.connection_string = os.getenv("ACS_CONNECTION_STRING", "")
        self.caller_id = os.getenv("ACS_CALLER_ID_NUMBER", "")

    def setup(self) -> TransferSetup:
        number = os.getenv("DEMO_TRANSFER_NUMBER") or None
        if not self.connection_string:
            return TransferSetup("acs:unconfigured", number, self.caller_id or None, None, None, None)
        try:
            from azure.communication.identity import CommunicationIdentityClient  # type: ignore

            client = CommunicationIdentityClient.from_connection_string(self.connection_string)
            user, token = client.create_user_and_token(scopes=["voip"])
            return TransferSetup("acs", number, self.caller_id or None, token.token, user.properties["id"], token.expires_on.isoformat())
        except Exception as exc:  # SDK missing or ACS error: fall back to the fake so the demo continues
            return TransferSetup(f"acs:error:{exc.__class__.__name__}", number, self.caller_id or None, None, None, None)


def get_telephony_provider():
    if os.getenv("TELEPHONY_PROVIDER", "fake").lower() == "acs":
        return AcsTelephony()
    return FakeTelephony()
