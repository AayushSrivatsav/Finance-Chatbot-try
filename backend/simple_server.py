from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            if path == '/health':
                response = {"status": "healthy", "message": "API is operational"}
            elif path == '/':
                response = {"message": "Finance RAG Chatbot API is running!"}
            elif path == '/news/latest':
                response = [
                    {
                        "title": "Tech Stocks Rally on Strong Earnings",
                        "description": "Major technology companies report better-than-expected quarterly results.",
                        "url": "https://example.com/tech-rally",
                        "published_at": "2024-08-04T10:00:00Z",
                        "source": "Reuters",
                        "sentiment": "positive"
                    }
                ]
            else:
                response = {"error": "Endpoint not found"}
            
            self.wfile.write(json.dumps(response).encode())
        except BrokenPipeError:
            # Client disconnected, ignore the error
            pass
        except Exception as e:
            print(f"Error in GET request: {e}")
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '')
                
                if 'stock' in message.lower():
                    response = {
                        "response": "Based on current market analysis, I recommend focusing on technology and healthcare sectors.",
                        "sources": [{"title": "Market Analysis", "url": "https://example.com"}],
                        "confidence": 0.85
                    }
                else:
                    response = {
                        "response": "I'm your AI financial assistant! I can help you with stock analysis, market news, and investment recommendations.",
                        "sources": [],
                        "confidence": 0.8
                    }
            except:
                response = {"error": "Invalid request"}
            
            self.wfile.write(json.dumps(response).encode())
        except BrokenPipeError:
            # Client disconnected, ignore the error
            pass
        except Exception as e:
            print(f"Error in POST request: {e}")
    
    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        except BrokenPipeError:
            # Client disconnected, ignore the error
            pass
        except Exception as e:
            print(f"Error in OPTIONS request: {e}")

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("🚀 Starting Simple Finance RAG Chatbot API...")
    print("📡 API will be available at: http://localhost:8000")
    print("✅ Health check: http://localhost:8000/health")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 