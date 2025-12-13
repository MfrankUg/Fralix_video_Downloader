// Global state
let currentVideoInfo = null;
let selectedFormat = null;

// DOM Elements
const videoUrlInput = document.getElementById('videoUrl');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');
const videoModal = document.getElementById('videoModal');
const closeModal = document.getElementById('closeModal');
const confirmDownload = document.getElementById('confirmDownload');
const formatList = document.getElementById('formatList');
const videoPreview = document.getElementById('videoPreview');
const modalTitle = document.getElementById('modalTitle');

// Event Listeners
downloadBtn.addEventListener('click', handleDownload);
closeModal.addEventListener('click', closeVideoModal);
confirmDownload.addEventListener('click', handleConfirmDownload);
videoModal.addEventListener('click', (e) => {
    if (e.target === videoModal) {
        closeVideoModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && videoModal.style.display !== 'none') {
        closeVideoModal();
    }
});

// Handle Enter key in input
videoUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleDownload();
    }
});

// Handle download button click
async function handleDownload() {
    const url = videoUrlInput.value.trim();
    
    if (!url) {
        showError('Please enter a video URL');
        return;
    }

    // Basic URL validation
    try {
        new URL(url);
    } catch {
        showError('Please enter a valid URL');
        return;
    }

    setLoading(true);
    hideError();

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze video');
        }

        currentVideoInfo = data;
        showVideoModal(data);
    } catch (error) {
        showError(error.message || 'An error occurred. Please try again.');
        console.error('Error:', error);
    } finally {
        setLoading(false);
    }
}

// Show video modal with format options
function showVideoModal(videoInfo) {
    modalTitle.textContent = videoInfo.title || 'Select Format';
    
    // Show video preview
    if (videoInfo.thumbnail) {
        videoPreview.innerHTML = `
            <img src="${videoInfo.thumbnail}" alt="Video thumbnail" />
        `;
    } else {
        videoPreview.innerHTML = `
            <div style="padding: 2rem; text-align: center; background: var(--surface); border-radius: 12px;">
                <p>Video Preview</p>
            </div>
        `;
    }

    // Clear previous formats
    formatList.innerHTML = '';
    selectedFormat = null;
    confirmDownload.disabled = true;

    // Add format options
    if (videoInfo.formats && videoInfo.formats.length > 0) {
        videoInfo.formats.forEach((format, index) => {
            const formatItem = createFormatItem(format, index);
            formatList.appendChild(formatItem);
        });
    } else {
        // Add default "best" option
        const formatItem = createFormatItem({
            format_id: 'best',
            ext: 'mp4',
            resolution: 'Best available',
            quality: 0
        }, 0);
        formatList.appendChild(formatItem);
    }

    // Show modal
    videoModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// Create format item element
function createFormatItem(format, index) {
    const item = document.createElement('div');
    item.className = 'format-item';
    item.dataset.formatId = format.format_id;
    item.dataset.index = index;

    const sizeText = format.filesize 
        ? `(${(format.filesize / (1024 * 1024)).toFixed(2)} MB)`
        : '';

    item.innerHTML = `
        <div class="format-item-info">
            <span class="format-item-label">${format.resolution || 'Best Quality'}</span>
            <span class="format-item-details">${format.ext.toUpperCase()} ${sizeText}</span>
        </div>
    `;

    item.addEventListener('click', () => {
        // Remove previous selection
        document.querySelectorAll('.format-item').forEach(el => {
            el.classList.remove('selected');
        });

        // Add selection to clicked item
        item.classList.add('selected');
        selectedFormat = format.format_id;
        confirmDownload.disabled = false;
    });

    return item;
}

// Close video modal
function closeVideoModal() {
    videoModal.style.display = 'none';
    document.body.style.overflow = '';
    currentVideoInfo = null;
    selectedFormat = null;
}

// Handle confirm download
async function handleConfirmDownload() {
    if (!currentVideoInfo || !selectedFormat) {
        return;
    }

    const url = videoUrlInput.value.trim();
    confirmDownload.disabled = true;
    confirmDownload.innerHTML = '<span class="spinner"></span> Downloading...';

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                format_id: selectedFormat,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Download failed');
        }

        // Success - trigger download
        if (data.filename) {
            window.location.href = `/api/download-file/${encodeURIComponent(data.filename)}`;
            
            // Show success message
            showSuccess('Download started! Your video will be saved shortly.');
            
            // Close modal after a delay
            setTimeout(() => {
                closeVideoModal();
                videoUrlInput.value = '';
            }, 1500);
        }
    } catch (error) {
        showError(error.message || 'Download failed. Please try again.');
        confirmDownload.disabled = false;
        confirmDownload.innerHTML = 'Download Selected';
    }
}

// Set loading state
function setLoading(loading) {
    const btnText = downloadBtn.querySelector('.btn-text');
    const btnLoader = downloadBtn.querySelector('.btn-loader');
    
    if (loading) {
        downloadBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
    } else {
        downloadBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Show success message (temporary)
function showSuccess(message) {
    // Create temporary success message
    const successDiv = document.createElement('div');
    successDiv.className = 'error-message';
    successDiv.style.background = 'rgba(16, 185, 129, 0.1)';
    successDiv.style.borderLeftColor = '#10b981';
    successDiv.style.color = '#10b981';
    successDiv.textContent = message;
    
    errorMessage.parentNode.insertBefore(successDiv, errorMessage.nextSibling);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Platform logo click handlers
document.querySelectorAll('.platform-logo').forEach(logo => {
    logo.addEventListener('click', () => {
        const platform = logo.dataset.platform;
        const placeholder = getPlatformPlaceholder(platform);
        videoUrlInput.placeholder = placeholder;
        videoUrlInput.focus();
    });
});

function getPlatformPlaceholder(platform) {
    const placeholders = {
        youtube: 'Paste YouTube video link here...',
        linkedin: 'Paste LinkedIn video link here...',
        twitter: 'Paste X (Twitter) video link here...',
        instagram: 'Paste Instagram video link here...'
    };
    return placeholders[platform] || 'Paste video link here...';
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

