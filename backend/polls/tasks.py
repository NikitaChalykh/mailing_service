import logging
import os
import time
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

from mailings.models import Contact, Mailing, Message

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.ERROR
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RETRY_TIME = 10
TIME_FORMAT = "%Y-%m-%d - %H:%M:%S"
SENDING_API_TOKEN = os.getenv("SENDING_API_TOKEN")


class MissingValueException(Exception):
    """
    Custom exception for missing environment variables.
    """


class GetAPIException(Exception):
    """
    Custom exception for API request failures.
    """


def send_api_message(message_id, contact, message):
    """
    Send a message via an external API.
    """

    headers = {"Authorization": f"Bearer {SENDING_API_TOKEN}"}
    json = {
        "phone": contact,
        "text": message
    }
    try:
        response = requests.post(
            f"https://probe.fbrq.cloud/v1/send/{message_id}".format(
                message_id=message_id
            ),
            headers=headers,
            json=json
        )
        logger.info("Message sent via external API")
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as error:
        logger.error(f"Message sending failure: {error}")
        return False


def start_mailings():
    """
    Main logic for processing mailings.
    """

    logger.debug("-----------------")
    message_id = [1]
    finished_mailing_id = []
    if SENDING_API_TOKEN is None:
        logger.critical("Missing environment variables!")
        raise MissingValueException("Missing environment variables!")
    while True:
        try:
            logger.debug("Starting new iteration")
            mailings = Mailing.objects.all()
            for mailing in mailings:
                current_datetime = datetime.now()
                if (
                    datetime.strptime(
                        mailing["start_send_time"], TIME_FORMAT
                    ) <= current_datetime
                    and datetime.strptime(
                        mailing["end_send_time"], TIME_FORMAT
                    ) >= current_datetime
                    and mailing["id"] not in finished_mailing_id
                ):
                    mailing_id = mailing["id"]
                    tag = mailing["tag"]
                    code = mailing["code"]
                    text = mailing["text"]
                    contacts = Contact.objects.filter(
                        tag=tag
                    ).filter(
                        code=code
                    )
                    for contact in contacts:
                        current_datetime = datetime.now()
                        contact_id = contact["id"]
                        if (
                            current_datetime <= datetime.strptime(
                                mailing["end_send_time"], TIME_FORMAT
                            ) and send_api_message(
                                message_id[0],
                                contact,
                                text
                            )
                        ):
                            Message.objects.create(
                                status="S",
                                mailing=mailing_id,
                                contact=contact_id
                            )
                        else:
                            Message.objects.create(
                                status="N",
                                mailing=mailing_id,
                                contact=contact_id
                            )
                        message_id[0] += 1
                    finished_mailing_id.append(mailing_id)
            logger.debug("End of iteration")
            logger.debug("-----------------")
            time.sleep(RETRY_TIME)
        except Exception as error:
            logger.error(f"Program failure: {error}")
            logger.debug("-----------------")
            time.sleep(RETRY_TIME)
