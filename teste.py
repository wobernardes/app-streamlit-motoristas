import streamlit as st
from datetime import date

st.set_page_config(page_title="Cadastro de Motoristas", layout="wide")
st.title("Gestão de Transportadoras e Motoristas")

# 1. Inicializa os dados na memória da sessão
if "transportadoras" not in st.session_state:
    st.session_state.transportadoras = [
        {
            "nome": "Dallogs Express",
            "motoristas": [
                {
                    "nome": "Edson da Silva",
                    "cpf": "123.456.789-00",
                    "cnh": "123456789",
                    "validade": "15/08/2028",
                    "cetpp": "Sim",
                    "placa": "UDX-5A45",
                    "renavam": "00123456789"
                },
                {
                    "nome": "Luciane Oliveira",
                    "cpf": "987.654.321-11",
                    "cnh": "987654321",
                    "validade": "20/11/2027",
                    "cetpp": "Não",
                    "placa": "XYZ-9W87",
                    "renavam": "00987654321"
                },
            ]
        }
    ]

# 2. Formulário de Cadastro Completo
with st.expander("➕ Cadastrar Novo Motorista", expanded=True):
    with st.form("form_cadastro_motorista", clear_on_submit=True):
        # Linha 1: Transportadora
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            nomes_transp = [t["nome"] for t in st.session_state.transportadoras]
            transp_existente = st.selectbox("Transportadora Cadastrada:", nomes_transp)
        with col_t2:
            nova_transp = st.text_input("Ou digite uma Nova Transportadora (opcional):", placeholder="Ex: Braspress")

        # Linha 2: Dados Pessoais e Habilitação
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.2])
        with col1:
            nome = st.text_input("Nome Completo *")
        with col2:
            cpf = st.text_input("CPF *", placeholder="000.000.000-00")
        with col3:
            cnh = st.text_input("CNH *")
        with col4:
            validade = st.date_input("Validade CNH *", format="DD/MM/YYYY")

        # Linha 3: Documentação Específica e Veículo
        col5, col6, col7 = st.columns(3)
        with col5:
            cetpp = st.selectbox("Possui CETPP? *", ["Sim", "Não"])
        with col6:
            placa = st.text_input("Placa *", placeholder="ABC-1D23")
        with col7:
            renavam = st.text_input("RENAVAM *", placeholder="00000000000")

        enviado = st.form_submit_button("Salvar Cadastro", use_container_width=True)

        if enviado:
            nome_transportadora_final = nova_transp.strip() if nova_transp.strip() else transp_existente

            if nome and cpf and cnh and placa and renavam:
                novo_motorista = {
                    "nome": nome.strip(),
                    "cpf": cpf.strip(),
                    "cnh": cnh.strip(),
                    "validade": validade.strftime("%d/%m/%Y"),
                    "cetpp": cetpp,
                    "placa": placa.strip().upper(),
                    "renavam": renavam.strip()
                }

                encontrada = False
                for transp in st.session_state.transportadoras:
                    if transp["nome"].lower() == nome_transportadora_final.lower():
                        transp["motoristas"].append(novo_motorista)
                        encontrada = True
                        break

                if not encontrada:
                    st.session_state.transportadoras.append({
                        "nome": nome_transportadora_final,
                        "motoristas": [novo_motorista]
                    })

                st.success(f"Motorista **{nome}** vinculado à **{nome_transportadora_final}** com sucesso!")
            else:
                st.warning("Preencha todos os campos obrigatórios marcados com *.")

st.divider()

# 3. Campo de Pesquisa Multi-campo
busca = st.text_input("🔍 Pesquisar por Nome, CPF, CNH, Placa, RENAVAM ou Transportadora:")

for transp in st.session_state.transportadoras:
    motoristas_filtrados = [
        mot for mot in transp["motoristas"]
        if not busca or any(
            busca.lower() in str(valor).lower()
            for valor in [
                transp["nome"],
                mot["nome"],
                mot["cpf"],
                mot["cnh"],
                mot["cetpp"],
                mot["placa"],
                mot["renavam"]
            ]
        )
    ]

    if motoristas_filtrados:
        st.subheader(f"🚚 {transp['nome']}")
        st.dataframe(
            motoristas_filtrados,
            use_container_width=True,
            column_config={
                "nome": "Nome do Motorista",
                "cpf": "CPF",
                "cnh": "CNH",
                "validade": "Validade CNH",
                "cetpp": "CETPP",
                "placa": "Placa",
                "renavam": "RENAVAM"
            }
        )