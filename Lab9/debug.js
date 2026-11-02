const NODES = [1, 2, 3, 4, 5, 6, 7];
const POS = {
    1: [110, 110],
    2: [300, 110],
    3: [340, 255],
    4: [110, 275],
    5: [235, 380],
    6: [475, 110],
    7: [475, 300]
};
const R = 24;
const EDGES = [[1,2],[2,3],[3,4],[4,1],[3,5],[5,4],[2,6],[7,3],[7,6]];

const PHASE_LABEL = {
    init: 'เริ่มต้น',
    read: 'อ่าน input',
    build: 'สร้าง adj / rev_adj',
    dfs1: 'DFS รอบ 1',
    reset: 'รีเซ็ต visited',
    dfs2: 'DFS รอบ 2 (หา SCC)',
    done: 'เสร็จสิ้น'
};

function blankVisited() {
    return Array(NODES.length + 1).fill(false);
}

const state = {
    n: 0, m: 0,
    adj: {}, revAdj: {},
    visited: blankVisited(),
    order: [],
    stack: [],
    current: null,
    edge: null,
    phase: 'init',
    root: null,
    scc: [],
    sccSize: 0,
    maxScc: 0,
    result: null
};

let steps = [];
function step(line, desc) {
    steps.push({ line, desc, s: JSON.parse(JSON.stringify(state)) });
}

function dfs1(u) {
    state.stack.push(u);
    state.current = u;
    state.phase = 'dfs1';
    step(38, `เรียก dfs1(${u})`);
    state.visited[u] = true;
    step(39, `visited[${u}] = true`);
    for (const v of state.adj[u]) {
        if (!state.visited[v]) {
            state.edge = { u, v };
            step(42, `จาก dfs1(${u}) → เรียก dfs1(${v})`);
            dfs1(v);
            state.edge = null;
            state.current = u;
            step(42, `กลับจาก dfs1(${v}) > กลับมาทำงานต่อที่ dfs1(${u})`);
        } else {
            state.edge = { u, v };
            step(41, `ตรวจเพื่อนบ้าน ${v}: เยี่ยมชมไปแล้ว > ข้าม`);
            state.edge = null;
        }
    }
    state.order.push(u);
    step(43, `dfs1(${u}) ทำงานเสร็จ > order.push(${u}) ตอนนี้ order = [${state.order.join(', ')}]`);
    state.stack.pop();
    state.current = state.stack[state.stack.length - 1] || null;
    step(43, `return จาก dfs1(${u})`);
}

function dfs2(u) {
    state.stack.push(u);
    state.current = u;
    step(54, `เรียก dfs2(${u})`);
    state.visited[u] = true;
    state.sccSize += 1;
    if (!state.scc.includes(u)) state.scc.push(u);
    step(56, `visited[${u}] = true > นับเพิ่ม 1 > ขนาด SCC ของ ${u} ตอนนี้ = ${state.sccSize} กลุ่มที่พบ {${state.scc.join(', ')}}`);
    for (const v of state.revAdj[u]) {
        if (!state.visited[v]) {
            state.edge = { u, v };
            step(58, `จาก dfs2(${u}) (กราฟกลับทิศ) > เรียก dfs2(${v})`);
            dfs2(v);
            state.edge = null;
            state.current = u;
            step(58, `กลับจาก dfs2(${v}) > รวมเป็น SCC เดียวกัน ขนาดรวมของ ${u} = ${state.sccSize}`);
        } else {
            state.edge = { u, v };
            step(58, `ตรวจ ${v} บนกราฟกลับทิศ: เป็นสมาชิกกลุ่มเดียวกันแล้ว > ข้าม`);
            state.edge = null;
        }
    }
    state.stack.pop();
    state.current = state.stack[state.stack.length - 1] || null;
    step(60, `return จาก dfs2(${u})`);
}

