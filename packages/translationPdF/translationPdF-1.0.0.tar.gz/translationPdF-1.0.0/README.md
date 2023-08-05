A classe TranslatePDF é capaz de extrair texto e imagem de um PDF, bem como extrair texto de uma imagem, traduzir textos longos e curtos. Além disso, ela também permite criar um PDF a partir de um texto. <br>
Acesse: https://github.com/Willians-S-S/PacoteTranslation

**Obs:** Ao extrair o texto do PDF ele perde toda a formatação original. <br>
    Se você usar a extensão Code Runner, não execute o arquivo python por ela, pois irá da erro.

# Funcionabilidades
* Extrai texto e imagem do PDF <br>
* Traduz texto curto. <br>
* Traduz texto longo. <br>
* Criar PDF. <br>
* Extrai imagem do PDF. <br>
* Extrai texto da imagem. <br>

# Como usar

## Importar a biblioteca <br>
```python
    from pdftools import pdftools as tools
```

## Criar objeto da classe TranslatePDF

```python
    obj = tools.TranslatePDF()  
```
## Extrair texto e imagem do PDF
Parâmetros do método `extract_data_pdf`:<br>

`caminho` => Diretório até o pdf. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads/arquivo.pdf. <br>
`idioma` => Idioma para o qual o texto será traduzido. <br>
`caminho_save_pdf` => Diretório para salva o pdf gerado, esse parâmetro é opcional, caso não o use ele salva o pdf no diretorio do script. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads <br>
`page` => Indica uma página unica para extrair o que o usuário deseja, as páginas do PDF começa por 0. <br>
`interval` => Indica o intervalo de páginas  para extrair o que o usuário deseja. <br>
`ret` => ret='pdf' Indica que o método vai gerar um pdf com o texto traduzido, se não enviar o parâmetro texto traduzido vai ser impresso na saída padrão. <br>
`check_img` => Verifica se a imagem no pdf. <br>
`caminho_save_img` => Diretório para salvar as imagens do pdf, esse parâmetro é opcional, caso não o use ele salva o pdf no diretorio do script. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads<br>

```python
     def extract_data_pdf(
            self, 
            caminho: str, 
            idioma: str, 
            caminho_save_pdf: Optional[str] = None,
            page: Optional[int] = None, 
            interval: Optional[str] = None, 
            ret: Optional[str] = None,
            check_img: Optional[bool] = None,
            caminho_save_img: Optional[str] = None
            ) -> None:
```

Usando o método `extract_data_pdf`: <br>


```python
    Windows
    obj.extract_data_pdf("C:/Users/usuario/Downloads/arquivo.pdf", 
                        caminho_save_pdf="C:/Users/usuario/Downloads",
                        idioma='pt',
                        ret='pdf', 
                        page=0
                        )
    Linux
    obj.extract_data_pdf("/home/usuario/Documentos/arquivo.pdf", 
                        caminho_save_pdf="/home/usuario/Documentos",
                        idioma='pt',
                        ret='pdf', 
                        page=0
                        )
```
## Traduzir texto curto. (Texto com menos de 500 caracteres) <br>

Parâmetros do método `traducao`:<br>

`texto` => Texto que vai ser traduzido <br>
`idioma` => Idioma em que texto irá ser traduzido. <br> 

```python
    def traducao(self, texto, idioma) -> str:
```
Usando o método `traducao`: <br>

```python
    obj.traducao(texto, idioma)
```

## Traduzir texto longo. (Texto com mais de 500 caracteres) <br>

Parâmetros do método `trans_text_bigger`:<br>

`texto` => Texto que vai ser traduzido <br>
`idioma` => Idioma em que texto irá ser traduzido. <br> 

```python
    def trans_text_bigger(self, texto, idioma) -> str:
```
Usando o método `trans_text_bigger`: <br>

```python
    obj.trans_text_bigger(texto, idioma)
```
## Criar PDF. <br>

Parâmetros do método `gerarPDF`:<br>

`texto` => Texto para introduzir no PDF. <br>
`nome_arquivo` => Indica no nome do PDF. <br> 
`caminho_save_pdf` => Diretório para salva o pdf gerado, esse parâmetro é opcional, caso não o use ele salva o pdf no diretorio do script. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads <br>

```python
    def gerarPDF(self, texto, nome_arquivo, caminho_save_pdf) -> None:
```
Usando o método `gerarPDF`: <br>

```python
    obj.gerarPDF(texto, nome_arquivo, caminho_save_pdf)
```
## Extrair imagem do PDF. <br>

Parâmetros do método `extrairIMG`:<br>

`caminho` => Diretório até o pdf. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads/arquivo.pdf. <br>
`caminho_save` => Diretório para salvar as imagens do pdf, esse parâmetro é opcional, caso não o use ele salva o pdf no diretorio do script. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads <br> 
`all_page` => Índice da página que contém a imagem a ser extraída. Se não for especificado, todas as páginas serão processadas. <br>

```python
    def extrairIMG(self, caminho, caminho_save: Optional[str] = None, all_page: Optional[int] = None) -> None:
```
Usando o método `extrairIMG`: <br>

```python
    obj.extrairIMG(caminho="C:/Users/usuario/Downloads/arquivo.pdf", 
                        caminho_save="C:/Users/usuario/Downloads",
                        all_page=1
                        )
    Linux
    obj.extrairIMG(caminho="/home/usuario/Documentos/arquivo.pdf", 
                        caminho_save_pdf="/home/usuario/Documentos",
                        all_page=1
                        )
```
## Extrair texto da imagem. <br>

**Para usar esse método é necessário instalar o tesseract** <br>
- **Windows:**
    * Acesse o site para baixar e instalar no windows: https://github.com/UB-Mannheim/tesseract/wiki <br>
    * Instale no diretório padrão do execultavel: C:\Users\usuario\AppData\Local\Programs\Tesseract-OCR

- **Linux:** <br>
    * Ubuntu e derivados:
        * Adicione o ppa:  sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel
        * Atualize o repositório: sudo apt update
        * Instalação: sudo apt-get install tesseract-ocr
        * Duvidas acesse: https://launchpad.net/~alex-p/+archive/ubuntu/tesseract-ocr-devel ou https://notesalexp.org/tesseract-ocr/#tesseract_5.x
    * Arch Linux e derivados:
        * pip install tesseract

Parâmetros do método `extract_text_img`:<br>

`caminho_image` => Diretório da imagem. No windows use / ao invés \ , ex: C:/Users/usuario/Downloads/img.jpg. <br>
`idioma` => Idioma em que texto irá ser traduzido. <br>

```python
    def extract_text_img(self, caminho_image, idioma: Optional[str] = None) -> None:
```
Usando o método `extract_text_img`: <br>

```python
    obj.extract_text_img(caminho_image="C:/Users/usuario/Downloads/img.jpg", 
                        idioma='en'
                        )
    Linux
    obj.extract_text_img(caminho_image="/home/usuario/Documentos/img.png", 
                        idioma='en'
                        )
```
## Línguas suportadas

```
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}
```