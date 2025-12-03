# main.py
# Final S.E.N.N.A. — Local-assets Rage Dash with Senna tribute
# Run: python main.py
# Requirements: dash, dash-bootstrap-components, plotly

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import os

# -------------------------
# TEAMS: final 2025 grid + Cadillac 2026
# All image values point to local files inside /assets/
# -------------------------
TEAMS = [
    {"id": "redbull", "name": "Red Bull Racing", "logo": "/assets/redbull_logo.png", "car": "/assets/redbull_car.png",
     "engine_name": "Honda RBPT V6 Hybrid", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈1000+ HP", "ERS": "Advanced"},
     "drivers": [{"name": "Max Verstappen", "no": 1, "wins": 54, "podiums": 98, "starts": 194, "photo": "/assets/max.png"},
                 {"name": "Yuki Tsunoda", "no": 22, "wins": 0, "podiums": 0, "starts": 82, "photo": "/assets/tsunoda.png"}],
     "history": "Dominant front-runner with strong aero and race strategy pedigree."},

    {"id": "mercedes", "name": "Mercedes-AMG Petronas", "logo": "/assets/mercedes_logo.png", "car": "/assets/mercedes_car.png",
     "engine_name": "Mercedes PU", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈1000 HP", "ERS": "Ultra Efficient"},
     "drivers": [{"name": "George Russell", "no": 63, "wins": 1, "podiums": 11, "starts": 105, "photo": "/assets/russell.png"},
                 {"name": "Andrea Kimi Antonelli", "no": 88, "wins": 0, "podiums": 0, "starts": 0, "photo": "/assets/antonelli.png"}],
     "history": "Seven-time double champions; expertise in powertrains and aero stability."},

    {"id": "ferrari", "name": "Scuderia Ferrari", "logo": "/assets/ferrari_logo.png", "car": "/assets/ferrari_car.png",
     "engine_name": "Ferrari PU", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈1000 HP", "ERS": "High Efficiency"},
     "drivers": [{"name": "Charles Leclerc", "no": 16, "wins": 5, "podiums": 32, "starts": 138, "photo": "/assets/leclerc.png"},
                 {"name": "Lewis Hamilton", "no": 44, "wins": 103, "podiums": 197, "starts": 334, "photo": "/assets/hamilton.png"}],
     "history": "Historic Italian team with a long championship legacy and passionate fanbase."},

    {"id": "mclaren", "name": "McLaren", "logo": "/assets/mclaren_logo.png", "car": "/assets/mclaren_car.png",
     "engine_name": "Mercedes Hybrid", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈980 HP", "ERS": "High Efficiency"},
     "drivers": [{"name": "Lando Norris", "no": 4, "wins": 1, "podiums": 16, "starts": 117, "photo": "/assets/norris.png"},
                 {"name": "Oscar Piastri", "no": 81, "wins": 0, "podiums": 9, "starts": 42, "photo": "/assets/piastri.png"}],
     "history": "British team known for chassis performance and driver development."},

    {"id": "astonmartin", "name": "Aston Martin", "logo": "/assets/astonmartin_logo.png", "car": "/assets/astonmartin_car.png",
     "engine_name": "Mercedes Hybrid", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈980 HP", "ERS": "Standard"},
     "drivers": [{"name": "Fernando Alonso", "no": 14, "wins": 32, "podiums": 106, "starts": 380, "photo": "/assets/alonso.png"},
                 {"name": "Lance Stroll", "no": 18, "wins": 0, "podiums": 3, "starts": 144, "photo": "/assets/stroll.png"}],
     "history": "Growing team with strong investments and a competitive chassis program."},

    {"id": "alpine", "name": "Alpine F1 Team", "logo": "/assets/alpine_logo.png", "car": "/assets/alpine_car.png",
     "engine_name": "Renault E-Tech Hybrid", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈960 HP", "ERS": "Standard"},
     "drivers": [{"name": "Pierre Gasly", "no": 10, "wins": 1, "podiums": 4, "starts": 140, "photo": "/assets/gasly.png"},
                 {"name": "Franco Colapinto", "no": 35, "wins": 0, "podiums": 0, "starts": 0, "photo": "/assets/colapinto.png"}],
     "history": "French works team focused on development and driver talent promotion."},

    {"id": "rb", "name": "Racing Bulls (RB)", "logo": "/assets/rb_logo.png", "car": "/assets/rb_car.png",
     "engine_name": "Honda RBPT Hybrid", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈1000 HP", "ERS": "Advanced"},
     "drivers": [{"name": "Liam Lawson", "no": 30, "wins": 0, "podiums": 0, "starts": 5, "photo": "/assets/lawson.png"},
                 {"name": "Isack Hadjar", "no": 77, "wins": 0, "podiums": 0, "starts": 0, "photo": "/assets/hadjar.png"}],
     "history": "Junior team with a focus on young talent and F1 exposure."},

    {"id": "haas", "name": "Haas F1 Team", "logo": "/assets/haas_logo.png", "car": "/assets/haas_car.png",
     "engine_name": "Ferrari Hybrid", "engine_stats": {"Type": "Hybrid V6 Turbo", "Combined Power": "≈950 HP", "ERS": "Standard"},
     "drivers": [{"name": "Esteban Ocon", "no": 31, "wins": 1, "podiums": 3, "starts": 131, "photo": "/assets/ocon.png"},
                 {"name": "Oliver Bearman", "no": 89, "wins": 0, "podiums": 0, "starts": 0, "photo": "/assets/bearman.png"}],
     "history": "American-run team with tight engineering budget but solid racecraft."},

    {"id": "williams", "name": "Williams Racing", "logo": "/assets/williams_logo.png", "car": "/assets/williams_car.png",
     "engine_name": "Mercedes Hybrid", "engine_stats": {"Type": "Hybrid V6", "Combined Power": "≈950 HP", "ERS": "Standard"},
     "drivers": [{"name": "Carlos Sainz", "no": 55, "wins": 3, "podiums": 19, "starts": 182, "photo": "/assets/sainz.png"},
                 {"name": "Alexander Albon", "no": 23, "wins": 0, "podiums": 2, "starts": 90, "photo": "/assets/albon.png"}],
     "history": "Legendary team with historic world titles, rebuilding with experienced drivers."},

    {"id": "sauber", "name": "Kick Sauber (Audi 2026)", "logo": "/assets/sauber_logo.png", "car": "/assets/sauber_car.png",
     "engine_name": "Ferrari Hybrid (→ Audi PU 2026)", "engine_stats": {"Type": "Hybrid V6 → 2026 Power Unit", "Combined Power": "≈950 HP", "ERS": "High Deployment 2026"},
     "drivers": [{"name": "Nico Hülkenberg", "no": 27, "wins": 0, "podiums": 1, "starts": 208, "photo": "/assets/hulkenberg.png"},
                 {"name": "Gabriel Bortoleto", "no": 99, "wins": 0, "podiums": 0, "starts": 0, "photo": "/assets/bortoleto.png"}],
     "history": "Sauber will become Audi works entry from 2026; 2025 season shows transition planning."},

    {"id": "cadillac", "name": "Cadillac Racing (2026 entry)", "logo": "/assets/cadillac_logo.png", "car": "/assets/cadillac_car.png",
     "engine_name": "GM Cadillac 2026 PU (est.)", "engine_stats": {"Type": "2026 Hybrid Power Unit", "Combined Power": "Estimated 1000 HP", "ERS": "Next-Gen High Voltage"},
     "drivers": [{"name": "Sergio Pérez", "no": 11, "wins": 6, "podiums": 35, "starts": 259, "photo": "/assets/perez.png"},
                 {"name": "Valtteri Bottas", "no": 77, "wins": 10, "podiums": 67, "starts": 223, "photo": "/assets/bottas.png"}],
     "history": "Cadillac has strong motorsport heritage (IMSA/Le Mans). Slated to join F1 as part of Andretti/Cadillac entry in 2026."}
]

