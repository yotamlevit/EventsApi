import sqlite3
import time
from datetime import datetime, timedelta
import pytz
from BL import EventActions
from BL.Logger import Logger as logging
from .Utils import parse_event


def run_reminder_thread():
    try:
        while True:
            send_event_reminders()
            time.sleep(60)
    except Exception as e:
        print(f"Error in reminder thread: {str(e)}")


def send_event_reminders():
    current_time = pytz.utc.localize(datetime.now())
    upcoming_events = get_upcoming_events()

    for event in upcoming_events:
        event = parse_event(event)
        event_time = datetime.fromisoformat(event['start_time'])
        if event_time - current_time <= timedelta(minutes=31):
            send_notification(event)


def get_upcoming_events():
    try:
        event_manager = EventActions(1)
        events, _ = event_manager.get_upcoming_events()
        return events
    except sqlite3.Error as e:
        print(f"Error fetching upcoming events: {str(e)}")
        return []


def send_notification(event):
    # TODO send notification by - ERMAIL/SMS etc
    logging.info(f"Sending notification about upcoming event: {event}")
    print(f"Sending reminder for event: {event}")

