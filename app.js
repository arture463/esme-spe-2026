/**
 * ESME Spé (S03) Course Portal - Application Logic
 */

// Helper to sanitize and fix any double-encoded UTF-8 strings
function cleanText(str) {
  if (!str) return '';
  return str
    .replace(/Ã©/g, 'é')
    .replace(/Ã¨/g, 'è')
    .replace(/Ãª/g, 'ê')
    .replace(/Ã«/g, 'ë')
    .replace(/Ã /g, 'à')
    .replace(/Ã¢/g, 'â')
    .replace(/Ã´/g, 'ô')
    .replace(/Ã®/g, 'î')
    .replace(/Ã¯/g, 'ï')
    .replace(/Ã¹/g, 'ù')
    .replace(/Ã»/g, 'û')
    .replace(/Ã§/g, 'ç')
    .replace(/Ã‰/g, 'É')
    .replace(/Ãˆ/g, 'È')
    .replace(/Ã€/g, 'À')
    .replace(/Ã‡/g, 'Ç')
    .replace(/Ã/g, 'à')
    .trim();
}

// Application State
const state = {
  data: null,
  activeSubject: null, // null means all
  activeType: 'all',   // 'all', 'Cours', 'TD', 'TD & Corrigé', 'Examen', 'TP', 'Projet'
  activeOrigin: 'all', // 'all', 'Paris', 'National'
  searchQuery: '',
  sortBy: 'default'
};

// Color palettes for UEs
const UE_CONFIG = {
  "UE1": {
    name: "UE1 : Mathématiques & Signal",
    desc: "Analyse numérique, maths fondamentales, outils maths, signaux & systèmes",
    border: "border-indigo-500",
    badge: "bg-indigo-100 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800"
  },
  "UE2": {
    name: "UE2 : Sciences de l'Ingénieur & Environnement",
    desc: "Systèmes technologiques, mécanique des fluides, gestion de projet, environnement",
    border: "border-emerald-500",
    badge: "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800"
  },
  "UE3": {
    name: "UE3 : Numérique, Électronique & Langues",
    desc: "Algorithmique avancée 2, électronique analogique 1, anglais professionnel",
    border: "border-violet-500",
    badge: "bg-violet-100 text-violet-700 dark:bg-violet-950 dark:text-violet-300 border-violet-200 dark:border-violet-800"
  },
  "UE4": {
    name: "UE4 : Entreprise & Management",
    desc: "Gestion d'entreprise 1, comptabilité, finance, économie",
    border: "border-fuchsia-500",
    badge: "bg-fuchsia-100 text-fuchsia-700 dark:bg-fuchsia-950 dark:text-fuchsia-300 border-fuchsia-200 dark:border-fuchsia-800"
  }
};

// Document type badges & icons
const TYPE_STYLES = {
  "Cours": {
    badge: "bg-blue-100 text-blue-800 dark:bg-blue-950/70 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60",
    icon: "book-open"
  },
  "TD": {
    badge: "bg-amber-100 text-amber-800 dark:bg-amber-950/70 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60",
    icon: "file-edit"
  },
  "TD & Corrigé": {
    badge: "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/70 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60",
    icon: "check-circle-2"
  },
  "Examen": {
    badge: "bg-rose-100 text-rose-800 dark:bg-rose-950/70 dark:text-rose-300 border border-rose-200 dark:border-rose-800/60 font-semibold",
    icon: "award"
  },
  "TP": {
    badge: "bg-purple-100 text-purple-800 dark:bg-purple-950/70 dark:text-purple-300 border border-purple-200 dark:border-purple-800/60",
    icon: "laptop"
  },
  "Projet": {
    badge: "bg-cyan-100 text-cyan-800 dark:bg-cyan-950/70 dark:text-cyan-300 border border-cyan-200 dark:border-cyan-800/60",
    icon: "folder-kanban"
  },
  "Syllabus": {
    badge: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700",
    icon: "clipboard-list"
  }
};

