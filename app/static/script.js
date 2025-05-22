class ImageUpscaler {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentFile = null;
        this.resultBlob = null;
    }

    initializeElements() {
        // DOM elements
        this.dropZone = document.getElementById('drop-zone');
        this.fileInput = document.getElementById('file-input');
        this.fileSelectBtn = document.getElementById('file-select-btn');
        this.notification = document.getElementById('notification');
        this.notificationMessage = document.getElementById('notification-message');
        this.notificationClose = document.getElementById('notification-close');
        this.progressContainer = document.getElementById('progress-container');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.resultContainer = document.getElementById('result-container');
        this.originalImage = document.getElementById('original-image');
        this.resultImage = document.getElementById('result-image');
        this.downloadBtn = document.getElementById('download-btn');
        this.uploadAnotherBtn = document.getElementById('upload-another-btn');
    }

    bindEvents() {
        // Drag and drop events
        this.dropZone.addEventListener('dragenter', this.handleDragEnter.bind(this));
        this.dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        this.dropZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.dropZone.addEventListener('drop', this.handleDrop.bind(this));
        
        // Click to select file
        this.fileSelectBtn.addEventListener('click', () => this.fileInput.click());
        this.dropZone.addEventListener('click', () => this.fileInput.click());
        
        // File input change
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // Notification close
        this.notificationClose.addEventListener('click', this.hideNotification.bind(this));
        
        // Result actions
        this.downloadBtn.addEventListener('click', this.downloadResult.bind(this));
        this.uploadAnotherBtn.addEventListener('click', this.resetApp.bind(this));
    }

    handleDragEnter(e) {
        e.preventDefault();
        this.dropZone.classList.add('drag-over');
    }

    handleDragOver(e) {
        e.preventDefault();
    }

    handleDragLeave(e) {
        e.preventDefault();
        if (!this.dropZone.contains(e.relatedTarget)) {
            this.dropZone.classList.remove('drag-over');
        }
    }

    handleDrop(e) {
        e.preventDefault();
        this.dropZone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    processFile(file) {
        console.log('Processing file:', file.name, file.type, file.size);
        
        // Validate file
        const validation = this.validateFile(file);
        if (!validation.valid) {
            this.showNotification(validation.message, 'error');
            return;
        }

        this.currentFile = file;
        this.uploadFile(file);
    }

    validateFile(file) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        const maxSize = 5 * 1024 * 1024; // 5MB

        if (!allowedTypes.includes(file.type)) {
            return {
                valid: false,
                message: 'Unsupported file type. Please use JPG, PNG, or WEBP.'
            };
        }

        if (file.size > maxSize) {
            return {
                valid: false,
                message: 'File exceeds 5MB limit. Please choose a smaller image.'
            };
        }

        return { valid: true };
    }

    async uploadFile(file) {
        try {
            this.showProgress('Uploading image...');
            
            // Create preview of original image
            const originalUrl = URL.createObjectURL(file);
            this.originalImage.src = originalUrl;
            
            const formData = new FormData();
            formData.append('image', file);

            console.log('Uploading to /api/upscale...');
            
            const response = await fetch('/api/upscale', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            this.updateProgress(80, 'Processing image...');

            // Get the result as blob
            this.resultBlob = await response.blob();
            
            this.updateProgress(100, 'Complete!');
            this.showResult();

        } catch (error) {
            console.error('Upload error:', error);
            this.showNotification(`Upload failed: ${error.message}`, 'error');
            this.hideProgress();
        }
    }

    showProgress(text) {
        this.hideNotification();
        this.dropZone.classList.add('hidden');
        this.resultContainer.classList.add('hidden');
        this.progressContainer.classList.remove('hidden');
        this.updateProgress(20, text);
    }

    updateProgress(percent, text) {
        this.progressFill.style.width = `${percent}%`;
        this.progressText.textContent = text;
    }

    hideProgress() {
        this.progressContainer.classList.add('hidden');
        this.dropZone.classList.remove('hidden');
    }

    showResult() {
        setTimeout(() => {
            this.progressContainer.classList.add('hidden');
            
            // Display result image
            const resultUrl = URL.createObjectURL(this.resultBlob);
            this.resultImage.src = resultUrl;
            
            this.resultContainer.classList.remove('hidden');
            this.showNotification('Image upscaled successfully!', 'success');
        }, 500);
    }

    downloadResult() {
        if (!this.resultBlob) return;

        const url = URL.createObjectURL(this.resultBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `upscaled_${this.currentFile.name.split('.')[0]}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        console.log('Download initiated');
    }

    resetApp() {
        // Reset all states
        this.currentFile = null;
        this.resultBlob = null;
        
        // Clean up object URLs
        if (this.originalImage.src.startsWith('blob:')) {
            URL.revokeObjectURL(this.originalImage.src);
        }
        if (this.resultImage.src.startsWith('blob:')) {
            URL.revokeObjectURL(this.resultImage.src);
        }
        
        // Reset UI
        this.fileInput.value = '';
        this.originalImage.src = '';
        this.resultImage.src = '';
        this.progressFill.style.width = '0%';
        
        // Show upload zone, hide others
        this.dropZone.classList.remove('hidden');
        this.progressContainer.classList.add('hidden');
        this.resultContainer.classList.add('hidden');
        this.hideNotification();

        console.log('App reset');
    }

    showNotification(message, type = 'error') {
        this.notificationMessage.textContent = message;
        this.notification.className = `notification ${type}`;
        this.notification.classList.remove('hidden');

        // Auto-hide success notifications
        if (type === 'success') {
            setTimeout(() => this.hideNotification(), 5000);
        }
    }

    hideNotification() {
        this.notification.classList.add('hidden');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.imageUpscaler = new ImageUpscaler();
    console.log('Image Upscaler initialized');
}); 