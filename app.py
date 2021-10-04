# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import json
import os
from utils.picker import sample_without_replacement

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Daily Stand Up"
server = app.server
# import candidate team members from json config
with open("config.json") as myjson:
    config = json.load(myjson)
    team_members = config["team_list"]
    team_name = config["team_name"]
    asset_filepath = config["asset_filepath"]

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children=f"{team_name} DSU"),
                        html.H2(children="Let's get scrumming."),
                    ],
                    style={"margin": "20px"},
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="dynamic_team_list_drop_down",
                            options=[
                                {"label": teammember, "value": teammember}
                                for teammember in team_members
                            ],
                            value=team_members,
                            multi=True,
                        ),
                    ],
                    style={"margin": "20px"},
                ),
                html.Div(
                    children=[
                        html.Button(
                            id="picker_button_state", n_clicks=0, children="Who's Next?"
                        ),
                        html.Div(id="output_state"),
                        html.Div(children = [
                            html.Img(id="image", style={"width" : "100%"})],
                         style={"height" : "500px", "width" : "500px"}),
                    ],
                    style={"margin": "20px"},
                ),
                dcc.Store(id="team_list", data=team_members),
                dcc.Store(id="current_name"),
            ],
            className="page-main",
        )
    ],
    className="page-container", style={"width" : "50%"}
)


@app.callback(
    Output("image", "src"),
    [Input("current_name", "data"), Input("picker_button_state", "n_clicks")],
)
def update_image_src(current_name, n_clicks):
    """
    returns an image to display.
    If we haven't started show a start image,
    then once the button has been clicked show the image of the name chosen,
    until we've done all the names and show the finish image

    Args:
        current_name (str): name chosen for which we display a picture of the same name
        n_clicks (int): number of times the button has been clicked

    Returns:
        [type]: [description]
    """
    if current_name == None:
        if n_clicks == 0:
            image_path = os.path.join(asset_filepath, "start.jpg")
        else:
            image_path = os.path.join(asset_filepath, "finish.jpg")
    else:
        image_path = os.path.join(asset_filepath, f"{current_name}.jpg")

    # if the image isn't there then put a static image
    if not os.path.exists(image_path):
        image_path = os.path.join(asset_filepath, "noimage.jpg")

    # and if that's not available, don't show anything
    print("Image: " + image_path)
    if os.path.exists(image_path):
        encoded_image = base64.b64encode(open(image_path, "rb").read())
        return "data:image/png;base64,{}".format(encoded_image.decode())
    else:
        return None


@app.callback(
    [Output("current_name", "data"), Output("team_list", "data")],
    [
        Input("picker_button_state", "n_clicks"),
        Input("team_list", "data"),
        Input("dynamic_team_list_drop_down", "value"),
    ],
)
def pick_from_team(n_clicks, current_team_list, original_team_list):
    """
    Picks a random name from the team_list

    Args:
        n_clicks (int): number of times the button has been clicked
        current_team_list (list): The updated team list with removed names based on button clicks
        original_team_list (list): The original set of team members (team list) chosen from the dropdown

    Returns:
        name (str): random name from team_list
        new_team_list (list): team_list with name removed
    """
    if (
        (n_clicks == 0)
        or len(current_team_list) == 0
        or (n_clicks > len(original_team_list))
    ):
        name = None
        new_team_list = original_team_list
    else:
        name, new_team_list = sample_without_replacement(current_team_list)
    return name, new_team_list


@app.callback(
    Output("output_state", "children"),
    Input("picker_button_state", "n_clicks"),
    Input("team_list", "data"),
    Input("current_name", "data"),
    Input("dynamic_team_list_drop_down", "value"),
)
def update_output(n_clicks, current_team_list, current_name, original_team_list):
    """
    Depending on the state, display appropriate text.
    Initial message -> Name of who's been picked -> End Message -> why you still clicking message

    Args:
        n_clicks (int): number of times the button has been clicked
        current_team_list (list): The updated team list with removed names based on button clicks
        current_name (str): random name from team_list
        original_team_list (list): The original set of team members (team list) chosen from the dropdown

    Returns:
        str: Text based on where we are in the workflow
    """
    if n_clicks == 0:
        return f"We've got {len(current_team_list)} people to get through today"
    elif n_clicks == len(original_team_list) + 1:
        return f"All done and dusted, have a lovely day!"
    elif n_clicks > len(original_team_list):
        return f"You're keen, we've already been!"
    else:
        return f"{current_name}, you're up!"


if __name__ == "__main__":
    app.run_server(debug=True)

