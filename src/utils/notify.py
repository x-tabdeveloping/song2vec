import subprocess


def send_message(message: str) -> None:
    """
    Sends the given message as a Linux notification

    Parameters
    ----------
    message: str
        The message of the notification to send
    """
    subprocess.Popen(["notify-send", message])
