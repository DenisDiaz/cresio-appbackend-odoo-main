#!/usr/bin/env python3
"""
Servidor proxy para evitar problemas de CORS
Ejecutar: python proxy_server.py
Luego abrir: http://localhost:8888
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json
import webbrowser

ODOO_URL = "http://localhost:8070"
PORT = 8888

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/test_endpoints.html':
            # Servir el HTML
            try:
                with open('test_endpoints.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "Archivo no encontrado")
        else:
            self.send_error(404)

    def do_POST(self):
        # Proxy para peticiones POST a Odoo
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            # Hacer petición a Odoo
            url = f"{ODOO_URL}{self.path}"
            req = urllib.request.Request(
                url,
                data=post_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                response_data = response.read()
                
                # Enviar respuesta al cliente
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
                
        except urllib.error.HTTPError as e:
            # Error HTTP de Odoo
            error_data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_data)
            
        except Exception as e:
            # Error de conexión
            error_response = {
                "error": "Error de conexión",
                "message": str(e),
                "odoo_url": ODOO_URL
            }
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

    def log_message(self, format, *args):
        # Personalizar logs
        if args[1] == '200':
            print(f"✓ {args[0]} - {args[1]}")
        else:
            print(f"✗ {args[0]} - {args[1]}")

print("\n" + "=" * 60)
print("  SERVIDOR PROXY - PROBADOR DE ENDPOINTS")
print("=" * 60)
print(f"\n✓ Servidor proxy iniciado en: http://localhost:{PORT}")
print(f"✓ Conectando a Odoo en: {ODOO_URL}")
print(f"✓ Abriendo navegador...")
print(f"\n📝 Para detener el servidor presiona Ctrl+C\n")
print("=" * 60 + "\n")

# Abrir navegador
webbrowser.open(f'http://localhost:{PORT}')

# Iniciar servidor
try:
    server = HTTPServer(('', PORT), ProxyHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print("\n\n✓ Servidor detenido correctamente\n")
except OSError as e:
    print(f"\n✗ Error: {e}")
    print(f"El puerto {PORT} puede estar ocupado. Intenta cerrar otros programas.\n")
