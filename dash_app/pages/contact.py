import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State, clientside_callback

dash.register_page(__name__, path="/contact", name="Contact")

layout = html.Div([
    html.H2("Jack Toke", className="mt-4"),
    html.H5("Data/Analytics Engineer", className="text-muted"),
    html.P(
        "Thanks for stopping by! I'd love to hear from you — whether it's about "
        "a potential collaboration, a question, or just to say hello. "
        "Fill out the form below and I'll get back to you as soon as I can.",
        className="mt-3 mb-4",
    ),
    html.Hr(),
    dbc.Form([
        dbc.Row([
            dbc.Col([
                dbc.Label("Email address", html_for="contact-email"),
                dbc.Input(id="contact-email", type="email", placeholder="your@email.com"),
            ], md=6),
            dbc.Col([
                dbc.Label("Phone number", html_for="contact-phone"),
                dbc.Input(id="contact-phone", type="tel", placeholder="+61 400 000 000"),
            ], md=6),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Subject", html_for="contact-subject"),
                dbc.Input(id="contact-subject", type="text", placeholder="What is this about?"),
            ]),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Message", html_for="contact-message"),
                dbc.Textarea(id="contact-message", placeholder="Your message...", style={"height": "180px"}),
            ]),
        ], className="mb-3"),
        dbc.Button("Send Message", id="contact-submit", color="primary", className="mt-2"),
    ]),
    html.Div(id="contact-status", className="mt-3"),
])

clientside_callback(
    """
    function(n_clicks, email, phone, subject, message) {
        if (!n_clicks) return "";
        if (!email || !subject || !message) {
            return "Please fill in at least your email, subject, and message.";
        }
        emailjs.send("service_msc0orv", "template_laj5hrw", {
            from_email: email,
            phone: phone || "Not provided",
            subject: subject,
            message: message
        }).then(
            function() {
                document.getElementById("contact-status").innerText = "Message sent successfully! I'll be in touch soon.";
                document.getElementById("contact-status").className = "mt-3 text-success fw-bold";
                document.getElementById("contact-email").value = "";
                document.getElementById("contact-phone").value = "";
                document.getElementById("contact-subject").value = "";
                document.getElementById("contact-message").value = "";
            },
            function(error) {
                document.getElementById("contact-status").innerText = "Something went wrong. Please try again.";
                document.getElementById("contact-status").className = "mt-3 text-danger fw-bold";
            }
        );
        return "Sending...";
    }
    """,
    Output("contact-status", "children"),
    Input("contact-submit", "n_clicks"),
    State("contact-email", "value"),
    State("contact-phone", "value"),
    State("contact-subject", "value"),
    State("contact-message", "value"),
    prevent_initial_call=True,
)
