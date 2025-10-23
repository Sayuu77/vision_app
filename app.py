import os
import streamlit as st
import base64
from openai import OpenAI

# Configuración de la página
st.set_page_config(
    page_title="Vision AI - Analizador de Imágenes",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Tema moderno con colores azules y morados
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        color: #f1f5f9;
    }
    .main-title {
        font-size: 2.8rem;
        text-align: center;
        background: linear-gradient(45deg, #6366f1, #8b5cf6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #c7d2fe;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .upload-card {
        background: rgba(255, 255, 255, 0.08);
        border: 2px dashed #6366f1;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    .upload-card:hover {
        background: rgba(99, 102, 241, 0.15);
        border-color: #8b5cf6;
        transform: translateY(-2px);
    }
    .api-input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #6366f1;
        border-radius: 15px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    .stButton button {
        background: linear-gradient(45deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        background: linear-gradient(45deg, #8b5cf6, #a855f7);
    }
    .response-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 6px solid #8b5cf6;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    .image-preview {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
    }
    .toggle-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .feature-badge {
        background: linear-gradient(45deg, #6366f1, #8b5cf6);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.3rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-title">🤖 Vision AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analizador Inteligente de Imágenes con GPT-4 Vision</div>', unsafe_allow_html=True)

# Badges de características
col_badges = st.columns(5)
with col_badges[0]:
    st.markdown('<div class="feature-badge">🔍 Análisis</div>', unsafe_allow_html=True)
with col_badges[1]:
    st.markdown('<div class="feature-badge">📝 Descripción</div>', unsafe_allow_html=True)
with col_badges[2]:
    st.markdown('<div class="feature-badge">🎯 Detalles</div>', unsafe_allow_html=True)
with col_badges[3]:
    st.markdown('<div class="feature-badge">🤖 IA</div>', unsafe_allow_html=True)
with col_badges[4]:
    st.markdown('<div class="feature-badge">🚀 Rápido</div>', unsafe_allow_html=True)

# Función para codificar imagen a base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Sección de API Key
st.markdown("### 🔑 Configuración de API")
st.markdown('<div class="api-input">', unsafe_allow_html=True)
ke = st.text_input(
    'Ingresa tu Clave de OpenAI',
    type="password",
    placeholder="sk-...",
    help="Necesitas una clave de OpenAI para usar el servicio",
    label_visibility="collapsed"
)
if ke:
    os.environ['OPENAI_API_KEY'] = ke
    st.success("✅ API Key configurada correctamente")
else:
    st.info("🔒 Ingresa tu API Key para comenzar")
st.markdown('</div>', unsafe_allow_html=True)

# Sección de carga de imagen
st.markdown("### 🖼️ Carga tu Imagen")
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Arrastra y suelta tu imagen aquí",
    type=["jpg", "png", "jpeg", "webp"],
    help="Formatos soportados: JPG, PNG, JPEG, WEBP",
    label_visibility="collapsed"
)

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} cargada exitosamente")
    # Mostrar información del archivo
    file_size = uploaded_file.size / 1024  # KB
    st.caption(f"📏 Tamaño: {file_size:.1f} KB | 🎯 Formato: {uploaded_file.type.split('/')[-1].upper()}")
else:
    st.info("📁 Selecciona una imagen para analizar")
st.markdown('</div>', unsafe_allow_html=True)

# Mostrar previsualización de la imagen
if uploaded_file:
    st.markdown("### 👀 Vista Previa")
    with st.container():
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(uploaded_file, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Sección de preguntas específicas
st.markdown('<div class="toggle-container">', unsafe_allow_html=True)
show_details = st.toggle(
    "🎯 Hacer una pregunta específica sobre la imagen",
    value=False,
    help="Activa esto para hacer preguntas detalladas sobre la imagen"
)

if show_details:
    additional_details = st.text_area(
        "💭 ¿Qué te gustaría saber sobre la imagen?",
        placeholder="Ej: ¿Qué emociones transmite esta imagen? ¿Qué objetos reconoces? Describe los colores y composición...",
        height=100,
        disabled=not show_details
    )
st.markdown('</div>', unsafe_allow_html=True)

# Botón de análisis
analyze_button = st.button(
    "🚀 Analizar Imagen con IA", 
    type="primary",
    use_container_width=True,
    disabled=not (uploaded_file and ke)
)

# Procesar análisis
if uploaded_file is not None and ke and analyze_button:
    with st.spinner("🔍 Analizando imagen con IA..."):
        try:
            # Codificar la imagen
            base64_image = encode_image(uploaded_file)
            
            # Construir el prompt
            prompt_text = "Describe detalladamente lo que ves en esta imagen en español. Incluye detalles sobre objetos, personas, escenas, colores, emociones y cualquier elemento relevante."
            
            if show_details and additional_details:
                prompt_text = additional_details
            
            # Crear el payload para la API
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }
            ]
            
            # Inicializar cliente de OpenAI
            client = OpenAI(api_key=ke)
            
            # Stream de respuesta
            full_response = ""
            message_placeholder = st.empty()
            
            # Mostrar tarjeta de respuesta
            with st.container():
                st.markdown('<div class="response-card">', unsafe_allow_html=True)
                st.markdown("### 🤖 Análisis de la Imagen")
                
                for completion in client.chat.completions.create(
                    model="gpt-4o", 
                    messages=messages,   
                    max_tokens=1500, 
                    stream=True
                ):
                    if completion.choices[0].delta.content is not None:
                        full_response += completion.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                # Respuesta final
                message_placeholder.markdown(full_response)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Métricas de la respuesta
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tokens usados", f"~{len(full_response.split())}")
                with col2:
                    st.metric("Caracteres", len(full_response))
                with col3:
                    st.metric("Modelo", "GPT-4 Vision")

        except Exception as e:
            st.error(f"❌ Error en el análisis: {str(e)}")
            st.info("💡 Verifica tu API Key y conexión a internet")

else:
    # Mensajes de advertencia
    if analyze_button:
        if not uploaded_file:
            st.warning("📸 Por favor carga una imagen primero")
        if not ke:
            st.warning("🔑 Necesitas ingresar tu API Key de OpenAI")

# Información adicional
with st.expander("ℹ️ ¿Cómo funciona?", expanded=False):
    st.markdown("""
    **🔍 Proceso de Análisis:**
    
    1. **Carga de Imagen**: Sube cualquier imagen en formatos JPG, PNG, JPEG o WEBP
    2. **Procesamiento**: La imagen se codifica y envía a GPT-4 Vision
    3. **Análisis IA**: El modelo analiza el contenido visual
    4. **Respuesta**: Recibes una descripción detallada en español
    
    **🎯 Características:**
    
    - Análisis de objetos, personas y escenas
    - Reconocimiento de emociones y contexto
    - Descripción de colores y composición
    - Respuestas en tiempo real con streaming
    
    **💡 Consejos:**
    
    - Usa preguntas específicas para obtener respuestas más detalladas
    - Imágenes con buena resolución dan mejores resultados
    - El análisis puede incluir interpretación contextual
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #c7d2fe; padding: 2rem;">
    <p>Desarrollado con ❤️ usando Streamlit y OpenAI GPT-4 Vision</p>
    <p style="font-size: 0.8rem; color: #a5b4fc;">Análisis inteligente de imágenes en tiempo real</p>
</div>
""", unsafe_allow_html=True)
