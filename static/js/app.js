// To-Do App Frontend Controller
let currentFilter = 'all';
let currentCategory = 'all';
let currentPriority = 'all';
let currentSort = 'created_desc';
let searchQuery = '';

// DOM Elements
const taskList = document.getElementById('taskList');
const taskForm = document.getElementById('taskForm');
const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');
const categoryFilter = document.getElementById('categoryFilter');
const priorityFilter = document.getElementById('priorityFilter');
const clearCompletedBtn = document.getElementById('clearCompletedBtn');
const statTotal = document.getElementById('statTotal');
const statActive = document.getElementById('statActive');
const statCompleted = document.getElementById('statCompleted');

// Edit Modal Elements
const editModal = document.getElementById('editModal');
const editForm = document.getElementById('editForm');
const editId = document.getElementById('editId');
const editTitle = document.getElementById('editTitle');
const editDescription = document.getElementById('editDescription');
const editPriority = document.getElementById('editPriority');
const editCategory = document.getElementById('editCategory');
const editDueDate = document.getElementById('editDueDate');
const cancelEditBtn = document.getElementById('cancelEditBtn');

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
  loadTasks();
  loadStats();
  setupEventListeners();
});

function setupEventListeners() {
  // Add task form
  taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const priority = document.getElementById('taskPriority').value;
    const category = document.getElementById('taskCategory').value.trim() || 'General';
    const dueDate = document.getElementById('taskDueDate').value || null;

    if (!title) return;

    try {
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, priority, category, due_date: dueDate })
      });

      if (res.ok) {
        taskForm.reset();
        loadTasks();
        loadStats();
      }
    } catch (err) {
      console.error('Error adding task:', err);
    }
  });

  // Filter Buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => {
        b.classList.remove('bg-indigo-600', 'text-white');
        b.classList.add('bg-white', 'text-slate-700', 'border', 'border-slate-200');
      });
      btn.classList.add('bg-indigo-600', 'text-white');
      btn.classList.remove('bg-white', 'text-slate-700', 'border', 'border-slate-200');
      currentFilter = btn.dataset.filter;
      loadTasks();
    });
  });

  // Category filter
  categoryFilter.addEventListener('change', () => {
    currentCategory = categoryFilter.value;
    loadTasks();
  });

  // Priority filter
  priorityFilter.addEventListener('change', () => {
    currentPriority = priorityFilter.value;
    loadTasks();
  });

  // Sort selector
  sortSelect.addEventListener('change', () => {
    currentSort = sortSelect.value;
    loadTasks();
  });

  // Live search with debounce
  let debounceTimeout;
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      searchQuery = searchInput.value;
      loadTasks();
    }, 250);
  });

  // Clear completed
  clearCompletedBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to delete all completed tasks?')) return;
    try {
      const res = await fetch('/api/tasks/clear-completed', { method: 'POST' });
      if (res.ok) {
        loadTasks();
        loadStats();
      }
    } catch (err) {
      console.error('Error clearing tasks:', err);
    }
  });

  // Edit Modal Cancel
  cancelEditBtn.addEventListener('click', () => {
    editModal.classList.add('hidden');
  });

  // Edit Form Submit
  editForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = editId.value;
    const updates = {
      title: editTitle.value.trim(),
      description: editDescription.value.trim(),
      priority: editPriority.value,
      category: editCategory.value.trim() || 'General',
      due_date: editDueDate.value || null
    };

    try {
      const res = await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      });
      if (res.ok) {
        editModal.classList.add('hidden');
        loadTasks();
        loadStats();
      }
    } catch (err) {
      console.error('Error updating task:', err);
    }
  });
}

// Fetch and render tasks
async function loadTasks() {
  const params = new URLSearchParams();
  if (currentFilter !== 'all') params.append('status', currentFilter);
  if (currentCategory !== 'all') params.append('category', currentCategory);
  if (currentPriority !== 'all') params.append('priority', currentPriority);
  if (currentSort) params.append('sort_by', currentSort);
  if (searchQuery) params.append('search', searchQuery);

  try {
    const res = await fetch(`/api/tasks?${params.toString()}`);
    const tasks = await res.json();
    renderTasks(tasks);
  } catch (err) {
    console.error('Failed to load tasks:', err);
  }
}

