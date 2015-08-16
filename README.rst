Overview
========
Wunderpy2 is a thin Python library for accessing `the official Wunderlist 2 API <https://developer.wunderlist.com/documentation>`_. What does a 'thin' library mean here?

1. Only the bare minimum of error-checking to pass `the Wunderlist API specifications <https://developer.wunderlist.com/documentation>`_ is performed (e.g. there's no checking whether a task's title is empty, even though the Wunderlist web client enforces nonempty titles)
2. There aren't any 'convenience' functions (e.g. get a list by its name)

These choices were made intentionally, so as to avoid getting mired in fancy feature requests.

Installation
============
::

    pip install wunderpy2

Usage & Examples
================
Getting a client
----------------
Wunderlist uses OAuth2 to allow applications to access users' data, so you'll need to `create an application <https://developer.wunderlist.com/apps>`_ before doing anything. If you only want to access your own Wunderlist, generate an access token after creating your application and use it and the client ID as follows::

    api = wunderpy.WunderApi()
    client = api.get_client(access_token, client_id)    # Fill in your values

If you want other Wunderlisters to use your application, you'll need to see the "Redirect users to request Wunderlist access" section of `the authorization docs <https://developer.wunderlist.com/documentation/concepts/authorization>`_ in order to get a temporary code when a user has authorized your app. Once you have the code, you only need one more step::

    api = wunderpy.WunderApi()
    access_token = api.get_access_token(temporary_code, client_id, client_secret)   # Fill in your values here
    client = api.get_client(access_token, client_id)    # Fill in your client ID

TODO 
====
* Implement the following endpoints:
    * Avatar
    * File
    * File preview
    * Folder
    * Positions
    * Reminder
    * Subtask
    * Task comment
    * Upload
    * User
    * Webhooks?
