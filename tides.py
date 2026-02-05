import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# URLs of the data sources
urls = [
    "https://comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Piattaforma.html",
    "https://comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Punta_Salute.html",
    "https://comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Burano.html"
]

# Read the data from the URLs
data_frames = []
for url in urls:
    try:
        data_frames.append(pd.read_html(url)[0])
    except Exception as e:
        st.error(f"Error reading {url}: {e}")

# Extract the first and second columns for x and y axes
x = data_frames[0].iloc[:, 0]
y = data_frames[0].iloc[:, 1]
z = data_frames[1].iloc[:, 1]
w = data_frames[2].iloc[:, 1]

# Create the plotly figure
fig = go.Figure()

# Add traces for each dataset
fig.add_trace(go.Scatter(x=x, y=y, name='Piattaforma CN', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=x, y=z, name='Punta Salute', line=dict(color='green')))
fig.add_trace(go.Scatter(x=x, y=w, name='Burano', line=dict(color='red')))

# Add a horizontal line at y=0
fig.add_shape(type='line', x0=x.min(), x1=x.max(), y0=0, y1=0, line=dict(color='black', width=0.5))

# Extract the last date for the title
d = data_frames[0].iloc[-1, 0]

# Update layout
fig.update_layout(
    title=f'Maree Laguna di Venezia - Ultimo dato: {d}',
    xaxis_title='Data',
    yaxis_title='Altezza sul livello del mare',
    legend=dict(orientation='v', yanchor="top", y=0.99, xanchor="left", x=0.01),
    #height=900,
    #width=1200,
    autosize=True
)

# Display the plot in Streamlit
st.plotly_chart(fig)