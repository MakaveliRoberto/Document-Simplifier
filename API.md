# Document Simplifier API Documentation

## Overview

The Document Simplifier API provides endpoints for uploading documents and receiving simplified text summaries. The API is built with Flask and supports multiple file formats including text files, PDFs, and images.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Upload and Simplify Document

**Endpoint**: `POST /`

**Description**: Upload a document file and receive both the original extracted text and a simplified version.

**Request**:
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: 
  - `file` (required): The document file to process

**Supported File Types**:
- Text files: `.txt`
- PDF files: `.pdf`
- Image files: `.png`, `.jpg`, `.jpeg`, `.gif`

**Request Example**:
```bash
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5000/
```

**Success Response** (200 OK):
```json
{
  "original": "This is the original extracted text from the document. It may be quite long and complex, containing detailed information that needs to be simplified for better understanding.",
  "simplified": "Original text simplified into a concise summary."
}
```

**Error Responses**:

**No file provided** (400 Bad Request):
```json
{
  "error": "No file part"
}
```

**No file selected** (400 Bad Request):
```json
{
  "error": "No selected file"
}
```

**Unsupported file type** (400 Bad Request):
```json
{
  "error": "File type not allowed"
}
```

### 2. Get Web Interface

**Endpoint**: `GET /`

**Description**: Serves the main web interface for document upload and processing.

**Request**:
- **Method**: GET
- **Content-Type**: text/html

**Response** (200 OK):
- Returns the HTML page with the document upload interface

## Processing Details

### Text Extraction

The API handles different file types as follows:

1. **Text Files (.txt)**:
   - Direct file reading
   - UTF-8 encoding assumed

2. **Image Files (.png, .jpg, .jpeg, .gif)**:
   - OCR processing using Tesseract
   - Automatic text extraction from images

3. **PDF Files (.pdf)**:
   - Basic text extraction
   - Note: Complex PDF layouts may not be processed correctly

### Text Simplification

- **Model**: Facebook BART-large-CNN
- **Parameters**:
  - Maximum length: 130 characters
  - Minimum length: 30 characters
  - Sampling: Disabled (deterministic output)
- **Purpose**: Summarization and simplification of complex text

## Error Handling

The API returns JSON error responses for the following scenarios:

1. **Missing file**: When no file is provided in the request
2. **Empty filename**: When a file field exists but no file is selected
3. **Unsupported format**: When the file extension is not in the allowed list
4. **Processing errors**: Internal server errors during text extraction or simplification

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing:
- Request rate limiting
- File size limits
- Processing timeouts

## Security Considerations

1. **File Validation**: Only specific file extensions are allowed
2. **Secure Filenames**: Uses `secure_filename()` to prevent path traversal
3. **Temporary Storage**: Files are stored temporarily in the uploads directory
4. **No Authentication**: Currently no authentication required (consider for production)

## Usage Examples

### Python Example

```python
import requests

# Upload a text file
with open('document.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/', files=files)
    
if response.status_code == 200:
    data = response.json()
    print(f"Original: {data['original']}")
    print(f"Simplified: {data['simplified']}")
else:
    print(f"Error: {response.json()['error']}")
```

### JavaScript Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.error) {
        console.error('Error:', data.error);
    } else {
        console.log('Original:', data.original);
        console.log('Simplified:', data.simplified);
    }
})
.catch(error => {
    console.error('Network error:', error);
});
```

### cURL Example

```bash
# Upload a PDF file
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5000/

# Upload an image file
curl -X POST \
  -F "file=@image.png" \
  http://localhost:5000/
```

## Response Format

All API responses are in JSON format:

**Success Response Structure**:
```json
{
  "original": "string",    // Extracted original text
  "simplified": "string"   // AI-generated simplified text
}
```

**Error Response Structure**:
```json
{
  "error": "string"        // Error message description
}
```

## Status Codes

- **200 OK**: Successful processing
- **400 Bad Request**: Invalid request (missing file, wrong format, etc.)
- **500 Internal Server Error**: Server-side processing error

## Notes

1. **File Size**: No explicit file size limits are currently implemented
2. **Language Support**: Optimized for English text processing
3. **Model Loading**: First request may take longer due to model initialization
4. **Temporary Files**: Uploaded files are stored temporarily and should be cleaned up
5. **Production Considerations**: Add authentication, rate limiting, and proper error handling for production use
