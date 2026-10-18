import sys
import types

from tirotir.core import execute


class FakeWidget:
    def __init__(self, root, **kwargs):
        self.root = root
        self.kwargs = kwargs
        self.packed = False

    def pack(self, **kwargs):
        self.packed = True


class FakeButton(FakeWidget):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.command = kwargs.get("command")
        root.buttons.append(self)

    def invoke(self):
        if self.command:
            self.command()


class FakeRoot:
    def __init__(self, module):
        self.module = module
        self.buttons = []
        self.title_value = None
        self.geometry_value = None
        module.roots.append(self)

    def title(self, value):
        self.title_value = value

    def geometry(self, value):
        self.geometry_value = value

    def mainloop(self):
        return None

    def destroy(self):
        return None


class FakeTk(types.SimpleNamespace):
    def __init__(self):
        super().__init__()
        self.roots = []
        self.Label = FakeWidget
        self.Button = FakeButton
        self.Entry = FakeWidget
        self.Checkbutton = FakeWidget
        self.Listbox = FakeWidget
        self.OptionMenu = FakeWidget
        self.Text = FakeWidget
        self.Scale = FakeWidget
        self.HORIZONTAL = "horizontal"
        self.END = "end"
        self.BooleanVar = lambda: object()
        self.StringVar = lambda **kwargs: object()
        self.Tk = lambda: FakeRoot(self)


def test_gui_keeps_widgets_and_dispatches_button_message(monkeypatch):
    fake_tk = FakeTk()
    monkeypatch.setitem(sys.modules, "tkinter", fake_tk)
    output = []
    execute(
        "پنجره بساز با -آزمایش- و ۳۲۰ و ۲۰۰\n"
        "برچسب بساز با -وضعیت-\n"
        "دکمه بساز با -اجرا- و -کلیک شد-\n",
        output=output.append,
        capabilities=["gui"],
    )

    root = fake_tk.roots[0]
    assert root.title_value == "آزمایش"
    assert root.geometry_value == "320x200"
    assert len(root.buttons) == 1
    root.buttons[0].invoke()
    assert output == ["کلیک شد"]