# -------------------------
# CSS (neon/rage)
# -------------------------
NEON_CSS = """
:root{--bg:#050507;--panel:#0d0d10;--neon:#ff1a1a;--accent:#ff7b00;--muted:#9aa0a6;--glass: rgba(255,255,255,0.03);}
body {background:var(--bg); color:#fff; font-family:Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue";}
.header{padding:18px 28px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.03);position:sticky;top:0;background:linear-gradient(90deg,rgba(0,0,0,0.3),transparent);z-index:999;}
.brand{display:flex;align-items:center;gap:12px;}
.brand .logo{height:40px;width:40px;border-radius:8px;background:linear-gradient(45deg,var(--neon),var(--accent));display:flex;align-items:center;justify-content:center;font-weight:800;color:black;}
.nav a{color:var(--muted);margin-left:18px;text-decoration:none;font-weight:600;} .nav a:hover{color:var(--neon);transform:translateY(-2px);}
.container{max-width:1200px;margin:28px auto;padding:0 20px;}
.team-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-top:16px;}
.team-card{background:var(--panel);border-radius:12px;padding:14px;border-left:4px solid rgba(255,255,255,0.02);transition:transform .18s ease,box-shadow .18s ease;}
.team-card:hover{transform:translateY(-6px);box-shadow:0 18px 60px rgba(255,0,0,0.06);border-left:4px solid var(--neon);}
.team-logo{height:64px;width:64px;object-fit:contain;background:var(--glass);padding:6px;border-radius:8px;}
.team-name{font-weight:800;font-size:16px;margin-top:8px;}
.team-meta{color:var(--muted);margin-top:6px;font-size:13px;}
.team-btn{margin-top:12px;padding:8px 12px;border-radius:9px;cursor:pointer;background:transparent;color:var(--neon);border:1px solid rgba(255,255,255,0.04);text-decoration:none;display:inline-block;}
.card{background:var(--panel);padding:14px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,0.6);}
.car-image{width:100%;border-radius:12px;}
.driver-card{display:flex;gap:12px;align-items:center;padding:10px;border-radius:10px;background:linear-gradient(90deg,rgba(255,255,255,0.01),transparent);margin-bottom:10px;}
.driver-photo{width:84px;height:84px;object-fit:cover;border-radius:8px;}
.stat-row{display:flex;gap:10px;margin-top:10px;}
.stat{background:rgba(255,255,255,0.02);padding:8px 10px;border-radius:8px;font-weight:700;color:var(--muted);}
.footer{text-align:center;color:var(--muted);margin:40px 0;}
.badge{padding:6px 10px;border-radius:999px;background:rgba(255,0,0,0.14);color:var(--neon);font-weight:800;}
"""

