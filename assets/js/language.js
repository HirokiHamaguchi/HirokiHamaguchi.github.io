document.addEventListener('DOMContentLoaded', function () {
  const controls = document.querySelector('.language-switch');
  if (!controls) return;

  const storageKey = 'site-language';
  const sections = document.querySelectorAll('[data-site-language]');
  const buttons = controls.querySelectorAll('[data-language]');
  let initialLanguage = 'ja';
  try {
    const savedLanguage = localStorage.getItem(storageKey);
    if (savedLanguage === 'en' || savedLanguage === 'ja') initialLanguage = savedLanguage;
  } catch (error) {
    // Storage can be unavailable in private browsing; switching still works.
  }

  function selectLanguage(language) {
    document.documentElement.lang = language;
    sections.forEach(section => { section.hidden = section.dataset.siteLanguage !== language; });
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.language === language));
    });
    const title = document.body.dataset[language === 'ja' ? 'titleJa' : 'titleEn'];
    if (title) document.title = title + ' - Hiroki Hamaguchi';
    try {
      localStorage.setItem(storageKey, language);
    } catch (error) {
      // A storage failure must not prevent changing the current page.
    }
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => selectLanguage(button.dataset.language));
  });
  selectLanguage(initialLanguage);
  controls.hidden = false;
});
