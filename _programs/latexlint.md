---
title: "LaTeX Lint"
authors: 'Hiroki Hamaguchi'
collection: programs
permalink: /programs/latex-lint
excerpt: 'Linter for LaTeX with useful commands for academic writing.'
thumbnail: "https://github.com/HirokiHamaguchi/latexlint/blob/master/images/mainIcon512.png?raw=true"
date: 2025-01-06
---

This is a VS Code extension that provides a Linter for LaTeX with useful commands for academic writing. The following is the [web version](https://hirokihamaguchi.github.io/latexlint/) of the extension.

<iframe
  id="latexlint-iframe"
  src="https://hirokihamaguchi.github.io/latexlint/"
  width="100%"
  style="border:none; min-height:600px;"
  title="LaTeX Lint"
  loading="lazy"
  onload="resizeIframe(this)">
</iframe>

<script>
function resizeIframe(iframe) {
  try {
    // 同一オリジンの場合、iframeのコンテンツの高さを取得
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    const height = Math.max(
      iframeDoc.body.scrollHeight,
      iframeDoc.documentElement.scrollHeight
    );
    iframe.style.height = height + 'px';
  } catch (e) {
    // クロスオリジンの場合はエラーをキャッチ
    console.log('Cannot access iframe content height:', e);
    iframe.style.height = '800px'; // フォールバック
  }
}

// コンテンツの変更を監視して高さを再調整
window.addEventListener('message', function(e) {
  if (e.data && e.data.type === 'resize') {
    const iframe = document.getElementById('latexlint-iframe');
    if (iframe) {
      iframe.style.height = e.data.height + 'px';
    }
  }
});
</script>