// File extension color & icon
function getFileMeta(extension) {
  const ext = (extension || '').toLowerCase();
  if (ext === 'pdf') {
    return { icon: 'file-text', color: 'text-rose-500 bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-800/50' };
  }
  if (['ipynb', 'py', 'c', 'h', 'java', 'm'].includes(ext)) {
    return { icon: 'code', color: 'text-amber-500 bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-800/50' };
  }
  if (['zip', 'rar', '7z', 'tar', 'gz'].includes(ext)) {
    return { icon: 'archive', color: 'text-orange-500 bg-orange-50 dark:bg-orange-950/40 border-orange-200 dark:border-orange-800/50' };
  }
  if (['docx', 'doc', 'pptx', 'ppt', 'xlsx', 'xls'].includes(ext)) {
    return { icon: 'file-spreadsheet', color: 'text-blue-500 bg-blue-50 dark:bg-blue-950/40 border-blue-200 dark:border-blue-800/50' };
  }
  return { icon: 'file', color: 'text-slate-500 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700' };
}

// DOM Elements
const elements = {
  sidebar: document.getElementById('sidebar'),
  ueGroupsContainer: document.getElementById('ueGroupsContainer'),
  btnAllSubjects: document.getElementById('btnAllSubjects'),
  badgeAllDocsCount: document.getElementById('badgeAllDocsCount'),
  statTotalDocs: document.getElementById('statTotalDocs'),
  statSubjectsCount: document.getElementById('statSubjectsCount'),
  statTotalSize: document.getElementById('statTotalSize'),
  documentsGrid: document.getElementById('documentsGrid'),
  emptyState: document.getElementById('emptyState'),
  displayedDocsCount: document.getElementById('displayedDocsCount'),
  activeFilterBadge: document.getElementById('activeFilterBadge'),
  searchInput: document.getElementById('searchInput'),
  clearSearchBtn: document.getElementById('clearSearchBtn'),
  sortSelect: document.getElementById('sortSelect'),
  typeFilterTabs: document.getElementById('typeFilterTabs'),
  subjectBanner: document.getElementById('subjectBanner'),
  bannerUeBadge: document.getElementById('bannerUeBadge'),
  bannerCode: document.getElementById('bannerCode'),
  bannerTitle: document.getElementById('bannerTitle'),
  bannerDesc: document.getElementById('bannerDesc'),
  bannerResetBtn: document.getElementById('bannerResetBtn'),
  resetSearchEmptyBtn: document.getElementById('resetSearchEmptyBtn'),
  themeToggleBtn: document.getElementById('themeToggleBtn'),
  viewerModal: document.getElementById('viewerModal'),
  modalCloseBtn: document.getElementById('modalCloseBtn'),
  pdfViewerFrame: document.getElementById('pdfViewerFrame'),
  nonPdfFallback: document.getElementById('nonPdfFallback'),
  modalDocTitle: document.getElementById('modalDocTitle'),
  modalSubjectBadge: document.getElementById('modalSubjectBadge'),
  modalTypeBadge: document.getElementById('modalTypeBadge'),
  modalSizeBadge: document.getElementById('modalSizeBadge'),
  modalExternalLink: document.getElementById('modalExternalLink'),
  modalDownloadLink: document.getElementById('modalDownloadLink'),
  fallbackTitle: document.getElementById('fallbackTitle'),
  fallbackDownloadBtn: document.getElementById('fallbackDownloadBtn'),
  mobileMenuBtn: document.getElementById('mobileMenuBtn')
};

// Initialize Application
async function init() {
  // Load data from embedded script or fallback to fetch
  if (window.COURSES_DATA) {
    state.data = window.COURSES_DATA;
  } else {
    try {
      const res = await fetch('courses_index.json');
      state.data = await res.json();
    } catch (e) {
      console.error('Erreur de chargement des données:', e);
      return;
    }
  }

  // Clean strings across data
  cleanDataset(state.data);

  // Init Theme
  initTheme();

  // Setup UI
  setupHeaderStats();
  renderSidebar();
  setupEventListeners();
  render();

  // Refresh Lucide icons
  if (window.lucide) {
    lucide.createIcons();
  }
}

