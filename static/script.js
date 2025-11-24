/* ================================================================================
   TASKFLOW - JAVASCRIPT INTERATIVO
   ================================================================================
   Gerencia modais, validações, chamadas API e interações do usuário
   ================================================================================ */

// ==================== VARIÁVEIS GLOBAIS ====================
let currentTaskId = null;
let currentFilter = 'all';
let deleteTaskId = null;

// ==================== FILTROS E BUSCA ====================

/**
 * Define o filtro ativo
 */
function setFilter(filter) {
    currentFilter = filter;
    
    // Atualiza botões ativos
    document.querySelectorAll('.filter-buttons .filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
    
    // Aplica filtros
    filterTasks();
}

/**
 * Filtra tarefas por busca e status
 */
function filterTasks() {
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const cards = document.querySelectorAll('.task-card');
    let visibleCount = 0;
    
    cards.forEach(card => {
        const titulo = card.getAttribute('data-titulo');
        const status = card.getAttribute('data-status');
        
        // Verifica busca
        const matchSearch = titulo.includes(searchTerm);
        
        // Verifica filtro
        const matchFilter = currentFilter === 'all' || status === currentFilter;
        
        // Mostra/oculta card
        if (matchSearch && matchFilter) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Mostra mensagem se não houver resultados
    const grid = document.querySelector('.tasks-grid');
    let noResults = document.getElementById('noResults');
    
    if (visibleCount === 0 && grid) {
        if (!noResults) {
            noResults = document.createElement('div');
            noResults.id = 'noResults';
            noResults.className = 'empty-state';
            noResults.innerHTML = `
                <i class="fas fa-search"></i>
                <h3>Nenhuma tarefa encontrada</h3>
                <p>Tente ajustar os filtros ou termo de busca.</p>
            `;
            grid.appendChild(noResults);
        }
    } else if (noResults) {
        noResults.remove();
    }
}

/**
 * Ordena tarefas
 */
function sortTasks() {
    const select = document.getElementById('sortSelect');
    const sortValue = select.value;
    const grid = document.querySelector('.tasks-grid');
    const cards = Array.from(document.querySelectorAll('.task-card'));
    
    cards.sort((a, b) => {
        let aValue, bValue;
        
        switch(sortValue) {
            case 'criacao-desc':
                aValue = new Date(a.getAttribute('data-criacao').split(' ').reverse().join(' '));
                bValue = new Date(b.getAttribute('data-criacao').split(' ').reverse().join(' '));
                return bValue - aValue;
            
            case 'criacao-asc':
                aValue = new Date(a.getAttribute('data-criacao').split(' ').reverse().join(' '));
                bValue = new Date(b.getAttribute('data-criacao').split(' ').reverse().join(' '));
                return aValue - bValue;
            
            case 'prazo-asc':
                aValue = parseDateBR(a.getAttribute('data-prazo'));
                bValue = parseDateBR(b.getAttribute('data-prazo'));
                return aValue - bValue;
            
            case 'prazo-desc':
                aValue = parseDateBR(a.getAttribute('data-prazo'));
                bValue = parseDateBR(b.getAttribute('data-prazo'));
                return bValue - aValue;
            
            case 'titulo-asc':
                return a.getAttribute('data-titulo').localeCompare(b.getAttribute('data-titulo'));
            
            case 'titulo-desc':
                return b.getAttribute('data-titulo').localeCompare(a.getAttribute('data-titulo'));
        }
    });
    
    // Reorganiza cards no DOM
    cards.forEach(card => grid.appendChild(card));
}

/**
 * Converte data BR para objeto Date
 */
function parseDateBR(dateStr) {
    const parts = dateStr.split('/');
    return new Date(parts[2], parts[1] - 1, parts[0]);
}

// ==================== MODAL DE TAREFAS ====================

/**
 * Abre o modal para criar nova tarefa
 */
function openTaskModal() {
    currentTaskId = null;
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus"></i> Nova Tarefa';
    document.getElementById('taskForm').reset();
    document.getElementById('taskId').value = '';
    document.getElementById('taskModal').classList.add('active');
}

/**
 * Abre o modal para editar tarefa existente
 */
function editTask(id, titulo, descricao, prazo) {
    currentTaskId = id;
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit"></i> Editar Tarefa';
    document.getElementById('taskId').value = id;
    document.getElementById('taskTitulo').value = titulo;
    document.getElementById('taskDescricao').value = descricao;
    document.getElementById('taskPrazo').value = prazo;
    document.getElementById('taskModal').classList.add('active');
}

/**
 * Fecha o modal de tarefas
 */
function closeTaskModal() {
    document.getElementById('taskModal').classList.remove('active');
    document.getElementById('taskForm').reset();
    currentTaskId = null;
}

/**
 * Salva tarefa (criar ou editar)
 */
async function saveTask(event) {
    event.preventDefault();
    
    const titulo = document.getElementById('taskTitulo').value;
    const descricao = document.getElementById('taskDescricao').value;
    const prazo = document.getElementById('taskPrazo').value;
    
    // Validação de data
    if (!validateDate(prazo)) {
        showToast('Data inválida! Use o formato DD/MM/AAAA', 'error');
        return;
    }
    
    const data = { titulo, descricao, prazo };
    
    try {
        let response;
        
        if (currentTaskId) {
            // Editar tarefa existente
            response = await fetch(`/api/tarefas/${currentTaskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            // Criar nova tarefa
            response = await fetch('/api/tarefas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(currentTaskId ? 'Tarefa atualizada!' : 'Tarefa criada!', 'success');
            closeTaskModal();
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast(result.erro || 'Erro ao salvar tarefa', 'error');
        }
    } catch (error) {
        showToast('Erro de conexão', 'error');
        console.error(error);
    }
}

// ==================== AÇÕES DE TAREFAS ====================

/**
 * Visualiza detalhes da tarefa
 */
function viewTaskDetails(id, titulo, descricao, prazo, criacao, status) {
    document.getElementById('detailTitulo').textContent = titulo;
    document.getElementById('detailDescricao').textContent = descricao;
    document.getElementById('detailPrazo').textContent = prazo;
    document.getElementById('detailCriacao').textContent = criacao;
    
    // Define status com ícone e cor
    const statusEl = document.getElementById('detailStatus');
    if (status === 'Concluída') {
        statusEl.innerHTML = '<span class="badge badge-success"><i class="fas fa-check-circle"></i> Concluída</span>';
    } else if (isOverdue(prazo, status)) {
        statusEl.innerHTML = '<span class="badge badge-danger"><i class="fas fa-exclamation-triangle"></i> Atrasada</span>';
    } else {
        statusEl.innerHTML = '<span class="badge badge-warning"><i class="fas fa-clock"></i> Pendente</span>';
    }
    
    document.getElementById('detailsModal').classList.add('active');
}

/**
 * Fecha modal de detalhes
 */
function closeDetailsModal() {
    document.getElementById('detailsModal').classList.remove('active');
}

/**
 * Abre modal de confirmação de exclusão
 */
function confirmDelete(id, titulo) {
    deleteTaskId = id;
    document.getElementById('confirmTaskTitle').textContent = titulo;
    document.getElementById('confirmModal').classList.add('active');
}

/**
 * Fecha modal de confirmação
 */
function closeConfirmModal() {
    deleteTaskId = null;
    document.getElementById('confirmModal').classList.remove('active');
}

/**
 * Executa a exclusão após confirmação
 */
async function executeDelete() {
    if (!deleteTaskId) return;
    
    try {
        const response = await fetch(`/api/tarefas/${deleteTaskId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            closeConfirmModal();
            showToast('Tarefa excluída com sucesso!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast(result.erro || 'Erro ao excluir tarefa', 'error');
        }
    } catch (error) {
        showToast('Erro de conexão', 'error');
        console.error(error);
    }
}

/**
 * Marca tarefa como concluída
 */
async function completeTask(id) {
    if (!confirm('Deseja marcar esta tarefa como concluída?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/tarefas/${id}/concluir`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('Tarefa concluída!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast(result.erro || 'Erro ao concluir tarefa', 'error');
        }
    } catch (error) {
        showToast('Erro de conexão', 'error');
        console.error(error);
    }
}

/**
 * Exclui uma tarefa
 */
async function deleteTask(id) {
    // Função mantida por compatibilidade mas substituída por confirmDelete
    confirmDelete(id, 'esta tarefa');
}

// ==================== VALIDAÇÕES ====================

/**
 * Valida formato de data DD/MM/AAAA
 */
function validateDate(dateString) {
    const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    const match = dateString.match(regex);
    
    if (!match) return false;
    
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    const year = parseInt(match[3], 10);
    
    if (month < 1 || month > 12) return false;
    if (day < 1 || day > 31) return false;
    if (year < 2000 || year > 2100) return false;
    
    // Validação de dias por mês
    const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    
    // Ano bissexto
    if ((year % 4 === 0 && year % 100 !== 0) || year % 400 === 0) {
        daysInMonth[1] = 29;
    }
    
    if (day > daysInMonth[month - 1]) return false;
    
    return true;
}

/**
 * Formata input de data automaticamente
 */
function formatDateInput(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2);
    }
    if (value.length >= 5) {
        value = value.substring(0, 5) + '/' + value.substring(5, 9);
    }
    
    input.value = value;
}

// ==================== TOAST DE NOTIFICAÇÃO ====================

/**
 * Exibe notificação toast
 */
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    
    // Define cor baseada no tipo
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    
    toast.style.background = colors[type] || colors.info;
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ==================== MENU MOBILE ====================

/**
 * Toggle do menu mobile
 */
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        
        if (navMenu.style.display === 'flex') {
            navMenu.style.position = 'absolute';
            navMenu.style.top = '100%';
            navMenu.style.left = '0';
            navMenu.style.right = '0';
            navMenu.style.background = 'white';
            navMenu.style.flexDirection = 'column';
            navMenu.style.padding = '1rem';
            navMenu.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }
    }
}

// ==================== EVENT LISTENERS ====================

document.addEventListener('DOMContentLoaded', function() {
    // Fecha modal ao clicar fora
    const modal = document.getElementById('taskModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeTaskModal();
            }
        });
    }
    
    // Fecha modais de detalhes e confirmação ao clicar fora
    const detailsModal = document.getElementById('detailsModal');
    if (detailsModal) {
        detailsModal.addEventListener('click', function(e) {
            if (e.target === detailsModal) {
                closeDetailsModal();
            }
        });
    }
    
    const confirmModal = document.getElementById('confirmModal');
    if (confirmModal) {
        confirmModal.addEventListener('click', function(e) {
            if (e.target === confirmModal) {
                closeConfirmModal();
            }
        });
    }
    
    // Formatação automática de data
    const prazoInput = document.getElementById('taskPrazo');
    if (prazoInput) {
        prazoInput.addEventListener('input', function() {
            formatDateInput(this);
        });
    }
    
    // Atalho ESC para fechar modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (modal && modal.classList.contains('active')) {
                closeTaskModal();
            }
            if (detailsModal && detailsModal.classList.contains('active')) {
                closeDetailsModal();
            }
            if (confirmModal && confirmModal.classList.contains('active')) {
                closeConfirmModal();
            }
        }
    });
    
    // Ajusta menu mobile ao redimensionar
    window.addEventListener('resize', function() {
        const navMenu = document.querySelector('.nav-menu');
        if (navMenu && window.innerWidth > 768) {
            navMenu.style.display = '';
            navMenu.style.position = '';
            navMenu.style.top = '';
            navMenu.style.left = '';
            navMenu.style.right = '';
            navMenu.style.background = '';
            navMenu.style.flexDirection = '';
            navMenu.style.padding = '';
            navMenu.style.boxShadow = '';
        }
    });
    
    // Inicializa ordenação e filtros
    if (document.getElementById('sortSelect')) {
        sortTasks();
    }
});

// ==================== ANIMAÇÕES E EFEITOS ====================

/**
 * Adiciona animação de entrada aos cards
 */
function animateCards() {
    const cards = document.querySelectorAll('.task-card, .stat-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.animation = 'slideUp 0.5s ease forwards';
        }, index * 50);
    });
}

// Executa animações quando a página carregar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', animateCards);
} else {
    animateCards();
}

// ==================== FUNÇÕES AUXILIARES ====================

/**
 * Carrega tarefas via API (para futuras implementações)
 */
async function loadTasks() {
    try {
        const response = await fetch('/api/tarefas');
        if (response.ok) {
            const tasks = await response.json();
            return tasks;
        }
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        return [];
    }
}

/**
 * Verifica se data está atrasada
 */
function isOverdue(prazoStr, status) {
    if (status === 'Concluída') return false;
    
    try {
        const parts = prazoStr.split('/');
        const prazo = new Date(parts[2], parts[1] - 1, parts[0]);
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        
        return prazo < hoje;
    } catch {
        return false;
    }
}

/**
 * Formata data para exibição
 */
function formatDate(dateStr) {
    try {
        const parts = dateStr.split('/');
        const date = new Date(parts[2], parts[1] - 1, parts[0]);
        
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
        return date.toLocaleDateString('pt-BR', options);
    } catch {
        return dateStr;
    }
}

// ==================== EXPORTAÇÃO ====================

/**
 * Prepara dados para exportação
 */
function exportData(format = 'json') {
    if (format === 'json') {
        // Implementar exportação JSON
        console.log('Exportando para JSON...');
    } else if (format === 'csv') {
        // Implementar exportação CSV
        console.log('Exportando para CSV...');
    }
}

// Log de inicialização
console.log('TaskFlow - Sistema carregado com sucesso!');
