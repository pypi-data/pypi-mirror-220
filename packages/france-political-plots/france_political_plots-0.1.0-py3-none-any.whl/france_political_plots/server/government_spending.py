from dash import Dash, dcc, html, Input, Output, callback
from typing import Self, List, Dict, Any
import dash_ag_grid as dag
import dash_mantine_components as dmc
import dash_iconify as dic

from .tools import AGGrid
from ..data.government_spending import GovernmentSpending
from ..utils import Pkg, Assets

FULL_SIZE_STYLE = {"width": "100vw", "height": "90vh"}

CONFIG = {"displayModeBar": False, "responsive": True}


class Dashboard:
    def __new__(cls) -> Self:
        cls.server = None
        cls.app = None
        return cls

    @classmethod
    def make(cls):
        data = GovernmentSpending()
        before, after = data.spending_change(kind="scatter")
        line_before, line_after = data.spending_change(kind="line")
        df = data.df.dropna(subset=["spending"])

        external_stylesheets = [
            "https://codepen.io/chriddyp/pen/bWLwgP.css",
            "https://fonts.googleapis.com/css2?family=Fira+Sans:wght@300;400;500;600;700&display=swap",
        ]

        app = Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            title="LFI 2022 Spending",
        )

        grid = AGGrid(df, app).make()

        components = html.Div(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label="Usual Spending",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            figure=before,
                                            style=FULL_SIZE_STYLE,
                                            config=CONFIG,
                                        )
                                    ],
                                    style=FULL_SIZE_STYLE,
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Comparison LFI 2022",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            figure=after,
                                            style=FULL_SIZE_STYLE,
                                            config=CONFIG,
                                        )
                                    ],
                                    style=FULL_SIZE_STYLE,
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Usual Spending per Year",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            figure=line_before,
                                            style=FULL_SIZE_STYLE,
                                            config=CONFIG,
                                        )
                                    ],
                                    style=FULL_SIZE_STYLE,
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Spending per Year LFI 2022",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            figure=line_after,
                                            style=FULL_SIZE_STYLE,
                                            config=CONFIG,
                                        )
                                    ],
                                    style=FULL_SIZE_STYLE,
                                )
                            ],
                        ),
                        dcc.Tab(label="Data", children=grid, style=FULL_SIZE_STYLE),
                    ]
                )
            ],
        )

        app.layout = dmc.MantineProvider(
            theme={
                "fontFamily": "'Fira Sans', sans-serif",
                "primaryColor": "violet",
                "components": {
                    "Button": {"styles": {"root": {"fontWeight": 400, "fontSize": 22}}},
                    "Alert": {"styles": {"title": {"fontWeight": 500}}},
                    "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
                },
            },
            inherit=True,
            withGlobalStyles=True,
            withNormalizeCSS=True,
            children=[
                dmc.Stack(
                    [
                        dmc.Header(
                            height=110,
                            style={"backgroundColor": "#82D0F4"},
                            children=[
                                dmc.Grid(
                                    [
                                        dmc.Center(
                                            [
                                                dmc.Image(
                                                    width=100,
                                                    height=100,
                                                    src="/assets/volt-data.svg",
                                                ),
                                                dmc.Space(w=50),
                                                dmc.Title("France Political Data"),
                                            ]
                                        )
                                    ],
                                    align="left",
                                    gutter="xs",
                                )
                            ],
                        ),
                        components,
                    ]
                )
            ],
        )

        app._favicon = "volt-data.ico"

        cls.server = app.server
        cls.app = app

        return app


dash = Dashboard()
dash.make()
server = dash.app.server
