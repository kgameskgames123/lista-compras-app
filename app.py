import streamlit as st
import math
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import tempfile

st.set_page_config(page_title="Lista de Compras", layout="centered")

# =========================
# LISTA COMPLETA
# =========================
itens = [
    # 🍚 Alimentação
    {"nome": "Arroz", "consumo": 10, "lote": 5, "unidade": "kg"},
    {"nome": "Feijão", "consumo": 4, "lote": 1, "unidade": "kg"},
    {"nome": "Macarrão", "consumo": 2, "lote": 1, "unidade": "kg"},
    {"nome": "Café", "consumo": 1, "lote": 1, "unidade": "kg"},
    {"nome": "Açúcar", "consumo": 2, "lote": 1, "unidade": "kg"},
    {"nome": "Sal", "consumo": 1, "lote": 1, "unidade": "kg"},
    {"nome": "Molho de tomate", "consumo": 6, "lote": 1, "unidade": "sachê"},
    {"nome": "Alho", "consumo": 0.5, "lote": 0.5, "unidade": "kg"},
    {"nome": "Óleo", "consumo": 3, "lote": 1, "unidade": "litro"},
    {"nome": "Molho inglês", "consumo": 1, "lote": 1, "unidade": "pote"},
    {"nome": "Nescau", "consumo": 1, "lote": 1, "unidade": "kg"},
    {"nome": "Sazon", "consumo": 1, "lote": 1, "unidade": "pacote"},
    {"nome": "Pipoca", "consumo": 1, "lote": 1, "unidade": "kg"},

    # 🧽 Limpeza
    {"nome": "Detergente", "consumo": 5, "lote": 1, "unidade": "frasco"},
    {"nome": "Esponja", "consumo": 1, "lote": 1, "unidade": "pacote"},
    {"nome": "Perfex", "consumo": 1, "lote": 1, "unidade": "pacote"},
    {"nome": "Veja", "consumo": 1, "lote": 1, "unidade": "frasco"},
    {"nome": "Cif", "consumo": 1, "lote": 1, "unidade": "frasco"},
    {"nome": "Desinfetante", "consumo": 4, "lote": 1, "unidade": "litro"},
    {"nome": "Cloro", "consumo": 2, "lote": 1, "unidade": "litro"},
    {"nome": "Álcool", "consumo": 1, "lote": 1, "unidade": "litro"},
    {"nome": "Sabão em pó", "consumo": 1, "lote": 1, "unidade": "kg"},
    {"nome": "Bombril", "consumo": 1, "lote": 1, "unidade": "pacote"},
    {"nome": "Saco de lixo", "consumo": 1, "lote": 1, "unidade": "rolo"},

    # 🚽 Banheiro
    {"nome": "Desodorizador sanitário", "consumo": 3, "lote": 1, "unidade": "unidade"},
    {"nome": "Aromatizador spray", "consumo": 1, "lote": 1, "unidade": "frasco"},
    {"nome": "Sabonete líquido", "consumo": 1, "lote": 1, "unidade": "litro"},

    # 🧻 Papéis
    {"nome": "Papel higiênico", "consumo": 24, "lote": 12, "unidade": "rolo"},
    {"nome": "Papel toalha", "consumo": 2, "lote": 2, "unidade": "rolo"},
    {"nome": "Filtro de papel", "consumo": 1, "lote": 1, "unidade": "caixa"},
    {"nome": "Papel filme", "consumo": 1, "lote": 1, "unidade": "rolo"},
    {"nome": "Papel alumínio", "consumo": 1, "lote": 1, "unidade": "rolo"},

    # 🧩 Outros
    {"nome": "SBP", "consumo": 1, "lote": 1, "unidade": "unidade"},
    {"nome": "Fósforo", "consumo": 1, "lote": 1, "unidade": "pacote"},
]

# =========================
# ESTADO
# =========================
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.lista_final = []

# =========================
# FLUXO
# =========================
if st.session_state.indice < len(itens):

    item = itens[st.session_state.indice]
    st.title(f"Produto: {item['nome']}")

    tem = st.radio("Tem em casa?", ["Sim", "Não"])

    comprar = 0

    if tem == "Não":
        estoque = st.number_input(
            f"Quanto ainda tem? ({item['unidade']})",
            min_value=0.0
        )
        necessidade = max(0, item["consumo"] - estoque)
        comprar = math.ceil(necessidade / item["lote"])
        st.write(f"👉 Precisa comprar: {comprar} unidade(s)")

    if st.button("Próximo"):
        st.session_state.lista_final.append(
            {"produto": item["nome"], "quantidade": comprar}
        )
        st.session_state.indice += 1
        st.rerun()

else:

    st.title("Lista Final de Compras")

    lista_para_pdf = []

    for item in st.session_state.lista_final:
        if item["quantidade"] > 0:
            texto = f"{item['produto']} - {item['quantidade']} unidade(s)"
            st.write(texto)
            lista_para_pdf.append(texto)

    if st.button("Gerar PDF"):

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        styles = getSampleStyleSheet()
        elementos = []

        elementos.append(Paragraph("Lista de Compras", styles["Heading1"]))
        elementos.append(Spacer(1, 20))

        for linha in lista_para_pdf:
            elementos.append(Paragraph(linha, styles["Normal"]))
            elementos.append(Spacer(1, 12))

        doc.build(elementos)

        with open(temp_file.name, "rb") as f:
            st.download_button(
                "Baixar PDF",
                f,
                file_name="lista_compras.pdf",
                mime="application/pdf"
            )

    if st.button("Reiniciar"):
        st.session_state.indice = 0
        st.session_state.lista_final = []
        st.rerun()
