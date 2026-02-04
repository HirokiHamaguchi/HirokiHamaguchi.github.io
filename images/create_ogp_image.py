#!/usr/bin/env python3
"""
OGP画像生成スクリプト
プロフィール画像を使用して、1200x630のOGP標準サイズの画像を生成します。
画像は中央に配置され、不足分は黒背景で埋められます。
"""

from PIL import Image
import os

# OGP画像の標準サイズ
OGP_WIDTH = 1200
OGP_HEIGHT = 630

# 入力画像ファイル名
INPUT_IMAGE = "profile.png"
# 出力画像ファイル名
OUTPUT_IMAGE = "ogp-image.png"


def create_ogp_image(input_path, output_path, ogp_width=OGP_WIDTH, ogp_height=OGP_HEIGHT):
    """
    プロフィール画像からOGP画像を生成する
    
    Args:
        input_path: 入力画像のパス
        output_path: 出力画像のパス
        ogp_width: OGP画像の幅（デフォルト: 1200）
        ogp_height: OGP画像の高さ（デフォルト: 630）
    """
    # 入力画像を開く
    print(f"入力画像を読み込み中: {input_path}")
    profile_img = Image.open(input_path)
    
    # 画像がRGBAでない場合は変換
    if profile_img.mode != 'RGBA':
        profile_img = profile_img.convert('RGBA')
    
    # 元の画像サイズ
    original_width, original_height = profile_img.size
    print(f"元の画像サイズ: {original_width}x{original_height}")
    
    # アスペクト比を維持しながら、OGPサイズに収まるようにリサイズ
    # 画像の縦横比を計算
    aspect_ratio = original_width / original_height
    ogp_aspect_ratio = ogp_width / ogp_height
    
    if aspect_ratio > ogp_aspect_ratio:
        # 画像が横長の場合、幅を基準にリサイズ
        new_width = ogp_width
        new_height = int(ogp_width / aspect_ratio)
    else:
        # 画像が縦長の場合、高さを基準にリサイズ
        new_height = ogp_height
        new_width = int(ogp_height * aspect_ratio)
    
    # 画像をリサイズ（高品質なLANCZOS補間を使用）
    print(f"画像をリサイズ中: {new_width}x{new_height}")
    resized_img = profile_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 黒背景の新しい画像を作成
    print(f"OGP画像を作成中: {ogp_width}x{ogp_height}")
    ogp_img = Image.new('RGB', (ogp_width, ogp_height), (0, 0, 0))
    
    # リサイズした画像を中央に配置
    x_offset = (ogp_width - new_width) // 2
    y_offset = (ogp_height - new_height) // 2
    
    # RGBAからRGBに変換して貼り付け（透明度を考慮）
    # 黒背景に合成
    rgb_img = Image.new('RGB', resized_img.size, (0, 0, 0))
    rgb_img.paste(resized_img, mask=resized_img.split()[3] if resized_img.mode == 'RGBA' else None)
    
    ogp_img.paste(rgb_img, (x_offset, y_offset))
    
    # 画像を保存
    print(f"OGP画像を保存中: {output_path}")
    ogp_img.save(output_path, 'PNG', optimize=True)
    
    print(f"✓ OGP画像の生成が完了しました: {output_path}")
    print(f"  サイズ: {ogp_width}x{ogp_height}")
    
    # ファイルサイズを表示
    file_size = os.path.getsize(output_path)
    print(f"  ファイルサイズ: {file_size / 1024:.2f} KB")


if __name__ == "__main__":
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 入力・出力パスを設定
    input_path = os.path.join(script_dir, INPUT_IMAGE)
    output_path = os.path.join(script_dir, OUTPUT_IMAGE)
    
    # 入力ファイルの存在確認
    if not os.path.exists(input_path):
        print(f"エラー: 入力画像が見つかりません: {input_path}")
        exit(1)
    
    # OGP画像を生成
    create_ogp_image(input_path, output_path)
