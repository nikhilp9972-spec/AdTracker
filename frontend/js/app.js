/**
 * AdPulse Intelligence - EdTech Competitor Ad Tracking & AI Strategy Engine
 * Complete Frontend Controller supporting all 8 operational views,
 * cross-platform Meta vs Google analysis, strict data transparency, and automated reporting.
 */

// Global Reactive State
const state = {
    competitors: [],
    ads: [],
    filteredAds: [],
    currentDigest: null,
    allDigests: [],
    stats: {},
    scheduler: {},
    settings: {},
    collectionLogs: [],
    crossPlatform: {},
    activeTab: 'overview',
    isDarkMode: false
};

const API_BASE = '';

// --- Lifecycle Initialization ---
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    if (window.lucide) lucide.createIcons();
    await loadInitialData();
});

function initTheme() {
    const saved = localStorage.getItem('adpulse_theme');
    if (saved === 'dark') {
        state.isDarkMode = true;
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    } else {
        state.isDarkMode = false;
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    }
    updateThemeIcon();
}

function toggleTheme() {
    state.isDarkMode = !state.isDarkMode;
    if (state.isDarkMode) {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
        localStorage.setItem('adpulse_theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        localStorage.setItem('adpulse_theme', 'light');
    }
    updateThemeIcon();
}

function updateThemeIcon() {
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.setAttribute('data-lucide', state.isDarkMode ? 'sun' : 'moon');
        if (window.lucide) lucide.createIcons();
    }
}

// --- API Helpers ---
async function apiGet(endpoint) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error(`GET ${endpoint} error:`, err);
        return null;
    }
}

async function apiPost(endpoint, body = {}) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        return await res.json();
    } catch (err) {
        console.error(`POST ${endpoint} error:`, err);
        return { status: 'error', message: err.message };
    }
}

// --- Master Data Loader ---
async function loadInitialData() {
    await Promise.all([
        loadStats(),
        loadCompetitors(),
        loadAds(),
        loadLatestDigest(),
        loadSchedulerStatus(),
        loadCrossPlatformData(),
        loadCollectionLogs(),
        loadNotificationLogs(),
        loadSettings()
    ]);
    renderAll();
}

async function loadSettings() {
    const data = await apiGet('/api/settings');
    if (data) state.settings = data;
}

async function loadStats() {
    const data = await apiGet('/api/stats');
    if (data) state.stats = data;
}

async function loadCompetitors() {
    const data = await apiGet('/api/competitors');
    if (data && Array.isArray(data)) {
        state.competitors = data;
    }
}

async function loadAds() {
    const data = await apiGet('/api/ads');
    if (data && Array.isArray(data)) {
        state.ads = data;
        state.filteredAds = [...data];
    }
}

async function loadLatestDigest() {
    const data = await apiGet('/api/digests/latest');
    if (data && data.id) {
        state.currentDigest = data;
    }
    const all = await apiGet('/api/digests');
    if (all && Array.isArray(all)) {
        state.allDigests = all;
    }
}

async function loadSchedulerStatus() {
    const data = await apiGet('/api/scheduler/status');
    if (data) state.scheduler = data;
}

async function loadCrossPlatformData() {
    const data = await apiGet('/api/analytics/cross-platform');
    if (data) state.crossPlatform = data;
}

async function loadCollectionLogs() {
    const data = await apiGet('/api/collection-logs');
    if (data && Array.isArray(data)) {
        state.collectionLogs = data;
        renderCollectionLogs(data);
    }
}

async function loadNotificationLogs() {
    const data = await apiGet('/api/notifications/logs');
    if (data && Array.isArray(data)) {
        renderNotificationLogs(data);
    }
}

