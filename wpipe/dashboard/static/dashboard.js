// Dashboard JavaScript

// Escape HTML to prevent XSS
function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

let graphState = {
    scale: 1,
    translateX: 0,
    translateY: 0,
    currentGraph: null,
    selectedNode: null,
    hoveredNode: null,
    isDragging: false,
    startX: 0,
    startY: 0
};

// ==================== SIDEBAR ====================
window.toggleSidebar = function() {
    const sidebar = document.getElementById('sidebar-menu');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (!sidebar || !overlay) return;
    
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
};

// Close sidebar when clicking outside on mobile
window.addEventListener('resize', () => {
    const sidebar = document.getElementById('sidebar-menu');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (window.innerWidth > 768) {
        sidebar?.classList.remove('active');
        overlay?.classList.remove('active');
    }
});

// ==================== INITIALIZATION ====================
function init() {
    loadPipelines();
    loadStats();
    setupEventListeners();
}

// ==================== STATS ====================
async function loadStats() {
    try {
        const res = await fetch('/api/stats');
        const stats = await res.json();
        renderStats(stats);
    } catch (e) {
        console.error('Error loading stats:', e);
    }
}

function renderStats(stats) {
    document.getElementById('s-total').textContent = stats.total_pipelines || 0;
    document.getElementById('s-success').textContent = (stats.success_rate || 0) + '%';
    document.getElementById('s-avg-time').textContent = fmtDuration(stats.avg_duration_ms);
    document.getElementById('s-steps').textContent = stats.total_steps || 0;
    document.getElementById('s-alerts').textContent = stats.unacknowledged_alerts || 0;
    document.getElementById('s-errors').textContent = stats.errors || 0;
}

window.refreshData = function() {
    loadPipelines();
    loadStats();
};

// ==================== MISSING FUNCTIONS ====================
let currentLang = 'en';

const translations = {
    en: {
        tutorialTitle: 'Dashboard Tutorial',
        tutorialIntro: 'Welcome to wpipe Dashboard! This guide will help you understand each view.',
        pipelineTabs: 'Pipeline Tabs (require selection)',
        graph: 'Graph - Visualizes the execution flow of a selected pipeline. Each node is a step.',
        graphHelp: '🔍 Zoom: Mouse wheel | ✋ Pan: Drag | 📜 History: Click clock button',
        data: 'Data - Shows input/output of each step in the selected pipeline.',
        globalTabs: 'Global Views (independent of selection)',
        timeline: 'Timeline - Shows execution trends over days (last 7/14/30 days).',
        analytics: 'Analytics - Overview: pie chart of statuses, slowest steps, total stats.',
        alerts: 'Alerts - Pipeline errors and warnings. Filter by severity.',
        events: 'Events - Log of all pipeline/step events (created, started, completed, failed).',
        states: 'States - Reusable step functions: most used, slowest, with most errors.',
        pipelines: 'Pipelines - Which pipelines are slowest, have most errors, recent runs.',
        history: 'To see past executions:',
        historySteps: '1. Select any pipeline from the right list\n2. Click the History button (🕐) in graph controls\n3. Click any previous execution to view it',
        close: 'Got it!'
    },
    es: {
        tutorialTitle: 'Tutorial del Dashboard',
        tutorialIntro: '¡Bienvenido a wpipe Dashboard! Esta guía te ayudará a entender cada vista.',
        pipelineTabs: 'Pestañas de Pipeline (requieren selección)',
        graph: 'Graph - Visualiza el flujo de ejecución del pipeline seleccionado. Cada nodo es un paso.',
        graphHelp: '🔍 Zoom: Rueda ratón | ✋ Mover: Arrastrar | 📜 Historial: Botón reloj',
        data: 'Data - Muestra entrada/salida de cada paso del pipeline seleccionado.',
        globalTabs: 'Vistas Globales (independientes de selección)',
        timeline: 'Timeline - Muestra tendencias de ejecución por días (últimos 7/14/30 días).',
        analytics: 'Analytics - Resumen: gráfico de estados, pasos más lentos, estadísticas.',
        alerts: 'Alerts - Errores y warnings de pipelines. Filtra por severidad.',
        events: 'Events - Registro de eventos de pipelines/pasos (creado, iniciado, completado, error).',
        states: 'States - Funciones de paso reutilizables: más usadas, lentas, con errores.',
        pipelines: 'Pipelines - Cuáles son más lentos, con más errores, ejecuciones recientes.',
        history: 'Para ver ejecuciones anteriores:',
        historySteps: '1. Selecciona un pipeline de la lista derecha\n2. Haz click en el botón History (🕐) en controles del graph\n3. Haz click en cualquier ejecución anterior para verla',
        close: '¡Entendido!'
    }
};

window.changeLanguage = function(lang) {
    currentLang = lang;
    console.log('Language changed to:', lang);
    updateI18n();
};

function updateI18n() {
    const t = translations[currentLang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) el.textContent = t[key];
    });
}

