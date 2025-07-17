import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import requests
import time

# Configuração da página
st.set_page_config(page_title="Lumen TTS Cloud", page_icon="🔊", layout="wide")
st.title("🔊 Conversor de Texto para Voz na Nuvem")
st.caption("Integração Colab + Streamlit | Por Lumen")

# Função principal
def text_to_speech(text, lang='pt-br', slow=False):
    try:
        # Cria o objeto gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Salva em buffer de memória
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        return audio_bytes
        
    except Exception as e:
        st.error(f"Erro na conversão: {str(e)}")
        return None

# Layout da interface
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Configurações")
    texto = st.text_area("Digite seu texto:", 
                        "Olá! Eu sou a Lumen, sua assistente de voz na nuvem. Como posso ajudar?", 
                        height=150)
    
    lang_options = {
        "Português Brasil": "pt-br",
        "Inglês EUA": "en",
        "Espanhol": "es",
        "Francês": "fr",
        "Alemão": "de"
    }
    
    lang = st.selectbox("Idioma:", list(lang_options.keys()), index=0)
    slow = st.checkbox("Falar mais devagar")
    convert_button = st.button("▶️ Converter para Voz", type="primary", use_container_width=True)

with col2:
    st.subheader("Resultado")
    status_placeholder = st.empty()
    audio_placeholder = st.empty()
    download_placeholder = st.empty()
    
    if convert_button and texto.strip():
        with st.spinner("Convertendo texto em voz..."):
            # Simula processamento na nuvem
            time.sleep(1)
            
            # Converte texto em áudio
            audio_bytes = text_to_speech(texto, lang_options[lang], slow)
            
            if audio_bytes:
                # Exibe player de áudio
                audio_placeholder.audio(audio_bytes, format='audio/mp3')
                
                # Cria link de download
                b64 = base64.b64encode(audio_bytes.read()).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="lumen_audio.mp3">⬇️ Baixar Áudio</a>'
                download_placeholder.markdown(href, unsafe_allow_html=True)
                
                status_placeholder.success("Conversão concluída com sucesso!")
            else:
                status_placeholder.error("Falha na conversão. Tente novamente.")

# Informações adicionais
st.divider()
st.info("""
**Como funciona:**
1. O texto é enviado para o serviço gTTS do Google
2. A conversão acontece na nuvem
3. O áudio é retornado e reproduzido diretamente no navegador

**Dicas:**
- Para textos longos, divida em partes menores
- Use pontuação para pausas naturais
- O serviço é gratuito para uso moderado
""")

# Rodapé
st.caption("Powered by Google gTTS | Hospedado no Streamlit Cloud")
