"Implement the form generation."

from itertools import count

from tkinter import (
    Tk,
    Toplevel,
    LEFT,
    RIGHT,
    VERTICAL,
    HORIZONTAL,
    NW,
    W,
    E,
    TOP,
    BOTH,
    X,
    Y,
    SOLID,
    NSEW,
    StringVar,
    IntVar,
    DoubleVar,
    BooleanVar,
    Listbox,
    Canvas,
    Scrollbar,
    TclError,
)
import tkinter.ttk as tk
from tkinter.messagebox import askokcancel

from pyskema.schema import Atom, AtomType, Node
from pyskema.validate import validate
from pyskema.visitor import Visitor

from .tooltip import Tooltip
from .assets import icon


def make_form(schema, callback, *, Window=Tk, title=None, init_data=None):
    "Build of form window from a schema. See :func:`FormFactory.make_toplevel`."
    return FormFactory.make_toplevel(
        schema, callback, Window=Window, title=title, init_data=init_data
    )


class FormFactory(Visitor):
    """The main factory.

    Implemented as a :class:`pyskema.visitor.Visitor`, it builds the tree of
    nodes from the schema and seam the network of pipes through.
    """

    @classmethod
    def make_toplevel(cls, schema, callback, *, Window=Tk, title=None, init_data=None):
        """Main constructor, it does the boring work.

        Boring work:

            - setup and wire the buttons
            - create the main window
            - (optional) set the window title
            - build the form and add it into a scollable container
            - (optional) inject initial data

        :param schema: the :mod:`pyskema` schema.
        :param callback: the callback that should treat the data at the end.
        :param Window: (kw only, :class:`tkinter.Tk`) the main window class.
        :param title: (kw only, :code:`None`) a title for the window.
        :param init_data: (kw only, :code:`None`) the initial data to inject in the form.
        """
        pipe = _Pipe()

        def cancel():
            callback(None)
            master.destroy()

        def extract():
            callback(pipe.pull())
            master.destroy()

        master = Window()
        if title:
            master.title(title)

        main_frame = tk.Frame(master)
        main_frame.pack(side=TOP, fill=BOTH, expand=True)

        scroll_frame = ScrollingFrame(main_frame)
        scroll_frame.pack(side=LEFT, fill=BOTH, expand=True)

        form_frame = scroll_frame.frame

        button_frame = tk.Frame(master)
        button_frame.pack(side=TOP, fill=X)

        b_cancel = tk.Button(button_frame, text="Cancel", command=cancel)
        b_ok = tk.Button(button_frame, text="Validate", command=extract)

        b_cancel.pack(side=LEFT)
        b_ok.pack(side=LEFT)

        res = cls().visit(schema, form_frame, pipe)

        if isinstance(schema.structure, Atom):
            Tooltip(res, text=schema.description)

        if init_data is not None:
            pipe.push(init_data)

        return master

    def visit_atom(self, atom, parent, pipe, *args):
        if atom.type_ == AtomType.STR:
            v = StringVar()
            w = tk.Entry(parent, textvariable=v)

        elif atom.type_ == AtomType.BOOL:
            v = BooleanVar()
            w = tk.Checkbutton(parent, text="", variable=v)

        elif atom.type_ == AtomType.FLOAT:
            v = DoubleVar()
            w = tk.Spinbox(parent, textvariable=v, incr=0.1)

        elif atom.type_ == AtomType.INT:
            v = IntVar()
            w = tk.Spinbox(parent, textvariable=v)

        elif atom.type_ == AtomType.OPTION:
            if len(atom.options) == 1:
                w = tk.Label(parent, text=atom.options[0])
                v = StringVar()
                v.set(atom.options[0])
            else:
                v = StringVar()
                v.set(atom.options[0])
                w = tk.OptionMenu(parent, v, *atom.options)

        else:
            raise NotImplementedError(f"{atom.type_} is not supported yet.")

        @pipe.puller
        def pull():
            return v.get()

        @pipe.pusher
        def push(data):
            return v.set(data)

        w.pack(anchor=W, side=TOP)  # , fill=X, expand=True
        return w

    def visit_union(self, union, parent, pipe, *args):
        frame = tk.Frame(parent)
        select_var = IntVar()
        options = []
        pipes = [_Pipe() for _ in union.options]

        for i, node in enumerate(union.options):
            if isinstance(node.structure, Atom):
                sub_frame = tk.Frame(frame)
                radio = tk.Radiobutton(sub_frame, variable=select_var, value=i)
                radio.pack(anchor=W, side=LEFT)
                field = self.visit(node, sub_frame, pipes[i])
                field.pack(anchor=E, side=RIGHT, fill=BOTH, expand=True)
                sub_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)
                options.append(sub_frame)
                if node.description:
                    Tooltip(radio, text=node.description)
            else:
                radio = tk.Radiobutton(frame, variable=select_var, value=i)
                sub_frame = _LabelWidgetFrame(frame, radio)
                sub_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)
                options.append(self.visit(node, sub_frame, pipes[i]))
                if node.description:
                    Tooltip(sub_frame.label_widget, text=node.description)

        @pipe.puller
        def pull():
            sel = select_var.get()
            return pipes[sel].pull()

        @pipe.pusher
        def push(data):
            op, _ = validate(data, Node(union))

            i = union.options.index(op)

            pipes[i].push(data)

            select_var.set(i)

        frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)
        return frame

    def visit_record(self, rec, parent, pipe, *args):
        frame = tk.Frame(parent)
        pipes = {key: _Pipe() for key in rec.fields}

        odd = True

        for key, node in rec.fields.items():
            if isinstance(node.structure, Atom):
                field_frame = tk.Frame(frame)
                label = tk.Label(field_frame, text=key)
                label.pack(side=LEFT)

                if odd:
                    sep = tk.Frame(field_frame)
                else:
                    sep = tk.Separator(field_frame, orient=HORIZONTAL)
                odd = not odd

                sep.pack(side=LEFT, fill=X, expand=True)
                field = self.visit(node, field_frame, pipes[key])
                field.pack(side=LEFT)
                if node.description:
                    Tooltip(field_frame, text=node.description)

            elif node.optional:
                field_frame = _FoldableLabelFrame(frame, text=key)
                if node.description:
                    Tooltip(field_frame.label_widget, text=node.description)
                self.visit(node, field_frame.content, pipes[key])
                odd = True

            else:
                label = tk.Label(frame, text=key)
                field_frame = _LabelWidgetFrame(frame, label)
                if node.description:
                    Tooltip(label, text=node.description)
                self.visit(node, field_frame, pipes[key])
                odd = True

            if node.optional:
                pipes[key].push(node.default)

            field_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)

        @pipe.puller
        def pull():
            return {key: p.pull() for key, p in pipes.items()}

        @pipe.pusher
        def push(data):
            if isinstance(field_frame, _FoldableLabelFrame):
                field_frame.switch_on()

            for key, d in data.items():
                pipes[key].push(d)

        frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)
        return frame

    def visit_collection(self, collection, parent, pipe, *args):
        frame = CollectionInput(parent, collection, pipe)

        frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)

        return frame

    def visit_map(self, map_, parent, pipe, *args):
        frame = MapInput(parent, map_, pipe)

        frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)

        return frame

    def visit_tuple(self, tup, parent, pipe, *args):
        frame = tk.Frame(parent)
        pipes = tuple(_Pipe() for _ in tup.fields)

        for i, node in enumerate(tup.fields):
            sub = tk.Frame(frame)
            self.visit(node, sub, node.description, pipes[i])
            sub.pack(anchor=W, side=TOP, fill=BOTH, expand=True)
            if node.description:
                Tooltip(sub, text=node.description)

        frame.pack(anchor=W, side=TOP, fill=BOTH, expand=True)

        @pipe.puller
        def pull():
            return tuple(p.pull() for p in pipes)

        @pipe.pusher
        def push(data):
            assert len(data) == len(pipes)

            for e, p in zip(data, pipes):
                p.push(e)

        return frame