# -------------------------
# DASH APP
# -------------------------
app = Dash(__name__, external_stylesheets=[
           dbc.themes.DARKLY], suppress_callback_exceptions=True)
app.index_string = app.index_string.replace(
    "</head>", f"<style>{NEON_CSS}</style></head>")

# -------------------------
# Helpers
# -------------------------


def make_nav():
    return html.Div(className="header", children=[
        html.Div(className="brand", children=[html.Div(
            className="logo", children="S"), html.H1("S.E.N.N.A. — RAGE DASH")]),
        html.Div(className="nav", children=[
            dcc.Link("Home", href="/", className="nav-link"),
            dcc.Link("Teams", href="/teams", className="nav-link"),
            dcc.Link("Drivers", href="/drivers", className="nav-link"),
            dcc.Link("Champions", href="/champions", className="nav-link"),
            dcc.Link("Predictions", href="/predictions", className="nav-link"),
            dcc.Link("Senna", href="/senna", className="nav-link"),
            dcc.Link("About", href="/about", className="nav-link"),
        ])
    ])


def team_card(team):
    return html.Div(className="team-card card", children=[
        html.Img(src=team["logo"], className="team-logo"),
        html.Div(className="team-name", children=team["name"]),
        html.Div(className="team-meta", children=team.get("history", "")),
        html.A("View", href=f"/team/{team['id']}", className="team-btn")
    ])


