import sys
import urllib.request
from html.parser import HTMLParser

class MarkdownPurist(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.depth = 0
        self.data = []
        self.ignored_depth = 0
        
        # 1. Etiquetas Semánticas (Las únicas que Pandoc debe ver)
        # Todo lo demás (div, span, article, section) será "desempaquetado"
        self.semantic_tags = {
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr',
            'ul', 'ol', 'li', 'dl', 'dt', 'dd',
            'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th',
            'blockquote', 'pre', 'code', 'em', 'strong', 'b', 'i', 'a', 'img',
            'del', 'sup', 'sub'
        }

        # 2. Marcadores de inicio de contenido principal
        self.content_markers = {
            'class': ['docs-main-content', 'markdown-body', 'prose', 'article-content', 'body-content'],
            'role': ['main']
        }
        
        # 3. Elementos prohibidos (Se borra la etiqueta Y su contenido)
        self.banned_tags = {'script', 'style', 'button', 'nav', 'aside', 'footer', 'form', 'iframe', 'noscript', 'svg'}
        
        # 4. Clases prohibidas (Patrones de UI a eliminar completamente)
        self.banned_class_substrings = [
            'feedback', 'body-footer', 'mobile-widgets', 'visual-diff', 
            'on-page-nav', 'breadcrumbs', 'anchor-link', 'surveypopup',
            'absolute', 'group/link' # Captura botones flotantes y enlaces fantasma
        ]

        # 5. Texto exacto a eliminar
        self.banned_text = {"Copy", "Report incorrect code", "Ask AI", "\u200b"}

    def handle_starttag(self, tag, attrs):
        attr_dict = {k: v for k, v in attrs if v}
        classes = attr_dict.get('class', '')

        # A. Bloqueo Recursivo
        if self.ignored_depth > 0:
            self.ignored_depth += 1
            return

        # B. Detección de Bloqueos (Tags o Clases Prohibidas)
        if tag in self.banned_tags or any(ban in classes for ban in self.banned_class_substrings):
            self.ignored_depth = 1
            return

        # C. Inicio de Grabación
        if not self.recording:
            is_start = False
            if tag == 'article' or ('role' in attr_dict and 'main' in attr_dict['role']):
                is_start = True
            else:
                for cls in classes.split():
                    if cls in self.content_markers['class']:
                        is_start = True
            
            if is_start:
                self.recording = True
                self.depth = 1
            return

        # D. Grabación Selectiva (El núcleo del cambio)
        if self.recording:
            self.depth += 1
            
            # SOLO escribimos la etiqueta si es semántica.
            # Si es un 'div' o 'span', NO la escribimos, pero procesamos su contenido.
            if tag in self.semantic_tags:
                clean_attrs = []
                for k, v in attrs:
                    if k in ['href', 'src', 'alt', 'lang']: # Solo atributos útiles
                        clean_attrs.append(f'{k}="{v}"')
                
                attr_str = ' '.join(clean_attrs)
                self.data.append(f"<{tag} {attr_str}>")
            else:
                # Inyectamos un salto de línea para evitar que el texto se pegue
                # al desaparecer el div
                self.data.append("\n")

    def handle_endtag(self, tag):
        if self.ignored_depth > 0:
            self.ignored_depth -= 1
            return

        if self.recording:
            self.depth -= 1
            if self.depth == 0:
                self.recording = False
            else:
                # Solo cerramos si es semántica
                if tag in self.semantic_tags:
                    self.data.append(f"</{tag}>")
                else:
                    self.data.append("\n")

    def handle_data(self, data):
        if self.recording and self.ignored_depth == 0:
            text = data
            # Filtros de texto basura
            if text.strip() in self.banned_text: return
            if text == '\u200b': return
            
            self.data.append(text)

    def get_content(self):
        return "".join(self.data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            parser = MarkdownPurist()
            parser.feed(html)
            content = parser.get_content()
            if content: print(content)
            else: print(html) # Fallback
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

# Funcion de prueba para CodeRabbit
def prueba():
    print("Hola mundo")
    var = 10
    if var == 10:
        return True
    else:
        return False