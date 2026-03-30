// Dashboard JavaScript

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

// ==================== INITIALIZATION ====================
function init() {
    loadPipelines();
    setupEventListeners();
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
    const list = document.getElementById('pipeline-list');
    if (!pipelines || pipelines.length === 0) {
        list.innerHTML = '<div class="empty-state"><p>No pipelines</p></div>';
        return;
    }
    
    list.innerHTML = pipelines.map(p => `
        <div class="pipeline-item" onclick="selectPipeline('${p.id}')">
            <div class="pipeline-status ${p.status}"></div>
            <div class="pipeline-info">
                <div class="pipeline-name">${p.name || p.id}</div>
                <div class="pipeline-meta">
                    <span>${p.status}</span>
                    ${p.total_duration_ms ? '<span>' + fmtDuration(p.total_duration_ms) + '</span>' : ''}
                </div>
            </div>
        </div>
    `).join('');
}

async function selectPipeline(id) {
    try {
        const res = await fetch('/api/pipelines/' + id + '/graph');
        const graph = await res.json();
        graphState.currentGraph = graph;
        renderGraph(graph);
        
        const pRes = await fetch('/api/pipelines/' + id);
        const pipeline = await pRes.json();
        renderSteps(pipeline);
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
    
    if (!graph.nodes || graph.nodes.length === 0) {
        svg.style.display = 'none';
        empty.style.display = 'block';
        return;
    }
    
    svg.style.display = 'block';
    empty.style.display = 'none';
    edgesG.innerHTML = '';
    nodesG.innerHTML = '';
    
    // Layout: horizontal line
    const svgW = 1200;
    const svgH = 500;
    const spacing = 150;
    const centerY = svgH / 2;
    
    svg.setAttribute('width', svgW);
    svg.setAttribute('height', svgH);
    
    // Position nodes
    graph.nodes.forEach((nd, idx) => {
        nd.x = 80 + idx * spacing;
        nd.y = centerY;
    });
    
    // Draw edges first (so they appear behind nodes)
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
        
        const color = statusColors[f.status] || '#64748b';
        
        edgesG.innerHTML += `
            <line x1="${f.x}" y1="${f.y}" x2="${t.x}" y2="${t.y}"
                  stroke="${color}" stroke-width="2" stroke-linecap="round"/>
        `;
    });
    
    // Draw nodes with hover
    graph.nodes.forEach(nd => {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('transform', `translate(${nd.x},${nd.y})`);
        g.style.cursor = 'pointer';
        g.setAttribute('data-node-id', nd.id);
        
        // Mouse events for hover
        g.addEventListener('mouseenter', (e) => showNodeTooltip(e, nd));
        g.addEventListener('mouseleave', hideNodeTooltip);
        g.addEventListener('click', () => selectNode(nd));
        
        const color = statusColors[nd.status] || '#64748b';
        
        if (nd.type === 'condition') {
            g.innerHTML = `
                <polygon points="0,-30 30,0 0,30 -30,0" fill="#8b5cf6" stroke="${color}" stroke-width="3"/>
                <text text-anchor="middle" dominant-baseline="central" fill="white" font-size="18" font-weight="bold">${nd.branch_taken === 'true' ? '✓' : '✗'}</text>
                <rect x="-50" y="35" width="100" height="20" rx="4" fill="rgba(15,23,42,0.9)"/>
                <text y="50" text-anchor="middle" fill="#fff" font-size="11">${nd.name.substring(0,12)}</text>
            `;
        } else if (nd.type === 'skipped') {
            g.innerHTML = `
                <circle r="25" fill="#374151" stroke="#4b5563" stroke-width="2" stroke-dasharray="4,2"/>
                <text text-anchor="middle" dominant-baseline="central" fill="#9ca3af" font-size="16">⊘</text>
                <rect x="-45" y="30" width="90" height="18" rx="4" fill="rgba(30,41,59,0.9)"/>
                <text y="43" text-anchor="middle" fill="#9ca3af" font-size="10">${nd.name.substring(0,10)}</text>
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

// ==================== NODE HOVER TOOLTIP ====================
function showNodeTooltip(e, node) {
    const tooltip = document.getElementById('tooltip');
    if (!tooltip) return;
    
    let content = `<strong>${node.name}</strong><br>`;
    content += `<span>Type: ${node.type || 'task'}</span><br>`;
    content += `<span>Status: ${node.status}</span>`;
    
    if (node.duration_ms) {
        content += `<br><span>Duration: ${fmtDuration(node.duration_ms)}</span>`;
    }
    if (node.start_time) {
        content += `<br><span>Started: ${fmtTime(node.start_time)}</span>`;
    }
    if (node.end_time) {
        content += `<br><span>Ended: ${fmtTime(node.end_time)}</span>`;
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
                <div class="step-icon ${s.status}">${getStepIcon(s.status)}</div>
                <div class="step-name" style="flex:1">${s.step_name}</div>
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
    
    if (step.start_time || step.end_time) {
        html += `<div style="margin-bottom:0.5rem;font-size:0.85rem;color:var(--text-muted)">`;
        if (step.start_time) html += `<div>Started: ${fmtTime(step.start_time)}</div>`;
        if (step.end_time) html += `<div>Ended: ${fmtTime(step.end_time)}</div>`;
        html += `</div>`;
    }
    
    if (step.input) {
        html += `<div style="margin-bottom:0.5rem"><strong>Input:</strong></div>`;
        html += `<pre style="background:var(--bg-secondary);padding:0.5rem;border-radius:4px;font-size:0.8rem;overflow-x:auto">${formatJSON(step.input)}</pre>`;
    }
    
    if (step.output) {
        html += `<div style="margin-bottom:0.5rem;margin-top:0.5rem"><strong>Output:</strong></div>`;
        html += `<pre style="background:var(--bg-secondary);padding:0.5rem;border-radius:4px;font-size:0.8rem;overflow-x:auto">${formatJSON(step.output)}</pre>`;
    }
    
    if (step.error) {
        html += `<div style="margin-top:0.5rem"><strong>Error:</strong></div>`;
        html += `<pre style="background:rgba(239,68,68,0.1);padding:0.5rem;border-radius:4px;font-size:0.8rem;overflow-x:auto;color:#ef4444">${step.error}</pre>`;
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

function toggleStepDetails(idx) {
    const details = document.getElementById(`step-details-${idx}`);
    const chevron = document.querySelectorAll('.step-chevron')[idx];
    if (details) {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
        if (chevron) chevron.style.transform = details.style.display === 'block' ? 'rotate(180deg)' : '';
    }
}

function toggleAllSteps() {
    const allDetails = document.querySelectorAll('[id^="step-details-"]');
    const allChevrons = document.querySelectorAll('.step-chevron');
    const isExpanded = allDetails[0]?.style.display === 'block';
    
    allDetails.forEach(d => d.style.display = isExpanded ? 'none' : 'block');
    allChevrons.forEach(c => c.style.transform = isExpanded ? '' : 'rotate(180deg)');
}

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
window.switchTab = function(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');
    
    document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
    document.getElementById(`tab-${tabName}`).style.display = 'block';
    
    if (tabName === 'states') {
        loadStatesAnalysis();
    } else if (tabName === 'pipelines') {
        loadPipelinesAnalysis();
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

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
