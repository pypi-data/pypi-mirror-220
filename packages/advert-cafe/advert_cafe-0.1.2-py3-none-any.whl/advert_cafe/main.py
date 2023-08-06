import logging

import netifaces as nif
import requests
from requests.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError

logger = logging.getLogger("advertcafe")


def mac_for_ip(ip):
    "Returns a list of MACs for interfaces that have given IP, returns None if not found"
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)
        try:
            if_mac = addrs[nif.AF_LINK][0]["addr"]
            if_ip = addrs[nif.AF_INET][0]["addr"]
        except (IndexError, KeyError):  # ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None


def ip_finder(request):
    """
    Finds the
    """
    try:
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            ip_address = request.environ["REMOTE_ADDR"]
        else:
            ip_address = request.environ["HTTP_X_FORWARDED_FOR"]  # if behind a proxy
        return ip_address
    except Exception as e:
        logger.error(e)
        return None


def payload_creator(
    request,
    user_id,
    event_type=None,
    path=None,
    event_url=None,
    event_source=None,
    app_name="test",
):
    ip_address = ip_finder(request)
    mac_address = mac_for_ip(ip_address)
    data = {
        "schema_version": 1,
        "user_id": str(user_id),
        "mac_address": mac_address,
        "ip_address": ip_address,
        "headers": {k: v for k, v in request.headers.items()},
        "event_type": event_type,
        "path": path,
        "event_url": event_url,
        "event_source": event_source,
        "app_name": app_name,
        "backend_status": 200,
        "base_url": request.base_url,
    }
    payload = {"data": data, "user_id": data["user_id"], "app_name": "test"}
    return payload


def advert_cafe_event_push(payload: dict, advert_cafe_url: str = None):
    """
    Events created in the app will be saved in advert.cafe
    Simply define a payload and it will save it.
    """
    logger.debug(payload)
    if advert_cafe_url is None:
        logger.error("No advert_cafe_url is provided")
        return ModuleNotFoundError
    if payload is None:
        logger.error("no payload supplied")
        return
    try:
        requests.post(advert_cafe_url, json=payload)
    except (ConnectionError, NewConnectionError) as e:
        logger.error(f"Got an advert error: {e}")
