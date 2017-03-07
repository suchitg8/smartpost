import math, random, itertools, datetime

from django.contrib.auth.models import User
from simply_posted_accounts.models import Post
from simply_posted_calendar.models import Publication

class ContentSelectionService:

  def __init__(self, user):
    self.user = user
    self.profile = user.profile

  # A = Plan (number of total posts in a 42 day period, which is 6 weeks -- the posting schedule)
  def plan(self):
    plans = {
      'Entry': 12,
      'Basic': 12,
      'Pro': 42,
      'Enterprise': 84
    }

    plan = self.user.customer.subscription_set.all().first().plan
    return plans[plan.stripe_id]

  # B = Number of posts NOT from their website link. Result of Topical/Promotional Slider (a number determined in voice match input by customer)
  def number_of_posts_not_from_their_website(self):
    values = [None, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
    factor = values[int(self.profile.business_type)]
    return int(math.ceil(self.plan() * factor))

  # L = Result of General/Local slider
  def general_local_slider(self):
    values = list(range(6))
    selected_value = values[int(self.profile.market_type) - 1]

    if self.plan() == 12 or selected_value == 0:
      return selected_value
    else:
      return (selected_value * 2) + 2

  # C = Result of Playful/Corporate Slider
  def playful_percentage(self):
    values = [None, 0.9, 0.8, 0.6, 0.4, 0.2, 0.1]
    return values[int(self.profile.temp_type)]

  # D = Number of total posts to be pulled from the spreadsheets
  def number_of_total_posts(self):
    return self.number_of_posts_not_from_their_website() - self.general_local_slider()

  # E = Number of posts per category
  def posts_per_category(self):
    categories_count = len(self.profile.selected_categories)
    total = self.number_of_total_posts()

    res = [total / categories_count for i in range(categories_count)]
    if total % categories_count != 0:
      for i in range(total % categories_count):
        res[i] += 1

    return res

  def select_posts(self):
    posts = []

    for index, item in enumerate(self.posts_per_category()):
      category = self.profile.selected_categories[index]
      posts_in_category = Post.objects.filter(category=category).exclude(users=self.user)[:item]
      posts.append(posts_in_category)

    return list(itertools.chain.from_iterable(posts))

  def random_datetime(self):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=28)

    delta = end - start
    delta_timestamp = delta.days * 24
    hour = random.randrange(delta_timestamp)

    return start + datetime.timedelta(hours=hour)


  def make_publications(self):
    posts = self.select_posts()
    publications = Publication.objects.bulk_create([Publication(user=self.user, post=post, publication_date=self.random_datetime()) for post in posts])
    playful_count = int(math.ceil(len(publications) * self.playful_percentage()))

    for publication in random.sample(publications, playful_count):
      publication.corporate_title = False

    return publications
