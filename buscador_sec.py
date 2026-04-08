import os
import requests
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- CONFIGURACIÓN ---
URL_NORMATIVA = "https://www.sec.cl/pliegos-tecnicos-ric/" # URL de pliegos RIC
CARPETA_DESTINO = "documentos_sec"

def descargar_pdfs():
    """Descarga todos los PDF de la página de la SEC si no existen localmente."""
    if not os.path.exists(CARPETA_DESTINO):
        os.makedirs(CARPETA_DESTINO)
    
    print(f"[*] Accediendo a {URL_NORMATIVA}...")
    try:
        response = requests.get(URL_NORMATIVA, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        pdf_count = 0
        for link in links:
            url_archivo = urljoin(URL_NORMATIVA, link['href'])
            if url_archivo.endswith(".pdf"):
                nombre_archivo = os.path.basename(url_archivo)
                ruta_local = os.path.join(CARPETA_DESTINO, nombre_archivo)
                
                if not os.path.exists(ruta_local):
                    print(f"[+] Descargando: {nombre_archivo}")
                    res_file = requests.get(url_archivo)
                    with open(ruta_local, 'wb') as f:
                        f.write(res_file.content)
                    pdf_count += 1
        print(f"[*] Proceso de descarga finalizado. {pdf_count} archivos nuevos.")
    except Exception as e:
        print(f"[!] Error en la descarga: {e}")

def buscar_texto(frase_busqueda):
    """Busca una frase exacta en los PDFs descargados."""
    print(f"\n[*] Buscando: '{frase_busqueda}' en archivos locales...")
    resultados = []
    
    if not os.path.exists(CARPETA_DESTINO):
        print("[!] No existe la carpeta de documentos. Descarga primero.")
        return

    for archivo in os.listdir(CARPETA_DESTINO):
        if archivo.endswith(".pdf"):
            ruta = os.path.join(CARPETA_DESTINO, archivo)
            try:
                doc = fitz.open(ruta)
                for num_pag, pagina in enumerate(doc):
                    texto = pagina.get_text("text")
                    if frase_busqueda.lower() in texto.lower():
                        # Extraer bloque específico para mostrar contexto
                        bloques = pagina.get_text("blocks")
                        for b in bloques:
                            if frase_busqueda.lower() in b[4].lower():
                                resultados.append({
                                    "archivo": archivo,
                                    "pagina": num_pag + 1,
                                    "contexto": b[4].strip().replace("\n", " ")
                                })
                doc.close()
            except Exception as e:
                print(f"[!] Error leyendo {archivo}: {e}")
    
    return resultados

# --- FLUJO PRINCIPAL ---
if __name__ == "__main__":
    # 1. Descargar (puedes comentar esta línea si ya los tienes)
    descargar_pdfs()
    
    # 2. Consultar
    palabra = input("\nIngrese la frase a buscar (ej: altura máxima de): ")
    hallazgos = buscar_texto(palabra)
    
    if hallazgos:
        print(f"\n{'='*60}")
        print(f"RESULTADOS ENCONTRADOS ({len(hallazgos)})")
        print(f"{'='*60}")
        for h in hallazgos:
            print(f"\nDOCUMENTO: {h['archivo']}")
            print(f"PÁGINA:    {h['pagina']}")
            print(f"EXTRACTO:  {h['contexto']}")
            print("-" * 30)
    else:
        print("\n[!] No se encontraron coincidencias.")