from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed


class SalmonAtom1Feed(Atom1Feed):
    def add_root_elements(self, handler):
        salmon = self.feed.get('salmon-endpoint')
        if salmon is not None:
            handler.addQuickElement(u'link', '', {u'rel': u'salmon',
                                                  u'href': salmon})
        super(SalmonAtom1Feed, self).add_root_elements(handler)


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