function cleanDataset(data) {
  if (!data) return;
  if (data.school) data.school = cleanText(data.school);
  if (data.promotion) data.promotion = cleanText(data.promotion);

  if (data.subjects) {
    Object.values(data.subjects).forEach(subj => {
      subj.name = cleanText(subj.name);
      subj.description = cleanText(subj.description);
      subj.documents.forEach(doc => {
        doc.title = cleanText(doc.title);
        doc.subject_name = cleanText(doc.subject_name);
        doc.section = cleanText(doc.section);
      });
    });
  }

  if (data.all_documents) {
    data.all_documents.forEach(doc => {
      doc.title = cleanText(doc.title);
      doc.subject_name = cleanText(doc.subject_name);
      doc.section = cleanText(doc.section);
    });
  }
}

function setupHeaderStats() {
  if (!state.data) return;
  elements.statTotalDocs.textContent = `${state.data.total_documents} documents`;
  elements.statSubjectsCount.textContent = state.data.total_subjects;
  elements.statTotalSize.textContent = state.data.total_size_formatted;
  elements.badgeAllDocsCount.textContent = state.data.total_documents;
}

// Render Sidebar grouped by UE
function renderSidebar() {
  if (!state.data || !state.data.subjects) return;

  const subjects = Object.values(state.data.subjects);
  
  // Group by UE
  const ues = {};
  subjects.forEach(subj => {
    const ueKey = subj.ue || "UE Divers";
    if (!ues[ueKey]) ues[ueKey] = [];
    ues[ueKey].push(subj);
  });

  elements.ueGroupsContainer.innerHTML = '';

  Object.keys(ues).sort().forEach(ueKey => {
    const group = ues[ueKey];
    const ueInfo = UE_CONFIG[ueKey] || { name: ueKey, desc: "", badge: "bg-slate-100 text-slate-700" };

    const ueDiv = document.createElement('div');
    ueDiv.className = 'space-y-1.5';

    // UE Header
    const ueHeader = document.createElement('div');
    ueHeader.className = 'px-2 py-1 text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider flex items-center justify-between';
    ueHeader.innerHTML = `
      <span>${ueInfo.name}</span>
      <span class="text-[10px] font-normal lowercase text-slate-400">(${group.length} mat.)</span>
    `;
    ueDiv.appendChild(ueHeader);

    // Subject buttons
    group.forEach(subj => {
      const btn = document.createElement('button');
      btn.dataset.subjectCode = subj.code;
      btn.className = 'sidebar-subject-btn w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60';
      
      btn.innerHTML = `
        <div class="flex items-center gap-2.5 min-w-0 text-left">
          <span class="w-2 h-2 rounded-full bg-${subj.color || 'indigo'}-500 flex-shrink-0"></span>
          <span class="truncate">${subj.name}</span>
        </div>
        <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 flex-shrink-0 ml-1.5 font-semibold">${subj.document_count}</span>
      `;

      btn.addEventListener('click', () => {
        selectSubject(subj.code);
      });

      ueDiv.appendChild(btn);
    });

    elements.ueGroupsContainer.appendChild(ueDiv);
  });
}

function selectSubject(subjectCode) {
  state.activeSubject = subjectCode;
  
  // Update sidebar active classes
  document.querySelectorAll('.sidebar-subject-btn').forEach(b => {
    if (b.dataset.subjectCode === subjectCode) {
      b.classList.add('active');
    } else {
      b.classList.remove('active');
    }
  });
  elements.btnAllSubjects.classList.remove('active');

  // Update banner
  if (subjectCode && state.data.subjects[subjectCode]) {
    const subj = state.data.subjects[subjectCode];
    elements.subjectBanner.classList.remove('hidden');
    elements.bannerUeBadge.textContent = subj.ue;
    elements.bannerCode.textContent = subj.code;
    elements.bannerTitle.textContent = subj.name;
    elements.bannerDesc.textContent = subj.description || 'Module de Spé (Semestre 3)';
  } else {
    elements.subjectBanner.classList.add('hidden');
  }

  render();
}

function selectAllSubjects() {
  state.activeSubject = null;
  elements.subjectBanner.classList.add('hidden');
  document.querySelectorAll('.sidebar-subject-btn').forEach(b => b.classList.remove('active'));
  elements.btnAllSubjects.classList.add('active');
  render();
}