// --- View Router ---
function switchTab(tabId) {
    state.activeTab = tabId;
    const tabIds = ['overview', 'competitors', 'vault', 'cross-platform', 'insights', 'reports', 'automation'];

    tabIds.forEach(id => {
        const content = document.getElementById(`tab-content-${id}`);
        const btn = document.getElementById(`tab-btn-${id}`);
        if (content) {
            if (id === tabId) {
                content.classList.remove('hidden');
                content.classList.add('fade-in');
            } else {
                content.classList.add('hidden');
                content.classList.remove('fade-in');
            }
        }
        if (btn) {
            if (id === tabId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        }
    });

    if (tabId === 'vault') filterAds();
    if (tabId === 'insights') renderCreativeInsights();
    if (tabId === 'cross-platform') renderCrossPlatform();
    if (tabId === 'reports') renderReportsView();
    if (window.lucide) lucide.createIcons();
}

// --- Render Master Function ---
function renderAll() {
    renderOverview();
    renderCompetitorsList();
    renderAdVault();
    renderCrossPlatform();
    renderCreativeInsights();
    renderReportsView();
    renderAutomationCard();
    renderDigestSelect();
    populateDropdowns();
    if (window.lucide) lucide.createIcons();
}

// --- 1. OVERVIEW RENDERING ---
function renderOverview() {
    const compCountEl = document.getElementById('stat-competitors-count');
    const compNamesEl = document.getElementById('stat-competitor-names');
    const avatarsEl = document.getElementById('stat-competitor-avatars');
    const adsCountEl = document.getElementById('stat-ads-count');
    const platformSplitEl = document.getElementById('stat-platform-split');
    const topCatEl = document.getElementById('stat-top-category');
    const topHookEl = document.getElementById('stat-top-hook');
    const nextRunText = document.getElementById('next-run-text');

    if (compCountEl) compCountEl.textContent = `${state.competitors.length} Active`;
    if (compNamesEl) compNamesEl.textContent = state.competitors.map(c => c.name).join(', ') || 'PW, Unacademy, Scaler';
    if (avatarsEl) {
        avatarsEl.innerHTML = state.competitors.map(c => `
            <img class="inline-block h-6 w-6 rounded-full ring-2 ring-white dark:ring-dark-800 object-cover" 
                 src="${c.logo_url || 'https://via.placeholder.com/32'}" 
                 alt="${escapeHtml(c.name)}" title="${escapeHtml(c.name)}">
        `).join('');
    }

    if (adsCountEl) adsCountEl.textContent = `${state.ads.length} Ads`;
    
    // Meta vs Google split
    const metaCount = state.ads.filter(a => (a.platform || '').toLowerCase() === 'meta').length;
    const googleCount = state.ads.filter(a => (a.platform || '').toLowerCase() === 'google').length;
    if (platformSplitEl) platformSplitEl.textContent = `${metaCount} Meta • ${googleCount} Google`;

    // Overview cross-platform bar
    const oMetaCount = document.getElementById('overview-meta-count');
    const oGoogleCount = document.getElementById('overview-google-count');
    const oMetaBar = document.getElementById('overview-meta-bar');
    const oGoogleBar = document.getElementById('overview-google-bar');
    if (oMetaCount) oMetaCount.textContent = `${metaCount} Ads`;
    if (oGoogleCount) oGoogleCount.textContent = `${googleCount} Ads`;
    const totalAds = (metaCount + googleCount) || 1;
    if (oMetaBar) oMetaBar.style.width = `${Math.round((metaCount / totalAds) * 100)}%`;
    if (oGoogleBar) oGoogleBar.style.width = `${Math.round((googleCount / totalAds) * 100)}%`;

    // Top Category & Hook
    if (state.currentDigest && state.currentDigest.macro_themes && state.currentDigest.macro_themes.length > 0) {
        if (topCatEl) topCatEl.textContent = state.currentDigest.macro_themes[0].theme;
        if (topHookEl && state.currentDigest.creative_intelligence && state.currentDigest.creative_intelligence.high_performing_hooks) {
            topHookEl.textContent = `Hook: "${state.currentDigest.creative_intelligence.high_performing_hooks[0] || 'Fast Track Career'}"`;
        }
    }

    // Scheduler pill
    if (nextRunText && state.scheduler) {
        if (state.scheduler.enabled) {
            nextRunText.textContent = `Next: ${state.scheduler.next_run}`;
        } else {
            nextRunText.textContent = 'Weekly Schedule Paused';
        }
    }

    // Executive summary callout
    const execEl = document.getElementById('overview-exec-summary');
    const topHooksContainer = document.getElementById('overview-top-hooks');
    if (execEl && state.currentDigest) {
        execEl.textContent = state.currentDigest.executive_summary || 'No summary synthesized yet.';
    }
    if (topHooksContainer && state.currentDigest && state.currentDigest.creative_intelligence) {
        const hooks = state.currentDigest.creative_intelligence.high_performing_hooks || [];
        topHooksContainer.innerHTML = hooks.slice(0, 4).map(h => `
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-indigo-50 dark:bg-brand-500/10 text-brand-700 dark:text-brand-300 border border-brand-200 dark:border-brand-500/20">
                ⚡ ${escapeHtml(h)}
            </span>
        `).join('');
    }

    // Competitors Fleet Snapshot
    const compGrid = document.getElementById('overview-competitors-grid');
    if (compGrid) {
        compGrid.innerHTML = state.competitors.slice(0, 3).map(c => {
            const cAds = state.ads.filter(a => a.competitor_id === c.id);
            const categories = [...new Set(cAds.map(a => (a.course_categories || '').split(',')[0].trim()).filter(Boolean))].slice(0, 2);
            return `
                <div class="p-4 rounded-xl border border-slate-200 dark:border-dark-600 bg-slate-50/50 dark:bg-dark-800/50 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <div class="flex items-center space-x-2">
                                <img src="${c.logo_url || 'https://via.placeholder.com/32'}" class="w-7 h-7 rounded-lg object-cover ring-1 ring-slate-200 dark:ring-dark-600">
                                <div>
                                    <h4 class="font-bold text-xs text-slate-900 dark:text-white">${escapeHtml(c.name)}</h4>
                                    <span class="text-[10px] text-slate-400">${escapeHtml(c.domain || 'edtech.com')}</span>
                                </div>
                            </div>
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400">
                                ${cAds.length} Ads
                            </span>
                        </div>
                        <div class="flex flex-wrap gap-1 mt-2">
                            ${categories.map(cat => `<span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 dark:bg-dark-700 text-slate-600 dark:text-slate-300">${escapeHtml(cat)}</span>`).join('')}
                        </div>
                    </div>
                    <div class="mt-3 pt-2 border-t border-slate-200 dark:border-dark-600 flex items-center justify-between text-[11px]">
                        <span class="text-slate-400">Monitored</span>
                        <button onclick="triggerCollectSingle('${c.id}')" class="text-brand-600 dark:text-brand-400 font-semibold hover:underline">
                            Collect Ads →
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Latest Creatives Grid
    const recentGrid = document.getElementById('overview-recent-ads-grid');
    if (recentGrid) {
        recentGrid.innerHTML = state.ads.slice(0, 3).map(ad => renderAdCardHtml(ad, true)).join('');
    }
}

// --- 2. COMPETITORS VIEW ---
function renderCompetitorsList() {
    const grid = document.getElementById('competitors-list-grid');
    if (!grid) return;

    grid.innerHTML = state.competitors.map(c => {
        const cAds = state.ads.filter(a => a.competitor_id === c.id);
        const cats = [...new Set(cAds.map(a => a.course_categories).filter(Boolean))].slice(0, 3);
        const lastAd = cAds[0];

        return `
            <div class="glass-card p-5 rounded-xl flex flex-col justify-between space-y-4">
                <div>
                    <!-- Header -->
                    <div class="flex items-start justify-between">
                        <div class="flex items-center space-x-3">
                            <img src="${c.logo_url || 'https://via.placeholder.com/48'}" alt="${escapeHtml(c.name)}" class="w-10 h-10 rounded-xl object-cover ring-1 ring-slate-200 dark:ring-dark-600">
                            <div>
                                <h3 class="font-bold text-sm text-slate-900 dark:text-white">${escapeHtml(c.name)}</h3>
                                <a href="https://${c.domain || '#'}" target="_blank" class="text-[11px] text-brand-600 dark:text-brand-400 hover:underline flex items-center space-x-0.5">
                                    <span>${escapeHtml(c.domain || 'website.com')}</span>
                                    <i data-lucide="external-link" class="w-2.5 h-2.5"></i>
                                </a>
                            </div>
                        </div>
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-500/20">
                            Active
                        </span>
                    </div>

                    <!-- Metrics -->
                    <div class="grid grid-cols-2 gap-2 mt-4 text-xs">
                        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-dark-700/50 border border-slate-100 dark:border-dark-600">
                            <span class="text-[10px] text-slate-400 block">Total Ads Collected</span>
                            <strong class="text-sm text-slate-900 dark:text-white font-bold">${cAds.length}</strong>
                        </div>
                        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-dark-700/50 border border-slate-100 dark:border-dark-600">
                            <span class="text-[10px] text-slate-400 block">New Ads This Week</span>
                            <strong class="text-sm text-emerald-600 dark:text-emerald-400 font-bold">${cAds.length}</strong>
                        </div>
                    </div>

                    <!-- Promoted Categories -->
                    <div class="mt-3">
                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Main Promoted Categories:</span>
                        <div class="flex flex-wrap gap-1">
                            ${cats.map(cat => `
                                <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 dark:bg-dark-700 text-slate-700 dark:text-slate-300">
                                    ${escapeHtml(cat)}
                                </span>
                            `).join('') || '<span class="text-[10px] text-slate-400">Online Courses</span>'}
                        </div>
                    </div>

                    ${lastAd ? `
                        <div class="mt-3 p-2.5 rounded-lg bg-slate-50 dark:bg-dark-800/80 border border-slate-100 dark:border-dark-600 text-xs">
                            <span class="text-[10px] text-slate-400 block">Latest Ad Headline:</span>
                            <p class="font-semibold text-slate-800 dark:text-slate-200 truncate mt-0.5">${escapeHtml(lastAd.headline)}</p>
                        </div>
                    ` : ''}
                </div>

                <!-- Footer Actions -->
                <div class="pt-3 border-t border-slate-100 dark:border-dark-600/60 flex items-center justify-between">
                    <button onclick="triggerCollectSingle('${c.id}')" class="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-brand-50 hover:bg-brand-100 dark:bg-brand-500/10 dark:hover:bg-brand-500/20 text-brand-600 dark:text-brand-400 transition-colors">
                        <i data-lucide="refresh-cw" class="w-3 h-3"></i>
                        <span>Collect Ads</span>
                    </button>
                    <div class="flex items-center space-x-1">
                        <button onclick="editCompetitor('${c.id}')" class="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-white" title="Edit">
                            <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
                        </button>
                        <button onclick="deleteCompetitor('${c.id}')" class="p-1.5 text-slate-400 hover:text-red-500" title="Delete">
                            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// --- 3. AD LIBRARY (VAULT) VIEW ---
function renderAdVault() {
    filterAds();
}

function filterAds() {
    const search = (document.getElementById('vault-search-input')?.value || '').toLowerCase();
    const compFilter = document.getElementById('vault-filter-comp')?.value || '';
    const catFilter = document.getElementById('vault-filter-category')?.value || '';
    const platFilter = document.getElementById('vault-filter-platform')?.value || 'all';
    const plcFilter = document.getElementById('vault-filter-placement')?.value || 'all';
    const offerFilter = document.getElementById('vault-filter-offer')?.value || 'all';
    const transFilter = document.getElementById('vault-filter-transparency')?.value || 'all';

    state.filteredAds = state.ads.filter(ad => {
        // Competitor
        if (compFilter && ad.competitor_id !== compFilter) return false;

        // Platform
        if (platFilter !== 'all' && (ad.platform || '').toLowerCase() !== platFilter.toLowerCase()) return false;

        // Placement
        if (plcFilter !== 'all') {
            const adPlc = ad.google_placement || '';
            if (adPlc !== plcFilter) return false;
        }

        // Category
        if (catFilter && !(ad.course_categories || '').toLowerCase().includes(catFilter.toLowerCase())) return false;

        // Offer
        if (offerFilter !== 'all') {
            const adOffer = (ad.offer_details || '').toLowerCase();
            if (!adOffer.includes(offerFilter.toLowerCase())) return false;
        }

        // Transparency
        if (transFilter === 'live' && ad.is_demo == 1) return false;
        if (transFilter === 'demo' && ad.is_demo != 1) return false;

        // Search text
        if (search) {
            const matchHead = (ad.headline || '').toLowerCase().includes(search);
            const matchBody = (ad.body_text || '').toLowerCase().includes(search);
            const matchHook = (ad.marketing_hook || '').toLowerCase().includes(search);
            const matchComp = (ad.competitor_name || '').toLowerCase().includes(search);
            if (!matchHead && !matchBody && !matchHook && !matchComp) return false;
        }

        return true;
    });

    const grid = document.getElementById('vault-ads-grid');
    if (!grid) return;

    if (state.filteredAds.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full py-12 text-center text-slate-400">
                <i data-lucide="inbox" class="w-8 h-8 mx-auto text-slate-400 mb-2"></i>
                <p class="text-xs">No advertisements match the selected filter criteria.</p>
            </div>
        `;
        if (window.lucide) lucide.createIcons();
        return;
    }

    grid.innerHTML = state.filteredAds.map(ad => renderAdCardHtml(ad)).join('');
    if (window.lucide) lucide.createIcons();
}

function renderAdCardHtml(ad, compact = false) {
    const isMeta = (ad.platform || '').toLowerCase() === 'meta';
    const isGoogle = (ad.platform || '').toLowerCase() === 'google';
    const isVerifiedDiscover = ad.google_placement === 'Google Discover' && ad.is_placement_verified == 1;
    const isDemo = ad.is_demo == 1;

    let placementBadge = '';
    if (isGoogle) {
        if (isVerifiedDiscover) {
            placementBadge = `<span class="badge-discover px-1.5 py-0.5 rounded text-[10px] font-bold">Discover • Verified</span>`;
        } else if (ad.google_placement === 'Demand Gen') {
            placementBadge = `<span class="badge-demandgen px-1.5 py-0.5 rounded text-[10px] font-bold">Demand Gen</span>`;
        } else if (ad.google_placement === 'Search') {
            placementBadge = `<span class="badge-search px-1.5 py-0.5 rounded text-[10px] font-bold">Search</span>`;
        } else {
            placementBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-100 dark:bg-dark-700 text-slate-600 dark:text-slate-300">Google Placement</span>`;
        }
    }

    const platformBadge = isMeta
        ? `<span class="badge-meta px-1.5 py-0.5 rounded text-[10px] font-bold">Meta</span>`
        : `<span class="badge-google px-1.5 py-0.5 rounded text-[10px] font-bold">Google</span>`;

    const transparencyPill = isDemo
        ? `<span class="badge-demo px-1.5 py-0.5 rounded text-[9px] font-bold" title="Historical Benchmark Data">DEMO</span>`
        : `<span class="badge-live px-1.5 py-0.5 rounded text-[9px] font-bold" title="Live Verified Advertisement">LIVE REAL AD</span>`;

    const courseCats = (ad.course_categories || 'Online Courses').split(',').map(c => c.trim()).filter(Boolean);

    return `
        <div class="ad-card glass-card rounded-xl overflow-hidden flex flex-col justify-between">
            <div>
                <!-- Media Preview -->
                <div class="ad-creative-media relative">
                    <img src="${ad.creative_url || 'https://via.placeholder.com/600x375'}" alt="Ad Creative" class="w-full h-full object-cover">
                    <div class="absolute top-2 left-2 flex items-center space-x-1">
                        ${platformBadge}
                        ${placementBadge}
                    </div>
                    <div class="absolute top-2 right-2">
                        ${transparencyPill}
                    </div>
                </div>

                <!-- Ad Content -->
                <div class="p-4 space-y-2.5">
                    <!-- Brand & Category Row -->
                    <div class="flex items-center justify-between text-xs">
                        <strong class="text-slate-900 dark:text-white font-bold">${escapeHtml(ad.competitor_name || 'EdTech Brand')}</strong>
                        <span class="text-[10px] text-slate-400">${escapeHtml(ad.first_seen || 'Recent')}</span>
                    </div>

                    <!-- Course Categories Chips -->
                    <div class="flex flex-wrap gap-1">
                        ${courseCats.slice(0, 2).map(cat => `
                            <span class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 dark:bg-dark-700 text-slate-700 dark:text-slate-300">
                                📚 ${escapeHtml(cat)}
                            </span>
                        `).join('')}
                    </div>

                    <!-- Headline & Marketing Hook -->
                    <div>
                        <h4 class="font-bold text-xs sm:text-sm text-slate-900 dark:text-white leading-snug line-clamp-2">
                            ${escapeHtml(ad.headline)}
                        </h4>
                        ${ad.marketing_hook ? `
                            <div class="mt-1 text-[11px] font-semibold text-brand-600 dark:text-brand-400 flex items-center space-x-1">
                                <i data-lucide="zap" class="w-3 h-3 flex-shrink-0"></i>
                                <span class="truncate">${escapeHtml(ad.marketing_hook)}</span>
                            </div>
                        ` : ''}
                    </div>

                    <!-- Copy Snippet -->
                    <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed line-clamp-3">
                        ${escapeHtml(ad.body_text)}
                    </p>

                    <!-- Value Prop & Offer Callout -->
                    ${ad.offer_details && ad.offer_details !== 'Standard Pricing' ? `
                        <div class="p-2 rounded-lg bg-rose-50/60 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/40 text-[11px] text-rose-800 dark:text-rose-300 font-semibold flex items-center space-x-1">
                            <span>🏷️ Offer:</span>
                            <span class="truncate">${escapeHtml(ad.offer_details)}</span>
                        </div>
                    ` : ''}

                    <!-- Audience Hypothesis -->
                    ${ad.audience_hypothesis && !compact ? `
                        <div class="text-[10px] text-slate-500 italic">
                            🎯 ${escapeHtml(ad.audience_hypothesis)}
                        </div>
                    ` : ''}
                </div>
            </div>

            <!-- Footer: CTA & Ad Library Deep-Link -->
            <div class="p-3 bg-slate-50 dark:bg-dark-800/80 border-t border-slate-100 dark:border-dark-600/60 flex items-center justify-between text-xs">
                <span class="px-2 py-0.5 rounded bg-indigo-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400 font-semibold text-[11px]">
                    CTA: ${escapeHtml(ad.cta_text || 'Learn More')}
                </span>
                ${ad.ad_library_url ? `
                    <a href="${ad.ad_library_url}" target="_blank" class="inline-flex items-center space-x-0.5 text-brand-600 dark:text-brand-400 hover:underline font-semibold text-[11px]">
                        <span>View Source</span>
                        <i data-lucide="external-link" class="w-3 h-3"></i>
                    </a>
                ` : '<span class="text-[10px] text-slate-400">Source: Direct</span>'}
            </div>
        </div>
    `;
}

// --- 4. CROSS-PLATFORM VIEW ---
function renderCrossPlatform() {
    const cp = state.crossPlatform || {};
    const metaCount = document.getElementById('cp-meta-count');
    const googleCount = document.getElementById('cp-google-count');
    const discoverCount = document.getElementById('cp-discover-count');
    const searchCount = document.getElementById('cp-search-count');

    if (metaCount) metaCount.textContent = `${cp.meta_ads_count || 0} Creatives`;
    if (googleCount) googleCount.textContent = `${cp.google_ads_count || 0} Creatives`;
    if (discoverCount) discoverCount.textContent = `${cp.google_discover_verified_count || 0} Verified`;
    if (searchCount) searchCount.textContent = `${cp.google_placements?.Search || 0} Ads`;
}

// --- 5. CREATIVE INSIGHTS VIEW ---
function renderCreativeInsights() {
    // Top Categories Frequency Bar Chart
    const catContainer = document.getElementById('insights-categories-bars');
    const hooksContainer = document.getElementById('insights-hooks-list');
    const offersContainer = document.getElementById('insights-offers-list');
    const vpsContainer = document.getElementById('insights-value-props-list');
    const oppsContainer = document.getElementById('insights-opportunities-list');

    // Count categories
    const catCounts = {};
    const hookCounts = {};
    const offerCounts = {};
    const vpCounts = {};

    state.ads.forEach(ad => {
        (ad.course_categories || '').split(',').forEach(c => {
            const clean = c.trim();
            if (clean) catCounts[clean] = (catCounts[clean] || 0) + 1;
        });
        if (ad.marketing_hook && ad.marketing_hook !== 'Headline Hook') {
            hookCounts[ad.marketing_hook] = (hookCounts[ad.marketing_hook] || 0) + 1;
        }
        if (ad.offer_details && ad.offer_details !== 'Standard Pricing') {
            offerCounts[ad.offer_details] = (offerCounts[ad.offer_details] || 0) + 1;
        }
        if (ad.value_proposition) {
            ad.value_proposition.split(',').forEach(v => {
                const clean = v.trim();
                if (clean) vpCounts[clean] = (vpCounts[clean] || 0) + 1;
            });
        }
    });

    const sortedCats = Object.entries(catCounts).sort((a, b) => b[1] - a[1]).slice(0, 5);
    const maxCat = sortedCats[0] ? sortedCats[0][1] : 1;

    if (catContainer) {
        catContainer.innerHTML = sortedCats.map(([cat, count]) => {
            const pct = Math.round((count / maxCat) * 100);
            return `
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span class="font-medium text-slate-800 dark:text-slate-200">${escapeHtml(cat)}</span>
                        <span class="font-bold text-slate-500">${count} ads</span>
                    </div>
                    <div class="w-full bg-slate-100 dark:bg-dark-700 h-2 rounded-full overflow-hidden">
                        <div class="bg-indigo-600 dark:bg-brand-500 h-full rounded-full" style="width: ${pct}%"></div>
                    </div>
                </div>
            `;
        }).join('') || '<p class="text-xs text-slate-400">Ingesting ads...</p>';
    }

    if (hooksContainer) {
        const topHooks = Object.entries(hookCounts).sort((a, b) => b[1] - a[1]).slice(0, 4);
        hooksContainer.innerHTML = topHooks.map(([hook, count]) => `
            <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-dark-800/60 border border-slate-200 dark:border-dark-600 flex items-center justify-between text-xs">
                <span class="font-semibold text-slate-800 dark:text-slate-200">"${escapeHtml(hook)}"</span>
                <span class="text-[10px] font-bold text-brand-600 dark:text-brand-400">${count} ads</span>
            </div>
        `).join('') || '<p class="text-xs text-slate-400">Analyzing hooks...</p>';
    }

    if (offersContainer) {
        const topOffers = Object.keys(offerCounts).slice(0, 4);
        offersContainer.innerHTML = topOffers.map(o => `<li>${escapeHtml(o)}</li>`).join('') || '<li>Free Live Masterclass Access</li><li>Scholarship Entrance Tests</li>';
    }

    if (vpsContainer) {
        const topVps = Object.keys(vpCounts).slice(0, 4);
        vpsContainer.innerHTML = topVps.map(v => `<li>${escapeHtml(v)}</li>`).join('') || '<li>1-on-1 Mentorship</li><li>Alumni Placements</li>';
    }

    if (oppsContainer && state.currentDigest && state.currentDigest.counter_strategies) {
        oppsContainer.innerHTML = state.currentDigest.counter_strategies.slice(0, 3).map(s => `
            <li><strong>${escapeHtml(s.tactic)}:</strong> ${escapeHtml(s.action)}</li>
        `).join('');
    }
}

// --- 6. INTELLIGENCE REPORTS (7 SECTIONS) VIEW ---
function renderReportsView() {
    const digest = state.currentDigest;
    if (!digest) return;

    const titleEl = document.getElementById('report-title');
    const periodEl = document.getElementById('report-period');
    const execEl = document.getElementById('report-exec-summary');
    const compGrid = document.getElementById('report-competitors-grid');
    const trendsGrid = document.getElementById('report-market-trends');
    const creativeIntelEl = document.getElementById('report-creative-intel');
    const oppsEl = document.getElementById('report-opportunities');
    const cpIntelEl = document.getElementById('report-cross-platform-intel');
    const sourceTbody = document.getElementById('report-source-tbody');

    if (titleEl) titleEl.textContent = digest.title || 'EdTech Competitor Ad Intelligence Brief';
    if (periodEl) periodEl.textContent = `Monitored Period: ${digest.period_start} to ${digest.period_end}`;
    if (execEl) execEl.textContent = digest.executive_summary || 'No summary available.';

    // Section 2: Competitor-Wise Breakdown
    if (compGrid && digest.brand_breakdowns) {
        compGrid.innerHTML = digest.brand_breakdowns.map(b => `
            <div class="p-4 rounded-xl border border-slate-200 dark:border-dark-600 bg-slate-50/50 dark:bg-dark-800/50 space-y-2.5">
                <div class="flex items-center justify-between">
                    <h4 class="font-bold text-xs text-slate-900 dark:text-white">${escapeHtml(b.competitor_name)}</h4>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-brand-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400">${b.ads_tracked} Ads</span>
                </div>
                <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">${escapeHtml(b.primary_narrative)}</p>
                <div class="text-[11px] space-y-1 text-slate-500">
                    <div>📚 <strong>Courses:</strong> ${(b.promoted_categories || []).slice(0, 2).join(', ')}</div>
                    <div>⚡ <strong>Top Hook:</strong> ${(b.dominant_hooks || [])[0] || 'Skill Mastery'}</div>
                    <div>🏷️ <strong>Offer:</strong> ${(b.active_offers || [])[0] || 'Standard'}</div>
                    <div class="italic text-[10px]">🎯 ${escapeHtml(b.audience_hypothesis || '')}</div>
                </div>
            </div>
        `).join('');
    }

    // Section 3: Market Trends
    if (trendsGrid && digest.macro_themes) {
        trendsGrid.innerHTML = digest.macro_themes.map(m => `
            <div class="p-3.5 rounded-xl border border-slate-200 dark:border-dark-600 bg-slate-50/40 dark:bg-dark-800/40 space-y-1 text-xs">
                <strong class="text-brand-600 dark:text-brand-400 block">${escapeHtml(m.theme)}</strong>
                <p class="text-slate-600 dark:text-slate-300 leading-relaxed">${escapeHtml(m.observation)}</p>
            </div>
        `).join('');
    }

    // Section 4: Creative Intelligence
    if (creativeIntelEl && digest.creative_intelligence) {
        const hooks = (digest.creative_intelligence.high_performing_hooks || []).map(h => `<li>"${escapeHtml(h)}"</li>`).join('');
        const patterns = (digest.creative_intelligence.messaging_patterns || []).map(p => `<li>${escapeHtml(p)}</li>`).join('');
        creativeIntelEl.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <strong class="text-slate-700 dark:text-slate-300 block mb-1">High-Performing Creative Hooks:</strong>
                    <ul class="list-disc pl-4 space-y-1 text-slate-600 dark:text-slate-300">${hooks}</ul>
                </div>
                <div>
                    <strong class="text-slate-700 dark:text-slate-300 block mb-1">Messaging Patterns:</strong>
                    <ul class="list-disc pl-4 space-y-1 text-slate-600 dark:text-slate-300">${patterns}</ul>
                </div>
            </div>
        `;
    }

    // Section 5: Opportunities
    if (oppsEl && digest.counter_strategies) {
        oppsEl.innerHTML = digest.counter_strategies.map(s => `
            <div class="p-3 rounded-xl border border-emerald-200 dark:border-emerald-500/20 bg-emerald-50/30 dark:bg-emerald-950/20 text-xs text-slate-700 dark:text-slate-300">
                <strong class="text-emerald-700 dark:text-emerald-400 block mb-0.5">${escapeHtml(s.tactic)}</strong>
                <p>${escapeHtml(s.action)}</p>
            </div>
        `).join('');
    }

    // Section 6: Cross-Platform Summary
    if (cpIntelEl && digest.cross_platform_intelligence) {
        const cp = digest.cross_platform_intelligence;
        cpIntelEl.innerHTML = `
            <p class="leading-relaxed mb-2">${escapeHtml(cp.platform_comparison_summary || '')}</p>
            <div class="text-[11px] text-slate-500">${escapeHtml(cp.discover_placement_note || '')}</div>
        `;
    }

    // Section 7: Source References Table
    if (sourceTbody) {
        const refs = digest.source_references || [];
        if (refs.length > 0) {
            sourceTbody.innerHTML = refs.map(r => `
                <tr>
                    <td class="py-2 px-3 font-bold">${escapeHtml(r.brand)}</td>
                    <td class="py-2 px-3 truncate max-w-xs">${escapeHtml(r.headline)}</td>
                    <td class="py-2 px-3">${escapeHtml(r.platform)}</td>
                    <td class="py-2 px-3">${escapeHtml(r.category)}</td>
                    <td class="py-2 px-3">
                        <a href="${r.url}" target="_blank" class="text-brand-600 dark:text-brand-400 hover:underline flex items-center space-x-1">
                            <span>Open Ad</span>
                            <i data-lucide="external-link" class="w-2.5 h-2.5"></i>
                        </a>
                    </td>
                </tr>
            `).join('');
        } else {
            // Fallback from monitored ads
            sourceTbody.innerHTML = state.ads.slice(0, 10).map(a => `
                <tr>
                    <td class="py-2 px-3 font-bold">${escapeHtml(a.competitor_name)}</td>
                    <td class="py-2 px-3 truncate max-w-xs">${escapeHtml(a.headline)}</td>
                    <td class="py-2 px-3 uppercase">${escapeHtml(a.platform)}</td>
                    <td class="py-2 px-3">${escapeHtml((a.course_categories || '').split(',')[0])}</td>
                    <td class="py-2 px-3">
                        ${a.ad_library_url ? `
                            <a href="${a.ad_library_url}" target="_blank" class="text-brand-600 dark:text-brand-400 hover:underline flex items-center space-x-1">
                                <span>Ad Library</span>
                                <i data-lucide="external-link" class="w-2.5 h-2.5"></i>
                            </a>
                        ` : '<span class="text-slate-400">Direct</span>'}
                    </td>
                </tr>
            `).join('');
        }
    }
}

// --- 7. AUTOMATION & LOGS VIEW ---
function renderAutomationCard() {
    const s = state.scheduler || {};
    const dayEl = document.getElementById('auto-cadence-day');
    const timeEl = document.getElementById('auto-cadence-time');
    const pill = document.getElementById('automation-pill-status');

    if (dayEl) dayEl.textContent = s.target_day || 'Monday';
    if (timeEl) timeEl.textContent = `${s.target_time || '09:00'} (IST)`;
    if (pill) {
        pill.textContent = s.enabled ? 'Active' : 'Disabled';
        pill.className = s.enabled
            ? 'text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400'
            : 'text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500';
    }
}

function renderCollectionLogs(logs) {
    const tbody = document.getElementById('collection-logs-tbody');
    if (!tbody) return;

    if (!logs || logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="py-4 text-center text-slate-400">No collection audits recorded yet.</td></tr>`;
        return;
    }

    tbody.innerHTML = logs.map(l => {
        const isSuccess = l.status === 'SUCCESS';
        const isDemo = l.status === 'DEMO_FALLBACK' || l.status === 'MOCK_FALLBACK';
        const statusBadge = isSuccess
            ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-400">SUCCESS</span>`
            : (isDemo
                ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400">BENCHMARK</span>`
                : `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-700 dark:bg-rose-500/20 dark:text-rose-400">FAILED</span>`);

        return `
            <tr>
                <td class="py-2.5 px-3 font-mono text-[11px] text-slate-500">${escapeHtml(l.created_at || '')}</td>
                <td class="py-2.5 px-3 font-bold text-slate-900 dark:text-white">${escapeHtml(l.competitor_name || l.competitor_id)}</td>
                <td class="py-2.5 px-3 text-slate-600 dark:text-slate-300">${escapeHtml(l.source || 'Meta API')}</td>
                <td class="py-2.5 px-3 font-bold">${l.ads_retrieved} ads</td>
                <td class="py-2.5 px-3">${statusBadge}</td>
                <td class="py-2.5 px-3 text-slate-500 max-w-xs truncate" title="${escapeHtml(l.error_message || 'OK')}">${escapeHtml(l.error_message || 'OK')}</td>
            </tr>
        `;
    }).join('');
}

function renderNotificationLogs(logs) {
    const tbody = document.getElementById('notification-logs-tbody');
    if (!tbody) return;

    if (!logs || logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="py-4 text-center text-slate-400">No delivery attempts recorded yet.</td></tr>`;
        return;
    }

    tbody.innerHTML = logs.map(l => {
        const isSuccess = l.status === 'SUCCESS';
        const badge = isSuccess
            ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-400">SUCCESS</span>`
            : `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-700 dark:bg-rose-500/20 dark:text-rose-400">FAILED</span>`;

        return `
            <tr>
                <td class="py-2.5 px-3 uppercase font-bold text-slate-800 dark:text-slate-200">${escapeHtml(l.channel)}</td>
                <td class="py-2.5 px-3 truncate max-w-xs">${escapeHtml(l.recipient)}</td>
                <td class="py-2.5 px-3">${badge}</td>
                <td class="py-2.5 px-3 font-mono text-[11px] text-slate-500">${escapeHtml(l.dispatched_at || '')}</td>
                <td class="py-2.5 px-3 text-slate-500 max-w-xs truncate">${escapeHtml(l.error_message || 'Delivered')}</td>
            </tr>
        `;
    }).join('');
}

function renderDigestSelect() {
    const sel = document.getElementById('digest-archive-select');
    if (!sel || !state.allDigests.length) return;

    sel.innerHTML = state.allDigests.map((d, i) => `
        <option value="${d.id}">${i === 0 ? 'Latest: ' : ''}${escapeHtml(d.title)}</option>
    `).join('');
}

async function onDigestSelectChange(val) {
    if (val === 'latest') {
        await loadLatestDigest();
    } else {
        const found = state.allDigests.find(d => d.id === val);
        if (found) state.currentDigest = found;
    }
    renderReportsView();
    if (window.lucide) lucide.createIcons();
}

function populateDropdowns() {
    // Populate competitor selects
    const vaultSel = document.getElementById('vault-filter-comp');
    const importSel = document.getElementById('import-comp-id');

    const options = state.competitors.map(c => `<option value="${c.id}">${escapeHtml(c.name)}</option>`).join('');
    if (vaultSel) vaultSel.innerHTML = '<option value="">All Brands</option>' + options;
    if (importSel) importSel.innerHTML = options;
}

// --- ACTIONS & OPERATIONAL TRIGGERS ---

// Trigger Full End-to-End Pipeline
async function triggerPipelineRun() {
    const btn = document.getElementById('btn-run-pipeline');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin"></i><span>Scanning...</span>`;
        if (window.lucide) lucide.createIcons();
    }
    showToast('Starting automated competitive intelligence scan...', 'info');

    const res = await apiPost('/api/pipeline/run-now');
    if (res && res.status === 'success') {
        showToast('Audit complete! Real ads ingested and digest synthesized.', 'success');
        await loadInitialData();
    } else {
        showToast(res.message || 'Audit encountered an issue', 'error');
    }

    if (btn) {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="zap" class="w-3.5 h-3.5 text-amber-300"></i><span>Run Scan</span>`;
        if (window.lucide) lucide.createIcons();
    }
}

// Collect Ads For All Competitors
async function triggerCollectAds() {
    showToast('Ingesting ads from competitor platforms...', 'info');
    const res = await apiPost('/api/ads/collect', { ads_per_competitor: 4 });
    if (res) {
        showToast(`Ingestion completed for ${res.competitors_scanned || 0} brands.`, 'success');
        await loadAds();
        await loadCollectionLogs();
        await loadStats();
        renderAll();
    }
}

// Collect Ads for a Single Competitor
async function triggerCollectSingle(compId) {
    showToast(`Ingesting ads for competitor ${compId}...`, 'info');
    const res = await apiPost('/api/ads/collect-single', { competitor_id: compId, count: 4 });
    if (res && res.status === 'success') {
        showToast(`Collected ${res.ads_saved || 0} ads for ${compId}`, 'success');
        await loadAds();
        await loadCollectionLogs();
        renderAll();
    } else {
        showToast(res.message || 'Collection failed', 'error');
    }
}

// Regenerate Digest
async function regenerateDigest() {
    showToast('Re-synthesizing 7-section intelligence brief...', 'info');
    const res = await apiPost('/api/digests/generate', { days: 7 });
    if (res && res.id) {
        state.currentDigest = res;
        showToast('New intelligence digest synthesized successfully!', 'success');
        renderReportsView();
        renderOverview();
        if (window.lucide) lucide.createIcons();
    }
}

// Dispatch to Slack
async function dispatchToSlack() {
    showToast('Dispatching digest to Slack...', 'info');
    const res = await apiPost('/api/notifications/slack', { digest_id: state.currentDigest?.id });
    if (res && res.status === 'success') {
        showToast('Successfully posted brief to Slack channel!', 'success');
    } else {
        showToast(res.message || 'Slack dispatch failed', 'error');
    }
    await loadNotificationLogs();
}

// Dispatch to Email
async function dispatchToEmail() {
    showToast('Dispatching HTML email briefing...', 'info');
    const res = await apiPost('/api/notifications/email', { digest_id: state.currentDigest?.id });
    if (res && (res.status === 'success' || res.status === 'simulated')) {
        showToast(res.message || 'Email successfully sent!', 'success');
    } else {
        showToast(res.message || 'Email delivery failed', 'error');
    }
    await loadNotificationLogs();
}

// Test Slack Webhook
async function testSlackWebhook() {
    showToast('Sending test ping to Slack...', 'info');
    const res = await apiPost('/api/notifications/test-slack', {});
    if (res && res.status === 'success') {
        showToast('Slack verification ping passed!', 'success');
    } else {
        showToast(res.message || 'Slack test failed', 'error');
    }
}

async function testSlackWebhookFromInput() {
    const url = document.getElementById('setting-slack-webhook')?.value;
    if (!url) {
        showToast('Please enter a Webhook URL first', 'error');
        return;
    }
    showToast('Verifying Webhook URL...', 'info');
    const res = await apiPost('/api/notifications/test-slack', { webhook_url: url });
    if (res && res.status === 'success') {
        showToast(res.message, 'success');
    } else {
        showToast(res.message, 'error');
    }
}

function validateSlackInput() {
    const input = document.getElementById('setting-slack-webhook');
    const warning = document.getElementById('slack-input-warning');
    if (!input || !warning) return;

    const val = input.value.trim();
    if (val && !val.startsWith('https://hooks.slack.com/')) {
        warning.classList.remove('hidden');
    } else {
        warning.classList.add('hidden');
    }
}

// Test Email SMTP
async function testEmailSMTP() {
    const recip = prompt('Enter recipient email for verification test:', 'test@company.com');
    if (!recip) return;
    showToast(`Sending test email to ${recip}...`, 'info');
    const res = await apiPost('/api/notifications/test-email', { recipient: recip });
    if (res && res.status === 'success') {
        showToast(res.message, 'success');
    } else {
        showToast(res.message || 'SMTP test failed', 'error');
    }
}

// Manual Real Ad Import
async function submitManualAd(e) {
    e.preventDefault();
    const compId = document.getElementById('import-comp-id').value;
    const platform = document.getElementById('import-platform').value;
    const headline = document.getElementById('import-headline').value;
    const body = document.getElementById('import-body').value;
    const cta = document.getElementById('import-cta').value;
    const placement = document.getElementById('import-google-placement').value;
    const url = document.getElementById('import-url').value;

    const res = await apiPost('/api/ads/import-manual', {
        competitor_id: compId,
        platform: platform,
        headline: headline,
        body_text: body,
        cta_text: cta,
        google_placement: placement,
        is_placement_verified: placement === 'Google Discover' ? 1 : 0,
        ad_library_url: url
    });

    if (res && res.status === 'success') {
        showToast('Real verified ad imported successfully!', 'success');
        closeModal('modal-manual-import');
        document.getElementById('manual-import-form').reset();
        await loadAds();
        await loadCollectionLogs();
        renderAll();
    } else {
        showToast(res.message || 'Import failed', 'error');
    }
}

// Competitor Add / Edit / Delete
function openAddCompetitorModal() {
    document.getElementById('competitor-form').reset();
    document.getElementById('comp-form-id').value = '';
    document.getElementById('modal-competitor-title').textContent = 'Add EdTech Competitor';
    openModal('modal-competitor');
}

function editCompetitor(id) {
    const comp = state.competitors.find(c => c.id === id);
    if (!comp) return;
    document.getElementById('comp-form-id').value = comp.id;
    document.getElementById('comp-form-name').value = comp.name;
    document.getElementById('comp-form-domain').value = comp.domain || '';
    document.getElementById('comp-form-industry').value = comp.industry || 'EdTech';
    document.getElementById('comp-form-logo').value = comp.logo_url || '';
    document.getElementById('modal-competitor-title').textContent = `Edit ${comp.name}`;
    openModal('modal-competitor');
}

async function saveCompetitor(e) {
    e.preventDefault();
    const id = document.getElementById('comp-form-id').value;
    const name = document.getElementById('comp-form-name').value;
    const domain = document.getElementById('comp-form-domain').value;
    const industry = document.getElementById('comp-form-industry').value;
    const logo = document.getElementById('comp-form-logo').value;

    const res = await apiPost('/api/competitors', {
        id: id || undefined,
        name: name,
        domain: domain,
        industry: industry,
        logo_url: logo
    });

    if (res && res.id) {
        showToast(`Competitor ${name} saved successfully!`, 'success');
        closeModal('modal-competitor');
        await loadCompetitors();
        renderCompetitorsList();
        renderOverview();
        populateDropdowns();
    } else {
        showToast(res.message || 'Failed to save competitor', 'error');
    }
}

async function deleteCompetitor(id) {
    if (!confirm('Are you sure you want to remove this competitor?')) return;
    const res = await fetch(`/api/competitors/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data && data.status === 'success') {
        showToast(`Competitor removed`, 'info');
        await loadCompetitors();
        renderCompetitorsList();
        renderOverview();
    }
}

// Settings Save
async function saveSettings(e) {
    e.preventDefault();
    const metaToken = document.getElementById('setting-meta-token').value;
    const googleKey = document.getElementById('setting-google-key').value;
    const webhook = document.getElementById('setting-slack-webhook').value;
    const smtpHost = document.getElementById('setting-smtp-host').value;
    const smtpPort = document.getElementById('setting-smtp-port').value;
    const smtpUser = document.getElementById('setting-smtp-user').value;
    const smtpPass = document.getElementById('setting-smtp-pass').value;
    const recipients = document.getElementById('setting-email-recipients').value;
    const schedEnabled = document.getElementById('setting-schedule-enabled').checked;
    const schedDay = document.getElementById('setting-schedule-day').value;
    const schedTime = document.getElementById('setting-schedule-time').value;

    const settingsPayload = {};
    if (metaToken) settingsPayload.meta_access_token = metaToken;
    if (googleKey) settingsPayload.google_ads_api_key = googleKey;
    if (webhook) settingsPayload.slack_webhook_url = webhook;
    if (smtpHost) settingsPayload.smtp_host = smtpHost;
    if (smtpPort) settingsPayload.smtp_port = smtpPort;
    if (smtpUser) settingsPayload.smtp_user = smtpUser;
    if (smtpPass) settingsPayload.smtp_pass = smtpPass;
    if (recipients) settingsPayload.email_recipients = recipients;

    await apiPost('/api/settings', settingsPayload);

    // Update scheduler
    const [h, m] = schedTime.split(':');
    await apiPost('/api/scheduler/update', {
        enabled: schedEnabled,
        day: schedDay,
        hour: parseInt(h, 10),
        minute: parseInt(m, 10)
    });

    showToast('Configuration updated successfully!', 'success');
    closeModal('modal-settings');
    await loadSettings();
    await loadSchedulerStatus();
    renderOverview();
    renderAutomationCard();
}

function openSettingsModal() {
    const s = state.settings || {};
    const sch = state.scheduler || {};

    if (document.getElementById('setting-meta-token')) document.getElementById('setting-meta-token').value = s.meta_access_token || '';
    if (document.getElementById('setting-google-key')) document.getElementById('setting-google-key').value = s.google_ads_api_key || '';
    if (document.getElementById('setting-slack-webhook')) document.getElementById('setting-slack-webhook').value = s.slack_webhook_url || '';
    if (document.getElementById('setting-smtp-host')) document.getElementById('setting-smtp-host').value = s.smtp_host || '';
    if (document.getElementById('setting-smtp-port')) document.getElementById('setting-smtp-port').value = s.smtp_port || '587';
    if (document.getElementById('setting-smtp-user')) document.getElementById('setting-smtp-user').value = s.smtp_user || '';
    if (document.getElementById('setting-smtp-pass')) document.getElementById('setting-smtp-pass').value = s.smtp_pass || '';
    if (document.getElementById('setting-email-recipients')) document.getElementById('setting-email-recipients').value = s.email_recipients || '';

    if (document.getElementById('setting-schedule-enabled')) document.getElementById('setting-schedule-enabled').checked = sch.enabled || false;
    if (document.getElementById('setting-schedule-day')) document.getElementById('setting-schedule-day').value = (sch.target_day || 'monday').toLowerCase();
    if (document.getElementById('setting-schedule-time')) document.getElementById('setting-schedule-time').value = sch.target_time || '09:00';

    validateSlackInput();
    openModal('modal-settings');
}

function openManualImportModal() {
    openModal('modal-manual-import');
}

// Previews
async function openSlackPreview() {
    const container = document.getElementById('slack-preview-container');
    if (container) {
        container.innerHTML = '<p class="text-slate-400">Loading live Block Kit preview...</p>';
    }
    openModal('modal-slack-preview');

    const res = await apiGet('/api/notifications/preview-slack');
    if (res && res.blocks && container) {
        container.innerHTML = res.blocks.map(b => {
            if (b.type === 'header') {
                return `<div class="font-bold text-sm text-white pb-1">${escapeHtml(b.text.text)}</div>`;
            }
            if (b.type === 'context') {
                return `<div class="text-[11px] text-slate-400 pb-2">${escapeHtml(b.elements[0].text)}</div>`;
            }
            if (b.type === 'divider') {
                return `<div class="border-b border-slate-700/60 my-2"></div>`;
            }
            if (b.type === 'section') {
                return `<div class="text-xs text-slate-300 leading-relaxed">${formatSlackMrkdwn(b.text.text)}</div>`;
            }
            return '';
        }).join('');
    }
}

function formatSlackMrkdwn(text) {
    return escapeHtml(text)
        .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
        .replace(/_(.*?)_/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code class="bg-[#111317] text-amber-300 px-1 rounded">$1</code>')
        .replace(/\n/g, '<br>');
}

function openEmailPreview() {
    const iframe = document.getElementById('email-preview-iframe');
    if (iframe) iframe.src = '/api/notifications/preview-email';
    openModal('modal-email-preview');
}

// Modal Helpers
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('hidden');
        if (window.lucide) lucide.createIcons();
    }
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add('hidden');
}

// Toast System
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const colors = {
        success: 'bg-emerald-600 text-white',
        error: 'bg-rose-600 text-white',
        info: 'bg-slate-900 text-white dark:bg-dark-700'
    };

    const toast = document.createElement('div');
    toast.className = `toast-enter px-4 py-2.5 rounded-xl shadow-xl text-xs font-semibold flex items-center space-x-2 pointer-events-auto ${colors[type] || colors.info}`;
    toast.innerHTML = `<span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.2s ease';
        setTimeout(() => toast.remove(), 200);
    }, 3500);
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
