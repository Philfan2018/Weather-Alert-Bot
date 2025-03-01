import feedparser
from plyer import notification
import time
import os

url = "https://weather.im/iembot-rss/room/botstalk.xml"
checked_entries = set()

Severe_thunderstorm_watch_issued = "issues Severe Thunderstorm Watch"
Severe_thunderstorm_watch_update = "updates Severe Thunderstorm Watch"
Severe_thunderstorm_warning_issued = "issues Severe Thunderstorm Warning"
Severe_thunderstorm_warning_continued = "continues Severe Thunderstorm Warning"
Severe_thunderstorm_warning_updated = "updates Severe Thunderstorm Warning"

Tornado_watch_issued = "issues Tornado Watch"
Tornado_watch_update = "updates Tornado Watch"
Tornado_warn_issued = "issues Tornado Warning"
Tornado_warn_continue = "continues Tornado Warning"
Tornado_warn_update = "updates Tornado Warning"

def New_severe_weather_alert(Type_of_alert):
    notification.notify(
    title="New Weather Alert",
    message= f"{Type_of_alert}! Check the console",
    app_name='Weather Alert',
    timeout=10  # Duration in seconds
    )
    print(title)
    print(entry.link)

while True:
    os.system("cls")
    feed = feedparser.parse(url)
    new_entries = []

    for entry in feed.entries:
        if entry.link not in checked_entries:
            new_entries.append(entry)
            checked_entries.add(entry.link)

    for entry in new_entries:
        title = entry.title
        summary = entry.summary

        if Severe_thunderstorm_watch_issued in title:
            New_severe_weather_alert("New Severe Thunderstorm Watch Issued")
        elif Severe_thunderstorm_watch_update in title:
            New_severe_weather_alert("Severe Thunderstorm Watch updated")
        elif Severe_thunderstorm_warning_issued in title:
            New_severe_weather_alert("New Severe Thunderstorm Warning issued")
        elif Severe_thunderstorm_warning_continued in title:
            New_severe_weather_alert("continues Severe Thunderstorm Warning")
        elif Severe_thunderstorm_warning_updated in title:
            New_severe_weather_alert("Severe Thunderstorm Warning Updated")
        elif Tornado_watch_issued in title:
            New_severe_weather_alert("New Tornado Watch issued")
        elif Tornado_watch_update in title:
            New_severe_weather_alert("Tornado Watch Updated")
        elif Tornado_warn_issued in title:
            New_severe_weather_alert("New Tornado Warning issued")
        elif Tornado_warn_continue in title:
            New_severe_weather_alert("A Tornado Warning has been continued")
        elif Tornado_warn_update in title:
            New_severe_weather_alert("Tornado Warning updated")

    # Wait for a certain period before checking again (e.g., 5 minutes)
    time.sleep(60)
