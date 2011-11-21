.. _request:

Request
=======

.. attribute:: request.env

    Return the current env.

.. method:: response.execute()

    Execute the query and return a ``Spyre.Respose`` object.

.. method:: response.host([host])

    If there is no argument, return the host. If host is passed as an arguement, set the new host and return its value.

.. method:: response.port([port])

    If there is no argument, return the port. If port is passed as an arguement, set the new port and return its value.

.. method:: response.script_name([script_name])

    If there is no argument, return the script_name. If script_name is passed as an arguement, set the new script_name and return its value.

.. method:: response.http_host()

    Return the full http host.

.. method:: response.scheme([scheme])

    If there is no argument, return the scheme. If scheme is passed as an arguement, set the new scheme and return its value.

.. method:: response.path([path])

    If there is no argument, return the path. If path is passed as an arguement, set the new path and return its value.

.. method:: response.base()

    Return the base url.