window.showTutorial = function() {
    const modal = document.getElementById('tutorial-modal');
    if (!modal) return;
    
    const t = translations[currentLang];
    
    modal.style.display = 'flex';
    document.getElementById('tutorial-content').innerHTML = `
        <h2 style="margin-bottom:0.5rem"><i class="fas fa-rocket"></i> ${t.tutorialTitle}</h2>
        <p style="color:var(--text-muted);margin-bottom:1.5rem;font-size:0.9rem">${t.tutorialIntro}</p>
        
        <div style="text-align:left;line-height:1.8">
            <div style="background:var(--bg-tertiary);padding:0.75rem;border-radius:8px;margin-bottom:1rem">
                <div style="font-size:0.75rem;text-transform:uppercase;color:var(--text-muted);margin-bottom:0.5rem">${t.pipelineTabs}</div>
                <p style="margin:0.25rem 0"><i class="fas fa-diagram-project" style="width:20px;color:#3b82f6"></i> <strong>${t.graph}</strong></p>
                <p style="font-size:0.8rem;color:var(--text-muted);margin-left:20px;margin-bottom:0.5rem">${t.graphHelp}</p>
                <p style="margin:0.25rem 0"><i class="fas fa-database" style="width:20px;color:#10b981"></i> <strong>${t.data}</strong></p>
            </div>
            
            <div style="background:var(--bg-tertiary);padding:0.75rem;border-radius:8px;margin-bottom:1rem">
                <div style="font-size:0.75rem;text-transform:uppercase;color:var(--text-muted);margin-bottom:0.5rem">${t.globalTabs}</div>
                <p style="margin:0.25rem 0"><i class="fas fa-chart-gantt" style="width:20px;color:#8b5cf6"></i> ${t.timeline}</p>
                <p style="margin:0.25rem 0"><i class="fas fa-chart-line" style="width:20px;color:#ec4899"></i> ${t.analytics}</p>
                <p style="margin:0.25rem 0"><i class="fas fa-bell" style="width:20px;color:#f59e0b"></i> ${t.alerts}</p>
                <p style="margin:0.25rem 0"><i class="fas fa-bookmark" style="width:20px;color:#06b6d4"></i> ${t.events}</p>
                <p style="margin:0.25rem 0"><i class="fas fa-cubes" style="width:20px;color:#ef4444"></i> ${t.states}</p>
                <p style="margin:0.25rem 0"><i class="fas fa-project-diagram" style="width:20px;color:#14b8a6"></i> ${t.pipelines}</p>
            </div>
            
            <div style="background:rgba(59,130,246,0.1);padding:0.75rem;border-radius:8px;border-left:3px solid #3b82f6">
                <div style="font-size:0.85rem;font-weight:600;margin-bottom:0.5rem">${t.history}</div>
                <pre style="font-size:0.8rem;white-space:pre-wrap;margin:0;color:var(--text-secondary)">${t.historySteps}</pre>
            </div>
        </div>
        
        <button onclick="document.getElementById('tutorial-modal').style.display='none'" class="btn btn-primary" style="margin-top:1.5rem">${t.close}</button>
    `;
};

window.filterPipelinesBySearch = function(query) {
    const items = document.querySelectorAll('.pipeline-item');
    items.forEach(item => {
        const name = item.querySelector('.pipeline-name')?.textContent.toLowerCase() || '';
        item.style.display = name.includes(query.toLowerCase()) ? '' : 'none';
    });
};

