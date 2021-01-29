import time
import config
import mailbox
import http.client
import json
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

class CatchTerm():
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.kill_now = False

    def exit_gracefully(self, signum, frame):
        print('Exit now!!!')
        self.kill_now = True

class MyFileSystemEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        print(f'Hello, you create a file {event.src_path}')

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            print(f'Hello you modify a file, {event.src_path}')
            mb = config.DevConfig.MAILBOX_PATH + '/' + config.DevConfig.MAIL_USER
            if event.src_path == mb:
                print('You have mailed me!')
                messages = mailbox.mbox(mb)
                try:
                    time.sleep(5)
                    messages.lock()
                    for k, m in messages.items():
                        print(f"Message {k} Subject {m['subject']}")
                        if m['subject']:
                            cmd_action = m['subject'].split(':')
                            if len(cmd_action) == 2:
                                cmd = cmd_action[0][:2]
                                action = cmd_action[1][:1]
                                print(f'{cmd} {action}')
                                self.create_cmd_action(cmd, action)
                        messages.remove(k)
                        print(f'Message {k} remove')
                except:
                    print('error in processing mailbox')
                messages.close()

    def create_cmd_action(self, cmd, action):
        conn = http.client.HTTPSConnection(config.DevConfig.AUTH0_DOMAIN)
        payload = config.DevConfig.PAYLOAD 
        headers = { "content-type": "application/x-www-form-urlencoded" }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        token = json.loads(data.decode('utf-8'))['access_token']
        print(f'{token}') 
        conn.close()

        try: 
            payload = {"cmd": cmd, "action": action}
            payload = json.dumps(payload)
            headers = { "content-type": "application/json",
                        "Authorization": "bearer " + token }
            conn = http.client.HTTPConnection(host = "rcontrol", port = 5000)
            conn.request("POST", "/cmd", payload, headers)
            res = conn.getresponse()
            data = res.read()
            conn.close()
        except Exception as e:
            print(e)


print('1', config.DevConfig.MAILBOX_PATH)
event_handler = MyFileSystemEventHandler()
observer = Observer()
observer.schedule(event_handler, config.DevConfig.MAILBOX_PATH, recursive=False)
observer.start()

catchterm = CatchTerm()
try:
    while not catchterm.kill_now:
        time.sleep(1)
except KeyboardInterrupt:
    pass
observer.stop()
observer.join()