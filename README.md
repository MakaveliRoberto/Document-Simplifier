# Document Simplifier

A Flask-based web application that simplifies complex documents using AI-powered text summarization. The app can process various file formats including text files, PDFs, and images (PNG, JPG, JPEG, GIF) by extracting text and generating simplified versions.

## Features

- **Multi-format Support**: Upload and process text files, PDFs, and images
- **OCR Capability**: Extract text from images using Tesseract OCR
- **AI-Powered Simplification**: Uses Facebook's BART model for intelligent text summarization
- **Modern Web Interface**: Clean, responsive UI built with Tailwind CSS
- **Real-time Processing**: Upload files and get simplified results instantly

## How It Works

1. **File Upload**: Users can drag and drop or select files through the web interface
2. **Text Extraction**: 
   - For text files: Direct reading
   - For images: OCR processing using Tesseract
   - For PDFs: Text extraction (basic implementation)
3. **AI Simplification**: The extracted text is processed through Facebook's BART-large-CNN model
4. **Results Display**: Both original and simplified text are shown side by side

## Installation

### Prerequisites

- Python 3.7 or higher
- Tesseract OCR installed on your system

### System Dependencies

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

#### Windows
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### Python Dependencies

1. Clone or download this repository
2. Install required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:5000`

3. **Upload a document**:
   - Drag and drop a file onto the upload area, or
   - Click the upload area to select a file
   - Supported formats: TXT, PDF, PNG, JPG, JPEG, GIF

4. **View results**:
   - The original text and simplified version will be displayed
   - Simplified text is typically 30-130 characters long

## API Endpoints

### POST /
Upload and process a file for text simplification.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: File upload with key 'file'

**Response**:
```json
{
  "original": "Original extracted text...",
  "simplified": "Simplified text summary..."
}
```

**Error Response**:
```json
{
  "error": "Error message description"
}
```

### GET /
Serves the main web interface.

## Configuration

The application can be configured by modifying the following variables in `app.py`:

- `UPLOAD_FOLDER`: Directory for temporary file storage (default: 'uploads/')
- `ALLOWED_EXTENSIONS`: Supported file types (default: txt, pdf, png, jpg, jpeg, gif)

## Technical Details

### AI Model
- **Model**: facebook/bart-large-cnn
- **Purpose**: Text summarization and simplification
- **Parameters**:
  - Max length: 130 characters
  - Min length: 30 characters
  - Sampling: Disabled (deterministic output)

### OCR Processing
- **Engine**: Tesseract OCR
- **Image Support**: PNG, JPG, JPEG, GIF
- **Language**: English (default)

### File Processing
- **Security**: Uses `secure_filename()` to prevent path traversal attacks
- **Storage**: Temporary files are stored in the uploads directory
- **Cleanup**: Consider implementing automatic cleanup for production use

## Limitations

1. **PDF Processing**: Basic text extraction (may not work with complex PDF layouts)
2. **File Size**: No explicit file size limits (consider adding for production)
3. **Language Support**: Primarily optimized for English text
4. **Model Limitations**: BART model has context length limitations

## Development

### Project Structure
```
document_simplifier/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Web interface template
├── uploads/            # Temporary file storage (created automatically)
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

### Adding New Features

1. **Additional File Formats**: Modify `ALLOWED_EXTENSIONS` and add processing logic
2. **Custom Simplification**: Adjust the `simplify_text()` function parameters
3. **Batch Processing**: Implement multiple file upload support
4. **Export Options**: Add download functionality for simplified text

## Troubleshooting

### Common Issues

1. **Tesseract not found**:
   - Ensure Tesseract is installed and in your system PATH
   - On some systems, you may need to specify the Tesseract path in the code

2. **Model download issues**:
   - The first run will download the BART model (~1.5GB)
   - Ensure stable internet connection

3. **Memory issues**:
   - Large files may cause memory issues
   - Consider implementing file size limits

4. **OCR accuracy**:
   - Image quality affects OCR accuracy
   - Consider preprocessing images for better results

## License

This project is open source. Please ensure you comply with the licenses of the dependencies:
- Flask
- Transformers (Hugging Face)
- Tesseract OCR
- PIL/Pillow

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error messages in the browser console
3. Check the Flask application logs
