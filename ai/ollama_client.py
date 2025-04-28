import subprocess

# Modelo local exacto instalado en Ollama
MODEL = "deepseek-r1:1.5b"

def query(prompt: str) -> str:
    """
    Ejecuta un prompt contra deepseek-r1:1.5b usando la CLI de Ollama.
    Captura errores y devuelve cadena vacía como fallback.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""
