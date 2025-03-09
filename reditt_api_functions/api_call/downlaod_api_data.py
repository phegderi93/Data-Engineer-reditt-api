from datetime import datetime

from configs.credentials import reddit_login,api_call
import requests
import pandas as pd
from reditt_api_functions.logger.logger import logger
from reditt_api_functions.file_systems.convert_file import ConvertFile


class RedittApi:
    def __init__(self):
        self.login_data = reddit_login['login_data']
        self.headers = reddit_login['headers']
        self.auth = requests.auth.HTTPBasicAuth(reddit_login['client_id'], reddit_login['secret_key'])
        self.response = requests.post(reddit_login['auth'],auth=self.auth,data=self.login_data, headers=self.headers)
        self.token = self.response.json()['access_token']
        self.headers = {**self.headers, **{'Authorization': f'bearer {self.token}'}}

    def get_api_data(self):
        all_data = pd.DataFrame()
        logger.info("Getting data from Reddit API")
        for i in api_call:
            response = requests.get(reddit_login['url']+i,headers=self.headers,params={'limit':'50'})
            for post in response.json()['data']['children']:

                post_data = {
                    'subreddit': post['data']['subreddit'],
                    'author_fullname': post['data']['author_fullname'],
                    'created at': datetime.utcfromtimestamp(post['data']['created']),
                    'selftext': post['data']['selftext'],
                    'upvote_ratio': post['data']['upvote_ratio'],
                    'Post ID': post['kind'] + '_' + post['data']['id'],
                    'post_type': i
                }
                all_data = pd.concat([all_data, pd.DataFrame([post_data])], ignore_index=True)
            if len(all_data) > 0:
                convert = ConvertFile()
                convert.convert_to_csv(all_data, i)

        # return all_data
        #



