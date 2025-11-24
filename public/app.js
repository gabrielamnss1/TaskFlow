// LocalStorage Manager
const Storage = {
    get(key) {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    },
    set(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    },
    remove(key) {
        localStorage.removeItem(key);
    }
};

// Initialize data
function initializeData() {
    if (!Storage.get('users')) {
        Storage.set('users', []);
    }
    if (!Storage.get('tasks')) {
        Storage.set('tasks', []);
    }
}

// Auth Functions
let currentUser = Storage.get('currentUser');

function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
}

function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
}

function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('loginUser').value.trim();
    const password = document.getElementById('loginPass').value;

    const users = Storage.get('users') || [];
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        currentUser = user;
        Storage.set('currentUser', user);
        showAlert('Login realizado com sucesso!', 'success');
        setTimeout(() => {
            showApp();
        }, 500);
    } else {
        showAlert('Login ou senha incorretos!', 'error');
    }
}

function handleRegister(event) {
    event.preventDefault();
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const username = document.getElementById('regUser').value.trim();
    const password = document.getElementById('regPass').value;

    const users = Storage.get('users') || [];

    if (users.find(u => u.username === username)) {
        showAlert('Este login já está em uso!', 'error');
        return;
    }

    if (users.find(u => u.email === email)) {
        showAlert('Este e-mail já está cadastrado!', 'error');
        return;
    }

    const newUser = {
        id: Date.now(),
        name,
        email,
        username,
        password,
        createdAt: new Date().toISOString()
    };

    users.push(newUser);
    Storage.set('users', users);

    showAlert('Cadastro realizado com sucesso! Faça login para continuar.', 'success');
    setTimeout(() => {
        showLogin();
        document.getElementById('loginUser').value = username;
    }, 1500);
}

function showAlert(message, type) {
    const alert = document.getElementById('authAlert');
    alert.textContent = message;
    alert.className = `alert ${type}`;
    alert.style.display = 'flex';

    setTimeout(() => {
        alert.style.display = 'none';
    }, 3000);
}

function showApp() {
    document.getElementById('authScreen').style.display = 'none';
    document.getElementById('appScreen').style.display = 'block';
    document.getElementById('userName').textContent = currentUser.name;
    showDashboard();
}

function logout() {
    if (confirm('Deseja realmente sair?')) {
        currentUser = null;
        Storage.remove('currentUser');
        document.getElementById('authScreen').style.display = 'flex';
        document.getElementById('appScreen').style.display = 'none';
        document.getElementById('loginUser').value = '';
        document.getElementById('loginPass').value = '';
    }
}

// Navigation
function toggleMobileMenu() {
    document.querySelector('.nav-menu').classList.toggle('show');
}

function setActiveNav(navId) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.getElementById(navId).classList.add('active');
}

function showDashboard() {
    setActiveNav('navDashboard');
    document.getElementById('dashboardScreen').style.display = 'block';
    document.getElementById('reportsScreen').style.display = 'none';
    document.getElementById('profileScreen').style.display = 'none';
    renderDashboard();
}

function showReports() {
    setActiveNav('navReports');
    document.getElementById('dashboardScreen').style.display = 'none';
    document.getElementById('reportsScreen').style.display = 'block';
    document.getElementById('profileScreen').style.display = 'none';
    renderReports();
}

function showProfile() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.getElementById('dashboardScreen').style.display = 'none';
    document.getElementById('reportsScreen').style.display = 'none';
    document.getElementById('profileScreen').style.display = 'block';
    renderProfile();
}

// Dashboard
let currentFilter = 'all';
let currentSort = 'created_desc';

