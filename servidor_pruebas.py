#!/usr/bin/env python3
"""
Servidor HTTP simple para probar los endpoints sin problemas de CORS
Ejecutar: python servidor_pruebas.py
Luego abrir: http://localhost:8000
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8888

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Agregar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

print("\n" + "=" * 60)
print("  SERVIDOR DE PRUEBAS - ENDPOINTS ODOO")
print("=" * 60)
print(f"\n✓ Servidor iniciado en: http://localhost:{PORT}")
print(f"✓ Abriendo navegador...")
print(f"\n📝 Para detener el servidor presiona Ctrl+C\n")
print("=" * 60 + "\n")

# Abrir navegador automáticamente
webbrowser.open(f'http://localhost:{PORT}/test_endpoints.html')

# Iniciar servidor
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Servidor detenido correctamente\n")