def points_bar():
    df = {"Team": [t["name"] for t in TEAMS], "Points": [
        sum(d.get("wins", 0)*25 for d in t["drivers"]) + 150 for t in TEAMS]}
    fig = px.bar(df, x="Team", y="Points", color="Team",
                 title="Season Points (simulated)")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", showlegend=False, title_font=dict(size=18))
    return fig

# -------------------------
# Pages
# -------------------------


def page_home():
    return html.Div(className="container", children=[
        html.Div(className="card", children=[html.H2("S.E.N.N.A. — Rage Edition"), html.P(
            "High-performance F1 analytics with local assets.")]),
        html.H3("Teams", style={"marginTop": "18px"}),
        html.Div(className="team-grid",
                 children=[team_card(t) for t in TEAMS]),
        html.Div(className="footer",
                 children="S.E.N.N.A. — Tribute to Ayrton Senna")
    ])


def page_teams():
    return html.Div(className="container", children=[html.H2("Teams — Pick one", className="section-title"), html.Div(className="team-grid", children=[team_card(t) for t in TEAMS])])


def page_team_detail(team_id):
    t = next((x for x in TEAMS if x["id"] == team_id), None)
    if not t:
        return html.Div(className="container", children=[html.H3("Team not found")])
    return html.Div(className="container", children=[
        html.Div(className="team-page", children=[
            html.Div(className="team-main", children=[
                html.Div(className="card", children=[
                    html.Img(src=t["car"], className="car-image"),
                    html.H2(t["name"], style={"marginTop": "12px"}),
                    html.Div("Engine: " + t["engine_name"],
                             style={"color": "var(--muted)"}),
                    html.Div(className="stat-row", children=[
                        html.Div(className="stat", children="Power: " +
                                 t["engine_stats"]["Combined Power"]),
                        html.Div(className="stat", children="ERS: " +
                                 t["engine_stats"]["ERS"]),
                        html.Div(className="stat", children="PU: " +
                                 t["engine_stats"]["Type"])
                    ]),
                    html.P(t.get("history", ""), style={
                           "color": "var(--muted)"})
                ]),
                html.H3("Drivers", style={"marginTop": "18px"}),
                html.Div(children=[
                    html.Div(className="driver-card", children=[
                        html.Img(src=d["photo"], className="driver-photo"),
                        html.Div(children=[html.Div(html.Strong(d["name"] + f"  #{d['no']}")), html.Div(style={
                                 "color": "var(--muted)"}, children=f"Wins: {d.get('wins', 0)}  • Podiums: {d.get('podiums', 0)}  • Starts: {d.get('starts', 0)}")])
                    ]) for d in t["drivers"]
                ])
            ]),
            html.Div(className="team-side", children=[
                html.Div(className="card", children=[html.H4("Quick Stats"), html.Div("Season form: RAGE mode", style={"color": "var(--neon)"}), html.Ul(
                    children=[html.Li("Downforce: HIGH"), html.Li("Top Speed: ELITE"), html.Li("Reliability: STRONG")], style={"color": "var(--muted)"})]),
                html.Div(className="card", style={"marginTop": "12px"}, children=[html.H4("Recent Upgrades"), html.Ul(
                    children=[html.Li("Aero floor update"), html.Li("Cooling inlet patch")], style={"color": "var(--muted)"})])
            ])
        ])
    ])


def page_drivers():
    rows = []
    for t in TEAMS:
        for d in t["drivers"]:
            rows.append(html.Div(className="card", style={"marginBottom": "10px"}, children=[html.Div(style={"display": "flex", "gap": "12px", "alignItems": "center"}, children=[html.Img(src=d["photo"], style={"width": "80px", "height": "80px", "objectFit": "cover", "borderRadius": "8px"}), html.Div(
                children=[html.Div(html.Strong(d["name"] + f"  —  {t['name']}")), html.Div(style={"color": "var(--muted)"}, children=f"Wins: {d.get('wins', 0)} • Podiums: {d.get('podiums', 0)} • Starts: {d.get('starts', 0)}")])])]))
    return html.Div(className="container", children=[html.H2("Drivers", className="section-title")] + rows)


