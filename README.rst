=============
django-salmon
=============

This is ``django-salmon``, a drop-in `Django`_ application that adds support for the `Salmon Protocol`_. 

.. _Django: http://www.djangoproject.com/
.. _Salmon Protocol: http://www.salmon-protocol.org/salmon-protocol-summary

It doesn't work yet. Stay tuned though!

Instructions
------------

To use ``django-salmon``, add it to your ``INSTALLED_APPS`` in ``settings.py``: ::

   INSTALLED_APPS = (
       ...
       'salmon',
       ...
   )

You will need models to represent feeds and comments. Set up signals for your feed model: ::

   import salmon
   ...
   def salmon_subscriber(sender, **kwargs):
       feed = kwargs.get('instance', None)
       if not feed:
           return
       salmon.subscribe(feed, feed.url)
   post_save.connect(salmon_subscriber, sender=Feed) 

   def salmon_unsubscriber(sender, **kwargs):
       feed = kwargs.get('instance', None)
       if not feed:
           return
       salmon.unsubscribe(feed)
   post_delete.connect(salmon_unsubscriber, sender=Feed)

Set up the following signal for your comment model: ::

   def comment_handler(sender, **kwargs):
       comment = kwargs.get('instance', None)
       if not comment:
           return
       url = 'https://%s%s' % (
           Site.objects.get_current(),
           comment.get_absolute_url())
       feed = SalmonAtom1EntryFeed(
           comment.comment,
           url,
           comment.comment,
           author_name=comment.user_name,
           author_link='acct:' + comment.user_email,
           pubdate=comment.submit_date,
       )
       parent = comment.content_object
       salmon.slap(feed, parent.feed)
   post_save.connect(comment_handler, sender=Comment)

Because this is an incomplete package, in order to test the current functionality, you will need to add a private key to ``settings.py`` or equivalent: ::

   SALMON_USER_KEYPAIR = 'RSA.<modulus>.<public exponent>.<private exponent>'

To generate a sample key using `PyCrypto`_: ::

   import base64

   from Crypto import Random
   from Crypto.PublicKey import RSA
   from Crypto.Util import number

   rng = Random.new().read
   RSAkey = RSA.generate(1024, rng)

   encode = lambda a: base64.urlsafe_b64encode(number.long_to_bytes(a))

   exp = encode(RSAkey.n)
   private_exp = encode(RSAkey.d)
   mod = encode(RSAkey.e)
   print "RSA.%s.%s.%s" % (mod, exp, private_exp)

.. _PyCrypto: http://pycrypto.org/

** NOTE: ** This is a work in progress and at the moment is not functional.
