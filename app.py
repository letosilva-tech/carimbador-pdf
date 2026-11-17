
import streamlit as st
import fitz
import io
import zipfile

st.set_page_config(
    page_title="Carimbador de PDF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Carimbador de PDF")
st.write("Sistema para aplicar carimbos em documentos PDF.")

st.divider()

st.subheader("1. Selecionar documentos")

arquivos = st.file_uploader(
    "Escolha um ou vários arquivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

st.divider()

st.subheader("2. Configurar o carimbo")

contrato = st.text_input(
    "Número do contrato",
    value="226/2025"
)

unidade = st.text_input(
    "Nome da unidade",
    value="PS ARNALDO DE FIGUEIREDO"
)

local = st.text_input(
    "Identificação / localização",
    value="FREITAS - BARUERI/SP"
)

posicao = st.selectbox(
    "Posição do carimbo",
    [
        "Inferior direito",
        "Inferior esquerdo",
        "Superior direito",
        "Superior esquerdo"
    ]
)

st.caption(
    "O carimbo será aplicado em todas as páginas de cada PDF."
)

st.divider()

st.subheader("3. Gerar documentos carimbados")

if st.button("GERAR PDFS CARIMBADOS", type="primary"):

    if not arquivos:
        st.warning("Selecione pelo menos um arquivo PDF.")

    elif (
        not contrato.strip()
        or not unidade.strip()
        or not local.strip()
    ):
        st.warning("Preencha todos os campos do carimbo.")

    else:
        zip_buffer = io.BytesIO()
        processados = 0

        with zipfile.ZipFile(
            zip_buffer, "w", zipfile.ZIP_DEFLATED
        ) as pacote:

            for arquivo in arquivos:
                try:
                    documento = fitz.open(
                        stream=arquivo.getvalue(),
                        filetype="pdf"
                    )

                    texto_carimbo = (
                        f"Contrato de Gestão nº {contrato.strip()}\n"
                        f"{unidade.strip()}\n"
                        f"{local.strip()}"
                    )

                    for pagina in documento:
                        largura = pagina.rect.width
                        altura = pagina.rect.height

                        margem = 24
                        largura_carimbo = min(
                            230, largura - 2 * margem
                        )
                        altura_carimbo = min(
                            48, altura - 2 * margem
                        )

                        if posicao == "Inferior direito":
                            x = largura - largura_carimbo - margem
                            y = altura - altura_carimbo - margem

                        elif posicao == "Inferior esquerdo":
                            x = margem
                            y = altura - altura_carimbo - margem

                        elif posicao == "Superior direito":
                            x = largura - largura_carimbo - margem
                            y = margem

                        else:
                            x = margem
                            y = margem

                        area = fitz.Rect(
                            x,
                            y,
                            x + largura_carimbo,
                            y + altura_carimbo
                        )

                        pagina.insert_textbox(
                            area,
                            texto_carimbo,
                            fontname="tiit",
                            fontsize=8,
                            lineheight=1.3,
                            color=(0, 0, 0),
                            align=fitz.TEXT_ALIGN_CENTER,
                            overlay=True
                        )

                    nome_saida = arquivo.name.rsplit(".", 1)[0]
                    nome_saida += "_carimbado.pdf"

                    pacote.writestr(
                        nome_saida,
                        documento.tobytes()
                    )

                    documento.close()
                    processados += 1

                except Exception as erro:
                    st.error(
                        f"Erro ao processar {arquivo.name}: {erro}"
                    )

        zip_buffer.seek(0)

        if processados > 0:
            st.success(
                f"{processados} documento(s) processado(s) com sucesso!"
            )

            st.download_button(
                label="📥 BAIXAR DOCUMENTOS CARIMBADOS",
                data=zip_buffer.getvalue(),
                file_name="documentos_carimbados.zip",
                mime="application/zip",
                type="primary"
            )

st.divider()

st.caption("Carimbador de PDF | Processamento de documentos")
st.markdown("**Desenvolvido por Leto Milton**")