function renderDashboard() {
    const tasks = getUserTasks();
    const stats = calculateStats(tasks);

    const html = `
        <div class="dashboard-header">
            <h2><i class="fas fa-home"></i> Dashboard</h2>
            <button onclick="openNewTaskModal()" class="btn btn-success">
                <i class="fas fa-plus"></i> Nova Tarefa
            </button>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon total">
                    <i class="fas fa-tasks"></i>
                </div>
                <div class="stat-content">
                    <h3>${stats.total}</h3>
                    <p>Total de Tarefas</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon pending">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="stat-content">
                    <h3>${stats.pending}</h3>
                    <p>Pendentes</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon completed">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-content">
                    <h3>${stats.completed}</h3>
                    <p>Concluídas</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon overdue">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="stat-content">
                    <h3>${stats.overdue}</h3>
                    <p>Atrasadas</p>
                </div>
            </div>
        </div>

        <div class="tasks-controls">
            <div class="filters-row">
                <button class="filter-btn ${currentFilter === 'all' ? 'active' : ''}" onclick="setFilter('all')">
                    <i class="fas fa-list"></i> Todas
                </button>
                <button class="filter-btn ${currentFilter === 'pending' ? 'active' : ''}" onclick="setFilter('pending')">
                    <i class="fas fa-clock"></i> Pendentes
                </button>
                <button class="filter-btn ${currentFilter === 'completed' ? 'active' : ''}" onclick="setFilter('completed')">
                    <i class="fas fa-check-circle"></i> Concluídas
                </button>
                <button class="filter-btn ${currentFilter === 'overdue' ? 'active' : ''}" onclick="setFilter('overdue')">
                    <i class="fas fa-exclamation-triangle"></i> Atrasadas
                </button>
            </div>
            <div class="search-sort-row">
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" id="searchInput" placeholder="Buscar tarefas..." oninput="filterTasks()">
                </div>
                <div class="sort-box">
                    <select id="sortSelect" onchange="sortTasks()">
                        <option value="created_desc">Mais recentes</option>
                        <option value="created_asc">Mais antigas</option>
                        <option value="deadline_asc">Prazo mais próximo</option>
                        <option value="deadline_desc">Prazo mais distante</option>
                        <option value="title_asc">Título (A-Z)</option>
                        <option value="title_desc">Título (Z-A)</option>
                    </select>
                </div>
            </div>
        </div>

        <div id="tasksContainer" class="tasks-grid"></div>
    `;

    document.getElementById('dashboardScreen').innerHTML = html;
    document.getElementById('sortSelect').value = currentSort;
    renderTasks();
}

function getUserTasks() {
    const allTasks = Storage.get('tasks') || [];
    return allTasks.filter(task => task.userId === currentUser.id);
}

function calculateStats(tasks) {
    const now = new Date();
    const stats = {
        total: tasks.length,
        pending: 0,
        completed: 0,
        overdue: 0
    };

    tasks.forEach(task => {
        if (task.completed) {
            stats.completed++;
        } else {
            stats.pending++;
            if (task.deadline && new Date(task.deadline) < now) {
                stats.overdue++;
            }
        }
    });

    return stats;
}

function setFilter(filter) {
    currentFilter = filter;
    renderDashboard();
}

function filterTasks() {
    renderTasks();
}

function sortTasks() {
    currentSort = document.getElementById('sortSelect').value;
    renderTasks();
}