// Fetch stats & update category options
async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    const stats = await res.json();
    statTotal.textContent = stats.total;
    statActive.textContent = stats.active;
    statCompleted.textContent = stats.completed;

    // Update categories filter options
    const prevSelected = categoryFilter.value;
    categoryFilter.innerHTML = '<option value="all">All Categories</option>';
    stats.categories.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat;
      opt.textContent = cat;
      if (cat === prevSelected) opt.selected = true;
      categoryFilter.appendChild(opt);
    });
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

// Render task list
function renderTasks(tasks) {
  if (tasks.length === 0) {
    taskList.innerHTML = `
      <div class="text-center py-16 px-4 bg-white rounded-2xl border border-dashed border-slate-300">
        <svg class="mx-auto h-12 w-12 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        <p class="text-base font-medium text-slate-600">No tasks found</p>
        <p class="text-xs text-slate-400 mt-1">Add a new task above or adjust your search filters.</p>
      </div>
    `;
    return;
  }

  taskList.innerHTML = tasks.map(task => {
    const isCompleted = task.completed;
    const priorityColors = {
      High: 'bg-rose-50 text-rose-700 border-rose-200',
      Medium: 'bg-amber-50 text-amber-700 border-amber-200',
      Low: 'bg-emerald-50 text-emerald-700 border-emerald-200'
    };
    const priorityClass = priorityColors[task.priority] || priorityColors.Medium;

    let dueDateBadge = '';
    if (task.due_date) {
      const today = new Date().toISOString().split('T')[0];
      const isOverdue = !isCompleted && task.due_date < today;
      const isToday = task.due_date === today;
      const dateColor = isOverdue 
        ? 'text-rose-600 font-semibold' 
        : isToday 
        ? 'text-amber-600 font-medium' 
        : 'text-slate-500';

      dueDateBadge = `
        <span class="inline-flex items-center gap-1 text-xs ${dateColor}">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          ${isOverdue ? 'Overdue: ' : ''}${task.due_date}
        </span>
      `;
    }

    return `
      <div class="task-card bg-white rounded-xl p-4 sm:p-5 border border-slate-200 flex items-start gap-4 ${isCompleted ? 'task-completed' : ''}" data-id="${task.id}">
        <!-- Checkbox -->
        <button onclick="toggleTask('${task.id}')" class="mt-0.5 flex-shrink-0 w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-colors ${isCompleted ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-300 hover:border-indigo-500 bg-white'}">
          ${isCompleted ? `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
          ` : ''}
        </button>

        <!-- Task Body -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-2">
            <h3 class="task-title text-base font-semibold text-slate-800 break-words">${escapeHtml(task.title)}</h3>
            <!-- Actions -->
            <div class="flex items-center gap-1.5 flex-shrink-0">
              <button onclick='openEditModal(${JSON.stringify(task).replace(/'/g, "&apos;")})' class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-slate-100 rounded-lg transition-colors" title="Edit task">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
              </button>
              <button onclick="deleteTask('${task.id}')" class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors" title="Delete task">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>

          ${task.description ? `
            <p class="text-sm text-slate-600 mt-1 line-clamp-2">${escapeHtml(task.description)}</p>
          ` : ''}

          <!-- Metadata Badges -->
          <div class="flex flex-wrap items-center gap-2 mt-3 pt-2 border-t border-slate-100">
            <span class="inline-flex items-center text-xs px-2.5 py-0.5 rounded-full border ${priorityClass} font-medium">
              ${task.priority} Priority
            </span>
            <span class="inline-flex items-center text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium">
              📁 ${escapeHtml(task.category)}
            </span>
            ${dueDateBadge}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Toggle Task
async function toggleTask(id) {
  try {
    const res = await fetch(`/api/tasks/${id}/toggle`, { method: 'PATCH' });
    if (res.ok) {
      loadTasks();
      loadStats();
    }
  } catch (err) {
    console.error('Error toggling task:', err);
  }
}

// Delete Task
async function deleteTask(id) {
  try {
    const res = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    if (res.ok) {
      loadTasks();
      loadStats();
    }
  } catch (err) {
    console.error('Error deleting task:', err);
  }
}

// Open Edit Modal
function openEditModal(task) {
  editId.value = task.id;
  editTitle.value = task.title;
  editDescription.value = task.description || '';
  editPriority.value = task.priority;
  editCategory.value = task.category || 'General';
  editDueDate.value = task.due_date || '';
  editModal.classList.remove('hidden');
}

// Escape HTML helper
function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}
