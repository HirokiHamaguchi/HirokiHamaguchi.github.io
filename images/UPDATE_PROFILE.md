# プロフィール画像の更新手順

## 新しいプロフィール画像（ダイヤモンド/クリスタル画像）への更新

### 手順

1. **画像のダウンロード**
   - 提供されたURL（https://github.com/user-attachments/assets/7bbab496-4606-4dcc-b27f-ebfeb148589a）から画像を右クリックして保存
   - または、ブラウザで画像を開いて「名前を付けて保存」
   - ファイル名を `profile.png` として保存

2. **画像の配置**
   - 保存した画像を `/images/` ディレクトリに配置
   - 既存の `profile.png` を上書き、または別の名前で保存してスクリプトを更新

3. **OGP画像の再生成**
   ```bash
   cd images
   python create_ogp_image.py
   ```

4. **確認**
   - 生成された `ogp-image.png` (1200x630ピクセル) を確認
   - 黒背景の中央にダイヤモンド/クリスタル画像が配置されているはず

5. **コミットとプッシュ**
   ```bash
   git add images/profile.png images/ogp-image.png
   git commit -m "Update profile and OGP images with new crystal design"
   git push
   ```

### 別の方法：スクリプトでの直接指定

`create_ogp_image.py` の最後の部分を編集して、異なる入力ファイルを使用することもできます：

```python
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 新しい画像ファイル名を指定
    input_path = os.path.join(script_dir, "your_new_image.png")
    output_path = os.path.join(script_dir, "ogp-image.png")
    
    if not os.path.exists(input_path):
        print(f"エラー: 入力画像が見つかりません: {input_path}")
        exit(1)
    
    create_ogp_image(input_path, output_path)
```

## 注意事項
- GitHub Assets URLは直接ダウンロードできないため、手動でダウンロードする必要があります
- 画像は黒背景と相性が良いデザインなので、現在のスクリプト設定がぴったりです
