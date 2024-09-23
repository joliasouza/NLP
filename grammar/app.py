import streamlit as st
import language_tool_python

def text_correction(txt):
    tool = language_tool_python.LanguageTool('pt-BR')
    matches = tool.check(txt)
    corrected_text = language_tool_python.utils.correct(txt, matches)
    return corrected_text

def main():
    st.header("CORRETOR DE TEXTO")
    text_area = st.text_area("Digite seu texto:")
    if text_area:
        if st.button("Enviar"):
            st.write("Texto original:")
            st.success(text_area)
            st.write("Texto corrigido:")
            corrected_text = text_correction(text_area)
            st.success(corrected_text)

if __name__ == "__main__":
    main()