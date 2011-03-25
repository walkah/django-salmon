from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.xmlutils import SimplerXMLGenerator

ATOM_NS = 'http://www.w3.org/2005/Atom'


class SalmonAtom1Feed(Atom1Feed):
    def add_root_elements(self, handler):
        salmon = self.feed.get('salmon-endpoint')
        if salmon is not None:
            handler.addQuickElement(u'link', '', {u'rel': u'salmon',
                                                  u'href': salmon})
        super(SalmonAtom1Feed, self).add_root_elements(handler)


class SalmonAtom1EntryFeed(Atom1Feed):
    def __init__(self, title, link, description, author_name,
                 author_link, pubdate, **kwargs):
        """
        We don't create an atom:feed element, so don't force the caller
        to pass in the same kwargs as are required by Atom1Feed's constructor.
        Instead, mimic the signature of Atom1Feed.add_item with some stricter
        requirements (author and updated aren't optional elements in Atom 1.0).
        See: http://tools.ietf.org/html/rfc4287#section-4.1.2
        """
        super(SalmonAtom1EntryFeed, self).__init__(
            title=u'',
            link=u'',
            description=u'')
        self.add_item(title, link, description,
                      author_name=author_name,
                      author_link=author_link,
                      pubdate=pubdate, **kwargs)

    def item_attributes(self, item):
        """Put the Atom namespace into the entry element."""
        return {
            'xmlns': ATOM_NS,
        }

    def __unicode__(self):
        """Write out XML into a string buffer."""
        sb = StringIO()
        sb.write(u'<?xml version="1.0" encoding="utf-8"?>')
        handler = SimplerXMLGenerator(out=sb)
        self.write_items(handler)
        return sb.getvalue()


class SalmonFeed(Feed):
    feed_type = SalmonAtom1Feed

    def get_object(self, request):
        super(SalmonFeed, self).get_object(request)
        self._request = request

    def feed_extra_kwargs(self, obj):
        endpoint = self._request.build_absolute_uri(reverse('salmon_endpoint'))
        return {
            'salmon-endpoint': endpoint,
        }
