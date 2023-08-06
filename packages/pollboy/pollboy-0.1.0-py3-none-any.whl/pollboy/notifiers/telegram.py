from pollboy.logger import get_logger
from pollboy.config import Config
import requests

log = get_logger(__name__)
SEND_MESSAGE_URL = 'https://api.telegram.org/bot%s/sendMessage'

def strip_unsupported_html(text):
    repl_map = {
        '<p>': '',
        '<br>': '',
        '<br/>': '',
        '<br />': '',
        '</p>': '\n'
    }
    for token in repl_map:
        text = text.replace(token, repl_map[token])
    return text

def notify(feed_item, settings):
    log.debug('Sending telegram notification')
    url = SEND_MESSAGE_URL % (settings['token'])
    response = requests.post(url, data={
        'chat_id': settings['chat_id'],
        'text': strip_unsupported_html(feed_item.description),
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    })
    log.debug(f'Received status code {response.status_code}')
    if response.status_code > 300 or response.status_code < 200:
        log.error(response.json())