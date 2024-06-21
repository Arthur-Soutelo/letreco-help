import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State

import sys
from os.path import abspath, dirname

# Add the parent directory to the sys.path
current_dir = dirname(abspath(__file__))
parent_dir = dirname(current_dir)
sys.path.append(parent_dir)


from main import *

LOGO = "/app/logos/logo-alt-dark-theme.png"

BASE_STYLE = {
    "textAlign": "center",
    "fontSize": "30px",  # Bigger font size
    "width": "175px",  # Optional: Adjust width as needed
}

position_constraints = []
position_letter_pairs = []
letters_to_remove = []
required_letters = []
styles = [BASE_STYLE.copy() for _ in range(25)]

with open("br-5-letras.txt", "r", encoding="utf-8") as infile:
    words = infile.read().splitlines()
filtered_words = words

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "overflowY": "scroll",
    # "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def create_sidebar(words):
    return html.Div(create_list(words), style=SIDEBAR_STYLE, id="output-container")


def create_input(row, col):
    return dbc.Input(
        id=f"input-{row}-{col}",
        placeholder="Letter",
        maxLength=1,
        style=BASE_STYLE.copy(),
    )


def create_button(row, col):
    return dbc.ButtonGroup(
        [
            dbc.Button(
                "X",
                color="danger",
                id=f"button-left-{row}-{col}",
                n_clicks=0,
            ),
            dbc.Button(
                "-",
                color="warning",
                id=f"button-middle-{row}-{col}",
                n_clicks=0,
            ),
            dbc.Button(
                "✓",
                color="success",
                id=f"button-right-{row}-{col}",
                n_clicks=0,
            ),
        ],
        size="sm",
        className=("button"),
    )


def create_input_button_pair(row, col):
    return dbc.Col(
        [
            dbc.Row(create_input(row, col)),
            dbc.Row(create_button(row, col)),
        ],
        align="center",
        className=("pair_container"),
        width={"size": 2},
    )


def create_pair_row(row):
    return html.Div(
        [
            dbc.Row(
                [
                    create_input_button_pair(row, 1),
                    create_input_button_pair(row, 2),
                    create_input_button_pair(row, 3),
                    create_input_button_pair(row, 4),
                    create_input_button_pair(row, 5),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "gap": "20px",  # Space between buttons
                },
            )
        ],
        className="pair_row",
    )


def create_list(words):
    list_group = []
    for word in words:
        list_group.append(dbc.ListGroupItem(word))

    list_group = dbc.ListGroup(
        list_group,
        # numbered=True,
    )
    return list_group


# ==================== LAYOUT ==================== #

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE, "app/styles.css"])


app.layout = dbc.Container(
    className="container",
    children=[
        create_sidebar([]),
        html.Div(
            [
                html.H4("LETRECO  HELP"),
                html.Hr(),
                create_pair_row(1),
                html.Br(),
                create_pair_row(2),
                html.Br(),
                create_pair_row(3),
                html.Br(),
                create_pair_row(4),
                html.Br(),
                create_pair_row(5),
            ],
            style=CONTENT_STYLE,
        ),
    ],
    fluid=True,
)

# ==================== CALLBACKS ==================== #


