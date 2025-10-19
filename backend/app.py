from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pdf_processor import PDFProcessor

# Get the base directory (parent of backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/static/<path:filename>')
def send_static(filename):
    static_dir = os.path.join(BASE_DIR, 'static')
    print(f"📂 Serving static file: {filename} from {static_dir}")
    return send_from_directory(static_dir, filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"📄 Processing file: {filename}")
        
        # Process the PDF
        processor = PDFProcessor(filepath)
        results = processor.process()
        
        print(f"✅ Results: {results}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'results': results
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Base directory: {BASE_DIR}")
    print(f"🚀 Server starting at http://localhost:5001")
    app.run(debug=True, port=5001, host='0.0.0.0')
