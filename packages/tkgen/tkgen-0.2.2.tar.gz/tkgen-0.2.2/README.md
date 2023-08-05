# TkGen 

## About

`tkgen` is a python package that automatically generate a Tkinter form window from a [Pyskema](https://pypi.org/project/pyskema/) schema.
It provide a simple interface to initialize the window and collect the data inputed by user.
The data is provided as python native objects that would be valid regarding the schema.
It depends on tkinter and Pyskema.

## Installation

Recommended:
Use `pip install tkgen`.

Manual:
Clone this project.
Run `pip install .` in this folder.

## Usage

The main entrypoint of this package is the function `tkgen.make_form`.
Here is a minimal exemple of its usage:
```python
from tkgen import make_form
from pyskema import Node, AtomType

schema = Node.of_record({
    "a": Node.of_atom(AtomType.INT),
})

win = make_form(schema, print)
win.mainloop()
```

The first parameter of `make_toplevel` (the model) is the schema that define the form.
The second parameter (the callback) is a function to be called when the form is submitted.
The callback is passed a single argument which is either None (if the user pressed cancel) or the data inputed.
This dictionary mirror the structure of the model.

### Extracting data

Once the form is filled, you want to access its data.
This is done through the callback parameter of `make_form`.
This callback is an arbitrary function you should provide that will receive the data in the form of a dictionary.

Here is a simple example of saving the data in an arbitrary json file:

```python
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
```

### Loading data

You may want to be able to load back some data from a previous instance of the form.
This is possible thanks to the `init_data` optional parameter.
For simplicity it is also possible through the optional `data` parameter of `make_form`.

If you were to use the previous example and save a file named *plumbus.json*, the following example would load data from the json file and produce a filled form identical to what it looked when you saved the file.

```python
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

with open(filename, "r") as f:
    data = json.load(f)

saved_data = {
    "filename": filename,
    "Plumbus": data,
}

def save_data(result):
    filename = result["filename"]
    data = result["Plumbus"]
    with open(filename, "w") as f:
        json.dump(f, data)

win = make_form(model, save_data, init_data=saved_data)
win.mainloop()
```
