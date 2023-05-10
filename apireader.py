from flask import Flask, request
from PyPDF4 import PdfFileReader
from loguru import logger

app = Flask(__name__)

@app.route('/buscar-palavras', methods=['POST'])
def buscar_palavras():
    arquivos = request.json.get('arquivos', [])
    palavras = request.json.get('palavras', [])

    logger.info(f'Lista de arquivos: {arquivos}')
    logger.info(f'Lista de palabras: {palavras}')

    if not arquivos:
        return 'Lista de arquivos vazia', 400

    if not palavras:
        return 'Lista de palavras vazia', 400
    
    resultados = {}

    try:
        for arquivo in arquivos:
            logger.info(f'Lendo o arquivo {arquivo}')
            
            with open(arquivo, 'rb') as pdf_file:
                pdf_reader = PdfFileReader(pdf_file)
                total_palavras = 0
                palavras_encontradas = 0

                for page in range(pdf_reader.getNumPages()):
                    page_obj = pdf_reader.getPage(page)
                    texto = page_obj.extractText().lower()
                    total_palavras += len(texto.split())

                    for palavra in palavras:
                        if palavra.lower() in texto:
                            palavras_encontradas += 1

                if total_palavras > 0:
                    porcentagem = palavras_encontradas / len(palavras) * 100
                    resultados[arquivo] = porcentagem

    except Exception as e:
        return str(e), 500
    
    ranking = {k: v for k, v in sorted(resultados.items(), key=lambda item: item[1], reverse=True)}

    return ranking


@app.route('/', methods=['GET'])
def ola():
    return 'Ola, esse servidor está rodando'

app.run(debug=True)