function buildSteps() {
    step(6, 'เข้าสู่ฟังก์ชัน solve() > กำลังจะอ่านไฟล์ testcase.txt');
    state.phase = 'read';
    step(9, 'อ่านไฟล์ Lab9/testcase.txt สำเร็จ > แยกเนื้อหาออกเป็นคำ');
    state.n = 7;
    step(18, 'n = int(input_data[0]) > n = 7 : จำนวนเกาะ');
    state.m = 9;
    step(19, 'm = int(input_data[1]) > m = 9 : จำนวนถนน');
    state.phase = 'build';
    for (const i of NODES) {
        state.adj[i] = [];
        state.revAdj[i] = [];
    }
    step(22, 'สร้าง adj > ทุกเกาะ 1..7 มี list ว่างรอรับถนนที่ออกจากเกาะนั้น');
    step(23, 'สร้าง rev_adj > ทุกเกาะมี list ว่างรอรับถนนที่เข้าสู่เกาะนั้น (ใช้กับ DFS รอบที่ 2)');
    for (const [u, v] of EDGES) {
        state.edge = { u, v };
        state.adj[u].push(v);
        step(30, `อ่านถนน ${u} > ${v} : เพิ่ม adj[${u}] = [${state.adj[u].join(', ')}]`);
        state.revAdj[v].push(u);
        step(31, `อัปเดตกราฟกลับทิศพร้อมกัน > rev_adj[${v}] = [${state.revAdj[v].join(', ')}]`);
    }
    state.edge = null;
    state.visited = blankVisited();
    step(34, 'visited = [False] * 8 > ยังไม่มีเกาะไหนถูกเยี่ยมชม');
    state.order = [];
    step(35, 'order = [] > เตรียมเก็บลำดับ DFS ที่ทำงานเสร็จ (finishing time)');

    for (let i = 1; i <= state.n; i++) {
        step(46, `วนตรวจเกาะ i = ${i}`);
        if (!state.visited[i]) {
            step(48, `เกาะ ${i} ยังไม่ถูกเยี่ยมชม > เริ่ม DFS จากเกาะ ${i}`);
            dfs1(i);
        } else {
            step(47, `เกาะ ${i} เยี่ยมชมไปแล้ว > ข้าม`);
        }
    }

    state.phase = 'reset';
    state.current = null;
    state.stack = [];
    state.edge = null;
    state.visited = blankVisited();
    step(51, 'รีเซ็ต visited กลับเป็น False ทั้งหมด เพื่อเตรียม DFS รอบที่ 2 (order ยังเก็บไว้)');
    state.maxScc = 0;
    step(62, 'max_scc_size = 0');

    state.phase = 'dfs2';
    for (let i = state.n - 1; i >= 0; i--) {
        const u = state.order[i];
        step(65, `วน order จากท้ายมาหน้า : i = ${i} > เกาะ u = ${u}`);
        if (!state.visited[u]) {
            state.root = u;
            state.sccSize = 0;
            state.scc = [];
            state.stack = [];
            step(69, `เกาะ ${u} ยังไม่ถูกจับใน SCC ใด > เริ่ม SCC กลุ่มใหม่ เรียก dfs2(${u})`);
            dfs2(u);
            const size = state.sccSize;
            step(70, `dfs2(${u}) จบ > SCC กลุ่มนี้คือ {${state.scc.join(', ')}} ขนาด = ${size}`);
            if (size > state.maxScc) {
                const prev = state.maxScc;
                state.maxScc = size;
                step(71, `ขนาด ${size} มากกว่าค่าเดิม ${prev} > max_scc_size = ${size}`);
            }
        } else {
            step(67, `เกาะ ${u} เป็นสมาชิกของ SCC ที่ค้นไปแล้ว > ข้าม`);
        }
    }

    state.phase = 'done';
    state.result = state.maxScc;
    step(74, `พิมพ์คำตอบ : "จำนวนเกาะสูงสุดที่เดินทางผ่านได้ : ${state.maxScc}"`);
}

buildSteps();

let idx = 0;
let timer = null;

const $ = (id) => document.getElementById(id);

