import plotly.express as px
import plotly.graph_objects as go

def apply_layout(fig, title="", height=400):
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig