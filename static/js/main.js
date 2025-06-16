// Funções utilitárias
function showToast(message, type = 'info', duration = 5000) {
    // Remover toasts existentes
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());

    // Criar novo toast
    const toastHtml = `
        <div class="toast show" role="alert" style="min-width: 300px;">
            <div class="toast-header">
                <i class="fas fa-${getToastIcon(type)} text-${type} me-2"></i>
                <strong class="me-auto">${getToastTitle(type)}</strong>
                <button type="button" class="btn-close" onclick="this.closest('.toast').remove()"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;

    // Adicionar toast container se não existir
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
    }

    // Adicionar toast
    container.insertAdjacentHTML('beforeend', toastHtml);

    // Auto-remover após duration
    if (duration > 0) {
        const toastElement = container.lastElementChild;
        setTimeout(() => {
            if (toastElement && toastElement.parentNode) {
                toastElement.remove();
            }
        }, duration);
    }
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': 
        case 'danger': return 'times-circle';
        case 'warning': return 'exclamation-triangle';
        case 'info': return 'info-circle';
        default: return 'info-circle';
    }
}

function getToastTitle(type) {
    switch (type) {
        case 'success': return 'Sucesso';
        case 'error': 
        case 'danger': return 'Erro';
        case 'warning': return 'Atenção';
        case 'info': return 'Informação';
        default: return 'Notificação';
    }
}

// Função para loading
function showLoading(element, show = true) {
    if (show) {
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Carregando...';
        element.disabled = true;
    } else {
        element.disabled = false;
    }
}

// Auto-save form
function setupAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave]');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                console.log('Auto-saving form:', form.id);
                // Implementar auto-save se necessário
            });
        });
    });
}

// Verificar status do bot
async function checkBotStatus() {
    try {
        const response = await fetch('/api/bot_status');
        const data = await response.json();

        const statusElement = document.getElementById('bot-status');
        if (statusElement) {
            let statusClass = 'status-offline';
            if (data.status === 'running') {
                statusClass = 'status-online';
            } else if (data.status === 'error') {
                statusClass = 'status-warning';
            }

            statusElement.innerHTML = `
                <span class="status-indicator ${statusClass}"></span>
                ${data.message}
            `;
        }
    } catch (error) {
        console.error('Erro ao verificar status do bot:', error);
    }
}

// Atualizar estatísticas
async function updateStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const stats = await response.json();

        // Atualizar elementos de estatística
        Object.keys(stats).forEach(key => {
            const element = document.getElementById(`stat-${key}`);
            if (element) {
                element.textContent = stats[key] || 0;
            }
        });
    } catch (error) {
        console.error('Erro ao atualizar estatísticas:', error);
    }
}

// Função para reiniciar bot
async function restartBot() {
    const confirmRestart = confirm('Tem certeza que deseja reiniciar o bot?');
    if (!confirmRestart) return;

    try {
        showToast('Reiniciando bot...', 'info');

        const response = await fetch('/api/restart_bot', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            showToast('Bot reiniciado com sucesso!', 'success');
            setTimeout(() => {
                checkBotStatus();
            }, 3000);
        } else {
            showToast('Erro ao reiniciar bot: ' + data.message, 'error');
        }
    } catch (error) {
        showToast('Erro ao reiniciar bot: ' + error.message, 'error');
    }
}

// Validação de formulários
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                showToast('Por favor, preencha todos os campos obrigatórios', 'warning');
            }
            form.classList.add('was-validated');
        });
    });
}

// Função para formatar números
function formatNumber(num) {
    return new Intl.NumberFormat('pt-BR').format(num);
}

// Inicialização quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Painel Bot Telegram - Inicializado');

    // Configurar auto-save
    setupAutoSave();

    // Configurar validação de formulários
    setupFormValidation();

    // Verificar status do bot periodicamente
    checkBotStatus();
    setInterval(checkBotStatus, 30000); // A cada 30 segundos

    // Atualizar estatísticas periodicamente
    updateStatistics();
    setInterval(updateStatistics, 60000); // A cada 1 minuto

    // Adicionar fade-in às páginas
    document.body.classList.add('fade-in');

    // Ativar tela cheia automaticamente
    setTimeout(function() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(function(err) {
                console.log('Não foi possível ativar tela cheia automaticamente:', err);
            });
        }
    }, 1000); // Aguarda 1 segundo para evitar bloqueio do navegador

    // Add CSS for toasts
    const style = document.createElement('style');
    style.textContent = `
        .toast-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }

        .toast {
            background: #333;
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            margin-bottom: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease;
        }

        .toast-success { background: #28a745; }
        .toast-error { background: #dc3545; }
        .toast-warning { background: #ffc107; color: #333; }
        .toast-info { background: #17a2b8; }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }

        .status-dot.online { background: #28a745; }
        .status-dot.offline { background: #dc3545; }
    `;
    document.head.appendChild(style);
});

// The following functions were present in the original code but not in the edited snippet.
// They are added back to maintain the original functionality.

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeMobileNavigation() {
    // Placeholder for mobile navigation initialization
}

function initializeAccessibility() {
    // Placeholder for accessibility initialization
}

function updateResponsiveElements() {
    // Placeholder for responsive elements update
}

function monitorPerformance() {
    // Placeholder for performance monitoring
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+S to save forms
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        const forms = document.querySelectorAll('form');
        if (forms.length > 0) {
            const event = new Event('submit');
            forms[0].dispatchEvent(event);
        }
    }

    // Ctrl+R to refresh (prevent default browser refresh)
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        updateStatistics(); // Changed from updateDashboardStats to updateStatistics
        showToast('Dados atualizados', 'info');
    }

    // F11 for fullscreen
    if (e.key === 'F11') {
        e.preventDefault();
        toggleFullscreen();
    }

    // Escape to close modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        });
    }
});

// Update responsive elements on window resize
let resizeTimeout;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(updateResponsiveElements, 250);
});

// Enhanced error handling
window.addEventListener('unhandledrejection', function(event) {
    console.error('Erro não tratado:', event.reason);
    showToast('Ocorreu um erro inesperado', 'error');
});

// Offline/Online detection with enhanced feedback
window.addEventListener('online', function() {
    showToast('Conexão restaurada', 'success');
    checkBotStatus();
});

window.addEventListener('offline', function() {
    showToast('Conexão perdida - Modo offline', 'warning');
    checkBotStatus();
});

// Exportar funções para uso global
window.showToast = showToast;
window.restartBot = restartBot;
window.checkBotStatus = checkBotStatus;
window.updateStatistics = updateStatistics;
window.copyToClipboard = function copyToClipboard(text) { // Re-implementing the function as it was removed in edited snippet, but called in other places.
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copiado para a área de transferência!', 'success');
    }).catch(err => {
        showToast('Erro ao copiar texto', 'error');
    });
};
window.setButtonLoading = function setButtonLoading(buttonElement, isLoading) { // Re-implementing the function as it was removed in edited snippet, but called in other places.
    if (isLoading) {
        buttonElement.disabled = true;
        const originalText = buttonElement.innerHTML;
        buttonElement.setAttribute('data-original-text', originalText);
        buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Carregando...';
    } else {
        buttonElement.disabled = false;
        const originalText = buttonElement.getAttribute('data-original-text');
        if (originalText) {
            buttonElement.innerHTML = originalText;
        }
    }
};
window.validateForm = function validateForm(formId) { // Re-implementing the function as it was removed in edited snippet, but called in other places.
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
};
window.toggleFullscreen = toggleFullscreen;
window.startBot = startBot;
window.stopBot = stopBot;
window.testBotToken = testBotToken;