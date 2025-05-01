/**
 * Educational Guidance JavaScript
 * 
 * This script handles the educational guidance tooltips and modal functionality.
 * It attaches event listeners to educational guidance elements and fetches
 * explanations from the Gemini API via AJAX.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Create modal if it doesn't exist
    if (!document.getElementById('educationModal')) {
        createEducationModal();
    }
    
    // Get all elements with educational guidance triggers
    const educationTriggers = document.querySelectorAll('[data-education-topic]');
    
    // Add click event listeners to each trigger
    educationTriggers.forEach(function(trigger) {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const topic = this.dataset.educationTopic;
            fetchEducationalContent(topic);
        });
    });
});

/**
 * Creates the modal element for displaying educational content
 */
function createEducationModal() {
    const modalHTML = `
        <div class="modal fade" id="educationModal" tabindex="-1" aria-labelledby="educationModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title" id="educationModalLabel">Educational Guidance</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div id="educationContent">
                            <div class="text-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <p class="mt-2">Loading educational content...</p>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="d-flex align-items-center justify-content-between w-100">
                            <div class="dropdown">
                                <button class="btn btn-outline-primary dropdown-toggle" type="button" id="otherTopicsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                    Explore Other Topics
                                </button>
                                <ul class="dropdown-menu" aria-labelledby="otherTopicsDropdown">
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="volume_confirmation">Volume Confirmation</a></li>
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="atr_stop">ATR Stop Loss</a></li>
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="chandelier_exit">Chandelier Exit</a></li>
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="consolidation">Price Consolidation</a></li>
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="rr_ratio">Risk-Reward Ratio</a></li>
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="position_sizing">Position Sizing</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item education-topic-link" href="#" data-education-topic="default">Classic Breakout Strategy</a></li>
                                </ul>
                            </div>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create a div element to hold the modal
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    
    // Append the modal to the body
    document.body.appendChild(modalContainer);
    
    // Add event listeners to the topic links in the dropdown
    const topicLinks = document.querySelectorAll('.education-topic-link');
    topicLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const topic = this.dataset.educationTopic;
            fetchEducationalContent(topic);
        });
    });
}

/**
 * Fetches educational content for a topic using AJAX
 * @param {string} topic - The educational topic to fetch
 */
function fetchEducationalContent(topic) {
    // Show loading spinner
    const contentElement = document.getElementById('educationContent');
    contentElement.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Loading educational content...</p>
        </div>
    `;
    
    // Update modal title
    const modalTitle = document.getElementById('educationModalLabel');
    modalTitle.textContent = formatTopicName(topic);
    
    // Show the modal
    const educationModal = new bootstrap.Modal(document.getElementById('educationModal'));
    educationModal.show();
    
    // Fetch the educational content
    fetch(`/education/query/?topic=${encodeURIComponent(topic)}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Replace content with the explanation
        contentElement.innerHTML = `
            <h4>${formatTopicName(data.topic)}</h4>
            <div class="education-explanation">
                ${formatExplanation(data.explanation)}
            </div>
            <div class="text-end mt-3">
                <a href="/education/query/?topic=${encodeURIComponent(data.topic)}" class="text-primary" target="_blank">
                    <i class="fas fa-external-link-alt"></i> Open in new page
                </a>
            </div>
        `;
    })
    .catch(error => {
        // Show error message
        contentElement.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle"></i> Error loading educational content: ${error.message || 'Unknown error'}
            </div>
            <p>Please try again later or contact support if the problem persists.</p>
        `;
    });
}

/**
 * Formats a topic name for display
 * @param {string} topic - The topic identifier
 * @return {string} - The formatted topic name
 */
function formatTopicName(topic) {
    // Convert snake_case to title case
    const words = topic.split('_');
    const titleWords = words.map(word => word.charAt(0).toUpperCase() + word.slice(1));
    
    // Special case handling
    switch (topic) {
        case 'atr_stop':
            return 'ATR Stop Loss';
        case 'rr_ratio':
            return 'Risk-Reward Ratio';
        case 'default':
            return 'Classic Breakout Strategy';
        default:
            return titleWords.join(' ');
    }
}

/**
 * Formats the explanation text with proper HTML
 * @param {string} explanation - The explanation text
 * @return {string} - The formatted HTML
 */
function formatExplanation(explanation) {
    if (!explanation) {
        return '<p class="text-muted">No explanation available.</p>';
    }
    
    // Convert newlines to paragraphs and return
    return explanation
        .split('\n\n')
        .map(para => para.trim())
        .filter(para => para)
        .map(para => `<p>${para}</p>`)
        .join('');
}
