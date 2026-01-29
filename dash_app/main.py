from dash import Dash, html, dcc, page_container, page_registry

app = Dash(__name__, use_pages=True, pages_folder="pages", suppress_callback_exceptions=True)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link {
                text-decoration: none;
                color: teal;
                font-weight: 700;
            }
            .nav-link:hover {
                color: #004d4d;
            }
        </style>
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

app.layout = html.Div([
    html.Nav(
        html.Div([
            html.Img(
                src="/assets/grampians-logo.png",
                style={"height": "40px", "flex": "0 0 auto"}
            ),
            html.Ul(
                [
                    html.Li(
                        dcc.Link(page["name"], href=page["path"], className="nav-link"),
                        style={"display": "inline", "marginRight": "20px"}
                    )
                    for page in page_registry.values()
                ],
                style={"listStyle": "none", "display": "flex", "margin": "0", "padding": "0",
                        "flex": "1 1 auto", "justifyContent": "center"}
            ),
            # Spacer to balance the logo so links stay truly centered
            html.Div(style={"width": "120px", "flex": "0 0 auto"}),
        ], style={"display": "flex", "alignItems": "center", "maxWidth": "75%", "margin": "0 auto", "padding": "10px 0"}),
        style={"backgroundColor": "#f8f9fa", "borderBottom": "1px solid #dee2e6"}
    ),
    html.Div(page_container, style={"maxWidth": "75%", "margin": "0 auto", "padding": "20px 0"})
])

if __name__ == '__main__':
    app.run(debug=True)
