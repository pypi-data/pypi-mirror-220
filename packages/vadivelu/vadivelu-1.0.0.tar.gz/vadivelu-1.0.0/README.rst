Vadivelu
========
A Python library for accessing the `Vadivelu API <https://vadivelu.anoram.com/>`_.

Installation
------------
**Must have Python 3.7 or higher**

.. code:: sh

    pip install vadivelu

API Reference
-------------

``vadivelu.get_available_formats(code)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Get the available formats for a HTTP code. The formats can be gif, jpg, or both.

Parameters
^^^^^^^^^^
code: ``int``
    The HTTP code to use

Returns
^^^^^^^
``Tuple[str, str]`` A tuple containing the avaiable formats

Raises
^^^^^^
``ValueError`` if the code provided is not supported by the API

``pick_available_format(code, priority)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pick a format (gif or jpg) that the API supports for a specific HTTP code.

Parameters
^^^^^^^^^^
code: ``int``
    The HTTP code to use
priority: ``str``
    The format to pick in the case both gif and jpg are available, defaults to gif

Returns
^^^^^^^
``str`` The chosen format (gif or jpg)

Raises
^^^^^^
``ValueError`` if the code provided is not supported by the API or if ``priority`` is not *gif* or *jpg*

``get_media_url(code, media_format)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Get the media URL for the specified code in the specified format.

Parameters
^^^^^^^^^^
code: ``int``
    The HTTP code to use
media_format: ``str``
    The media format to get (gif or jpg)

Returns
^^^^^^^
``str`` Theurl for the media

Raises
^^^^^^
``ValueError`` ``media_format`` is not available for the given code, use ``pick_available_format`` to avoid this error

Example
-------

.. code:: python

    import requests
    import vadivelu

    code = 404
    url = vadivelu.get_media_url(code, vadivelu.pick_available_format(code, 'jpg'))

    # save jpg to 404.jpg file
    with open('404.jpg', 'wb') as f:
        f.write(requests.get(url).content)
