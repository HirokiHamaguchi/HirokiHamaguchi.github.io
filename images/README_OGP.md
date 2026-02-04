# OGP画像の設定方法

## 概要
このディレクトリには、ブログのOGP（Open Graph Protocol）画像を生成するためのスクリプトとリソースが含まれています。

## 使用方法

### 1. プロフィール画像の準備
新しいプロフィール画像を使用する場合は、以下の手順で画像を準備してください：

1. 使いたい画像をダウンロードして、`profile.png` という名前でこのディレクトリに保存します
2. または、既存の `profile.png` を新しい画像で置き換えます

### 2. OGP画像の生成
以下のコマンドを実行して、OGP画像を生成します：

```bash
cd images
python create_ogp_image.py
```

このスクリプトは以下の処理を行います：
- `profile.png` を読み込み
- アスペクト比を維持したまま、1200x630のOGP標準サイズにリサイズ
- 画像を中央に配置し、不足分を黒背景で埋める
- `ogp-image.png` として保存

### 3. 生成された画像の確認
生成された `ogp-image.png` を確認してください。サイズは1200x630ピクセルになっているはずです。

### 4. GitにコミットしてPush
変更をコミットしてGitHubにプッシュすると、自動的にブログに反映されます。

## OGP画像の仕様
- **サイズ**: 1200 x 630 ピクセル（OGP標準サイズ）
- **背景**: 黒 (#000000)
- **配置**: プロフィール画像を中央に配置

## メタタグ
OGP画像は `_layouts/default.html` で以下のメタタグとして設定されています：

```html
<meta property="og:image" content="https://hirokihamaguchi.github.io/images/ogp-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://hirokihamaguchi.github.io/images/ogp-image.png">
```

これにより、ブログのリンクがTwitterやFacebookなどのSNSで共有されたときに、美しいリンクカードが表示されます。

## トラブルシューティング

### Pillowがインストールされていない場合
```bash
pip install Pillow
```

### 画像が正しく生成されない場合
- `profile.png` が存在することを確認してください
- 画像形式が対応している形式（PNG、JPEG等）であることを確認してください
- スクリプトの実行権限を確認してください
