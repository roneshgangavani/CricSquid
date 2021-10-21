external_stylesheets = [
    "/static/assets/css/dashlite.css", "/static/assets/css/theme.css",
    "/static/css/globle.css",
    "/static/css/custome_scrollbar.css"
]

colors = {
    "background": "#FFF",
    'text': '#364a63',
    "plot-background": "#f5f6fa"
}

colors_lines = [
    'rgb(25, 117, 250)',
    'rgb(183, 72, 170)',
]

def update_fig_vs(fig):
    fig.update_layout(plot_bgcolor=colors['plot-background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      font=dict(size=14),
                      height = 400,
                      title_x=0.5)

def update_fig(fig):
    fig.update_layout(plot_bgcolor=colors['plot-background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      font=dict(size=14),
                      title_x=0.5)

def update_mobile_fig(fig):
    fig.update_layout(
        plot_bgcolor=colors['plot-background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font=dict(size=10),
        title_x=0.5,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5,
        ),

    )

def update_gis_fig(fig):
    fig.update_layout(
        plot_bgcolor=colors['plot-background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font=dict(size=10),
        title_x=0.5,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),

    )

def update_mobile_fig_v2(fig):
    fig.update_layout(
        plot_bgcolor=colors['plot-background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font=dict(size=10),
        title_x=0.5,
        margin=dict(
            l=1,
            r=1,
            t=10,
            b=1,
        )
    )