import time
from atproto_client.models.app.bsky.notification.list_notifications import Notification
from src import client
from datetime import datetime

SYS_MESSAGE_PREFIX = "[Listener]: "
NOTIFICATIONS_PROCESS_DELAY_SECONDS = 3

class DRBListener:
    def __init__(self, cli: client.DRBClient):
        self.cli = cli
        self.shutdown_signal = False
        username = self.cli \
            .handle \
            .split(".")[0]
        self.name = f"LSTNR-{username}"
        print(SYS_MESSAGE_PREFIX + f"Listener for client initialized: {self.name}")

    def listen(self) -> None:
        bsky_client = self.cli.cli
        unread: list[Notification] = list()
        print(SYS_MESSAGE_PREFIX + f"Now listening for tags to {self.cli.name} every {NOTIFICATIONS_PROCESS_DELAY_SECONDS} seconds")

        while not self.shutdown_signal:
            time.sleep(NOTIFICATIONS_PROCESS_DELAY_SECONDS)
            response = bsky_client.app.bsky.notification.list_notifications()
            last_seen_time = bsky_client.get_current_time_iso()

            for notif in response.notifications:
                if not notif.is_read and notif.reason == "mention":
                    unread.append(notif)

            if len(unread) == 0:
                print(SYS_MESSAGE_PREFIX + "No new tags in notifications.")
            else:
                for notif in unread:
                    self.cli.make_reply(notif.cid, notif.uri)
                unread.clear()

            print(SYS_MESSAGE_PREFIX + f"Notifications processed at {last_seen_time}")
            bsky_client.app.bsky.notification.update_seen({'seen_at': last_seen_time})

    def shutdown(self):
        self.shutdown_signal = True

    def __str__(self) -> str:
        return f"""{self.name}
    Assigned to: {self.cli.name}
    Is running: {not self.shutdown_signal}
                """
