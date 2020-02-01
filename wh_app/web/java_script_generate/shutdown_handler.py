from wh_app.config_and_backup.config import timeout_message, full_address


def generate_message_shutdown_server() -> str:
    """Create simple handler """

    result = list()
    result.append('<script type="text/javascript">')
    result.append('function handl() {')
    result.append('var xhr = new XMLHttpRequest();')
    result.append('xhr.open("GET", "{0}/server-ready-to-shutdown", false);'.format(full_address))
    result.append('xhr.send();')
    result.append('if (xhr.responseText) {')
    result.append('alert( xhr.responseText ); }')
    result.append('}')
    result.append('setInterval(handl, {0});'.format(timeout_message))
    result.append('</script>')
    return "\n".join(result)
