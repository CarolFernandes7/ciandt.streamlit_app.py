import streamlit as st
import pandas as pd

# Carregar os dados das perguntas e respostas
data_files = {
    "Q5": "Q5.csv",
    "Q6": "Q6.csv",
    "Q7": "Q7.csv",
    "Q8": "Q8.csv",
    "Q15": "Q15.csv",
    "Q22": "Q22.csv"
}

questions_text = {
    "Q5": "Q5: Which of the following best describes your combined household income?",
    "Q6": "Q6: Please select which of the following statements is closest to being true in relation to your household finances.",
    "Q7": "Q7: Do you own or rent your home?",
    "Q8": "Q8: What type of home do you own and live in?",
    "Q15": "Q15: Which of the following, if any, do you currently own?",
    "Q22": "Q22: In the table below, please indicate the option that best describes your home energy situation."
}

data = {}
for question, file in data_files.items():
    try:
        data[question] = pd.read_csv(file)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo {file}: {e}")

# Função para formatar porcentagens
def format_percentage(df):
    df["Percentage"] = (
        df["Percentage"]
        .str.replace("%", "")
        .astype(float) / 100
    )
    df["Percentage"] = (df["Percentage"] * 100).round(0).astype(int).astype(str) + "%"
    return df

# Configuração do Streamlit com abas
st.title("EON B2C - Survey Data & Segmentation")
tab1, tab2, tab3, tab4 = st.tabs(["Question Responses", "High", "Medium", "Low"])

# Aba Question Responses
with tab1:
    st.header("Question Responses")
    for question, df in data.items():
        st.subheader(questions_text[question])  # Exibir a pergunta no topo de cada tabela
        if question == "Q22":
            st.table(df)  # Exibir Q22 como está, sem formatar porcentagem
        else:
            st.table(format_percentage(df))

# Aba High
with tab2:
    st.header("High")
    st.subheader("Disposable income")
    st.table(format_percentage(data["Q5"].iloc[1:3]))

    st.subheader("Homeowner status")
    st.table(format_percentage(data["Q6"].iloc[1:4]))

    st.subheader("House type")
    st.table(format_percentage(data["Q8"].iloc[:4]))

    st.subheader("Product ownership")
    st.table(format_percentage(data["Q15"].iloc[:5]))

# Aba Medium
with tab3:
    st.header("Medium")
    st.subheader("Disposable income")
    st.table(format_percentage(data["Q5"].iloc[3:5]))

    st.subheader("Homeowner status")
    st.table(format_percentage(data["Q6"].iloc[1:4]))

    st.subheader("House type")
    st.table(format_percentage(data["Q8"].iloc[:4]))

# Aba Low
with tab4:
    st.header("Low")
    st.subheader("Group A (Renters)")
    st.table(format_percentage(data["Q7"].iloc[3:8]))

    st.subheader("Group B (Own Flat)")
    st.table(format_percentage(data["Q8"].iloc[4:6]))

    st.subheader("Group C (Low Income)")
    st.table(format_percentage(data["Q5"].iloc[1:3]))