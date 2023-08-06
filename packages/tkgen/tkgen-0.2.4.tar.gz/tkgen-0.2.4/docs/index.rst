.. tkgen documentation master file, created by
   sphinx-quickstart on Wed Mar  8 10:51:49 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to tkgen's documentation!
=================================

About
-----

`tkgen` is a python package that automatically generate a Tkinter form window
from a `Pyskema <https://pypi.org/project/pyskema/>`_ schema. It provides a
simple interface to initialize the window and collect the data inputed by
users. The data is provided as python basic objects (lists, tuples,
dictionaries, integers, floats, boolean and strings) that would be valid
regarding the schema. It depends on tkinter and Pyskema.

Installation
------------

Use :code:`pip install tkgen`.

Usage
-----

The main entrypoint of this package is the function :py:func:`tkgen.form.make_form`.
Here is a minimal exemple of its usage:

.. code:: python

    from tkgen import make_form
    from pyskema import Node, AtomType

    schema = Node.of_record({
        "a": Node.of_atom(AtomType.INT),
    })

    win = make_form(schema, print)
    win.mainloop()

The first parameter of :py:func:`tkgen.form.make_form` (the model) is the schema that define the form.
The second parameter (the callback) is a function to be called when the form is submitted.
The callback is passed a single argument which is either None (if the user pressed cancel) or the data inputed.
This dictionary mirror the structure of the model.

Extracting data
---------------

Once the form is filled, you want to access its data.
This is done through the callback parameter of :py:func:`tkgen.form.make_form`.
This callback is an arbitrary function you should provide that will receive the data in the form of a dictionary.

Here is a simple example of saving the data in an arbitrary json file:

.. code:: python

    import json
    from tkgen import make_form
    from pyskema import Node, AtomType

    model = Node.of_record({
        "filename": Node.of_atom(AtomType.STR),
        "Plumbus": Node.of_record({
            "number of schleem": Node.of_atom(AtomType.STR),
            "length of dinglepop": Node.of_atom(AtomType.FLOAT),
            "color of fleeb": Node.of_atom(AtomType.OPTION, [
                "pink",
                "red",
                "octarine",
            ]),
        }),
    })

    def save_data(result):
        filename = result["filename"]
        data = result["Plumbus"]
        with open(filename, "w") as f:
            json.dump(f, data)

    win = make_form(model, save_data)
    win.mainloop()

Loading data
------------

You may want to be able to load back some data from a previous instance of the form.
This is possible thanks to the `init_data` optional parameter.
For simplicity it is also possible through the optional `data` parameter of `make_form`.

If you were to use the previous example and save a file named *plumbus.json*, the following example would load data from the json file and produce a filled form identical to what it looked when you saved the file.

.. code:: python

    import json
    from tkgen import make_form
    from pyskema import Node, AtomType

    model = Node.of_record({
        "filename": Node.of_atom(AtomType.STR),
        "Plumbus": Node.of_record({
            "number of schleem": Node.of_atom(AtomType.STR),
            "length of dinglepop": Node.of_atom(AtomType.FLOAT),
            "color of fleeb": Node.of_atom(AtomType.OPTION, [
                "pink",
                "red",
                "octarine",
            ]),
        }),
    })

    # Load initial data from a file.
    with open(filename, "r") as f:
        data = json.load(f)

    saved_data = {
        "filename": filename,
        "Plumbus": data,
    }

    def save_data(result):
        "Callback that will receive the data when the user press validate."
        filename = result["filename"]
        data = result["Plumbus"]
        with open(filename, "w") as f:
            json.dump(f, data)

    # build the form
    win = make_form(model, save_data, init_data=saved_data)

    # open the window and wait for interactions
    win.mainloop()

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ref/tkgen


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