function buildCodePanel() {
    const src = $('codeSrc').textContent.replace(/^\n/, '').split('\n');
    const wrap = $('codeLines');
    wrap.innerHTML = '';
    src.forEach((text, i) => {
        const div = document.createElement('div');
        div.className = 'code-line';
        div.id = `code-${i + 1}`;
        const ln = document.createElement('span');
        ln.className = 'ln';
        ln.textContent = i + 1;
        const lc = document.createElement('span');
        lc.className = 'lc';
        lc.textContent = text || ' ';
        div.appendChild(ln);
        div.appendChild(lc);
        wrap.appendChild(div);
    });
}

function buildGraph() {
    const svg = $('graph');
    svg.innerHTML = '';
    svg.setAttribute('viewBox', '0 0 560 440');

    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    defs.innerHTML =
        '<marker id="arrowGray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/></marker>' +
        '<marker id="arrowOrange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f97316"/></marker>';
    svg.appendChild(defs);

    for (const [u, v] of EDGES) {
        const [x1, y1] = POS[u];
        const [x2, y2] = POS[v];
        const dx = x2 - x1;
        const dy = y2 - y1;
        const len = Math.hypot(dx, dy);
        const sx = x1 + dx / len * (R + 2);
        const sy = y1 + dy / len * (R + 2);
        const ex = x2 - dx / len * (R + 4);
        const ey = y2 - dy / len * (R + 4);
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', sx);
        line.setAttribute('y1', sy);
        line.setAttribute('x2', ex);
        line.setAttribute('y2', ey);
        line.setAttribute('class', 'g-edge');
        line.setAttribute('marker-end', 'url(#arrowGray)');
        line.dataset.u = u;
        line.dataset.v = v;
        svg.appendChild(line);
    }

    for (const n of NODES) {
        const [x, y] = POS[n];
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'g-node');
        g.dataset.n = n;
        const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('cx', x);
        c.setAttribute('cy', y);
        c.setAttribute('r', R);
        const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        t.setAttribute('x', x);
        t.setAttribute('y', y);
        t.textContent = n;
        g.appendChild(c);
        g.appendChild(t);
        svg.appendChild(g);
    }
}

function renderList(el, obj, edge, keyOfEdge) {
    el.innerHTML = '';
    for (const k of NODES) {
        const row = document.createElement('div');
        row.className = 'adj-row';
        const isHl = edge && Number(k) === keyOfEdge(edge);
        if (isHl) row.classList.add('hl');
        const key = document.createElement('span');
        key.className = 'key';
        key.textContent = k + ' :';
        const val = document.createElement('span');
        val.className = 'val';
        val.textContent = `[ ${obj[k].join(', ')} ]`;
        row.appendChild(key);
        row.appendChild(val);
        el.appendChild(row);
    }
}

function renderChips(el, items, opts) {
    el.innerHTML = '';
    if (!items.length) {
        el.innerHTML = '<span class="empty">ยังว่าง</span>';
        return;
    }
    for (const it of items) {
        const chip = document.createElement('span');
        chip.className = 'chip ' + (it.cls || 'on');
        chip.textContent = it.text;
        el.appendChild(chip);
    }
}

