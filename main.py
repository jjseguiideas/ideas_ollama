import subprocess
from docx import Document

# 📌 Leer el contenido del archivo DOCX en memoria
def read_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

file_path = "PROTOCOLOS.docx"  
document_text = read_docx(file_path)  

# 📌 Función para hacer preguntas a Deepseek-R1 en Ollama
def ask_deepseek(question):
    context = document_text[:3000]  
    prompt = f"""Usa el siguiente documento para responder preguntas:

    ---DOCUMENTO---
    {context}
    ----------------
    
    Pregunta: {question}
    
    Respuesta:"""

    # 🔹 Ejecutar Ollama con UTF-8
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:1.5b"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8" 
    )

    return result.stdout.strip()

# 📌 Interacción en bucle para hacer preguntas al documento
while True:
    question = input("\n🔹 Pregunta sobre el documento (o escribe 'salir' para terminar): ")
    if question.lower() == "salir":
        print("🔻 Saliendo del chat...")
        break
    response = ask_deepseek(question)
    print("\n🔹 Respuesta:\n", response)
