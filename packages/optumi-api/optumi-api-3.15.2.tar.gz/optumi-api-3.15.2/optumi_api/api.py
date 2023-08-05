##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .LoginServer import login as oauth_login
from .HoldoverTime import HoldoverTime
from .Workloads import Workloads
from requests.exceptions import ConnectionError

import phonenumbers

# Generic Operating System Services
import datetime, json, os
from typing import Union

# Optumi imports
import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    ServiceException,
    OptumiException,
)

DEBUG_LOGIN = False

# We will keep various lists from the controller in place of enums
_machines = None
_providers = None
_graphics_card_types = None


def machines():
    """Obtain the inventory of machines available from current cloud providers.

    Returns:
        list of str: The list of available machines where each element represents a machine provider and machine size, separated by a colon (':').
    """
    if _machines is None:
        _update_inventory_info()
    return _machines


def providers():
    """Obtain the list of current cloud providers.

    Returns:
        list of str: The list of cloud providers that are currently enabled for dyamic machine allocation.
    """
    if _providers is None:
        _update_inventory_info()
    return _providers


def graphics_card_types():
    """Obtain the list of current graphics cards.

    Returns:
        list of str: The list of GPU card types that are currently available in the machine inventory.
    """
    if _graphics_card_types is None:
        _update_inventory_info()
    return _graphics_card_types


def _update_inventory_info():
    global _machines, _providers, _graphics_card_types

    user_information = json.loads(optumi.core.get_user_information(True).text)

    _machines = []
    _providers = []
    _graphics_card_types = []

    for machine in user_information["machines"]:
        name = machine["name"]
        provider = name.split(":")[0]
        graphics_card_type = machine["graphicsCardType"]

        if not machine in _machines:
            _machines.append(name)

        if not provider in _providers:
            _providers.append(provider)

        if not graphics_card_type in _graphics_card_types:
            _graphics_card_types.append(graphics_card_type)

    _machines.sort()
    _providers.sort()
    _graphics_card_types.sort()


def login(
    connection_token=None,
    save_token=True,
):
    """Log in to the Optumi service platform.

    If a connection token is provided - as an argument or stored on the local disk - it will be leveraged to complete the login operation otherwise a new browser tab is opened to prompt the user for credentials.

    Args:
        connection_token (str, optional): A connection token (can be generated in the webapp). Defaults to None.
        save_token (bool, optional): Whether to store the connection token on disk. Defaults to True.

    Raises:
        NotLoggedInException: Raised if the login was not successful.
        OptumiException: Raised if the browser login could not be initiated.
    """
    dnsName = optumi.utils.get_portal()
    port = optumi.utils.get_portal_port()

    # On a dynamic machine we do not need to get an okta token
    if optumi.utils.is_dynamic():
        if DEBUG_LOGIN:
            print("Dynamic login")
        if not optumi.login.check_login(dnsName, port):
            if DEBUG_LOGIN:
                print("Not logged in")
            login_status, message = optumi.login.login_rest_server(
                dnsName,
                port,
                "",
                login_type="dynamic",
                save_token=save_token,
            )
    else:
        if DEBUG_LOGIN:
            print("Normal login")
        if not optumi.login.check_login(dnsName, port):
            if DEBUG_LOGIN:
                print("Not logged in")
            if connection_token == None:
                if DEBUG_LOGIN:
                    print("No connection token")
                if DEBUG_LOGIN:
                    print("Trying login with disk token")
                # Try to log in with the login token from the disk
                login_status, message = optumi.login.login_rest_server(dnsName, port, login_type="token", save_token=save_token)

                # Fall back on the browser login
                if login_status != 1:
                    if DEBUG_LOGIN:
                        print("Trying browser login")
                    try:
                        login_status, message = optumi.login.login_rest_server(
                            dnsName,
                            port,
                            oauth_login(),
                            login_type="oauth",
                            save_token=save_token,
                        )
                        if login_status != 1:
                            raise NotLoggedInException("Login failed: " + message)
                    except RuntimeError:
                        raise OptumiException(
                            "Unable to perform browser login from Notebook. Try logging in with a connection token as shown here: https://optumi.notion.site/Login-using-a-connection-token-710bccdeaf734cbf825aae94b79a8109"
                        )
            else:
                if DEBUG_LOGIN:
                    print("Connection token")
                login_status, message = optumi.login.login_rest_server(
                    dnsName,
                    port,
                    connection_token,
                    login_type="token",
                    save_token=save_token,
                )
                if login_status != 1:
                    raise NotLoggedInException("Login failed: " + message)

    user_information = json.loads(optumi.core.get_user_information(True).text)

    print("Logged in", user_information["name"])


