.. _response:

Response
========

.. attribute:: response.status

    Return the status of the request.

.. attribute:: response.status

    Same as ``response.status``.

.. attribute:: response.content

    Return the body of the response. This body may be modified by a middleware.

.. attribute:: response.body

    Same as ``response.content``.

.. attribute:: response.body

    Return the **raw** body of the response. This body is **never** modified by a middleware.

.. attribute:: response.content_type

    Return the content type of the response.

.. attribute:: response.content_length

    Return the lenght of the **raw body**.

.. attribute:: response.is_success

    Return ``True`` if the status of the response is **2xx**.

.. method:: response.header(header_name)

    Return the value of the given header. Return ``None`` if this header does not exists.

.. method:: response.headers()

    Return the list of headers for the response.