class _LabelWidgetFrame(tk.LabelFrame):
    """Create a frame with a widget label in the parent."""

    def __init__(self, parent, label_widget):
        super().__init__(parent)
        self.label_widget = label_widget
        self.configure(labelwidget=label_widget)


class _FoldableLabelFrame(_LabelWidgetFrame):
    "A label frame that can be folded to hide its content."

    def __init__(self, parent, text):
        label_widget = tk.Frame(parent)
        self.v = BooleanVar()
        ck = tk.Checkbutton(label_widget, variable=self.v, command=self.change)
        ck.pack(side=LEFT)
        label = tk.Label(label_widget, text=text)
        label.pack(side=LEFT)
        super().__init__(parent, label_widget)

        self.toggle = ck
        self.content = tk.Frame(self)
        self.hidden_content = tk.Label(self, text="default")
        self.hidden_content.pack()

    def switch_on(self):
        self.v.set(True)
        self.change()

    def switch_off(self):
        self.v.set(False)
        self.change()

    def change(self):
        self.hidden_content.forget()
        self.content.forget()

        if self.v.get():
            self.content.pack(fill=BOTH, expand=True)
        else:
            self.hidden_content.pack()


class _Pipe:
    """A pipe linking two remote ways of the code.

    You can either "pull" on the date (request data)
    or "push" on it (inject data).
    The link is one way.
    """

    def __init__(self):
        self._puller = None
        self._pusher = None

    def puller(self, fn):
        "decorator: set the pull function"
        self._puller = fn

    def pusher(self, fn):
        "decorator: set the push function"
        self._pusher = fn

    def pull(self):
        return self._puller()

    def push(self, data):
        self._pusher(data)