// Filtering & Rendering
function getFilteredDocuments() {
  if (!state.data || !state.data.all_documents) return [];

  return state.data.all_documents.filter(doc => {
    // Subject filter
    if (state.activeSubject && doc.subject_code !== state.activeSubject) {
      return false;
    }

    // Type filter
    if (state.activeType !== 'all') {
      if (state.activeType === 'TD' && doc.doc_type !== 'TD') return false;
      else if (state.activeType === 'TD & Corrigé' && doc.doc_type !== 'TD & Corrigé') return false;
      else if (state.activeType === 'Cours' && doc.doc_type !== 'Cours') return false;
      else if (state.activeType === 'Examen' && doc.doc_type !== 'Examen') return false;
      else if (state.activeType === 'TP' && doc.doc_type !== 'TP') return false;
      else if (state.activeType === 'Projet' && doc.doc_type !== 'Projet') return false;
    }

    // Origin filter (Paris / National)
    if (state.activeOrigin !== 'all') {
      if (state.activeOrigin === 'Paris') {
        const isParis = doc.origin.toLowerCase().includes('paris') || 
                        doc.origin.toLowerCase().includes('tous') || 
                        doc.origin.toLowerCase().includes('tronc');
        if (!isParis) return false;
      } else if (state.activeOrigin === 'National') {
        const isNat = doc.origin.toLowerCase().includes('national') || 
                      doc.origin.toLowerCase().includes('tous') || 
                      doc.origin.toLowerCase().includes('tronc');
        if (!isNat) return false;
      }
    }

    // Search query filter
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      const match = doc.title.toLowerCase().includes(q) ||
                    doc.subject_name.toLowerCase().includes(q) ||
                    (doc.section && doc.section.toLowerCase().includes(q)) ||
                    doc.filename.toLowerCase().includes(q) ||
                    doc.doc_type.toLowerCase().includes(q);
      if (!match) return false;
    }

    return true;
  });
}

function updateTabCounts() {
  if (!state.data) return;

  // Base list filtered only by current subject, origin and search query (independent of type tab)
  const baseDocs = state.data.all_documents.filter(doc => {
    if (state.activeSubject && doc.subject_code !== state.activeSubject) return false;
    
    if (state.activeOrigin !== 'all') {
      if (state.activeOrigin === 'Paris') {
        if (!doc.origin.toLowerCase().includes('paris') && !doc.origin.toLowerCase().includes('tous')) return false;
      } else if (state.activeOrigin === 'National') {
        if (!doc.origin.toLowerCase().includes('national') && !doc.origin.toLowerCase().includes('tous')) return false;
      }
    }

    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      return doc.title.toLowerCase().includes(q) ||
             doc.subject_name.toLowerCase().includes(q) ||
             (doc.section && doc.section.toLowerCase().includes(q)) ||
             doc.filename.toLowerCase().includes(q);
    }
    return true;
  });

  const counts = {
    all: baseDocs.length,
    cours: baseDocs.filter(d => d.doc_type === 'Cours').length,
    td: baseDocs.filter(d => d.doc_type === 'TD').length,
    corr: baseDocs.filter(d => d.doc_type === 'TD & Corrigé').length,
    exam: baseDocs.filter(d => d.doc_type === 'Examen').length,
    tp: baseDocs.filter(d => d.doc_type === 'TP').length,
    proj: baseDocs.filter(d => d.doc_type === 'Projet').length
  };

  document.getElementById('typeCountAll').textContent = counts.all;
  document.getElementById('typeCountCours').textContent = counts.cours;
  document.getElementById('typeCountTd').textContent = counts.td;
  document.getElementById('typeCountCorr').textContent = counts.corr;
  document.getElementById('typeCountExam').textContent = counts.exam;
  document.getElementById('typeCountTp').textContent = counts.tp;
  document.getElementById('typeCountProj').textContent = counts.proj;
}

