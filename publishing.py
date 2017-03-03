from django.conf import settings

import requests
import twitter

class FacebookPublishingService:
  
  def __init__(self, profile):
    self.profile = profile
    self.base_url = "https://graph.facebook.com/v2.8/"

  def post_to_wall(self):
    url = self.base_url + self.profile.extra_data['id'] + "/feed"
    params = { 'access_token': self.profile.extra_data['access_token'], 'message': 'api test', 'link': "http://www.example.com" }
    response = requests.post(url, params=params)
    return response

  def get_groups(self):
    url = self.base_url + self.profile.extra_data['id'] + "/groups"
    params = { 'access_token': self.profile.extra_data['access_token'] }
    response = requests.get(url, params=params)
    return response

  def post_to_group(self, group_id='1783628805298621'):
    url = self.base_url + group_id + "/feed"
    params = { 'access_token': self.profile.extra_data['access_token'], 'message': 'api test', 'link': "http://www.example.com" }
    response = requests.post(url, params=params)
    return response

  def post_to_groups(self, group_ids=['1783628805298621']):
    for group in group_ids:
      self.post_to_group(group)
    return None

  def get_pages(self):
    url = self.base_url + self.profile.extra_data['id'] + "/accounts"
    params = { 'access_token': self.profile.extra_data['access_token'] }
    response = requests.get(url, params=params)
    return response

  def post_to_page(self, page_id='154745755042534'):
    url = self.base_url + page_id + "/feed"
    params = { 'access_token': self.profile.extra_data['access_token'], 'message': 'api test', 'link': "http://www.example.com" }
    response = requests.post(url, params=params)
    return response

  def post_to_pages(self, page_ids=['154745755042534', '643185905866111']):
    for page in page_ids:
      self.post_to_page(page)
    return None

  def post_to_all(self, group_ids=['1783628805298621'], page_ids=['154745755042534', '643185905866111']):
    self.post_to_wall()
    self.post_to_groups(group_ids)
    self.post_to_pages(page_ids)

class LinkedInPublishingService:

  def __init__(self, profile):
    self.profile = profile
    self.url = "https://api.linkedin.com/v1/people/~/shares?format=json"
    self.format_param = "?format=json"
    self.headers = { 'x-li-format': 'json', 'Authorization': "Bearer " + profile.extra_data['access_token'] }

  def share(self):
    data = {
      "comment": "API test",
      "content": {
        "description": "description",
        "title": "title",
        "submitted-url": "http://www.test.com"
      },
      "visibility": {
        "code": "connections-only"
      }
    }

    response = requests.post(self.url, headers=self.headers, json=data)
    return response

class TwitterPublishingService:

  def tweet(self, profile):
    api = twitter.Api(
      consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
      consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
      access_token_key=profile.extra_data['access_token']['oauth_token'],
      access_token_secret=profile.extra_data['access_token']['oauth_token_secret']
    )

    post = api.PostUpdate('testing')
    return post
