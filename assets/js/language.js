document.addEventListener('DOMContentLoaded', function () {
  const controls = document.querySelector('.language-switch');
  if (!controls) return;

  const storageKey = 'site-language';
  const sections = document.querySelectorAll('[data-site-language]');
  const buttons = controls.querySelectorAll('[data-language]');
  // Browser languages are ordered by preference, including regional tags.
  // https://developer.mozilla.org/en-US/docs/Web/API/Navigator/languages
  const preferredLanguages = navigator.languages?.length ? navigator.languages : [navigator.language];
  let initialLanguage = preferredLanguages
    .map(language => (language || '').toLowerCase().split('-')[0])
    .find(language => language === 'ja' || language === 'en') || 'en';
  try {
    const savedLanguage = localStorage.getItem(storageKey);
    if (savedLanguage === 'en' || savedLanguage === 'ja') initialLanguage = savedLanguage;
  } catch (error) {
    // Storage can be unavailable in private browsing; switching still works.
  }

  function selectLanguage(language, remember = false) {
    document.documentElement.lang = language;
    sections.forEach(section => { section.hidden = section.dataset.siteLanguage !== language; });
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.language === language));
    });
    const title = document.body.dataset[language === 'ja' ? 'titleJa' : 'titleEn'];
    if (title) document.title = title + ' - Hiroki Hamaguchi';
    // Persist explicit choices, so an automatic default does not lock the language.
    if (remember) {
      try {
        localStorage.setItem(storageKey, language);
      } catch (error) {
        // A storage failure must not prevent changing the current page.
      }
    }
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => selectLanguage(button.dataset.language, true));
  });
  selectLanguage(initialLanguage);
  controls.hidden = false;
});
