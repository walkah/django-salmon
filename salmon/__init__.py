import urllib
import feedparser

from salmon.models import Subscription


def discover(url):
    d = feedparser.parse(url)
    weblinks = getattr(d.feed, 'links', [])
    for link in weblinks:
        if link.has_key('rel') and link['rel'] == 'salmon':
            if link.has_key('href'):
                return link['href']
    return None


def subscribe(obj, feed_url):
    salmon_endpoint = discover(feed_url)
    if not salmon_endpoint:
        return None
    return Subscription.objects.subscribe(obj, salmon_endpoint)


def unsubscribe(obj):
    Subscription.objects.unsubscribe(obj)


def slap(content, source):
    sub = Subscription.objects.get_for_object(source)
    if sub:
        # just post some test data right now
        urllib.urlopen(sub.salmon_endpoint, urllib.urlencode(dict(foo='bar')))
