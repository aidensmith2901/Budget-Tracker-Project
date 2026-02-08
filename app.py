from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Button, Static
from textual.screen import Screen
from textual.widget import Widget
from textual.reactive import reactive

class MainMenu(Vertical):
    """Main menu widget with buttons."""

    def compose(self) -> ComposeResult:
        yield Static("Main Menu", id="title")
        yield Button("Manage Categories", id="categories", variant="primary")
        yield Button("Manage Transactions", id="transactions")
        yield Button("View Reports", id="reports")
        yield Button("Exit", id="exit", variant="error")

class RatioBox(Container):
    ratio = reactive(2.4)  # wide rectangle

    def compose(self) -> ComposeResult:
        yield MainMenu()

    def on_resize(self, event):
        term_w = event.size.width
        term_h = event.size.height

        target_w = term_w
        target_h = int(target_w / self.ratio)

        if target_h > term_h:
            target_h = term_h
            target_w = int(target_h * self.ratio)

        self.styles.width = target_w
        self.styles.height = target_h

class MainMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            RatioBox(id="ratio-box"),
            id="centerer"
        )
        yield Footer()

class BudgetApp(App):
    CSS = """
    #centerer {
        align: center middle;
    }

    #ratio-box {
        border: solid green;
        align: center middle;
    }

    #menu {
        align: center middle;
        width: 50%;
        height: auto;
        padding: 2;
        border: solid green;
    }

    #title {
        text-style: bold;
        padding-bottom: 1;
    }

    Button {
        margin: 1 0;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "categories":
            self.console.log("Navigate to category screen")
        elif button_id == "transactions":
            self.console.log("Navigate to transaction screen")
        elif button_id == "reports":
            self.console.log("Navigate to reports screen")
        elif button_id == "exit":
            self.exit()

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())

if __name__ == "__main__":
    app = BudgetApp()
    app.run()