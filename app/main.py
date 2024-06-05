from . import cloudesire_client
from enum import Enum
from fastapi import FastAPI, status
import logging
from pydantic import BaseModel


class EventType(str, Enum):
    created = "CREATED"
    modified = "MODIFIED"
    deleted = "DELETED"


class EventNotification(BaseModel):
    entity: str
    id: int
    type: EventType


app = FastAPI()
logger = logging.getLogger("uvicorn.error")


@app.post("/event", status_code=status.HTTP_204_NO_CONTENT)
def handle_event(event: EventNotification):
    logger.info(
        "Received notification for %s with id %s of type %s",
        event.entity,
        event.id,
        event.type,
    )

    if event.entity != "Subscription":
        logger.debug("Skipping %s events", event.entity)
        return

    subscription = cloudesire_client.get_subscription(event.id)

    match event.type:
        case EventType.created | EventType.modified:
            subscription_deploy(subscription)
        case EventType.deleted:
            subscription_undeploy(subscription)


def subscription_deploy(subscription: dict):
    match subscription["deploymentStatus"]:
        case "PENDING":
            if subscription["paid"]:
                logger.info("Provision tenant resources")
                cloudesire_client.update_status(subscription["id"], "DEPLOYED")
        case "STOPPED":
            logger.info("Temporarily suspend the subscription")
        case "DEPLOYED":
            logger.info("Check if tenant is OK")


def subscription_undeploy(subscription: dict):
    logger.info("Unprovision tenant and release resources")
    cloudesire_client.update_status(subscription["id"], "UNDEPLOYED")
