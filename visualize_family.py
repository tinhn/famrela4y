import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import pandas as pd

# cyto.load_extra_layouts()

# data
pdf_data=pd.read_csv('my-family-relation.csv', sep=',')

def graph_elements(pdf, sourc_col='source', dest_col='target'):
    df = pdf.copy()
    
    A = list(df[sourc_col].unique())
    B = list(df[dest_col].unique())
    node_list = set(A + B)

    cy_nodes = [{"data": {"id": item, "label": item}} for item in node_list]

    cy_edges_with_label = []
    for i, r in enumerate(df.iterrows()):
        cy_edges_with_label.append({
            'data': {
                'id': f"edge-{i}",
                'source': r[1][sourc_col],
                'target': r[1][dest_col],
                'label': r[1]['label']
            }
        })

    # Tạo edges không label, không id
    df['edge'] = df.apply(lambda row: frozenset([row[sourc_col], row[dest_col]]), axis=1)
    unique_edges = df.drop_duplicates(subset='edge')[[sourc_col, dest_col]]
    cy_edges_without_label = [
        {'data': {'source': r[sourc_col], 'target': r[dest_col]}}
        for _, r in unique_edges.iterrows()
    ]

    initial_elements = cy_nodes + cy_edges_without_label
    full_elements = cy_nodes + cy_edges_with_label
    return initial_elements, full_elements

def filter_data(df, top_k, filter_value, sourc_col='source', dest_col='target'):
    df_limit = df.head(int(top_k))
    my_df = df_limit[
        (df_limit[sourc_col].str.strip()==filter_value) 
      | (df_limit[dest_col].str.strip()==filter_value)
    ]
    #.drop(columns=['index'])
    return my_df.sort_values('sim_score')

# 
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title="Cytoscape"


#
app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Family relationships",
        brand_style = {"font-size":"30px", "float":"left",},
        color="rgb(64,185,212)",
        dark=True,
        fluid = True,
    ),
    dbc.Container([
        dbc.Row([
            dbc.Col([html.P("Graph layout:")],width=1),
            dbc.Col([html.P("Node shape:")],width=1),
            dbc.Col([html.P("Shape size:")],width=1),
            dbc.Col([html.Div(children="Number of edge:", id="edge_select_id")])
        ]),
        dbc.Row([
            dbc.Col([dcc.Dropdown(['random','grid','circle'],'random', id='layout_id')],width=1),
            dbc.Col(
                [dcc.Dropdown(
                    ['ellipse','triangle','rectangle','diamond','pentagon','hexagon','heptagon','octagon','star','polygon'],
                    'ellipse', 
                    id='shape_id')
                ],
                width=1
            ),
            dbc.Col([dcc.Slider(min=10, max=60, value=15, id="shape_size_id")],width=1),
            dbc.Col([dcc.Slider(min=pdf_data.shape[0], max=pdf_data.shape[0], value=pdf_data.shape[0], id="top_edge_id")]),
        ]),
        dbc.Row([            
            dbc.Col([                
                html.Div(
                    style={"border":"1px silver solid"},
                    children=[
                        html.H3("Sơ đồ mạng quan về mối hệ gia đình", style={"textAlign": "center"}),
                        dcc.Store(id='store-full-elements'),
                        cyto.Cytoscape(id="cytoscape",style={"width": "98%", "height": "730px"})
                    ]),
            ])
        ]),
        # dbc.Row([
        #     dbc.Col([
        #         html.P(id="node_selected_id",style={'color': 'darkviolet','font-weight': 'bold','text-align':'center'}),
        #         html.Div([dash_table.DataTable(id='tbl_product', fixed_rows={'headers': True},style_table={'height': '200px'})])
        #     ])
        # ])
    ],fluid = True)
])

# 
@app.callback(
        Output('cytoscape', 'layout'),
        Input('layout_id', 'value')        
)
def update_cytoscape_layout(layout):
    return {'name': layout}

# 
@app.callback(
    Output('cytoscape', 'elements'),
    Output('store-full-elements','data'),
    Output('edge_select_id','children'),
    Input('top_edge_id', 'value')
)
def displayGraphElements(edge_limit_value):
    initial_elements, full_elements = graph_elements(pdf_data.head(int(edge_limit_value)))
    return full_elements, full_elements, f"Number of edge: {edge_limit_value}"

@app.callback(
    Output('cytoscape', 'stylesheet'),
    Input('cytoscape', 'tapNodeData'),
    Input('shape_id', 'value'),
    Input('shape_size_id', 'value'),
    State('store-full-elements', 'data')
)
def update_graph_on_node_click(node_data, node_shape, shape_size, full_elements):
    default_stylesheet = [
        {
            "selector": 'node',
            'style': {
                "label": "data(label)",
                "color": "#191A17",
                'shape': node_shape,
                'background-color': "#8DB4CA",
                "opacity": 1,
                "height": f"{shape_size}px",
                "width": f"{shape_size}px",
                "font-size": 14,
            }
        },
        {
            "selector": 'edge',
            'style': {
                'line-color': '#A3C4BC',
                "curve-style": "bezier",
                "opacity": 0.05
            }
        },
    ]

    if not node_data or not full_elements:
        return default_stylesheet

    selected_node_id = node_data['id']
    stylesheet = default_stylesheet.copy()

    # Highlight selected node
    stylesheet.append({
        "selector": f'node[id="{selected_node_id}"]',
        "style": {
            'background-color': 'darkviolet',
            "border-color": "purple",
            "border-width": 2,
            "border-opacity": 1,
            "label": "data(label)",
            "color": "darkviolet",
            "text-opacity": 1,
            "font-size": 18,
        }
    })

    # Highlight outgoing edges and target nodes
    for el in full_elements:
        if 'source' in el['data'] and el['data']['source'] == selected_node_id:
            target_id = el['data']['target']
            edge_id = el['data'].get('id', '')

            # Highlight target node
            stylesheet.append({
                "selector": f'node[id="{target_id}"]',
                "style": {
                    'background-color': 'green',
                    'opacity': 0.9,
                    "label": "data(label)",
                    "color": "darkviolet",
                    "font-size": 18,
                }
            })

            # Highlight edge with arrow
            stylesheet.append({
            "selector": f'edge[id="{edge_id}"]',
            "style": {
                "line-color": 'green',
                "target-arrow-shape": "triangle",
                "target-arrow-color": "green",
                "arrow-scale": 0.5,
                "curve-style": "bezier",
                'opacity': 0.9,
                "label": el['data'].get("label", ""),
                "font-size": 12,
                "color": "darkviolet",
                "text-opacity": 1,
            }
        })

    return stylesheet

if __name__ == "__main__":
    app.run(debug=False, use_reloader=True)