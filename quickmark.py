
import os
from PIL import Image, ImageDraw, ImageFont

# 定数の設定
FONT_PATH = 'arial.ttf'  # フォントファイルへのパス
FONT_SIZE = 36  # フォントのサイズ
WATERMARK_TEXT = 'Sample Watermark'  # ウォーターマークのテキスト（英語）
WATERMARK_POSITION = 2  # ウォーターマークの位置: 1 = 上部, 2 = 中央, 3 = 下部
TRANSPARENCY = 50  # ウォーターマークの透明度（100=不透明, 0=透明）
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp']  # 対応する画像ファイルの拡張子

def add_watermark(image_path, output_path):
    # 画像ファイルを開いてRGBAに変換
    with Image.open(image_path).convert("RGBA") as base:
        # ウォーターマーク用の透明レイヤーを作成
        watermark_layer = Image.new("RGBA", base.size)
        draw = ImageDraw.Draw(watermark_layer)
        # フォントの設定
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        # テキストのバウンディングボックスからテキストサイズを計算
        text_bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        # ウォーターマークの位置を計算
        if WATERMARK_POSITION == 1:
            position = ((base.width - text_width) / 2, (base.height / 4) - text_height / 2)
        elif WATERMARK_POSITION == 2:
            position = ((base.width - text_width) / 2, (base.height / 2) - text_height / 2)
        elif WATERMARK_POSITION == 3:
            position = ((base.width - text_width) / 2, (3 * base.height / 4) - text_height / 2)
        # 指定した透明度でウォーターマークを描画
        draw.text(position, WATERMARK_TEXT, font=font, fill=(255, 255, 255, int(255 * TRANSPARENCY / 100)))
        # ウォーターマークレイヤーを元の画像に合成しRGBに変換
        combined = Image.alpha_composite(base, watermark_layer).convert("RGB")
        # 最終的な画像をJPEG形式で保存
        combined.save(output_path, 'JPEG')

def process_directory(directory_path):
    # 出力ディレクトリのパスを設定
    output_directory = os.path.join(directory_path, "watermarked_images")
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # ディレクトリ内の全ファイルを処理
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # 対応する画像ファイル形式のみを処理
        if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in IMAGE_EXTENSIONS):
            output_path = os.path.join(output_directory, f"wm_{filename}")
            add_watermark(file_path, output_path)
            print(f"Processed {filename}")

if __name__ == '__main__':
    # ユーザーに画像が保存されているディレクトリのパスを入力させる
    directory_path = input("画像が保存されているディレクトリのパスを入力してください: ")
    process_directory(directory_path)
