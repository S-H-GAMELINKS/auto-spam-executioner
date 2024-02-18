from mastodon import Mastodon, StreamListener
from dotenv import load_dotenv
import os
import pprint
import time
import urllib.error
import urllib.request
import datetime

# .envの読み込み
load_dotenv()

# Mastodonのクライアント生成
client = Mastodon(api_base_url = os.environ['API_BASE_URL'], access_token = os.environ['ACCESS_TOKEN'])

# 連合タイムラインをListenするためのクラスを定義
class PublicStreamListener(StreamListener):

    # 引数に生成したMastodonのクライアントが必須
    def __init__(self, client):
        super(PublicStreamListener, self).__init__()
        self.client = client

    def handle_stream(self, response):
        try:
            super().handle_stream(response)
        except:
            pass

    def on_update(self, status):
        try:
            if len(status.mentions) > int(os.environ['MEMTION_COUNT']) and status.account.acct.find('@') > 0 and status.account.followers_count == 0:
                statusID = status.id
                account = status.account
                report = self.client.report(account.id, status_ids=[statusID])
                self.client.admin_account_moderate(account.id, 'suspend', report_id=report.id)

        except Exception as e:
            print(e)
            pass

# 連合タイムラインのListenerを生成            
public_stream_listener = PublicStreamListener(client)

# 連合タイムラインをListen
client.stream_public(public_stream_listener, remote=True)
