boxcomtools
===========

installing
----------

Usage
-----

box.com: get folder info
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from boxcomtools.box.client import Client

   client = Client(client_id, client_secret,
                   access_token, refresh_token)

   folder = client.folder()  # default value is "0"(root dir)
   folder_info = await folder.get()
   print(folder_info)


box.com: get file list
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    files = await folder.files
    
    for fi in files:
        print(await fi.get())


box.com: get metadata list
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    files = await folder.files
    
    for fi in files:
        print(await fi.get_metadata())

smartsheet: create sheet
~~~~~~~~~~~~~~~~~~~~

..code-block:: python
    s = Sheet(client)
    res = await s.create(data={
        'name': 'test_three',
        'columns': [
            {'title': 'col1', 'type': 'TEXT_NUMBER', 'primary': True},
            {'title': 'col2', 'type': 'TEXT_NUMBER'},
            {'title': 'col3', 'type': 'PICKLIST', 'options': ["one", 'two', 'three']}
        ]
    })
