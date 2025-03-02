import gradio as gr
import json
from agent.state import AgentState
from agent.graph import create_workflow
import pandas as pd
import os
import tempfile
import re

def inference(niche, locations, role):
    app = create_workflow(AgentState)
    results = app.invoke({
        "niche": niche,
        "locations": locations,
        "limit_per_location": 20, #default limit in google maps
        "role": role,
    })
    df = pd.DataFrame.from_dict(results['final_sheet'])

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "output.xlsx")
    
    df.to_excel(temp_path, index=False)

    

    html_df = df
    if 'summary' in html_df.columns:
        # Replace newlines with spaces
        html_df['summary'] = html_df['summary'].apply(lambda x: x.replace('\n', ' ') if isinstance(x, str) else x)
    
    html_table = html_df.to_html(classes='custom-table')
    styles = """
    <style>
    .custom-table {
        width: 100%;
    }
    .custom-table th {
        text-align: center;
    }
    .custom-table th:nth-child(1) {
        width: 20px;
    }
    .custom-table th:nth-child(2) {
        width: 150px;
    }
    .custom-table th:nth-child(3) {
        width: 50px;
    }
    .custom-table th:nth-child(4) {
        width: 180px;
    }
    .custom-table th:nth-child(5) {
        width: 120px;
    }
    .custom-table th:nth-child(6) {
        width: 600px;
    }
    </style>
    """


    html_table = styles + html_table

    html_table = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_table)

    return (html_table, temp_path)

brazil_cities = []

with open("src/utils/locations.json", "r") as f:
    locations = json.load(f)
    for local in locations:
        if local['country_code'] == 'BR':
            brazil_cities.append(
                local['canonical_name']
                )

with gr.Blocks() as demo:
    gr.Markdown("## Lead Capture Agent")
    niche = gr.Textbox(label="Niche")
    locations = gr.Dropdown([city for city in brazil_cities], label="Locations", multiselect=True, max_choices=3)
    role = gr.Textbox(label="Role")

    with gr.Row():
        generate = gr.Button("Run")

    output = gr.HTML(label="Results will be displayed here")
    save = gr.File(label="Download Results")

    generate.click(
        fn=inference,
        inputs=[niche, locations, role],
        outputs=[output, save],
        show_progress='minimal')
demo.launch()
