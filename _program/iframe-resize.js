// iframe の高さを自動調整するスクリプト
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
window.addEventListener('message', function (e) {
    if (e.data && e.data.type === 'resize' && e.data.iframeId) {
        const iframe = document.getElementById(e.data.iframeId);
        if (iframe) {
            iframe.style.height = e.data.height + 'px';
        }
    }
});