# Define callback to generate words based on input
@app.callback(
    [Output(f"input-{i}-{j}", "style") for i in range(1, 6) for j in range(1, 6)]
    + [
        Output(f"button-left-{i}-{j}", "n_clicks")
        for i in range(1, 6)
        for j in range(1, 6)
    ]
    + [
        Output(f"button-middle-{i}-{j}", "n_clicks")
        for i in range(1, 6)
        for j in range(1, 6)
    ]
    + [
        Output(f"button-right-{i}-{j}", "n_clicks")
        for i in range(1, 6)
        for j in range(1, 6)
    ]
    + [Output("output-container", "children")],
    # -----------------------------------------------------
    [State(f"input-{i}-{j}", "value") for i in range(1, 6) for j in range(1, 6)]
    + [
        Input(f"button-left-{i}-{j}", "n_clicks")
        for i in range(1, 6)
        for j in range(1, 6)
    ]
    + [
        Input(f"button-middle-{i}-{j}", "n_clicks")
        for i in range(1, 6)
        for j in range(1, 6)
    ]
    + [
        Input(f"button-right-{i}-{j}", "n_clicks")
        for i in range(1, 6)
        for j in range(1, 6)
    ],
)
def refresh_words(*args):
    n = 25  # Number of inputs in each category (5 rows x 5 columns)
    letters = args[:n]
    button_left_clicks = args[n : 2 * n]  # RED
    button_middle_clicks = args[2 * n : 3 * n]  # YELLOW
    button_right_clicks = args[3 * n : 4 * n]  # GREEN

    # Initialize button clicks to 0 if None
    button_left_clicks = [clicks or 0 for clicks in button_left_clicks]
    button_middle_clicks = [clicks or 0 for clicks in button_middle_clicks]
    button_right_clicks = [clicks or 0 for clicks in button_right_clicks]

    for i in range(n):
        style = BASE_STYLE.copy()
        letter = letters[i]

        # Calculate letter position in the word
        letter_position = (i + 1) % 5 - 1 if (i + 1) % 5 != 0 else 4

        if button_left_clicks[i] > 0:
            style["backgroundColor"] = "red"  # Red background for left button
            # letters_red.append(letter)
            button_left_clicks[i] = 0

            letters_to_remove.append(letter)

            if (letter_position, letter) in position_letter_pairs:
                position_letter_pairs.remove((letter_position, letter))
                required_letters.remove(letter)
                # letters_green.remove(letter)
                button_right_clicks[i] = 0
            if (letter_position, letter) in position_constraints:
                position_constraints.remove((letter_position, letter))
                # letters_yellow.remove(letter)
                button_middle_clicks[i] = 0

        if button_middle_clicks[i] > 0:
            style["backgroundColor"] = "yellow"  # Yellow background for middle button
            # letters_yellow.append(letter)
            button_middle_clicks[i] = 0

            position_constraints.append((letter_position, letter))
            required_letters.append(letter)

            if (letter_position, letter) in position_letter_pairs:
                position_letter_pairs.remove((letter_position, letter))
                required_letters.remove(letter)
                # letters_green.remove(letter)
                button_right_clicks[i] = 0
            if letter in letters_to_remove:
                letters_to_remove.remove(letter)
                # letters_red.remove(letter)
                button_left_clicks[i] = 0

        if button_right_clicks[i] > 0:
            style["backgroundColor"] = "green"  # Green background for right button
            # letters_green.append(letter)
            button_right_clicks[i] = 0

            position_letter_pairs.append((letter_position, letter))
            required_letters.append(letter)

            if (letter_position, letter) in position_constraints:
                position_constraints.remove((letter_position, letter))
                # letters_yellow.remove(letter)
                button_middle_clicks[i] = 0
            if letter in letters_to_remove:
                letters_to_remove.remove(letter)
                # letters_red.remove(letter)
                button_left_clicks[i] = 0

        # ---

        if (letter_position, letter) in position_letter_pairs:
            style["backgroundColor"] = "green"  # Green background for right button
        if (letter_position, letter) in position_constraints:
            style["backgroundColor"] = "yellow"  # Yellow background for middle button
        if letter in letters_to_remove:
            style["backgroundColor"] = "red"  # Red background for left button

        # styles.append(style)
        styles[i] = style

    # ----------------------------------------------

    print("-------------------------------------------------------")
    print("position_constraints:")
    print(position_constraints)
    print("position_letter_pairs:")
    print(position_letter_pairs)
    print("letters_to_remove:")
    print(letters_to_remove)
    print("required_letters:")
    print(required_letters)
    print("-------------------------------------------------------")

    filtered_words = remove_words_with_duplicate_letters(words)
    filtered_words = remove_words_with_letters(
        set(filtered_words), set(letters_to_remove)
    )
    filtered_words = filter_words_with_letter_at_position(
        filtered_words, set(position_letter_pairs)
    )
    filtered_words = filter_words_with_constraints(
        filtered_words, set(required_letters), position_constraints
    )
    filtered_words = return_real_words(filtered_words)

    return (
        styles
        + (
            list(button_left_clicks)
            + list(button_middle_clicks)
            + list(button_right_clicks)
        )
        + [create_list(filtered_words)]
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
