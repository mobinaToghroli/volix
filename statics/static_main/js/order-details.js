document.addEventListener('DOMContentLoaded', function() {
    // Initialize order timeline
    initializeTimeline();
    
    // Initialize print functionality
    initializePrint();
    
    // Initialize support chat
    initializeSupportChat();
});

function initializeTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    timelineItems.forEach(item => {
        if (item.classList.contains('current')) {
            // Add animation to current status
            const icon = item.querySelector('.timeline-icon');
            icon.style.animation = 'pulse 2s infinite';
        }
    });
}

function initializePrint() {
    const printButton = document.querySelector('.btn-primary');
    if (printButton) {
        printButton.addEventListener('click', function() {
            // Create a new window for printing
            const printWindow = window.open('', '_blank');
            
            // Get the order details content
            const orderContent = document.querySelector('.order-details-container').innerHTML;
            
            // Create print-friendly HTML
            const printContent = `
                <!DOCTYPE html>
                <html dir="rtl" lang="fa">
                <head>
                    <meta charset="UTF-8">
                    <title>فاکتور سفارش</title>
                    <style>
                        body {
                            font-family: 'Vazir', sans-serif;
                            padding: 2rem;
                            direction: rtl;
                        }
                        .print-header {
                            text-align: center;
                            margin-bottom: 2rem;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin: 1rem 0;
                        }
                        th, td {
                            padding: 0.5rem;
                            border: 1px solid #ddd;
                            text-align: right;
                        }
                        th {
                            background: #f8f9fa;
                        }
                        .total-row {
                            font-weight: bold;
                        }
                        @media print {
                            .no-print {
                                display: none;
                            }
                        }
                    </style>
                </head>
                <body>
                    <div class="print-header">
                        <h1>فاکتور سفارش</h1>
                        <p>تاریخ: ${new Date().toLocaleDateString('fa-IR')}</p>
                    </div>
                    ${orderContent}
                    <div class="no-print" style="text-align: center; margin-top: 2rem;">
                        <button onclick="window.print()">چاپ فاکتور</button>
                    </div>
                </body>
                </html>
            `;
            
            // Write content to new window
            printWindow.document.write(printContent);
            printWindow.document.close();
        });
    }
}

function initializeSupportChat() {
    const supportButton = document.querySelector('.btn-secondary');
    if (supportButton) {
        supportButton.addEventListener('click', function() {
            // Here you can implement your support chat functionality
            // For example, opening a chat widget or redirecting to a support page
            alert('سیستم پشتیبانی به زودی راه‌اندازی خواهد شد.');
        });
    }
}

// Add CSS animation for timeline
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0.4);
        }
        70% {
            transform: scale(1.1);
            box-shadow: 0 0 0 10px rgba(var(--primary-color-rgb), 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0);
        }
    }
`;
document.head.appendChild(style); 