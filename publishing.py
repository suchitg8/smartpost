from simply_posted_accounts.models import SocialProfile

from django.conf import settings

import requests
import twitter

class FacebookPublishingService:
  
  def __init__(self, profile, post):
    self.profile = profile
    self.facebook_data = SocialProfile.objects.get(social_auth=profile).facebook_data
    self.base_url = "https://graph.facebook.com/v2.8/"
    self.params = { 'access_token': profile.extra_data['access_token'], 'link': post.blog_link }

  def post_to_wall(self):
    url = self.base_url + self.profile.extra_data['id'] + "/feed"
    response = requests.post(url, params=self.params)
    return response

  def get_groups(self):
    url = self.base_url + self.profile.extra_data['id'] + "/groups"
    params = { 'access_token': self.profile.extra_data['access_token'] }
    response = requests.get(url, params=params)
    return response

  def post_to_group(self, group_id):
    url = self.base_url + group_id + "/feed"
    response = requests.post(url, params=self.params)
    return response

  def post_to_groups(self):
    group_ids = self.facebook_data['groups']

    for group in group_ids:
      self.post_to_group(group)
    return None

  def get_pages(self):
    url = self.base_url + self.profile.extra_data['id'] + "/accounts"
    params = { 'access_token': self.profile.extra_data['access_token'] }
    response = requests.get(url, params=params)
    return response

  def post_to_page(self, page_id):
    url = self.base_url + page_id + "/feed"
    response = requests.post(url, params=self.params)
    return response

  def post_to_pages(self):
    page_ids = self.facebook_data['pages']

    for page in page_ids:
      self.post_to_page(page)
    return None

  def post_to_all(self):
    self.post_to_wall()
    self.post_to_groups()
    self.post_to_pages()

class LinkedInPublishingService:

  def __init__(self, profile, post):
    self.profile = profile
    self.url = "https://api.linkedin.com/v1/people/~/shares?format=json"
    self.format_param = "?format=json"
    self.headers = { 'x-li-format': 'json', 'Authorization': "Bearer " + profile.extra_data['access_token'] }
    self.params = {
      "content": {
        "title": post.corporate_title,
        "submitted-url": post.blog_link
      },
      "visibility": {
        "code": "connections-only"
      }
    }

  def share(self):
    response = requests.post(self.url, headers=self.headers, json=self.params)
    return response

class TwitterPublishingService:

  def tweet(self, profile, post):
    api = twitter.Api(
      consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
      consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
      access_token_key=profile.extra_data['access_token']['oauth_token'],
      access_token_secret=profile.extra_data['access_token']['oauth_token_secret']
    )

    post = api.PostUpdate(post.corporate_title + " " + post.blog_link)
    return post