def logout(remove_token=True):
    """Log out of the Optumi service platform, optionally removing any stored connection token.

    Args:
        remove_token (bool, optional): Whether to remove the connection token on logout. Defaults to True.
    """
    try:
        optumi.login.logout(remove_token=remove_token)
    except NotLoggedInException:
        pass


def get_phone_number():
    """Obtain the user's phone number.

    Returns:
        str: The user's international phone number, starting with a plus sign ('+') and the country code.
    """
    return json.loads(optumi.core.get_user_information(False).text)["phoneNumber"]


def set_phone_number(phone_number):
    """Prompt the user for a verification code and store the phone number in the user's profile.

    Args:
        phone_number (str): The international phone number that the user wants to store.

    Raises:
        OptumiException: Raised if the phone number is invalid or the verification code is incorrect.
    """
    if phone_number == "":
        optumi.core.clear_phone_number()
    else:
        number = phonenumbers.parse(phone_number, "US")
        if not phonenumbers.is_valid_number(number):
            raise OptumiException("The string supplied did not seem to be a valid phone number.")

        formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)

        optumi.core.send_verification_code(formatted_number)

        while True:
            code = input("Enter code sent to " + formatted_number + ": ")
            text = optumi.core.check_verification_code(formatted_number, code).text

            if text:
                print(text)
                # This is kind of sketchy but wont break if the message changes, it will just continue prompting the user for their code
                if text == "Max check attempts reached":
                    break
            else:
                optumi.set_user_information("notificationsEnabled", True)
                break


def get_holdover_time():
    """Obtain the current holdover time.

    The holdover time is the period of time that machines are retained (provisioned) after a workload finishes. Holdover time is global and applies to all workloads.

    Returns:
        The holdover time as an integer representing minutes.
    """
    res = optumi.core.get_user_information(False)
    return HoldoverTime(int(json.loads(optumi.core.get_user_information(False).text)["userHoldoverTime"]) // 60)  # Convert to minutes


def set_holdover_time(holdover_time: Union[int, HoldoverTime]):
    """Configure the holdover time.

    The holdover time is the period of time that machines are retained (provisioned) after a workload finishes. Holdover time is global and applies to all workloads.

    Args:
        holdover_time (Union[int, HoldoverTime]): The holdover time as either an integer representing minutes or a HoldoverTime object.
    """
    optumi.core.set_user_information(
        "userHoldoverTime",
        str(holdover_time.seconds if type(holdover_time) is HoldoverTime else holdover_time * 60),  # Convert to seconds
    )


def get_connection_token(forceNew=False):
    """Obtain a connection token.

    Args:
        forceNew (bool, optional): If true, generate a new connection token and return it, otherwise return the existing connection token. Defaults to False.

    Returns:
        A dictionary representing the connection token in the format {'expiration': '<ISO 8601 string>', 'token': '<token string>'}
    """
    return json.loads(optumi.core.get_connection_token(forceNew).text)


def redeem_signup_code(signupCode):
    """Redeem a signup code used to obtain access to the Optumi service platform.

    Args:
        signupCode (str): Signup code provided by Optumi.
    """
    optumi.core.redeem_signup_code(signupCode)


def send_notification(message, details=True):
    """Send a notification via text message to the phone number associated with the current user.

    Optionally, additional details about the workload can be attached to the end of the message.
    If no phone number is associated with the user, a warning message will be printed to console instead.

    Args:
        message (str): The message to send as a string.
        details (bool, optional): Whether to append details about the current workload (only applies when this function is called on a machine that was dynamically allocated by Optumi). Defaults to True.
    """
    if get_phone_number():
        try:
            optumi.core.send_notification("From " + str(Workloads.current()) + ": " + message if details and optumi.utils.is_dynamic() else message)
        except:
            optumi.core.send_notification(message)
    else:
        print("Unable to send notification - no phone number specified")
