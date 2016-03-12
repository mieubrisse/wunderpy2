Overview
========
Wunderpy2 is a thin Python library for accessing `the official Wunderlist 2 API <https://developer.wunderlist.com/documentation>`_. What does a thin library mean here?

1. Only the bare minimum of error-checking to pass `the Wunderlist API specifications <https://developer.wunderlist.com/documentation>`_ is performed (e.g. there's no checking whether a task's title is empty, even though the Wunderlist web client enforces nonempty titles).
2. There aren't any 'convenience' functions, like getting a list by name instead of ID (that being said, I'll likely get tired of repeating the same things myself, write a few, and bundle them in a separate helper module).

Installation
============
::

    pip install wunderpy2

Usage & Examples
================
Getting a client
----------------
Wunderlist uses OAuth2 to allow applications to access users' data, so you'll need to `create an application <https://developer.wunderlist.com/apps>`_ before doing anything. If you only want to access your own Wunderlist, generate an access token after creating your application and use it and the client ID as follows::

    import wunderpy2
    api = wunderpy2.WunderApi()
    client = api.get_client(access_token, client_id)    # Fill in your values

If you want other Wunderlisters to use your application, you'll need to see the "Redirect users to request Wunderlist access" section of `the authorization docs <https://developer.wunderlist.com/documentation/concepts/authorization>`_ in order to get a temporary code when a user has authorized your app. Once you have the code, you only need one more step::

    api = wunderpy2.WunderApi()
    access_token = api.get_access_token(temporary_code, client_id, client_secret)   # Fill in your values here
    client = api.get_client(access_token, client_id)    # Fill in your client ID

Wunderlist Objects
------------------
All Wunderlist objects are merely Python objects with special keys. For convenience, these keys are laid out in a class format in :code:`model.py`. Note that not every object will have every key (e.g. List objects with type 'inbox' do not have creation metadata).

Examples
--------
Creating a task with a due date, note, 'starred' flag, and subtask::

    lists = client.get_lists()
    list = lists[0]
    task = client.create_task(1234, "My new task", due_date="2015-08-02", starred=True)
    client.create_note(task[wunderpy2.Task.ID], "My note")   
    client.create_subtask(task[wunderpy2.Task.ID], "My subtask")

Shuffling the order of tasks within a list (see `the Positions endpoint documentation <https://developer.wunderlist.com/documentation/endpoints/positions>`_)::

    import random
    task_positions_obj = client.get_task_positions_obj(list[wunderpy2.List.ID])
    ordering = task_positions_obj[wunderpy2.Task.VALUES]
    random.shuffle(ordering)
    client.update_task_positions_obj(task_positions_obj[wunderpy2.TaskPositionsObj.ID], task_positions_obj[wunderpy2.TaskPositionsObj.REVISION], ordering)

TODO 
====
* Endpoint implementation:
    * Avatar
    * File
    * File preview
    * Folder
    * Reminder
    * Task comment
    * Upload
    * User
    * Webhooks?
