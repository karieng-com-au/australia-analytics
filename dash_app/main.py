import os
from dash import Dash, dcc, html, page_container, page_registry
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
            .dash-spinner {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"
                integrity="sha384-SALc35EccAf6RzGw4iNsyj7kTPr33K7RoGzYu+7heZhT8s0GZouafRiCg1qy44AS"
                crossorigin="anonymous"></script>
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
                html.Img(src="/assets/grampians-logo-new-2026.png", style={"height": "60px"}),
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
                dbc.NavItem(dbc.NavLink("Hire me", href="/contact")),
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

footer = html.Div(
    html.Div([
        html.Div([
            html.Span("2026 Grampians AI. All rights reserved.", style={"color": "#167d7f", "fontWeight": "500"}),
        ], style={"flex": "1"}),
        html.Div([
            html.A("LinkedIn", href="https://www.linkedin.com/in/jackptoke/", target="_blank",
                   style={"color": "#167d7f", "fontWeight": "700", "textDecoration": "none", "marginRight": "20px"}),
            html.A("GitHub", href="https://github.com/karieng-com-au", target="_blank",
                   style={"color": "#167d7f", "fontWeight": "700", "textDecoration": "none"}),
        ]),
    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "maxWidth": "75%",
        "margin": "0 auto",
        "padding": "15px 0",
    }),
    className="bg-light border-top",
)

app.layout = html.Div([
    navbar,
    html.Div(
        dcc.Loading(page_container, type="circle", color="#167d7f"),
        style={"maxWidth": "75%", "margin": "0 auto", "padding": "20px 0", "flex": "1"},
    ),
    footer,
], style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"})

server = app.server


@server.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if os.environ.get("HTTPS_ENABLED", "false").lower() == "true":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


if __name__ == '__main__':
    app.run(debug=os.environ.get("DASH_DEBUG", "false").lower() == "true",
            port=int(os.environ.get("PORT", 8050)))
