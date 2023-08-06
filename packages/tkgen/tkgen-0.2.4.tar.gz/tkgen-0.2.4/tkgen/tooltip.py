"An implementation of a tooltip buble for documenting elements of forms."
import tkinter as tk
import tkinter.ttk as ttk


class Semaphore:
    "A semaphore letting several tooltips synchronising themself."

    def __init__(self):
        self.state = None
        self.held = False

    def request(self, ident):
        if self.held:
            return False

        self.state = ident
        return True

    def hold(self, ident):
        if self.held:
            return False

        if self.state is not ident:
            return False

        self.held = True
        return True

    def release(self, ident):
        if self.held and self.state is ident:
            self.held = False
            self.state = None


_default_sem = Semaphore()


class Tooltip:
    """Create a floating tooltip next to the attached widget.

    Credits:

    - Originally written by vegaseat on 2014.09.09 (`blog post`_).
    - Modified to include a delay time by Victor Zaccardo on 2016.03.25 (`stackoverflow answer 1`_).
    - Modified by Alberto Vassena on 2016.11.05 (`stackoverflow answer 2`_):

        - to correct extreme right and extreme bottom behavior,
        - to stay inside the screen whenever the tooltip might go out on
          the top but still the screen is higher than the tooltip,
        - to use the more flexible mouse positioning,
        - to add customizable background color, padding, waittime and
          wraplength on creation

    - Modified to fix a scheduling bug by Erik Bethke on 2016.12.29 (`stackoverflow answer 3`_).
    - Modified by Théo Cavignac to prevent more than one visible tooltip at
      a time, causing superpositions of tooltips in complex widget tree,
      on 2022.09.04 (in `tkgen sources`_).

    Tested on Archlinux (kernel 6.2.2), running Python 3.10.9

    .. _blog post: http://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
    .. _stackoverflow answer 1: https://stackoverflow.com/a/36221216/6324751
    .. _stackoverflow answer 2: https://stackoverflow.com/a/41079350/6324751
    .. _stackoverflow answer 3: https://stackoverflow.com/a/41381685/6324751
    .. _tkgen sources: https://git.sr.ht/~lattay/python-tkgen/tree/bdb9ba3c1ee173d2765966cd23f5acdb6f07007f/item/tkform/tooltip.py#L36-197
    """

    def __init__(
        self,
        widget,
        *,
        bg="#FFFFEA",
        pad=(5, 3, 5, 3),
        text="widget info",
        waittime=200,
        wraplength=250,
        sem=_default_sem
    ):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None
        self.ident = object()
        self.sem = sem

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        if self.sem.request(self.ident):
            self.unschedule()
            self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        self.sem.release(self.ident)
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        if not self.sem.hold(self.ident):
            return

        def tip_pos_calculator(widget, label, *, tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (
                pad[0] + label.winfo_reqwidth() + pad[2],
                pad[1] + label.winfo_reqheight() + pad[3],
            )

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = tk.Toplevel(widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw, background=bg, borderwidth=0)
        label = ttk.Label(
            win,
            text=self.text,
            justify=tk.LEFT,
            background=bg,
            relief=tk.SOLID,
            borderwidth=0,
            wraplength=self.wraplength,
        )

        label.grid(padx=(pad[0], pad[2]), pady=(pad[1], pad[3]), sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None