class _Flag:
    "A flag to pass a boolean around."

    def __init__(self, initial=False):
        self._on = initial

    def on(self):
        self._on = True

    def off(self):
        self._on = False

    def __bool__(self):
        return self._on


def _get_name(data):
    return str(data)


class ScrollingFrame(tk.Frame):
    "A frame that encapsulate a scrollable content."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(
            self, width=12, orient=VERTICAL, command=self.canvas.yview
        )
        self.scrollbar.pack(side=RIGHT, fill=BOTH, expand=False)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)

        self.canvas.create_window(
            0,
            0,
            window=self.frame,
            anchor=NW,
        )

        self.frame.bind("<Configure>", self.frame_config)

        self.canvas.bind("<MouseWheel>", self.scroll_canvas)
        self.canvas.bind("<Configure>", self.canvas_config)

    def scroll_canvas(self, event):
        self.canvas.yview_scroll(-(event.delta // 120), "units")

    def frame_config(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.configure(width=12)

    def canvas_config(self, event):
        self.canvas.itemconfigure("all", width=event.width)
        self.scrollbar.configure(width=12)


class _CollectionInput(tk.Frame):
    "A special widget for inputing a elements to a collection."

    def __init__(self, parent, schema, pipe):
        super().__init__(parent)

        self.data_storage = {}

        self.lock = _Flag(False)

        self.subform_sch = schema

        button_frame = tk.Frame(self)
        button_frame.pack(side=LEFT)

        self.img_storage = []

        for icon_name, command in [
            ("add", self.new),
            ("edit", self.edit),
            ("delete", self.remove),
        ]:
            img = icon(icon_name)
            self.img_storage.append(img)
            b = tk.Button(button_frame, image=img, command=command)
            b.pack(side=TOP, fill=BOTH, expand=True)

        self.listbox = Listbox(self, height=7, selectmode="browse")
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        pipe.puller(self.pull)
        pipe.pusher(self.push)

    def add_item(self, data):
        name = _get_name(data)
        self.listbox.insert(len(self.data_storage), name)
        self.data_storage[name] = data

    def delete_item(self, i):
        try:
            name = self.listbox.get(i)
        except TclError:
            return

        self.listbox.delete(i)
        del self.data_storage[name]

    def remove(self):
        if self.lock:
            return

        self.delete_item(self.listbox.curselection())

    def edit(self):
        if self.lock:
            return

        selec = self.listbox.curselection()

        try:
            name = self.listbox.get(self.listbox.curselection())
        except TclError:
            return

        def cb(data):
            if data is not None:
                self.delete_item(selec)
                self.add_item(data)
            self.lock.off()
            form.destroy()

        init_data = self.data_storage[name]
        self.lock.on()
        form = FormFactory.make_toplevel(
            self.subform_sch,
            cb,
            Window=Toplevel,
            init_data=self.prepare_data(name, init_data),
        )

    def prepare_data(self, name, init_data):
        return init_data

    def new(self):
        if self.lock:
            return

        def cb(data):
            if data is not None:
                self.add_item(data)
            self.lock.off()
            form.destroy()

        self.lock.on()
        form = FormFactory.make_toplevel(
            self.subform_sch, cb, title="New element...", Window=Toplevel
        )

    def pull(self):
        n = len(self.data_storage)
        return [self.data_storage[name] for name in self.listbox.get(0, n)]

    def push(self, data):
        while self.data_storage:
            self.delete_item(0)

        for d in data:
            self.add_item(d)


class CollectionInput(_CollectionInput):
    "A special widget for inputing elements to a collection."

    def __init__(self, parent, schema, pipe):
        super().__init__(parent, schema.element, pipe)


class MapInput(_CollectionInput):
    "A special widget for inputing named elements to a map."

    def __init__(self, parent, schema, pipe):
        super().__init__(
            parent,
            Node.of_record(
                {
                    "name": Node.of_atom(AtomType.STR),
                    "value": schema.element,
                }
            ),
            pipe,
        )

    def prepare_data(self, name, data):
        return {"value": data, "name": name}

    def add_item(self, data):
        key = data["name"]
        elem = data["value"]
        self.listbox.insert(len(self.data_storage), key)
        self.data_storage[key] = elem

    def pull(self):
        n = len(self.data_storage)
        return {name: self.data_storage[name] for name in self.listbox.get(0, n)}

    def push(self, data):
        while self.data_storage:
            self.delete_item(0)

        for k, d in data.items():
            self.add_item(k, d)