function sortDocuments(docs) {
  const sorted = [...docs];
  if (state.sortBy === 'titleAsc') {
    sorted.sort((a, b) => a.title.localeCompare(b.title));
  } else if (state.sortBy === 'titleDesc') {
    sorted.sort((a, b) => b.title.localeCompare(a.title));
  } else if (state.sortBy === 'sizeDesc') {
    sorted.sort((a, b) => b.size_bytes - a.size_bytes);
  } else {
    // default: preserve pedagogical order
    sorted.sort((a, b) => {
      const pA = a.order_priority !== undefined ? a.order_priority : 50;
      const pB = b.order_priority !== undefined ? b.order_priority : 50;
      if (pA !== pB) return pA - pB;
      return a.title.localeCompare(b.title);
    });
  }
  return sorted;
}

function createCard(doc) {
  const card = document.createElement('div');
  card.className = 'doc-card rounded-2xl p-4 flex flex-col justify-between group cursor-pointer';
  
  const fileMeta = getFileMeta(doc.extension);
  const typeMeta = TYPE_STYLES[doc.doc_type] || { badge: 'bg-slate-100 text-slate-700', icon: 'file' };

  // Origin chip formatting
  let originChip = '';
  if (doc.origin && doc.origin.includes('Paris')) {
    originChip = `<span class="inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-300 border border-blue-200 dark:border-blue-900/40">🗼 Paris</span>`;
  } else if (doc.origin && doc.origin.includes('National')) {
    originChip = `<span class="inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900/40">🌐 National</span>`;
  }

  // Solution badge
  const hasSolution = doc.doc_type === 'TD & Corrigé' || (doc.title && (doc.title.includes('Corrigé') || doc.title.includes('Réponses')));
  const solutionBadge = hasSolution 
    ? `<span class="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700/60 shadow-xs"><i data-lucide="check-check" class="w-3 h-3 text-emerald-600 dark:text-emerald-400"></i> Corrigé inclus</span>`
    : '';

  card.innerHTML = `
    <div>
      <!-- Top row: File Icon, Subject & Type Badges -->
      <div class="flex items-start justify-between gap-2 mb-3">
        <div class="flex items-center gap-2 min-w-0">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 border ${fileMeta.color}">
            <i data-lucide="${fileMeta.icon}" class="w-4 h-4"></i>
          </div>
          <div class="min-w-0">
            <span class="text-[10px] font-bold text-slate-400 dark:text-slate-500 block truncate">${doc.ue} • ${doc.subject_code}</span>
            <span class="text-xs font-semibold text-slate-700 dark:text-slate-300 truncate block">${doc.subject_name}</span>
          </div>
        </div>
        <div class="flex flex-col items-end gap-1 flex-shrink-0">
          <span class="text-[10px] px-2 py-0.5 rounded-full ${typeMeta.badge}">
            ${doc.doc_type}
          </span>
          ${originChip}
        </div>
      </div>

      <!-- Title -->
      <h4 class="text-sm font-semibold text-slate-900 dark:text-white line-clamp-2 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors leading-snug mb-2" title="${doc.title}">
        ${doc.title}
      </h4>

      <!-- Section / Chapter & Solution Badge -->
      <div class="flex items-center gap-2 flex-wrap mb-4">
        <div class="text-[11px] text-slate-500 dark:text-slate-400 flex items-center gap-1.5 truncate max-w-full">
          <i data-lucide="folder" class="w-3 h-3 flex-shrink-0 text-slate-400"></i>
          <span class="truncate">${doc.section || 'Général'}</span>
        </div>
        ${solutionBadge}
      </div>
    </div>

    <!-- Bottom actions -->
    <div class="pt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
      <span class="text-[11px] font-medium text-slate-400 dark:text-slate-500 uppercase">${doc.extension} • ${doc.size_formatted}</span>
      
      <div class="flex items-center gap-1.5" onclick="event.stopPropagation()">
        <button class="btn-preview px-2.5 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/60 dark:hover:bg-indigo-900/60 text-indigo-600 dark:text-indigo-400 font-medium transition-colors flex items-center gap-1 text-xs">
          <i data-lucide="eye" class="w-3 h-3"></i>
          Consulter
        </button>
        <a href="${doc.relative_path}" download class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" title="Télécharger">
          <i data-lucide="download" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </div>
  `;

  // Card click opens viewer
  card.addEventListener('click', () => openViewer(doc));
  
  const previewBtn = card.querySelector('.btn-preview');
  if (previewBtn) {
    previewBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openViewer(doc);
    });
  }

  return card;
}