def page_champions():
    champs = [{"year": 2023, "winner": "Max Verstappen"}, {"year": 2022,
                                                           "winner": "Max Verstappen"}, {"year": 2021, "winner": "Max Verstappen"}]
    return html.Div(className="container", children=[html.H2("Previous Champions", className="section-title")] + [html.Div(className="card", style={"marginBottom": "8px"}, children=[html.Strong(str(c["year"]) + " — "), html.Span(c["winner"])]) for c in champs])


def page_predictions():
    fig = points_bar()
    return html.Div(className="container", children=[html.H2("Predictions & Season Metrics", className="section-title"), dcc.Graph(figure=fig), html.Div(className="card", children=[html.H4("Model"), html.P("Simple weighted model using wins/podiums/points/upgrades. Replace with CSV-driven model later.")])])


def page_about():
    return html.Div(className="container", children=[html.H2("About S.E.N.N.A. — Rage Edition"), html.P("S.E.N.N.A. is a demo F1 analytics dashboard for project showcase. Uses local assets for stable offline demos.")])

# -------------------------
# Ayrton Senna tribute page
# -------------------------


def page_senna():
    # Use local assets/senna.png (you placed it in assets/)
    return html.Div(className="container", children=[
        html.Div(className="card", children=[html.H2("Ayrton Senna — Tribute"), html.P(
            "Ayrton Senna remains one of the greatest Formula 1 drivers of all time. This tribute highlights career, achievements and legacy.")]),
        html.Div(style={"display": "flex", "gap": "16px", "marginTop": "12px"}, children=[
            html.Img(src="/assets/senna.png",
                     style={"width": "320px", "borderRadius": "8px"}),
            html.Div(children=[
                html.H3("Career highlights"),
                html.Ul(children=[
                    html.Li("3x World Champion (1988, 1990, 1991)"),
                    html.Li("65 Grand Prix wins"),
                    html.Li("Legendary qualifying speed and wet-weather mastery"),
                ]),
                html.P("Senna's driving was fierce, spiritual and technically brilliant. His death at Imola in 1994 changed motorsport safety forever.")
            ])
        ]),
        html.H3("Gallery & Famous Quotes", style={"marginTop": "18px"}),
        html.Div(className="card", children=[html.P(
            '"Being second is to be the first of the ones who lose." — Ayrton Senna')]),
        html.Div(className="card", style={"marginTop": "12px"}, children=[html.H4(
            "Senna media / screenshot (local upload)"), html.Img(src="/assets/senna.png", style={"width": "100%", "borderRadius": "8px"})])
    ])


# -------------------------
# Layout + router
# -------------------------
app.layout = html.Div(children=[dcc.Location(
    id="url"), make_nav(), html.Div(id="page-content")])


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def router(pathname):
    if pathname == "/teams":
        return page_teams()
    if pathname and pathname.startswith("/team/"):
        team_id = pathname.split("/team/")[1]
        return page_team_detail(team_id)
    if pathname == "/drivers":
        return page_drivers()
    if pathname == "/champions":
        return page_champions()
    if pathname == "/predictions":
        return page_predictions()
    if pathname == "/senna":
        return page_senna()
    if pathname == "/about":
        return page_about()
    return page_home()


# -------------------------
# Startup: check assets and run
# -------------------------
if __name__ == "__main__":
    missing = []
    for t in TEAMS:
        for k in ("logo", "car"):
            p = t.get(k)
            if p and p.startswith("/assets/"):
                local = p.replace("/assets/", "assets/")
                if not os.path.exists(local):
                    missing.append(local)
        for d in t["drivers"]:
            ph = d.get("photo", "")
            if ph and ph.startswith("/assets/"):
                local = ph.replace("/assets/", "assets/")
                if not os.path.exists(local) and local not in missing:
                    missing.append(local)
    # check senna image
    if not os.path.exists("assets/senna.png"):
        missing.append("assets/senna.png")
    if missing:
        print("WARNING: missing asset files (place these in ./assets/):")
        for m in missing:
            print("  -", m)
    print("Starting S.E.N.N.A. dashboard on http://127.0.0.1:8060")
    app.run(debug=False, port=8080)