window.filterPipelines = function(status) {
    const items = document.querySelectorAll('.pipeline-item');
    items.forEach(item => {
        const itemStatus = item.querySelector('.pipeline-status')?.className || '';
        if (!status || itemStatus.includes(status)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
};

// ==================== PIPELINE HISTORY ====================
let currentPipelineId = null;
let currentPipelineName = null;

window.showCurrentPipelineHistory = function() {
    if (currentPipelineName) {
        showPipelineHistoryModal(currentPipelineName, currentPipelineId);
    } else {
        showAllPipelinesHistory();
    }
};

window.showAllPipelinesHistory = function() {
    const modal = document.getElementById('tutorial-modal');
    if (!modal) return;
    
    const title = currentLang === 'es' ? 'Todas las Ejecuciones' : 'All Pipeline Executions';
    const selectMsg = currentLang === 'es' ? 'Selecciona un pipeline:' : 'Select a pipeline:';
    
    modal.style.display = 'flex';
    document.getElementById('tutorial-content').innerHTML = `
        <h2 style="margin-bottom:1rem"><i class="fas fa-history"></i> ${title}</h2>
        <p style="color:var(--text-muted);margin-bottom:1rem;font-size:0.9rem">${selectMsg}</p>
        <div id="all-pipelines-list" style="max-height:400px;overflow-y:auto">
            <div class="loading"><div class="spinner"></div></div>
        </div>
        <button onclick="document.getElementById('tutorial-modal').style.display='none'" class="btn btn-ghost" style="margin-top:1rem">Close</button>
    `;
    
    fetch('/api/pipelines')
        .then(r => r.json())
        .then(pipelines => {
            if (!pipelines || pipelines.length === 0) {
                document.getElementById('all-pipelines-list').innerHTML = '<p style="color:var(--text-muted)">No pipelines found</p>';
                return;
            }
            
            // Group by pipeline name
            const grouped = {};
            pipelines.forEach(p => {
                const name = p.name || p.id;
                if (!grouped[name]) grouped[name] = [];
                grouped[name].push(p);
            });
            
            let html = '';
            Object.keys(grouped).sort().forEach(name => {
                const runs = grouped[name].slice(0, 5); // Show max 5 recent
                html += `
                    <div style="margin-bottom:1rem">
                        <div style="font-weight:600;margin-bottom:0.5rem">${escapeHtml(name)}</div>
                        ${runs.map(p => `
                            <div class="pipeline-item" onclick="selectPipeline('${escapeHtml(p.id)}');document.getElementById('tutorial-modal').style.display='none'" 
                                 style="margin:0.25rem 0;padding:0.5rem;font-size:0.85rem">
                                <div class="pipeline-status ${escapeHtml(p.status)}" style="width:8px;height:8px"></div>
                                <span style="color:var(--text-muted)">${fmtTime(p.created_at)}</span>
                                <span class="status-badge ${escapeHtml(p.status)}" style="font-size:0.7rem">${escapeHtml(p.status)}</span>
                                ${p.total_duration_ms ? '<span style="color:var(--text-muted)">'+fmtDuration(p.total_duration_ms)+'</span>' : ''}
                            </div>
                        `).join('')}
                    </div>
                `;
            });
            document.getElementById('all-pipelines-list').innerHTML = html;
        });
};

async function loadPipelineHistory(pipelineName) {
    try {
        const res = await fetch(`/api/pipelines/by-name/${encodeURIComponent(pipelineName)}`);
        const data = await res.json();
        return data;
    } catch (e) {
        console.error('Error loading pipeline history:', e);
        return [];
    }
}

function showPipelineHistoryModal(pipelineName, currentId) {
    const modal = document.getElementById('tutorial-modal');
    if (!modal) return;
    
    modal.style.display = 'flex';
    document.getElementById('tutorial-content').innerHTML = `
        <h2 style="margin-bottom:1rem"><i class="fas fa-history"></i> Pipeline History: ${pipelineName}</h2>
        <div id="history-list" style="max-height:400px;overflow-y:auto">
            <div class="loading"><div class="spinner"></div> Loading...</div>
        </div>
        <button onclick="document.getElementById('tutorial-modal').style.display='none'" class="btn btn-ghost" style="margin-top:1rem">Close</button>
    `;
    
    fetch(`/api/pipelines/by-name/${encodeURIComponent(pipelineName)}`)
        .then(r => r.json())
        .then(pipelines => {
            const list = document.getElementById('history-list');
            if (!pipelines || pipelines.length === 0) {
                list.innerHTML = '<p style="color:var(--text-muted)">No history found</p>';
                return;
            }
            
            list.innerHTML = pipelines.map(p => `
                <div class="pipeline-item" onclick="selectPipeline('${escapeHtml(p.id)}');document.getElementById('tutorial-modal').style.display='none'" 
                     style="margin:0.5rem 0;padding:0.75rem;cursor:pointer;${p.id === currentId ? 'border:2px solid #3b82f6' : ''}">
                    <div class="pipeline-status ${escapeHtml(p.status)}"></div>
                    <div class="pipeline-info">
                        <div class="pipeline-name">${escapeHtml(p.name || p.id)}</div>
                        <div class="pipeline-meta">
                            <span>${escapeHtml(p.status)}</span>
                            <span>${fmtTime(p.started_at)}</span>
                            ${p.total_duration_ms ? '<span>' + fmtDuration(p.total_duration_ms) + '</span>' : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        });
}

// ==================== PIPELINES ====================
async function loadPipelines() {
    try {
        const res = await fetch('/api/pipelines');
        const pipelines = await res.json();
        renderPipelineList(pipelines);
    } catch (e) {
        console.error('Error loading pipelines:', e);
    }
}

function renderPipelineList(pipelines) {
    console.log('Rendering pipelines:', pipelines?.length);
    const list = document.getElementById('pipeline-list');
    if (!pipelines || pipelines.length === 0) {
        list.innerHTML = '<div class="empty-state"><p>No pipelines</p></div>';
        return;
    }
    
    // Group pipelines by name
    const grouped = {};
    pipelines.forEach(p => {
        const name = p.name || 'Unnamed';
        if (!grouped[name]) {
            grouped[name] = [];
        }
        grouped[name].push(p);
    });
    
    // Sort executions by date (most recent first) within each group
    Object.keys(grouped).forEach(name => {
        grouped[name].sort((a, b) => new Date(b.started_at) - new Date(a.started_at));
    });
    
    // Render grouped pipelines with collapsible sections
    let html = '';
    Object.keys(grouped).sort().forEach(name => {
        const executions = grouped[name];
        const latestStatus = executions[0].status;
        const latestDuration = executions[0].total_duration_ms;
        const count = executions.length;
        
        // Escape quotes in name for onclick
        const safeName = name.replace(/'/g, "\\'");
        
        html += `
            <div class="pipeline-group">
                <div class="pipeline-group-header" onclick="togglePipelineGroup('${safeName}', event)">
                    <i class="fas fa-chevron-right expand-icon"></i>
                    <div class="pipeline-status ${latestStatus}"></div>
                    <div class="pipeline-info">
                        <div class="pipeline-name">${name}</div>
                        <div class="pipeline-meta">
                            <span>${count} execution${count !== 1 ? 's' : ''}</span>
                            <span>${latestStatus}</span>
                            ${latestDuration ? '<span>' + fmtDuration(latestDuration) + '</span>' : ''}
                        </div>
                    </div>
                </div>
                
                <div class="pipeline-group-content" style="display:none;">
                    ${executions.map(p => `
                        <div class="pipeline-execution" onclick="selectPipeline('${escapeHtml(p.id)}')">
                            <div class="pipeline-status ${escapeHtml(p.status)}"></div>
                            <div class="pipeline-info">
                                <div class="pipeline-id">${escapeHtml(p.id)}</div>
                                <div class="pipeline-meta">
                                    <span>${escapeHtml(p.status)}</span>
                                    <span>${fmtTime(p.started_at)}</span>
                                    ${p.total_duration_ms ? '<span>' + fmtDuration(p.total_duration_ms) + '</span>' : ''}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    list.innerHTML = html;
}

// Toggle pipeline group expansion
window.togglePipelineGroup = function(name, evt) {
    if (evt) evt.stopPropagation();
    
    // Find the group by looking for the header that contains this name
    const headers = document.querySelectorAll('.pipeline-group-header');
    let targetGroup = null;
    
    for (let header of headers) {
        const nameEl = header.querySelector('.pipeline-name');
        if (nameEl && nameEl.textContent.trim() === name) {
            targetGroup = header.closest('.pipeline-group');
            break;
        }
    }
    
    if (!targetGroup) return;
    
    const content = targetGroup.querySelector('.pipeline-group-content');
    const icon = targetGroup.querySelector('.expand-icon');
    
    if (!content || !icon) return;
    
    const isExpanded = content.style.display !== 'none';
    content.style.display = isExpanded ? 'none' : 'block';
    icon.classList.toggle('expanded', !isExpanded);
}

async function selectPipeline(id) {
    console.log('Selecting pipeline:', id);
    try {
        const pRes = await fetch('/api/pipelines/' + id);
        if (!pRes.ok) throw new Error('Pipeline fetch failed');
        const pipeline = await pRes.json();
        
        if (!pipeline) return;

        currentPipelineId = id;
        currentPipelineName = pipeline.name || id;
        
        // Mark execution as active in the list
        document.querySelectorAll('.pipeline-execution').forEach(el => {
            el.classList.remove('active');
        });
        document.querySelector(`.pipeline-execution[onclick="selectPipeline('${id}')"]`)?.classList.add('active');
        
        const gRes = await fetch('/api/pipelines/' + id + '/graph');
        if (gRes.ok) {
            const graph = await gRes.json();
            graphState.currentGraph = graph;
            try {
                renderGraph(graph);
            } catch (ge) {
                console.error('Render graph error:', ge);
            }
        }
        
        try {
            renderSteps(pipeline);
        } catch (se) {
            console.error('Render steps error:', se);
        }
        
        // Update pipeline info in header
        const info = document.getElementById('graph-pipeline-info');
        if (info) {
            info.innerHTML = `
                <span style="font-size:0.8rem;color:var(--text-muted)">${currentPipelineName}</span>
                <button onclick="showCurrentPipelineHistory()" style="margin-left:0.5rem;padding:2px 8px;font-size:0.7rem" class="btn btn-ghost">
                    <i class="fas fa-history"></i> History
                </button>
            `;
        }
    } catch (e) {
        console.error('Error selecting pipeline:', e);
    }
}

// ==================== GRAPH RENDERING ====================
function renderGraph(graph) {
    const svg = document.getElementById('graph-svg');
    const edgesG = document.getElementById('graph-edges');
    const nodesG = document.getElementById('graph-nodes');
    const empty = document.getElementById('graph-empty');
    const container = document.getElementById('graph-container');
    
    if (!graph.nodes || graph.nodes.length === 0) {
        svg.style.display = 'none';
        empty.style.display = 'block';
        return;
    }
    
    svg.style.display = 'block';
    empty.style.display = 'none';
    edgesG.innerHTML = '';
    nodesG.innerHTML = '';
    
    // --- NUEVO ALGORITMO DE LAYOUT ---
    // Agrupamos nodos por nivel jerárquico y parent_step_id
    const nodesMap = {};
    graph.nodes.forEach(n => nodesMap[n.id] = n);
    
    const levels = {}; // Nivel horizontal -> Lista de nodos
    const nodePositions = {}; // node.id -> {level, offset}
    
    // Asignar niveles basándose en el flujo secuencial y jerarquía
    let currentLevel = 0;
    
    graph.nodes.forEach(node => {
        if (!node.parent_step_id) {
            // Nodos principales (sin padre) se ponen secuencialmente
            nodePositions[node.id] = { level: currentLevel, offset: 0 };
            if (!levels[currentLevel]) levels[currentLevel] = [];
            levels[currentLevel].push(node.id);
            currentLevel++;
        } else {
            // Sub-nodos (paralelos) se ponen en el mismo nivel que su padre pero con offset
            const parentId = `step_${node.parent_step_id}`;
            const parentPos = nodePositions[parentId];
            
            if (parentPos) {
                const subLevel = parentPos.level + 1;
                if (!levels[subLevel]) levels[subLevel] = [];
                
                // Determinamos offset vertical (cuántos sub-nodos hay ya en este nivel para este padre)
                const siblings = levels[subLevel].filter(id => nodesMap[id] && nodesMap[id].parent_step_id === node.parent_step_id);
                nodePositions[node.id] = { level: subLevel, offset: siblings.length };
                levels[subLevel].push(node.id);
            } else {
                // Fallback si no encontramos al padre o el padre no ha sido posicionado aún
                nodePositions[node.id] = { level: currentLevel, offset: 0 };
                if (!levels[currentLevel]) levels[currentLevel] = [];
                levels[currentLevel].push(node.id);
                currentLevel++;
            }
        }
    });

    const spacingX = 180;
    const spacingY = 120;
    const startX = 100;
    const centerY = 250;
    
    // Calculamos coordenadas X, Y para cada nodo
    graph.nodes.forEach(nd => {
        const pos = nodePositions[nd.id];
        nd.x = startX + (pos.level * spacingX);
        
        // El offset vertical centra los nodos paralelos alrededor del centro
        const siblingsInLevel = levels[pos.level].length;
        if (siblingsInLevel > 1) {
            const totalH = (siblingsInLevel - 1) * spacingY;
            nd.y = (centerY - totalH/2) + (levels[pos.level].indexOf(nd.id) * spacingY);
        } else {
            nd.y = centerY;
        }
    });
    
    const svgW = Math.max(1200, startX + (Object.keys(levels).length * spacingX) + 100);
    const svgH = 600;
    
    svg.setAttribute('width', svgW);
    svg.setAttribute('height', svgH);
    
    // Reset transform state
    graphState.scale = 1;
    graphState.translateX = 0;
    graphState.translateY = 0;
    
    // Add zoom/pan handlers to container
    setupGraphPanZoom(container, svg);
    
    // Draw edges
    const statusColors = {
        completed: '#10b981',
        error: '#ef4444',
        running: '#3b82f6',
        pending: '#f59e0b'
    };
    
    graph.edges.forEach(e => {
        const f = graph.nodes.find(n => n.id === e.from);
        const t = graph.nodes.find(n => n.id === e.to);
        if (!f || !t) return;
        
        const color = e.color || statusColors[f.status] || '#64748b';
        const isParallel = e.label === 'parallel';
        const isSkipped = e.label === 'skipped';
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', f.x);
        line.setAttribute('y1', f.y);
        line.setAttribute('x2', t.x);
        line.setAttribute('y2', t.y);
        line.setAttribute('stroke', color);
        line.setAttribute('stroke-width', isParallel ? '1.5' : '2.5');
        if (isParallel || isSkipped) line.setAttribute('stroke-dasharray', '5,5');
        line.setAttribute('stroke-linecap', 'round');
        edgesG.appendChild(line);
    });
    
    // Draw nodes
    graph.nodes.forEach(nd => {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('transform', `translate(${nd.x},${nd.y})`);
        g.style.cursor = 'pointer';
        g.setAttribute('data-node-id', nd.id);
        
        g.addEventListener('mouseenter', (e) => showNodeTooltip(e, nd));
        g.addEventListener('mouseleave', hideNodeTooltip);
        g.addEventListener('click', () => selectNode(nd));
        
        const color = statusColors[nd.status] || '#64748b';
        const isParallel = nd.step_type === 'parallel';
        
        if (isParallel) {
            // Nodo especial para el bloque Parallel (Caja)
            g.innerHTML = `
                <rect x="-40" y="-30" width="80" height="60" rx="8" fill="#1e293b" stroke="${color}" stroke-width="3"/>
                <path d="M-15,-10 L15,-10 M-15,0 L15,0 M-15,10 L15,10" stroke="${color}" stroke-width="3" stroke-linecap="round"/>
                <rect x="-55" y="35" width="110" height="22" rx="5" fill="rgba(15,23,42,0.95)"/>
                <text y="51" text-anchor="middle" fill="#00f2fe" font-size="11" font-weight="bold">${nd.name.toUpperCase()}</text>
            `;
        } else if (nd.type === 'condition') {
            g.innerHTML = `
                <polygon points="0,-30 30,0 0,30 -30,0" fill="#8b5cf6" stroke="${color}" stroke-width="3"/>
                <text text-anchor="middle" dominant-baseline="central" fill="white" font-size="18" font-weight="bold">${nd.branch_taken === 'true' ? '✓' : '✗'}</text>
                <rect x="-50" y="35" width="100" height="20" rx="4" fill="rgba(15,23,42,0.9)"/>
                <text y="50" text-anchor="middle" fill="#fff" font-size="11">${nd.name.substring(0,12)}</text>
            `;
        } else {
            const icon = { completed: '✓', error: '✗', running: '▶', pending: '○' }[nd.status] || '○';
            g.innerHTML = `
                <circle r="28" fill="${color}" stroke="${color}" stroke-width="2"/>
                <text text-anchor="middle" dominant-baseline="central" fill="white" font-size="18" font-weight="bold">${icon}</text>
                <rect x="-55" y="35" width="110" height="22" rx="5" fill="rgba(15,23,42,0.95)"/>
                <text y="51" text-anchor="middle" fill="#e2e8f0" font-size="11">${nd.name.substring(0,14)}</text>
            `;
        }
        
        nodesG.appendChild(g);
    });
    
    document.getElementById('steps-section').style.display = 'block';
}

// ==================== GRAPH ZOOM/PAN ====================
function setupGraphPanZoom(container, svg) {
    if (!container) return;
    
    const contentGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    contentGroup.id = 'graph-content';
    
    // Move existing elements into content group
    const edgesG = document.getElementById('graph-edges');
    const nodesG = document.getElementById('graph-nodes');
    if (edgesG) contentGroup.appendChild(edgesG);
    if (nodesG) contentGroup.appendChild(nodesG);
    
    const svgEl = document.getElementById('graph-svg');
    if (svg) {
        // Re-append content group after defs
        const defs = svg.querySelector('defs');
        if (defs && contentGroup.parentNode !== svg) {
            svg.insertBefore(contentGroup, defs.nextSibling);
        }
    }
    
    // Mouse wheel zoom
    container.onwheel = function(e) {
        e.preventDefault();
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        graphState.scale = Math.max(0.3, Math.min(3, graphState.scale * delta));
        updateGraphTransform();
    };
    
    // Mouse drag pan
    container.onmousedown = function(e) {
        if (e.target.tagName === 'button') return;
        graphState.isDragging = true;
        graphState.startX = e.clientX - graphState.translateX;
        graphState.startY = e.clientY - graphState.translateY;
        container.style.cursor = 'grabbing';
    };
    
    container.onmousemove = function(e) {
        if (!graphState.isDragging) return;
        graphState.translateX = e.clientX - graphState.startX;
        graphState.translateY = e.clientY - graphState.startY;
        updateGraphTransform();
    };
    
    container.onmouseup = function() {
        graphState.isDragging = false;
        container.style.cursor = 'grab';
    };
    
    container.onmouseleave = function() {
        graphState.isDragging = false;
        container.style.cursor = 'grab';
    };
    
    container.style.cursor = 'grab';
}

function updateGraphTransform() {
    const content = document.getElementById('graph-content');
    if (content) {
        content.setAttribute('transform', `translate(${graphState.translateX}, ${graphState.translateY}) scale(${graphState.scale})`);
    }
}

window.graphZoomIn = function() {
    graphState.scale = Math.min(3, graphState.scale * 1.2);
    updateGraphTransform();
};

window.graphZoomOut = function() {
    graphState.scale = Math.max(0.3, graphState.scale / 1.2);
    updateGraphTransform();
};

window.graphReset = function() {
    graphState.scale = 1;
    graphState.translateX = 0;
    graphState.translateY = 0;
    updateGraphTransform();
};

window.graphFit = function() {
    const container = document.getElementById('graph-container');
    const svg = document.getElementById('graph-svg');
    if (!container || !svg) return;
    
    const containerRect = container.getBoundingClientRect();
    const svgW = parseFloat(svg.getAttribute('width')) || 1200;
    const svgH = parseFloat(svg.getAttribute('height')) || 500;
    
    const scaleX = (containerRect.width - 40) / svgW;
    const scaleY = (containerRect.height - 40) / svgH;
    graphState.scale = Math.min(scaleX, scaleY, 1);
    graphState.translateX = 0;
    graphState.translateY = 0;
    updateGraphTransform();
};

// ==================== NODE HOVER TOOLTIP ====================
function showNodeTooltip(e, node) {
    const tooltip = document.getElementById('tooltip');
    if (!tooltip) return;
    
    let content = `<strong>${node.name}</strong><br>`;
    content += `<span>Type: ${node.type || 'task'}</span><br>`;
    content += `<span>Status: <strong style="color: ${node.status === 'completed' ? '#10b981' : node.status === 'error' ? '#f43f5e' : node.status === 'running' ? '#3b82f6' : '#f59e0b'}">${node.status}</strong></span>`;
    
    if (node.duration_ms) {
        content += `<br><span>Duration: <strong>${fmtDuration(node.duration_ms)}</strong></span>`;
    }
    if (node.start_time) {
        content += `<br><span>Started: ${fmtTime(node.start_time)}</span>`;
    }
    if (node.end_time) {
        content += `<br><span>Ended: ${fmtTime(node.end_time)}</span>`;
    }
    
    // Show condition info if applicable
    if (node.type === 'condition') {
        content += `<br><span style="border-top: 1px solid rgba(148, 163, 184, 0.3); padding-top: 0.5rem; margin-top: 0.5rem;">`;
        content += `<strong>Condition:</strong><br>`;
        if (node.expression) {
            content += `${node.expression}<br>`;
        }
        if (node.branch_taken) {
            content += `<strong>Branch: ${node.branch_taken === 'true' ? '✓ TRUE' : '✗ FALSE'}</strong>`;
        }
        if (node.error_message) {
            content += `<br><span style="color: #f43f5e;"><strong>Error:</strong><br>${node.error_message}</span>`;
        }
        content += `</span>`;
    }
    
    // Show error message if present
    if (node.error_message && node.type !== 'condition') {
        content += `<br><span style="color: #f43f5e; border-top: 1px solid rgba(148, 163, 184, 0.3); padding-top: 0.5rem; margin-top: 0.5rem;"><strong>Error:</strong><br>${node.error_message}</span>`;
    }
    
    tooltip.innerHTML = content;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.pageX + 15) + 'px';
    tooltip.style.top = (e.pageY + 15) + 'px';
}

function hideNodeTooltip() {
    const tooltip = document.getElementById('tooltip');
    if (tooltip) tooltip.style.display = 'none';
}

function selectNode(node) {
    graphState.selectedNode = node;
    // Could expand step details here
    console.log('Selected node:', node);
}

// ==================== EXECUTION STEPS ====================
function renderSteps(pipeline) {
    const sec = document.getElementById('steps-section');
    const list = document.getElementById('steps-list');
    if (!pipeline.steps || !pipeline.steps.length) {
        sec.style.display = 'none';
        return;
    }
    
    sec.style.display = 'block';
    list.innerHTML = pipeline.steps.map((s, idx) => `
        <div class="step-card" onclick="toggleStepDetails(${idx})" style="cursor:pointer">
            <div class="step-header" style="display:flex;align-items:center;gap:0.75rem">
                <div class="step-icon ${escapeHtml(s.status)}">${getStepIcon(s.status)}</div>
                <div class="step-name" style="flex:1">${escapeHtml(s.step_name)}</div>
                <div class="step-meta">
                    ${s.duration_ms ? fmtDuration(s.duration_ms) : ''}
                    <i class="fas fa-chevron-down step-chevron" style="margin-left:0.5rem;font-size:0.7rem"></i>
                </div>
            </div>
            <div class="step-details" id="step-details-${idx}" style="display:none;margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid var(--border)">
                ${renderStepDetails(s)}
            </div>
        </div>
    `).join('');
}

function getStepIcon(status) {
    const icons = { completed: '✓', error: '✗', running: '▶', pending: '○', skipped: '⊘' };
    return icons[status] || '○';
}

function renderStepDetails(step) {
    let html = '';
    
    if (step.status) {
        html += `<div style="margin-bottom:0.5rem"><strong>Status:</strong> <span class="status-badge ${step.status}">${step.status}</span></div>`;
    }
    
    const startTime = step.started_at || step.start_time;
    const endTime = step.completed_at || step.end_time;
    if (startTime || endTime) {
        html += `<div style="margin-bottom:0.5rem;font-size:0.85rem;color:var(--text-muted)">`;
        if (startTime) html += `<div>Started: ${fmtTime(startTime)}</div>`;
        if (endTime) html += `<div>Ended: ${fmtTime(endTime)}</div>`;
        if (step.duration_ms) html += `<div>Duration: ${fmtDuration(step.duration_ms)}</div>`;
        html += `</div>`;
    }
    
    if (step.input_data) {
        html += `<div style="margin-bottom:0.5rem"><strong>Input:</strong></div>`;
        html += `<pre style="background:var(--bg-secondary);padding:0.5rem;border-radius:4px;font-size:0.8rem;overflow-x:auto">${formatJSON(step.input_data)}</pre>`;
    }
    
    if (step.output_data) {
        html += `<div style="margin-bottom:0.5rem;margin-top:0.5rem"><strong>Output:</strong></div>`;
        html += `<pre style="background:var(--bg-secondary);padding:0.5rem;border-radius:4px;font-size:0.8rem;overflow-x:auto">${formatJSON(step.output_data)}</pre>`;
    }
    
    if (step.error_message) {
        html += `<div style="margin-top:0.5rem"><strong>Error:</strong></div>`;
        html += `<pre style="background:rgba(239,68,68,0.1);padding:0.5rem;border-radius:4px;font-size:0.8rem;overflow-x:auto;color:#ef4444">${step.error_message}</pre>`;
    }
    
    return html || '<div style="color:var(--text-muted);font-size:0.85rem">No details available</div>';
}

function formatJSON(obj) {
    if (!obj) return '';
    if (typeof obj === 'string') {
        try { obj = JSON.parse(obj); } catch { return obj; }
    }
    try { return JSON.stringify(obj, null, 2); } catch { return String(obj); }
}

window.toggleStepDetails = function(idx) {
    const details = document.getElementById(`step-details-${idx}`);
    const chevron = document.querySelectorAll('.step-chevron')[idx];
    if (details) {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
        if (chevron) chevron.style.transform = details.style.display === 'block' ? 'rotate(180deg)' : '';
    }
};

window.toggleAllSteps = function() {
    const allDetails = document.querySelectorAll('[id^="step-details-"]');
    const allChevrons = document.querySelectorAll('.step-chevron');
    const isExpanded = allDetails[0]?.style.display === 'block';
    
    allDetails.forEach(d => d.style.display = isExpanded ? 'none' : 'block');
    allChevrons.forEach(c => c.style.transform = isExpanded ? '' : 'rotate(180deg)');
};

// ==================== UTILITIES ====================
function fmtDuration(ms) {
    if (!ms) return '0ms';
    if (ms < 1000) return Math.round(ms) + 'ms';
    if (ms < 60000) return (ms / 1000).toFixed(1) + 's';
    return (ms / 60000).toFixed(1) + 'm';
}

function fmtTime(ts) {
    if (!ts) return '';
    return new Date(ts).toLocaleTimeString();
}

function setupEventListeners() {
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
        });
    });
}

// ==================== TAB SWITCHING ====================
const pipelineTabs = ['graph', 'data'];

window.switchTab = function(tabName) {
    // Check if pipeline-specific tab requires selection
    if (pipelineTabs.includes(tabName) && !currentPipelineId) {
        const msg = currentLang === 'es' 
            ? 'Selecciona un pipeline de la lista derecha primero'
            : 'Select a pipeline from the right list first';
        alert(msg);
        return;
    }
    
    // Update all tabs (old layout)
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    const oldTab = document.querySelector(`.tab[data-tab="${tabName}"]`);
    if (oldTab) oldTab.classList.add('active');
    
    // Update new layout nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    const navBtn = document.querySelector(`.nav-btn[data-tab="${tabName}"]`);
    if (navBtn) navBtn.classList.add('active');
    
    // Update pipeline-specific tabs
    document.querySelectorAll('.pipeline-tabs .tab').forEach(t => t.classList.remove('active'));
    const pipelineTab = document.querySelector(`.pipeline-tabs .tab[data-tab="${tabName}"]`);
    if (pipelineTab) pipelineTab.classList.add('active');
    
    document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
    document.getElementById(`tab-${tabName}`).style.display = 'block';
    
    if (tabName === 'states') {
        loadStatesAnalysis();
    } else if (tabName === 'pipelines') {
        loadPipelinesAnalysis();
    } else if (tabName === 'analytics') {
        loadAnalytics();
    } else if (tabName === 'alerts') {
        loadAlerts();
    } else if (tabName === 'events') {
        loadEvents();
    } else if (tabName === 'data') {
        loadDataTable();
    } else if (tabName === 'timeline') {
        loadTimeline();
    }
};

// Scroll to nav button when switching tab
window.scrollToNav = function(tabName) {
    const navBtn = document.querySelector(`.nav-btn[data-tab="${tabName}"]`);
    if (navBtn) {
        navBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
    }
};

// ==================== STATES ANALYSIS ====================
async function loadStatesAnalysis() {
    try {
        const res = await fetch('/api/analysis/states');
        const data = await res.json();
        renderStatesAnalysis(data);
    } catch (e) {
        console.error('Error loading states analysis:', e);
    }
}

function renderStatesAnalysis(data) {
    const summary = document.getElementById('states-summary');
    if (!summary) return;
    
    summary.innerHTML = `
        <div class="stat-card blue">
            <div class="stat-value">${data.total_states || 0}</div>
            <div class="stat-label">Total States</div>
        </div>
        <div class="stat-card green">
            <div class="stat-value">${data.total_executions || 0}</div>
            <div class="stat-label">Total Executions</div>
        </div>
        <div class="stat-card rose">
            <div class="stat-value">${data.total_errors || 0}</div>
            <div class="stat-label">Total Errors</div>
        </div>
    `;
    
    renderTable('states-most-used', data.most_used || [], ['state_name', 'execution_count', 'avg_duration_ms']);
    renderTable('states-slowest', data.slowest || [], ['state_name', 'execution_count', 'avg_duration_ms']);
    renderTable('states-errors', data.most_errors || [], ['state_name', 'error_count', 'error_rate']);
}

// ==================== PIPELINES ANALYSIS ====================
async function loadPipelinesAnalysis() {
    try {
        const res = await fetch('/api/analysis/pipelines');
        const data = await res.json();
        renderPipelinesAnalysis(data);
    } catch (e) {
        console.error('Error loading pipelines analysis:', e);
    }
}

function renderPipelinesAnalysis(data) {
    const summary = document.getElementById('pipelines-summary');
    if (!summary) return;
    
    summary.innerHTML = `
        <div class="stat-card blue">
            <div class="stat-value">${data.total_pipelines || 0}</div>
            <div class="stat-label">Total Pipelines</div>
        </div>
        <div class="stat-card green">
            <div class="stat-value">${data.total_runs || 0}</div>
            <div class="stat-label">Total Runs</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-value">${data.avg_duration_ms ? fmtDuration(data.avg_duration_ms) : '0ms'}</div>
            <div class="stat-label">Avg Duration</div>
        </div>
        <div class="stat-card rose">
            <div class="stat-value">${data.total_errors || 0}</div>
            <div class="stat-label">Total Errors</div>
        </div>
    `;
    
    renderTable('pipelines-slowest', data.slowest || [], ['name', 'execution_count', 'avg_duration_ms']);
    renderTable('pipelines-errors', data.most_errors || [], ['name', 'error_count', 'error_rate']);
    renderTable('pipelines-recent', data.recent || [], ['name', 'status', 'created_at', 'total_duration_ms']);
}

function renderTable(containerId, rows, columns) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (!rows || rows.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted);font-size:0.85rem">No data</p>';
        return;
    }
    
    const labels = { 
        state_name: 'State', 
        name: 'Pipeline',
        execution_count: 'Runs', 
        avg_duration_ms: 'Avg Duration', 
        error_count: 'Errors', 
        error_rate: 'Error Rate',
        status: 'Status',
        created_at: 'Created',
        total_duration_ms: 'Duration'
    };
    
    container.innerHTML = `
        <table class="data-table">
            <thead><tr>${columns.map(c => `<th>${labels[c] || c}</th>`).join('')}</tr></thead>
            <tbody>
                ${rows.slice(0, 10).map(row => `
                    <tr>
                        ${columns.map(c => {
                            let val = row[c];
                            if (c.includes('duration') || c === 'total_duration_ms') val = fmtDuration(val);
                            else if (c === 'error_rate') val = val ? (val*100).toFixed(1)+'%' : '0%';
                            else if (c === 'created_at') val = fmtTime(val);
                            else if (c === 'status') val = `<span class="status-badge ${val}">${val}</span>`;
                            return `<td>${val !== undefined ? val : ''}</td>`;
                        }).join('')}
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// ==================== ANALYTICS ====================
let analyticsChart = null;
async function loadAnalytics() {
    try {
        const [statsRes, trendsRes, slowRes] = await Promise.all([
            fetch('/api/stats'),
            fetch('/api/trends'),
            fetch('/api/slow-steps')
        ]);
        
        const stats = await statsRes.json();
        const trends = await trendsRes.json();
        const slowSteps = await slowRes.json();
        
        renderAnalyticsCharts(stats, trends);
        renderSlowSteps(slowSteps);
        renderPipelineAnalysis(stats);
    } catch (e) {
        console.error('Error loading analytics:', e);
    }
}

function renderAnalyticsCharts(stats, trends) {
    const ctx = document.getElementById('pie-chart');
    if (!ctx) return;
    
    if (analyticsChart) analyticsChart.destroy();
    
    const data = {
        labels: ['Completed', 'Running', 'Error', 'Pending'],
        datasets: [{
            data: [
                stats.completed || 0,
                stats.running || 0,
                stats.error || 0,
                stats.pending || 0
            ],
            backgroundColor: ['#10b981', '#3b82f6', '#ef4444', '#f59e0b']
        }]
    };
    
    analyticsChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function renderSlowSteps(steps) {
    const container = document.getElementById('slow-steps-list');
    if (!container) return;
    
    if (!steps || steps.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted)">No data</p>';
        return;
    }
    
    container.innerHTML = steps.slice(0, 5).map(s => `
        <div style="display:flex;justify-content:space-between;padding:0.5rem;border-bottom:1px solid var(--border)">
            <span>${escapeHtml(s.step_name)}</span>
            <span style="color:var(--text-muted)">${fmtDuration(s.avg_duration)}</span>
        </div>
    `).join('');
}

function renderPipelineAnalysis(stats) {
    const container = document.getElementById('pipeline-analysis');
    if (!container) return;
    
    container.innerHTML = `
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem">
            <div class="stat-card blue">
                <div class="stat-value">${stats.total || 0}</div>
                <div class="stat-label">Total Pipelines</div>
            </div>
            <div class="stat-card green">
                <div class="stat-value">${stats.completed || 0}</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat-card purple">
                <div class="stat-value">${stats.avg_duration ? fmtDuration(stats.avg_duration) : '0ms'}</div>
                <div class="stat-label">Avg Duration</div>
            </div>
            <div class="stat-card rose">
                <div class="stat-value">${stats.error || 0}</div>
                <div class="stat-label">Errors</div>
            </div>
        </div>
    `;
}

// ==================== ALERTS ====================
let currentAlerts = [];
async function loadAlerts() {
    try {
        const res = await fetch('/api/alerts');
        const alerts = await res.json();
        currentAlerts = alerts;
        renderAlerts(alerts);
    } catch (e) {
        console.error('Error loading alerts:', e);
    }
}

function renderAlerts(alerts) {
    const container = document.getElementById('alerts-list');
    if (!container) return;
    
    if (!alerts || alerts.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No alerts</p></div>';
        return;
    }
    
    container.innerHTML = alerts.map(a => `
        <div class="alert-card ${a.severity}" style="margin-bottom:0.75rem;padding:1rem;border-radius:8px;background:var(--bg-secondary);border-left:4px solid ${a.severity === 'critical' ? '#ef4444' : '#f59e0b'}">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <strong>${a.alert_name}</strong>
                    <div style="font-size:0.85rem;color:var(--text-muted)">${a.message}</div>
                </div>
                <span class="badge ${a.severity}">${a.severity}</span>
            </div>
            <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.5rem">
                ${fmtTime(a.created_at)}
                ${a.pipeline_id ? ` • Pipeline: ${a.pipeline_id}` : ''}
            </div>
        </div>
    `).join('');
}

window.filterAlerts = function(severity) {
    document.querySelectorAll('#tab-alerts .chip').forEach(c => c.classList.remove('active'));
    event.target.classList.add('active');
    const filtered = severity ? currentAlerts.filter(a => a.severity === severity) : currentAlerts;
    renderAlerts(filtered);
};

// ==================== EVENTS ====================
async function loadEvents() {
    try {
        const res = await fetch('/api/events');
        const events = await res.json();
        renderEvents(events);
    } catch (e) {
        console.error('Error loading events:', e);
    }
}

function renderEvents(events) {
    const container = document.getElementById('events-list');
    if (!container) return;
    
    if (!events || events.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No events</p></div>';
        return;
    }
    
    container.innerHTML = events.slice(0, 50).map(e => `
        <div class="event-item" style="display:flex;gap:1rem;padding:0.75rem;border-bottom:1px solid var(--border)">
            <div style="color:var(--text-muted);font-size:0.8rem;min-width:80px">${fmtTime(e.created_at)}</div>
            <div>
                <span class="event-type" style="background:var(--bg-tertiary);padding:2px 8px;border-radius:4px;font-size:0.75rem">${e.event_type}</span>
                <span>${e.pipeline_id || e.step_id || ''}</span>
            </div>
        </div>
    `).join('');
}

// ==================== DATA ====================
let dataPage = 1;
let dataTotal = 0;
async function loadDataTable() {
    const table = document.getElementById('data-table-select')?.value || 'pipelines';
    const search = document.getElementById('data-search')?.value || '';
    const status = document.getElementById('data-status-filter')?.value || '';
    
    try {
        const res = await fetch(`/api/data/${table}?page=${dataPage}&page_size=20&search=${search}&status=${status}`);
        const data = await res.json();
        renderDataTable(data, table);
    } catch (e) {
        console.error('Error loading data:', e);
    }
}

function renderDataTable(data, table) {
    const thead = document.getElementById('data-thead');
    const tbody = document.getElementById('data-tbody');
    if (!thead || !tbody) return;
    
    const items = data.items || data.data || [];
    if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;color:var(--text-muted)">No data</td></tr>';
        return;
    }
    
    const columns = Object.keys(items[0]);
    thead.innerHTML = `<tr>${columns.map(c => `<th>${c}</th>`).join('')}</tr>`;
    
    tbody.innerHTML = items.map(row => `
        <tr>${columns.map(c => `<td>${row[c] !== null ? row[c] : ''}</td>`).join('')}</tr>
    `).join('');
    
    dataTotal = data.total || 0;
    if (data.total_pages) {
        dataPage = data.page || 1;
    }
    updateDataPagination();
}

function updateDataPagination() {
    const info = document.getElementById('data-pagination-info');
    const prev = document.getElementById('data-btn-prev');
    const next = document.getElementById('data-btn-next');
    
    if (info) info.textContent = `Page ${dataPage} of ${Math.ceil(dataTotal / 20)} (${dataTotal} total)`;
    if (prev) prev.disabled = dataPage <= 1;
    if (next) next.disabled = dataPage >= Math.ceil(dataTotal / 20);
}

window.dataPrevPage = function() {
    if (dataPage > 1) { dataPage--; loadDataTable(); }
};
window.dataNextPage = function() {
    dataPage++; loadDataTable();
};

// ==================== TIMELINE ====================
let timelineChart = null;
async function loadTimeline() {
    const days = document.getElementById('timeline-filter')?.value || 7;
    
    try {
        const res = await fetch(`/api/trends?days=${days}`);
        const data = await res.json();
        renderTimelineChart(data);
    } catch (e) {
        console.error('Error loading timeline:', e);
    }
}

function renderTimelineChart(data) {
    const ctx = document.getElementById('timeline-chart');
    if (!ctx) return;
    
    if (timelineChart) timelineChart.destroy();
    
    const labels = data.map(d => d.date || d.day);
    const completed = data.map(d => d.completed || 0);
    const errors = data.map(d => d.errors || 0);
    
    timelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                { label: 'Completed', data: completed, borderColor: '#10b981', tension: 0.3 },
                { label: 'Errors', data: errors, borderColor: '#ef4444', tension: 0.3 }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
