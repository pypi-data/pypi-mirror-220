from dataclasses import dataclass
from klip_nav.utils import Highlight, SortedClippings
import urwid
import clipboard


class BookFrame(urwid.Frame):
    """inhereted widget to include keybindings"""

    def keypress(self, size, key):
        if key == "J" or key == "j":
            self.keypress(size, "down")
        if key == "K" or key == "k":
            self.keypress(size, "up")
        if key == "H" or key == "h":
            self.keypress(size, "left")
        if key == "L" or key == "l":
            self.keypress(size, "right")
        if key == "U" or key == "u":
            self.keypress(size, "page up")
        if key == "D" or key == "d":
            self.keypress(size, "page down")
        return super(BookFrame, self).keypress(size, key)

    def mouse_event(self, size, event, button, col, row, focus):
        if event == "mouse press":
            if button == 4:
                self.keypress(size, "up")
            if button == 5:
                self.keypress(size, "down")
        return super().mouse_event(size, event, button, col, row, focus)


@dataclass
class App:
    clippings: SortedClippings
    filename: str
    browse: bool = True

    def __post_init__(self) -> None:
        """start urwid main loop"""
        self.main = self.main_menu()
        self.main_loop = urwid.MainLoop(
            self.main,
            unhandled_input=self.quit_listener,
            palette=[
                ("reversed", "standout", ""),
                ("titlebar", "bold, white", "black"),
                ("banner", "white, bold", "dark gray"),
                ("note", "white, bold", "dark blue"),
                ("highlight", "white, bold", "dark green"),
            ],
        )
        self.main_loop.run()

    def main_menu(self) -> BookFrame:
        """renders main menu via urwid Frame"""
        header = urwid.AttrMap(urwid.Text(self.filename, "right"), "titlebar")
        body = self.main_menu_body()
        return BookFrame(header=header, body=body)

    def main_menu_body(self) -> urwid.ListBox:
        """create and return the list of books widget used in main menu body"""
        body = list()
        for book_title in sorted(self.clippings.books.keys(), key=str.casefold):
            button = urwid.Button(book_title)
            urwid.connect_signal(
                button,
                "click",
                self.book_chosen,
                user_args=[book_title, self.clippings.books[book_title]],
            )
            button = urwid.AttrMap(button, None, focus_map="reversed")
            body.append(button)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def book_chosen(self, title, book, button) -> None:
        """creates and renders overlay of chosen book"""
        header = urwid.AttrMap(urwid.Text(title, "right"), "titlebar")

        body = list()
        for note in book.notes:
            if type(note) is Highlight:
                card_type = urwid.Text("HIGHLIGHT")
            else:
                card_type = urwid.Text("PERSONAL NOTE")
            clipboard_button = urwid.Button("Copy to clipboard")
            urwid.connect_signal(
                clipboard_button,
                "click",
                self.copy_to_clipboard,
                user_args=[note.content],
            )
            clipboard_button = urwid.AttrMap(
                clipboard_button, None, focus_map="banner"
            )
            card_info_text = urwid.Text(["LOC: " + note.location])
            card_info = urwid.Columns(
                [card_info_text, (21, clipboard_button)],
            )
            time = urwid.Text(note.time)
            card_info = urwid.Pile([card_type, card_info, time])

            # set background color of titlebar for each card
            if type(note) is Highlight:
                card_info = urwid.AttrMap(card_info, "highlight")
            else:
                card_info = urwid.AttrMap(card_info, "note")

            card_text = urwid.Text(note.content)
            card = urwid.Pile([card_info, urwid.Divider("/"), card_text])
            card = urwid.LineBox(card)
            card = urwid.Padding(card, align="center", width=("relative", 90))
            body.append(card)
        body = urwid.ListBox(urwid.SimpleFocusListWalker(body))

        layout = urwid.Frame(header=header, body=body)

        self.browse = False
        self.main.body = urwid.Overlay(
            layout,
            self.main.body,
            align="center",
            width=("relative", 100),
            height=("relative", 100),
            valign="middle",
        )

    def copy_to_clipboard(self, text: str, button) -> None:
        """copies a string to clipboard, prints success message"""
        clipboard.copy(text)
        print("===== COPIED =====")

    def quit_listener(self, key):
        """Q listener as there are two behaviors desired depending on frame"""
        if key == "Q" or key == "q":
            if self.browse:
                raise urwid.ExitMainLoop()
            else:
                self.main.body = self.main.body[0]
                self.browse = True
