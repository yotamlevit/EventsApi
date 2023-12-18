import sqlite3
import time
from datetime import datetime, timedelta
from threading import Thread
import pytz
from BL import EventManager


class EventReminder:
    def __init__(self, db_name='Application.db'):
        self.db_name = db_name
        self.stop_thread = False
        self.reminder_thread = Thread(target=self.run_reminder_thread)
        self.reminder_thread.start()
        self.event_manager = EventManager(1)

    def stop(self):
        self.stop_thread = True
        self.reminder_thread.join()

    def run_reminder_thread(self):
        while not self.stop_thread:
            try:
                self.send_event_reminders()
                time.sleep(60)  # Check for reminders every minute
            except Exception as e:
                print(f"Error in reminder thread: {str(e)}")

    def send_event_reminders(self):
        current_time = pytz.utc.localize(datetime.now())
        upcoming_events = self.get_upcoming_events()

        for event in upcoming_events:
            event_time = datetime.strptime(event['start_time'])
            if event_time - current_time <= timedelta(minutes=30):
                self.send_notification(event)

    def get_upcoming_events(self):
        try:
            #connection = sqlite3.connect(self.db_name)
            #cursor = connection.cursor()
            #cursor.execute(f"SELECT * FROM events WHERE start_time > ?", (current_time,))
            #upcoming_events = cursor.fetchall()
            return self.event_manager.get_upcoming_events()
        except sqlite3.Error as e:
            print(f"Error fetching upcoming events: {str(e)}")
            return []

    def send_notification(self, event):
        # Implement your notification logic here
        print(f"Sending reminder for event: {event['name']}")

if __name__ == '__main__':
    reminder = EventReminder()
    try:
        while True:
            pass  # Keep the main thread running
    except KeyboardInterrupt:
        reminder.stop()
