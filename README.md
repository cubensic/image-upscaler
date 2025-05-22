# AI Image Upscaler

A minimal web application that allows users to drag-and-drop images and enhance their resolution using AI upscaling. Built with FastAPI backend and vanilla JavaScript frontend, optimized for deployment on Vercel.

## 🚀 Features

- **Drag & Drop Interface**: Simply drag an image onto the upload zone
- **File Validation**: Client and server-side validation for file type and size
- **Supported Formats**: JPG, PNG, WEBP (up to 5MB)
- **Progress Tracking**: Real-time feedback during upload and processing
- **Image Comparison**: Side-by-side view of original vs upscaled image
- **Download**: One-click download of the enhanced image
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

- **Backend**: Python 3.9+ with FastAPI
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Image Processing**: Pillow (PIL)
- **Deployment**: Vercel (serverless functions)
- **Testing**: Pytest

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js (for Vercel CLI, optional)
- Git

## 🏃‍♂️ Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd image-upscaler
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000`

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

## 🌐 Deployment

### Deploy to Vercel

1. **Install Vercel CLI** (optional)
   ```bash
   npm i -g vercel
   ```

2. **Configure environment variables**
   Create environment variables in Vercel dashboard:
   - `AI_API_URL`: URL for the AI upscaling service
   - `AI_API_KEY`: API key for the AI service
   - `MAX_FILE_SIZE_MB`: Maximum file size (default: 5)

3. **Deploy**
   ```bash
   vercel --prod
   ```

   Or simply push to your connected GitHub repository for automatic deployment.

## 📁 Project Structure

```
image-upscaler/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API endpoints (placeholder)
│   └── static/
│       ├── index.html       # Main HTML file
│       ├── styles.css       # Styles
│       └── script.js        # Frontend logic
├── tests/
│   └── test_api.py         # API tests
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel configuration
├── .env.development        # Development environment
├── .env.production         # Production environment
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

- `AI_API_URL`: Endpoint for the AI upscaling service (currently stubbed)
- `AI_API_KEY`: Authentication key for the AI service
- `MAX_FILE_SIZE_MB`: Maximum allowed file size in MB (default: 5)
- `ENVIRONMENT`: Current environment (development/production)

### File Validation

- **Supported formats**: JPEG, JPG, PNG, WEBP
- **Maximum file size**: 5MB (configurable)
- **Validation**: Both client-side and server-side

## 📡 API Endpoints

### `POST /api/upscale`

Upload and upscale an image.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `image` (binary file)

**Response:**
- Success (200): Binary PNG image
- Error (400): Invalid file type/size
- Error (500): Processing error

**Example:**
```javascript
const formData = new FormData();
formData.append('image', file);

const response = await fetch('/api/upscale', {
    method: 'POST',
    body: formData
});

const blob = await response.blob();
```

### `GET /api/health`

Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "service": "image-upscaler"
}
```

## 🎨 Frontend Components

### DragDropZone
- Handles file drag-and-drop and click-to-select
- Provides visual feedback for drag states
- Validates files before upload

### ProgressIndicator
- Shows upload and processing progress
- Animated progress bar with status text
- Multiple states: idle, uploading, processing, done

### ResultViewer
- Displays original and upscaled images side-by-side
- Download button for enhanced image
- "Upload Another" button to reset the app

### NotificationBanner
- Shows success/error messages
- Auto-dismisses success notifications
- User-dismissible error notifications

## 🔄 Current Status

This is an MVP implementation with the following characteristics:

- ✅ **Fully functional** drag-and-drop upload interface
- ✅ **Complete** file validation (client and server-side)
- ✅ **Working** FastAPI backend with proper error handling
- ✅ **Responsive** modern UI design
- ⚠️ **Stubbed** AI upscaling (currently just converts to PNG)
- ⚠️ **Ready** for AI integration (placeholder endpoints)

## 🚧 Next Steps

1. **AI Integration**: Replace the stub with actual AI upscaling service
2. **Scaling Options**: Add 2x, 4x upscaling factor selection
3. **Enhanced UI**: Add before/after slider comparison
4. **Caching**: Implement result caching for improved performance
5. **Authentication**: Add user accounts and usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Module not found errors:**
```bash
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**CORS issues in development:**
The application includes CORS middleware for development. For production, configure appropriate origins.

## 📞 Support

For questions, issues, or contributions, please:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include steps to reproduce any bugs
4. Provide environment details (OS, Python version, etc.) 