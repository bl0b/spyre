.. _getting_started:

Getting started: How to use spyre
=================================

To use ``spyre``, you'll need some API descriptions. You can find some on the `official repository <https://github.com/SPORE/api-description>`_


Creating your first client
--------------------------

For this tutorial, we will use the GitHub API. You can find the description of the API on the repository.

    >>> client = Spyre.new_from_spec('tests/specs/api.json')
    >>> user = client.get_user_info(username='franckcuny')
    >>> print user.content
    {"type":"User","location":"San Francisco","hireable":false,"followers":91,"company":"SAY Media","email":"franck.cuny@gmail.com","bio":null,"following":77,"avatar_url":"https://secure.gravatar.com/avatar/7d5e23c5839c464c42d0d49f1c954abb?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png","html_url":"https://github.com/franckcuny","url":"https://api.github.com/users/franckcuny","public_repos":111,"public_gists":72,"created_at":"2009-03-02T08:12:31Z","name":"franck","gravatar_id":"7d5e23c5839c464c42d0d49f1c954abb","id":59291,"login":"franckcuny","blog":"http://lumberjaph.net/"}

Applying a middleware
---------------------

Middleware are here to handle specific tasks in the process of a request.

    >>> client.enable('formatjson')
    >>> user = client.get_user_info(username='franckcuny')
    >>> print user.content
    {u'public_repos': 111, u'public_gists': 72, u'name': u'franck', u'created_at': u'2009-03-02T08:12:31Z', u'url': u'https://api.github.com/users/franckcuny', u'company': u'SAY Media', u'html_url': u'https://github.com/franckcuny', u'id': 59291, u'blog': u'http://lumberjaph.net/', u'hireable': False, u'avatar_url': u'https://secure.gravatar.com/avatar/7d5e23c5839c464c42d0d49f1c954abb?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png', u'followers': 91, u'location': u'San Francisco', u'bio': None, u'gravatar_id': u'7d5e23c5839c464c42d0d49f1c954abb', u'following': 77, u'login': u'franckcuny', u'type': u'User', u'email': u'franck.cuny@gmail.com'}

or, if you want to enable the middleware only for a specific case

    >>> client.enable_if('formatjson')
