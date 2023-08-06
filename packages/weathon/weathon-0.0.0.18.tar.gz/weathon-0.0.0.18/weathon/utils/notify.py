import requests
from weathon.dl.utils.constants import BARK_WEBHOOK_URL


def send_message(title: str = "", description: str = "", content: str = "",
                 webhook_url=BARK_WEBHOOK_URL):
    if webhook_url:
        try:
            data = {
                "title": title,
                "description": description,
                "content": content,
            }
            res = requests.post(url=webhook_url, json=data)
            if res.status_code != 200:
                print(f'response code {res.status_code}! , Failed to send message.')
        except Exception as e:
            print(f'Failed to send message.{e.args}')


if __name__ == "__main__":
    title = "is_activate"
    description = title
    content = title
    send_message(title, description, content)
