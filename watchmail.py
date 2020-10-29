import time
import config
import mailbox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

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
                        messages.remove(k)
                        print(f'Message {k} remove')
                except:
                    print('error in processing mailbox')
                messages.close()

event_handler = MyFileSystemEventHandler()
observer = Observer()
observer.schedule(event_handler, config.DevConfig.MAILBOX_PATH, recursive=False)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()