function render() {
  updateTabCounts();
  const docs = sortDocuments(getFilteredDocuments());
  elements.displayedDocsCount.textContent = docs.length;

  // Active filter badge
  const filterLabels = [];
  if (state.activeSubject) filterLabels.push(state.data.subjects[state.activeSubject]?.name || state.activeSubject);
  if (state.activeType !== 'all') filterLabels.push(state.activeType);
  if (state.activeOrigin !== 'all') filterLabels.push(`Campus: ${state.activeOrigin}`);
  if (state.searchQuery) filterLabels.push(`"${state.searchQuery}"`);

  if (filterLabels.length > 0) {
    elements.activeFilterBadge.classList.remove('hidden');
    elements.activeFilterBadge.textContent = filterLabels.join(' • ');
  } else {
    elements.activeFilterBadge.classList.add('hidden');
  }

  // Empty state
  if (docs.length === 0) {
    elements.documentsGrid.innerHTML = '';
    elements.emptyState.classList.remove('hidden');
    elements.emptyState.classList.add('flex');
    return;
  }

  elements.emptyState.classList.add('hidden');
  elements.emptyState.classList.remove('flex');
  elements.documentsGrid.innerHTML = '';

  const fragment = document.createDocumentFragment();

  // Mode 1: A specific subject is selected -> Group cleanly by Section / Chapter
  if (state.activeSubject) {
    const sectionGroups = [];
    const sectionMap = new Map();

    docs.forEach(doc => {
      const sec = doc.section || 'Général';
      if (!sectionMap.has(sec)) {
        const group = { section: sec, docs: [] };
        sectionMap.set(sec, group);
        sectionGroups.push(group);
      }
      sectionMap.get(sec).docs.push(doc);
    });

    sectionGroups.forEach(group => {
      const secHeader = document.createElement('div');
      secHeader.className = 'col-span-full mt-6 mb-2 first:mt-0 flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2.5';
      
      let secIcon = 'folder';
      const secLower = group.section.toLowerCase();
      if (secLower.includes('examen') || secLower.includes('annale') || secLower.includes('interro')) {
        secIcon = 'award';
      } else if (secLower.includes('td') || secLower.includes('dirigé') || secLower.includes('devoir')) {
        secIcon = 'file-edit';
      } else if (secLower.includes('tp') || secLower.includes('pratique') || secLower.includes('matlab')) {
        secIcon = 'laptop';
      } else if (secLower.includes('projet') || secLower.includes('template') || secLower.includes('livrable')) {
        secIcon = 'folder-kanban';
      } else if (secLower.includes('cours') || secLower.includes('séance') || secLower.includes('chapitre')) {
        secIcon = 'book-open';
      }

      secHeader.innerHTML = `
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 rounded-lg bg-indigo-50 dark:bg-indigo-950/70 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold">
            <i data-lucide="${secIcon}" class="w-4 h-4"></i>
          </div>
          <h3 class="font-bold text-slate-800 dark:text-slate-100 text-sm md:text-base">${group.section}</h3>
        </div>
        <span class="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-semibold">
          ${group.docs.length} ressource${group.docs.length > 1 ? 's' : ''}
        </span>
      `;
      fragment.appendChild(secHeader);

      group.docs.forEach(doc => {
        fragment.appendChild(createCard(doc));
      });
    });
  } 
  // Mode 2: "Toutes les matières" with default pedagogical sorting -> Group by Subject
  else if (state.sortBy === 'default') {
    const subjGroups = [];
    const subjMap = new Map();

    docs.forEach(doc => {
      const code = doc.subject_code;
      if (!subjMap.has(code)) {
        const group = {
          subject_code: code,
          subject_name: doc.subject_name,
          ue: doc.ue,
          docs: []
        };
        subjMap.set(code, group);
        subjGroups.push(group);
      }
      subjMap.get(code).docs.push(doc);
    });

    subjGroups.forEach(group => {
      const subjHeader = document.createElement('div');
      subjHeader.className = 'col-span-full mt-7 mb-2 first:mt-0 flex flex-wrap items-center justify-between gap-2 border-b-2 border-slate-200 dark:border-slate-800 pb-2.5';
      subjHeader.innerHTML = `
        <div class="flex items-center gap-2.5">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-indigo-600 text-white shadow-xs">${group.ue}</span>
          <h3 class="font-bold text-slate-900 dark:text-white text-base">${group.subject_name}</h3>
          <span class="text-xs font-mono text-slate-400 hidden sm:inline">(${group.subject_code})</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-semibold">
            ${group.docs.length} doc${group.docs.length > 1 ? 's' : ''}
          </span>
          <button class="btn-isolate-subject text-xs px-2.5 py-1 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:border-indigo-500 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors flex items-center gap-1 font-medium" data-subj="${group.subject_code}">
            <span>Isoler cette matière</span>
            <i data-lucide="arrow-right" class="w-3 h-3"></i>
          </button>
        </div>
      `;

      const btnIsolate = subjHeader.querySelector('.btn-isolate-subject');
      if (btnIsolate) {
        btnIsolate.addEventListener('click', () => {
          selectSubject(group.subject_code);
        });
      }

      fragment.appendChild(subjHeader);

      group.docs.forEach(doc => {
        fragment.appendChild(createCard(doc));
      });
    });
  } 
  // Mode 3: Custom sort (A-Z, Z-A, Taille) -> Flat continuous list
  else {
    docs.forEach(doc => {
      fragment.appendChild(createCard(doc));
    });
  }

  elements.documentsGrid.appendChild(fragment);

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Document Modal Viewer
function openViewer(doc) {
  if (!doc) return;

  elements.modalDocTitle.textContent = doc.title;
  elements.modalSubjectBadge.textContent = `${doc.ue} - ${doc.subject_name}`;
  elements.modalTypeBadge.textContent = doc.doc_type;
  elements.modalSizeBadge.textContent = `${doc.extension.toUpperCase()} (${doc.size_formatted})`;
  
  elements.modalExternalLink.href = doc.relative_path;
  elements.modalDownloadLink.href = doc.relative_path;
  elements.modalDownloadLink.setAttribute('download', doc.filename);

  const isPdf = doc.extension === 'pdf';
  const isHtml = doc.extension === 'html';

  if (isPdf || isHtml) {
    elements.nonPdfFallback.classList.add('hidden');
    elements.nonPdfFallback.classList.remove('flex');
    elements.pdfViewerFrame.classList.remove('hidden');
    elements.pdfViewerFrame.src = doc.relative_path;
  } else {
    // Non-previewable direct file
    elements.pdfViewerFrame.classList.add('hidden');
    elements.pdfViewerFrame.src = '';
    elements.nonPdfFallback.classList.remove('hidden');
    elements.nonPdfFallback.classList.add('flex');
    elements.fallbackTitle.textContent = doc.filename;
    elements.fallbackDownloadBtn.href = doc.relative_path;
    elements.fallbackDownloadBtn.setAttribute('download', doc.filename);
  }

  elements.viewerModal.classList.remove('hidden');
  document.body.classList.add('overflow-hidden');

  if (window.lucide) {
    lucide.createIcons();
  }
}

function closeViewer() {
  elements.viewerModal.classList.add('hidden');
  elements.pdfViewerFrame.src = '';
  document.body.classList.remove('overflow-hidden');
}

// Event Listeners setup
function setupEventListeners() {
  // All subjects button
  elements.btnAllSubjects.addEventListener('click', selectAllSubjects);
  elements.bannerResetBtn.addEventListener('click', selectAllSubjects);

  // Type Filter Tabs
  elements.typeFilterTabs.addEventListener('click', (e) => {
    const btn = e.target.closest('.type-pill');
    if (!btn) return;
    
    document.querySelectorAll('.type-pill').forEach(b => {
      b.classList.remove('active', 'bg-indigo-600', 'text-white', 'font-semibold');
      b.classList.add('text-slate-600', 'dark:text-slate-300');
    });

    btn.classList.add('active', 'bg-indigo-600', 'text-white', 'font-semibold');
    btn.classList.remove('text-slate-600', 'dark:text-slate-300');

    state.activeType = btn.dataset.type;
    render();
  });

  // Origin Switcher (Paris / National / All)
  document.querySelectorAll('.origin-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.origin-pill').forEach(b => {
        b.classList.remove('active', 'bg-white', 'dark:bg-slate-900', 'text-slate-900', 'dark:text-white', 'font-medium', 'shadow-xs');
        b.classList.add('text-slate-600', 'dark:text-slate-400');
      });

      btn.classList.add('active', 'bg-white', 'dark:bg-slate-900', 'text-slate-900', 'dark:text-white', 'font-medium', 'shadow-xs');
      btn.classList.remove('text-slate-600', 'dark:text-slate-400');

      state.activeOrigin = btn.dataset.origin;
      render();
    });
  });

  // Search input
  let searchTimeout = null;
  elements.searchInput.addEventListener('input', (e) => {
    const val = e.target.value.trim();
    if (val.length > 0) {
      elements.clearSearchBtn.classList.remove('hidden');
    } else {
      elements.clearSearchBtn.classList.add('hidden');
    }

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      state.searchQuery = val;
      render();
    }, 120);
  });

  // Clear search button
  elements.clearSearchBtn.addEventListener('click', () => {
    elements.searchInput.value = '';
    elements.clearSearchBtn.classList.add('hidden');
    state.searchQuery = '';
    elements.searchInput.focus();
    render();
  });

  // Reset all filters button on empty state
  elements.resetSearchEmptyBtn.addEventListener('click', () => {
    elements.searchInput.value = '';
    elements.clearSearchBtn.classList.add('hidden');
    state.searchQuery = '';
    state.activeType = 'all';
    state.activeOrigin = 'all';
    state.activeSubject = null;

    // Reset UI tabs
    document.querySelectorAll('.type-pill').forEach(b => {
      b.classList.toggle('active', b.dataset.type === 'all');
      b.classList.toggle('bg-indigo-600', b.dataset.type === 'all');
      b.classList.toggle('text-white', b.dataset.type === 'all');
      b.classList.toggle('font-semibold', b.dataset.type === 'all');
    });

    document.querySelectorAll('.origin-pill').forEach(b => {
      b.classList.toggle('active', b.dataset.origin === 'all');
      b.classList.toggle('bg-white', b.dataset.origin === 'all');
      b.classList.toggle('dark:bg-slate-900', b.dataset.origin === 'all');
      b.classList.toggle('text-slate-900', b.dataset.origin === 'all');
      b.classList.toggle('dark:text-white', b.dataset.origin === 'all');
    });

    selectAllSubjects();
  });

  // Sorting
  elements.sortSelect.addEventListener('change', (e) => {
    state.sortBy = e.target.value;
    render();
  });

  // Keyboard shortcut Ctrl+K or / for search
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && document.activeElement !== elements.searchInput)) {
      e.preventDefault();
      elements.searchInput.focus();
    }
    if (e.key === 'Escape') {
      if (!elements.viewerModal.classList.contains('hidden')) {
        closeViewer();
      }
    }
  });

  // Modal close handlers
  elements.modalCloseBtn.addEventListener('click', closeViewer);
  elements.viewerModal.addEventListener('click', (e) => {
    if (e.target === elements.viewerModal) {
      closeViewer();
    }
  });

  // Mobile menu toggle
  elements.mobileMenuBtn.addEventListener('click', () => {
    elements.sidebar.classList.toggle('hidden');
  });

  // Theme toggle
  elements.themeToggleBtn.addEventListener('click', toggleTheme);
}

// Theme Management
function initTheme() {
  const saved = localStorage.getItem('theme');
  if (saved === 'light') {
    document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  if (window.lucide) {
    lucide.createIcons();
  }
}

// Start
document.addEventListener('DOMContentLoaded', init);
