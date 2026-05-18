export function initSearchModal() {
  const modal = document.getElementById('search-modal');
  const input = document.getElementById('search-input') as HTMLInputElement | null;
  const trigger = document.getElementById('search-trigger');
  const backdrop = document.getElementById('search-backdrop');
  const closeBtn = document.getElementById('search-close');
  const resultsList = document.getElementById('search-results-list');
  const loadingEl = document.getElementById('search-loading');
  const emptyEl = document.getElementById('search-empty');
  const noResultsEl = document.getElementById('search-no-results');

  if (!modal || !input || !trigger) return;

  function openModal() {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    setTimeout(() => input?.focus(), 100);
  }

  function closeModal() {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
    if (input) input.value = '';
    if (resultsList) resultsList.innerHTML = '';
    if (loadingEl) loadingEl.classList.add('hidden');
    if (emptyEl) emptyEl.classList.remove('hidden');
    if (noResultsEl) noResultsEl?.classList.add('hidden');
  }

  trigger.addEventListener('click', openModal);
  backdrop?.addEventListener('click', closeModal);
  closeBtn?.addEventListener('click', closeModal);

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (!modal.classList.contains('hidden')) closeModal();
      input?.blur();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      if (modal.classList.contains('hidden')) openModal();
      else closeModal();
    }
  });

  // Search with Pagefind
  let debounceTimer: ReturnType<typeof setTimeout>;
  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const query = input.value.trim();

    if (!query) {
      if (resultsList) resultsList.innerHTML = '';
      if (loadingEl) loadingEl.classList.add('hidden');
      if (emptyEl) emptyEl.classList.remove('hidden');
      if (noResultsEl) noResultsEl?.classList.add('hidden');
      return;
    }

    debounceTimer = setTimeout(async () => {
      if (!resultsList || !loadingEl || !emptyEl || !noResultsEl) return;

      resultsList.innerHTML = '';
      loadingEl.classList.remove('hidden');
      emptyEl.classList.add('hidden');
      noResultsEl.classList.add('hidden');

      try {
        if (typeof (window as any).pagefind !== 'undefined') {
          const pagefind = (window as any).pagefind;
          const search = await pagefind.search(query, {
            excerptLength: 30,
          });

          loadingEl.classList.add('hidden');

          if (!search?.results?.length) {
            noResultsEl.classList.remove('hidden');
            return;
          }

          for (const result of search.results.slice(0, 10)) {
            const data = await result.data();
            const el = document.createElement('a');
            el.href = data.url;
            el.className = 'block p-3 rounded-lg hover:bg-primary-50 transition-colors border border-transparent hover:border-primary-100';
            el.innerHTML = `
              <div class="text-sm font-semibold text-primary-800">${data.meta?.title || data.url}</div>
              <div class="text-xs text-primary-400 mt-1 line-clamp-2">${data.excerpt || ''}</div>
            `;
            resultsList.appendChild(el);
          }
        } else {
          // Pagefind not available (dev mode or not built)
          loadingEl.classList.add('hidden');
          noResultsEl.classList.remove('hidden');
          if (noResultsEl) noResultsEl.innerHTML = '<div class="text-center py-8 text-primary-400 text-sm">搜索功能需构建后可用（运行 npm run build 后预览）</div>';
        }
      } catch (err) {
        console.error('Pagefind search error:', err);
        loadingEl.classList.add('hidden');
        noResultsEl.classList.remove('hidden');
      }
    }, 300);
  });
}
