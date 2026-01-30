import os
from dash import Dash, html, page_container, page_registry
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, pages_folder="pages", suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.MINTY])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link, .dropdown-item {
                color: #167d7f !important;
                font-weight: 700;
            }
            .nav-link:hover, .dropdown-item:hover {
                color: #0F5657 !important;
                background-color: transparent !important;
            }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
        <script>emailjs.init("jKaPfNa0AwNE4oV_f");</script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

navbar = html.Div(
    html.Div([
        # Left: logo
        html.Div(
            html.A(
                html.Img(src="/assets/grampians-logo.png", style={"height": "40px"}),
                href="/",
            ),
            style={"flex": "1"},
        ),
        # Center: nav links
        html.Div(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Election Analysis", href="/election"),
                        dbc.DropdownMenuItem("Immigration Analysis", href="/immigration"),
                    ],
                    label="Articles",
                    nav=True,
                    in_navbar=True,
                ),
                dbc.NavItem(dbc.NavLink("Contact", href="/contact")),
            ]),
            style={"flex": "1", "display": "flex", "justifyContent": "center"},
        ),
        # Right: spacer to balance logo
        html.Div(style={"flex": "1"}),
    ], style={
        "display": "flex",
        "alignItems": "center",
        "maxWidth": "75%",
        "margin": "0 auto",
        "padding": "10px 0",
    }),
    className="bg-light border-bottom",
)

app.layout = html.Div([
    navbar,
    html.Div(page_container, style={"maxWidth": "75%", "margin": "0 auto", "padding": "20px 0"})
])

server = app.server

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 8050)))