function renderTasks() {
    let tasks = getUserTasks();
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';

    // Apply filter
    if (currentFilter === 'pending') {
        tasks = tasks.filter(t => !t.completed);
    } else if (currentFilter === 'completed') {
        tasks = tasks.filter(t => t.completed);
    } else if (currentFilter === 'overdue') {
        const now = new Date();
        tasks = tasks.filter(t => !t.completed && t.deadline && new Date(t.deadline) < now);
    }

    // Apply search
    if (searchTerm) {
        tasks = tasks.filter(t => 
            t.title.toLowerCase().includes(searchTerm) ||
            t.description.toLowerCase().includes(searchTerm)
        );
    }

    // Apply sort
    tasks.sort((a, b) => {
        switch (currentSort) {
            case 'created_desc':
                return new Date(b.createdAt) - new Date(a.createdAt);
            case 'created_asc':
                return new Date(a.createdAt) - new Date(b.createdAt);
            case 'deadline_asc':
                if (!a.deadline) return 1;
                if (!b.deadline) return -1;
                return new Date(a.deadline) - new Date(b.deadline);
            case 'deadline_desc':
                if (!a.deadline) return 1;
                if (!b.deadline) return -1;
                return new Date(b.deadline) - new Date(a.deadline);
            case 'title_asc':
                return a.title.localeCompare(b.title);
            case 'title_desc':
                return b.title.localeCompare(a.title);
            default:
                return 0;
        }
    });

    const container = document.getElementById('tasksContainer');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <i class="fas fa-inbox"></i>
                <h3>Nenhuma tarefa encontrada</h3>
                <p>Crie sua primeira tarefa para começar!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = tasks.map(task => {
        const status = getTaskStatus(task);
        const statusText = status === 'completed' ? 'Concluída' : 
                          status === 'overdue' ? 'Atrasada' : 'Pendente';

        return `
            <div class="task-card ${status}">
                <div class="task-header">
                    <div class="task-title">${task.title}</div>
                    <span class="task-status ${status}">${statusText}</span>
                </div>
                <div class="task-description">${task.description}</div>
                <div class="task-meta">
                    <span><i class="fas fa-calendar"></i> ${formatDate(task.createdAt)}</span>
                    ${task.deadline ? `<span><i class="fas fa-clock"></i> ${formatDate(task.deadline)}</span>` : ''}
                </div>
                <div class="task-actions">
                    <button onclick="viewTaskDetails(${task.id})" class="btn btn-sm btn-info" title="Ver detalhes completos">
                        <i class="fas fa-eye"></i><span class="btn-text">Detalhes</span>
                    </button>
                    ${!task.completed ? `
                        <button onclick="editTask(${task.id})" class="btn btn-sm btn-warning" title="Editar tarefa">
                            <i class="fas fa-edit"></i><span class="btn-text">Editar</span>
                        </button>
                        <button onclick="completeTask(${task.id})" class="btn btn-sm btn-success" title="Marcar como concluída">
                            <i class="fas fa-check"></i><span class="btn-text">Concluir</span>
                        </button>
                    ` : ''}
                    <button onclick="confirmDelete(${task.id})" class="btn btn-sm btn-danger" title="Excluir tarefa">
                        <i class="fas fa-trash"></i><span class="btn-text">Excluir</span>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function getTaskStatus(task) {
    if (task.completed) return 'completed';
    if (task.deadline && new Date(task.deadline) < new Date()) return 'overdue';
    return 'pending';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Task Modals
function openNewTaskModal() {
    const html = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-plus"></i> Nova Tarefa</h3>
                <button class="modal-close" onclick="closeModal('taskModal')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="taskForm" onsubmit="saveTask(event)">
                    <div class="form-group">
                        <label><i class="fas fa-heading"></i> Título</label>
                        <input type="text" id="taskTitle" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-align-left"></i> Descrição</label>
                        <textarea id="taskDescription" rows="4" required></textarea>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-calendar"></i> Prazo (opcional)</label>
                        <input type="date" id="taskDeadline" min="${new Date().toISOString().split('T')[0]}">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button onclick="closeModal('taskModal')" class="btn btn-secondary">Cancelar</button>
                <button onclick="document.getElementById('taskForm').requestSubmit()" class="btn btn-primary">
                    <i class="fas fa-save"></i> Salvar
                </button>
            </div>
        </div>
    `;

    document.getElementById('taskModal').innerHTML = html;
    document.getElementById('taskModal').classList.add('show');
}

function editTask(taskId) {
    const tasks = Storage.get('tasks') || [];
    const task = tasks.find(t => t.id === taskId);

    if (!task) return;

    const html = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-edit"></i> Editar Tarefa</h3>
                <button class="modal-close" onclick="closeModal('taskModal')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="taskForm" onsubmit="updateTask(event, ${taskId})">
                    <div class="form-group">
                        <label><i class="fas fa-heading"></i> Título</label>
                        <input type="text" id="taskTitle" value="${task.title}" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-align-left"></i> Descrição</label>
                        <textarea id="taskDescription" rows="4" required>${task.description}</textarea>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-calendar"></i> Prazo (opcional)</label>
                        <input type="date" id="taskDeadline" value="${task.deadline || ''}" min="${new Date().toISOString().split('T')[0]}">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button onclick="closeModal('taskModal')" class="btn btn-secondary">Cancelar</button>
                <button onclick="document.getElementById('taskForm').requestSubmit()" class="btn btn-primary">
                    <i class="fas fa-save"></i> Atualizar
                </button>
            </div>
        </div>
    `;

    document.getElementById('taskModal').innerHTML = html;
    document.getElementById('taskModal').classList.add('show');
}

function saveTask(event) {
    event.preventDefault();

    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const deadline = document.getElementById('taskDeadline').value;

    const tasks = Storage.get('tasks') || [];
    
    const newTask = {
        id: Date.now(),
        userId: currentUser.id,
        title,
        description,
        deadline: deadline || null,
        completed: false,
        createdAt: new Date().toISOString()
    };

    tasks.push(newTask);
    Storage.set('tasks', tasks);

    closeModal('taskModal');
    showToast('Tarefa criada com sucesso!', 'success');
    renderDashboard();
}

function updateTask(event, taskId) {
    event.preventDefault();

    const tasks = Storage.get('tasks') || [];
    const taskIndex = tasks.findIndex(t => t.id === taskId);

    if (taskIndex === -1) return;

    tasks[taskIndex].title = document.getElementById('taskTitle').value.trim();
    tasks[taskIndex].description = document.getElementById('taskDescription').value.trim();
    tasks[taskIndex].deadline = document.getElementById('taskDeadline').value || null;

    Storage.set('tasks', tasks);

    closeModal('taskModal');
    showToast('Tarefa atualizada com sucesso!', 'success');
    renderDashboard();
}

function completeTask(taskId) {
    const tasks = Storage.get('tasks') || [];
    const taskIndex = tasks.findIndex(t => t.id === taskId);

    if (taskIndex === -1) return;

    tasks[taskIndex].completed = true;
    tasks[taskIndex].completedAt = new Date().toISOString();

    Storage.set('tasks', tasks);
    showToast('Tarefa concluída!', 'success');
    renderDashboard();
}

function viewTaskDetails(taskId) {
    const tasks = Storage.get('tasks') || [];
    const task = tasks.find(t => t.id === taskId);

    if (!task) return;

    const status = getTaskStatus(task);
    const statusText = status === 'completed' ? 'Concluída' : 
                      status === 'overdue' ? 'Atrasada' : 'Pendente';

    const html = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-info-circle"></i> Detalhes da Tarefa</h3>
                <button class="modal-close" onclick="closeModal('detailsModal')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="detail-row">
                    <i class="fas fa-heading"></i>
                    <div><strong>Título:</strong> ${task.title}</div>
                </div>
                <div class="detail-row">
                    <i class="fas fa-align-left"></i>
                    <div><strong>Descrição:</strong> ${task.description}</div>
                </div>
                <div class="detail-row">
                    <i class="fas fa-info-circle"></i>
                    <div><strong>Status:</strong> <span class="task-status ${status}">${statusText}</span></div>
                </div>
                <div class="detail-row">
                    <i class="fas fa-calendar-plus"></i>
                    <div><strong>Criada em:</strong> ${formatDate(task.createdAt)}</div>
                </div>
                ${task.deadline ? `
                    <div class="detail-row">
                        <i class="fas fa-calendar-check"></i>
                        <div><strong>Prazo:</strong> ${formatDate(task.deadline)}</div>
                    </div>
                ` : ''}
                ${task.completed ? `
                    <div class="detail-row">
                        <i class="fas fa-check-circle"></i>
                        <div><strong>Concluída em:</strong> ${formatDate(task.completedAt)}</div>
                    </div>
                ` : ''}
            </div>
            <div class="modal-footer">
                <button onclick="closeModal('detailsModal')" class="btn btn-secondary">Fechar</button>
            </div>
        </div>
    `;

    document.getElementById('detailsModal').innerHTML = html;
    document.getElementById('detailsModal').classList.add('show');
}

function confirmDelete(taskId) {
    const html = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-exclamation-triangle"></i> Confirmar Exclusão</h3>
                <button class="modal-close" onclick="closeModal('confirmModal')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <p>Tem certeza que deseja excluir esta tarefa? Esta ação não pode ser desfeita.</p>
            </div>
            <div class="modal-footer">
                <button onclick="closeModal('confirmModal')" class="btn btn-secondary">Cancelar</button>
                <button onclick="deleteTask(${taskId})" class="btn btn-danger">
                    <i class="fas fa-trash"></i> Excluir
                </button>
            </div>
        </div>
    `;

    document.getElementById('confirmModal').innerHTML = html;
    document.getElementById('confirmModal').classList.add('show');
}

function deleteTask(taskId) {
    let tasks = Storage.get('tasks') || [];
    tasks = tasks.filter(t => t.id !== taskId);
    Storage.set('tasks', tasks);

    closeModal('confirmModal');
    showToast('Tarefa excluída!', 'success');
    renderDashboard();
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Reports
function renderReports() {
    const tasks = getUserTasks();
    const stats = calculateStats(tasks);

    const html = `
        <h2><i class="fas fa-chart-bar"></i> Relatórios</h2>
        
        <div class="report-section">
            <h3><i class="fas fa-info-circle"></i> Estatísticas Gerais</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon total"><i class="fas fa-tasks"></i></div>
                    <div class="stat-content">
                        <h3>${stats.total}</h3>
                        <p>Total de Tarefas</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon pending"><i class="fas fa-clock"></i></div>
                    <div class="stat-content">
                        <h3>${stats.pending}</h3>
                        <p>Pendentes</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon completed"><i class="fas fa-check-circle"></i></div>
                    <div class="stat-content">
                        <h3>${stats.completed}</h3>
                        <p>Concluídas</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon overdue"><i class="fas fa-exclamation-triangle"></i></div>
                    <div class="stat-content">
                        <h3>${stats.overdue}</h3>
                        <p>Atrasadas</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="report-section">
            <h3><i class="fas fa-download"></i> Exportar Dados</h3>
            <div class="report-actions">
                <button onclick="exportJSON()" class="btn btn-info">
                    <i class="fas fa-file-code"></i> Exportar JSON
                </button>
                <button onclick="exportCSV()" class="btn btn-success">
                    <i class="fas fa-file-csv"></i> Exportar CSV
                </button>
            </div>
        </div>
    `;

    document.getElementById('reportsScreen').innerHTML = html;
}

function exportJSON() {
    const tasks = getUserTasks();
    const dataStr = JSON.stringify(tasks, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    downloadFile(blob, `tarefas_${currentUser.username}_${Date.now()}.json`);
    showToast('Relatório JSON exportado!', 'success');
}

function exportCSV() {
    const tasks = getUserTasks();
    let csv = 'ID,Título,Descrição,Status,Criada em,Prazo,Concluída em\n';

    tasks.forEach(task => {
        const status = getTaskStatus(task);
        const statusText = status === 'completed' ? 'Concluída' : 
                          status === 'overdue' ? 'Atrasada' : 'Pendente';
        
        csv += `${task.id},"${task.title}","${task.description}",${statusText},${formatDate(task.createdAt)},${task.deadline ? formatDate(task.deadline) : ''},${task.completedAt ? formatDate(task.completedAt) : ''}\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    downloadFile(blob, `tarefas_${currentUser.username}_${Date.now()}.csv`);
    showToast('Relatório CSV exportado!', 'success');
}

function downloadFile(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Profile
function renderProfile() {
    const tasks = getUserTasks();
    const stats = calculateStats(tasks);

    const html = `
        <div class="profile-container">
            <h2><i class="fas fa-user"></i> Meu Perfil</h2>

            <div class="profile-card">
                <div class="profile-header">
                    <div class="profile-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="profile-info">
                        <h2>${currentUser.name}</h2>
                        <p>@${currentUser.username}</p>
                    </div>
                </div>

                <div class="profile-details">
                    <div class="detail-row">
                        <i class="fas fa-envelope"></i>
                        <div><strong>E-mail:</strong> ${currentUser.email}</div>
                    </div>
                    <div class="detail-row">
                        <i class="fas fa-calendar-plus"></i>
                        <div><strong>Membro desde:</strong> ${formatDate(currentUser.createdAt)}</div>
                    </div>
                </div>
            </div>

            <div class="profile-card">
                <h3><i class="fas fa-chart-line"></i> Estatísticas</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon total"><i class="fas fa-tasks"></i></div>
                        <div class="stat-content">
                            <h3>${stats.total}</h3>
                            <p>Total de Tarefas</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon completed"><i class="fas fa-check-circle"></i></div>
                        <div class="stat-content">
                            <h3>${stats.completed}</h3>
                            <p>Concluídas</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon pending"><i class="fas fa-clock"></i></div>
                        <div class="stat-content">
                            <h3>${stats.pending}</h3>
                            <p>Pendentes</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.getElementById('profileScreen').innerHTML = html;
}

// Toast
function showToast(message, type) {
    const toast = document.getElementById('toast');
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Initialize
initializeData();

if (currentUser) {
    showApp();
} else {
    document.getElementById('authScreen').style.display = 'flex';
    document.getElementById('appScreen').style.display = 'none';
}
