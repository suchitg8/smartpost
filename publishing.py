from django.conf import settings

import requests
import twitter

def get_groups(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        url = "https://graph.facebook.com/v2.8/" + response['id'] + "/groups"
        params = { 'access_token': response['access_token'] }
        res = requests.get(url, params=params).json()
        response['groups'] = [group['id'] for group in res['data']]

def get_pages(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        url = "https://graph.facebook.com/v2.8/" + response['id'] + "/accounts"
        params = { 'access_token': response['access_token'] }
        res = requests.get(url, params=params).json()
        response['pages'] = [page['id'] for page in res['data']]

class FacebookPublishingService:
  
  def __init__(self, profile, post):
    self.profile = profile
    self.base_url = "https://graph.facebook.com/v2.8/"
    self.params = { 'access_token': profile.extra_data['access_token'], 'link': post.blog_link }

  def post_to_wall(self):
    url = self.base_url + self.profile.extra_data['id'] + "/feed"
    response = requests.post(url, params=self.params)
    return response

  def post_to_group(self, group_id):
    url = self.base_url + group_id + "/feed"
    response = requests.post(url, params=self.params)
    return response

  def post_to_groups(self):
    group_ids = self.profile.extra_data['groups']

    for group in group_ids:
      self.post_to_group(group)
    return None

  def post_to_page(self, page_id):
    url = self.base_url + page_id + "/feed"
    response = requests.post(url, params=self.params)
    return response

  def post_to_pages(self):
    page_ids = self.profile.extra_data['pages']

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

  def __init__(self, profile, post):
    self.post = post
    self.api = twitter.Api(
      consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
      consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
      access_token_key=profile.extra_data['access_token']['oauth_token'],
      access_token_secret=profile.extra_data['access_token']['oauth_token_secret']
    )

  def tweet(self):
    response = self.api.PostUpdate(self.post.corporate_title + " " + self.post.blog_link)
    return response

class PublishingService:

  def __init__(self, profiles, post):
    if profiles.filter(provider='facebook').first():
        self.facebook = FacebookPublishingService(profiles.get(provider='facebook'), post)
    if profiles.filter(provider='linkedin-oauth2').first():
        self.linkedin = LinkedInPublishingService(profiles.get(provider='linkedin-oauth2'), post)
    if profiles.filter(provider='twitter').first():
        self.twitter  = TwitterPublishingService(profiles.get(provider='twitter'), post)

  def publish_post(self):
    if hasattr(self, 'facebook'):
        self.facebook.post_to_all()
    if hasattr(self, 'linkedin'):
        self.linkedin.share()
    if hasattr(self, 'twitter'):
        self.twitter.tweet()

