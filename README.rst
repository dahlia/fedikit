FediKit: A Pythonic interface to the fediverse
==============================================

This package is a Pythonic interface to the fediverse, a collection of
federated social networks through ActivityPub and other standards.
You maybe already know some of the networks in the fediverse,
such as Mastodon, Misskey, GNU social, Pixelfed, PeerTube, and so on.
It aims to offer an easy way to build a fediverse software (server or client)
in Python.

It is still in early development, and the API is not stable yet.
The rough roadmap is to implement the following features out of the box:

- Python objects for `Activity Vocabulary`_ (including some community
  extensions)
- `HTTP Signatures`_
- ASGI middleware and application for ActivityPub_
- ActivityPub_ client
- Special touch for interoperability with Mastodon and few other
  popular fediverse software

.. _Activity Vocabulary: https://www.w3.org/TR/activitystreams-vocabulary/
.. _HTTP Signatures: https://tools.ietf.org/html/draft-cavage-http-signatures-12
.. _ActivityPub: https://www.w3.org/TR/activitypub/