function show(i) {
    idx = i;
    const st = steps[i].s;

    document.querySelectorAll('.code-line').forEach((el) => el.classList.remove('current'));
    const lineEl = $(`code-${steps[i].line}`);
    if (lineEl) {
        lineEl.classList.add('current');
        lineEl.scrollIntoView({ block: 'nearest', behavior: 'auto' });
    }

    $('stepDesc').textContent = `${steps[i].line ? 'บรรทัด ' + steps[i].line + ' — ' : ''}${steps[i].desc}`;
    $('stepCount').textContent = `สเต็ป ${i + 1} / ${steps.length}`;

    $('btnPrev').disabled = i === 0;
    $('btnNext').disabled = i === steps.length - 1;

    const phase = st.phase;
    const badge = $('phaseBadge');
    badge.textContent = PHASE_LABEL[phase] || phase;
    badge.className = 'phase-badge ' + (['dfs1', 'dfs2', 'done'].includes(phase) ? phase : '');

    $('varN').textContent = st.n || '-';
    $('varM').textContent = st.m || '-';
    $('varRoot').textContent = st.root ?? '-';
    $('varSize').textContent = phase === 'dfs2' ? st.sccSize : '-';
    $('varMax').textContent = st.maxScc;

    renderList($('adjList'), st.adj, st.edge, (e) => e.u);
    renderList($('revList'), st.revAdj, st.edge, (e) => e.v);

    const vr = $('visitedRow');
    vr.innerHTML = '';
    for (const n of NODES) {
        const chip = document.createElement('span');
        chip.className = 'chip' + (st.visited[n] ? ' on' : '');
        if (st.current === n) chip.classList.add('pop');
        chip.textContent = n;
        vr.appendChild(chip);
    }

    const or = $('orderRow');
    or.innerHTML = '';
    if (!st.order.length) {
        or.innerHTML = '<span class="empty">ยังว่าง</span>';
    } else {
        st.order.forEach((n, k) => {
            const chip = document.createElement('span');
            chip.className = 'chip on';
            chip.textContent = k + 1 + '.' + n;
            or.appendChild(chip);
        });
    }

    const sr = $('stackRow');
    sr.innerHTML = '';
    if (!st.stack.length) {
        sr.innerHTML = '<span class="empty">ว่าง</span>';
    } else {
        st.stack.forEach((n, k) => {
            const chip = document.createElement('span');
            chip.className = 'chip';
            const isTop = k === st.stack.length - 1;
            if (isTop) chip.classList.add(isTop && phase === 'dfs2' && st.scc.includes(n) ? 'scc' : 'on');
            else if (phase === 'dfs2') chip.classList.add('scc');
            chip.textContent = n;
            sr.appendChild(chip);
        });
    }

    document.querySelectorAll('#graph .g-edge').forEach((el) => {
        const active = st.edge && +el.dataset.u === st.edge.u && +el.dataset.v === st.edge.v;
        el.classList.toggle('active', !!active);
        el.setAttribute('marker-end', active ? 'url(#arrowOrange)' : 'url(#arrowGray)');
    });

    document.querySelectorAll('#graph .g-node').forEach((el) => {
        const n = +el.dataset.n;
        let cls = 'g-node';
        if (st.visited[n]) cls += phase === 'dfs2' ? ' visited2' : ' visited1';
        if (phase === 'dfs2' && st.visited[n]) cls += ' visited2';
        if (st.current === n) cls += ' current';
        el.setAttribute('class', cls);
    });

    const rb = $('resultBox');
    if (st.result !== null) {
        rb.classList.remove('hidden');
        $('resultVal').textContent = st.result;
    } else {
        rb.classList.add('hidden');
    }
}

function stopPlay() {
    if (timer) {
        clearInterval(timer);
        timer = null;
        $('btnPlay').textContent = '▶ เล่นอัตโนมัติ';
    }
}

$('btnNext').addEventListener('click', () => {
    stopPlay();
    if (idx < steps.length - 1) show(idx + 1);
});
$('btnPrev').addEventListener('click', () => {
    stopPlay();
    if (idx > 0) show(idx - 1);
});
$('btnReset').addEventListener('click', () => {
    stopPlay();
    show(0);
});
$('btnPlay').addEventListener('click', () => {
    if (timer) {
        stopPlay();
    } else {
        $('btnPlay').textContent = '⏸ หยุด';
        if (idx >= steps.length - 1) show(0);
        timer = setInterval(() => {
            if (idx < steps.length - 1) {
                show(idx + 1);
            } else {
                stopPlay();
            }
        }, 650);
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
        stopPlay();
        if (idx < steps.length - 1) show(idx + 1);
    } else if (e.key === 'ArrowLeft') {
        stopPlay();
        if (idx > 0) show(idx - 1);
    }
});

buildCodePanel();
buildGraph();
show(0);
