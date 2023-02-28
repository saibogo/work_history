"""This module contain functions to send message to user from browser"""

from flask import render_template
from wh_app.config_and_backup.config import timeout_message, full_address


def generate_message_shutdown_server() -> str:
    """Create simple handler """
    return render_template('message_script_template.html',
                           full_address=full_address(), timeout_message=timeout_message())
