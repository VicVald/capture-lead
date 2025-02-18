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
        "limit_per_location": 4,
        "role": role,
    })
    df = pd.DataFrame.from_dict(results['final_sheet'])
    # df = pd.DataFrame({
    #     "name": ["Clínica de Psicologia", "RD Clínica de Psicologia"],
    #     "phone": ["(11) 9999-9999", "(11) 9999-9999"],
    #     "website": ["https://www.clinicadepsicologia.com.br", "https://www.rdclinicadepsicologia.com.br"],
    #     "address": ["Rua dos Bobos, 0", "Rua dos Bobos, 0"],
    #     "summary": ["""**Sobre a Clínica de Psicologia**

    #     A Clínica de Psicologia tem um endereço em Bauru, Estado de São Paulo, Brasil, e pode ser contatada pelo telefone (14) 99198-4885. Seu site está vazio, o que pode dificultar a busca por informações sobre a clínica e serviços oferecidos.

    #     **Resumo da aparência online**

    #     A clínica não tem uma presença online definida, pois seu site está vazio. No entanto, pode ter uma presença nos principais motores de busca, como Google, se estiver utilizando técnicas de SEO (Search Engine Optimization).

    #     **Sugestão para melhorar a presença online**

    #     Um desenvolvedor web pode ajudar a Clínica de Psicologia a melhorar sua presença online de várias maneiras:

    #     1. **Desenvolver um site**: Criar um site com informações sobre a clínica, serviços oferecidos, equipe de profissionais, horários de funcionamento e contato.
    #     2. **Mapear a experiência do usuário**: Melhorar a navegação e a usabilidade do site para que os usuários possam encontrar facilmente as informações que precisam.
    #     3. **Otimizar para motores de busca**: Utilizar técnicas de SEO para que a clínica apareça nos primeiros resultados da busca nos principais motores de busca.
    #     4. **Gerenciar a presença nos redes sociais**: Criar e gerenciar contas nas principais redes sociais para que a clínica possa se conectar com seus clientes e potenciais clientes.
    #     5. **Integrar ferramentas de gestão de agendamento**: Integrar ferramentas de gestão de agendamento para que os clientes possam agendar consultas online.

    #     Essas são apenas algumas sugestões para melhorar a presença online da Clínica de Psicologia. Um desenvolvedor web pode ajudar a clínica a criar uma presença online forte e eficaz.""",
    #     """**Resumo da aparência online da clínica de psicologia:**

    #     A clínica de psicologia "RD Clínica de Psicologia" parece não ter uma presença online oficial, pois as informações disponíveis são limitadas. No entanto, com base nas informações fornecidas, podemos inferir que:

    #     * Ela não tem um site oficial (website = []).
    #     * Não há informações sobre redes sociais ou outras plataformas online.

    #     **Sugestão para um desenvolvedor web:**

    #     Para ajudar a clínica de psicologia a melhorar sua presença online, eu sugeriria:

    #     1. **Desenvolver um site oficial**: Crie um site simples e intuitivo que forneça informações básicas sobre a clínica, como serviços oferecidos, equipe de psicólogos, contatos, etc.
    #     2. **Implementar redes sociais**: Crie perfis nas principais redes sociais (Facebook, Instagram, Twitter, etc.) e atualize-as regularmente com conteúdo relevante, como notícias, dicas de saúde mental, etc.
    #     3. **Otimizar para SEO**: Ajuste o site para que ele seja mais visível nas buscas do Google, utilizando palavras-chave relevantes e otimizando a estrutura do site.
    #     4. **Integrar sistema de agendamento online**: Desenvolva um sistema de agendamento online que permita aos pacientes marcar consultas de forma fácil e rápida.
    #     5. **Mantenha a consistência**: Certifique-se de que a presença online seja atualizada regularmente para manter a consistência e a credibilidade da clínica.

    #     Essas sugestões podem ajudar a clínica de psicologia a melhorar sua presença online e atrair mais pacientes."""]
    #         })

    # Create Excel file in memory
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "output.xlsx")
    
    # Save DataFrame to Excel file
    df.to_excel(temp_path, index=False)

    

    # Create Markdown table from DataFrame
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

    # Replace Markdown bold with HTML bold
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
