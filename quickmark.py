import os
from PIL import Image, ImageDraw, ImageFont

# 定数の設定
FONT_PATH = 'arial.ttf'  # 使用するフォントファイルのパス
FONT_SIZE = 36  # フォントサイズ
WATERMARK_TEXT = 'Sample Watermark'  # ウォーターマークのテキスト
WATERMARK_POSITION = 2  # ウォーターマークの位置（1=上部、2=中央、3=下部）
TRANSPARENCY = 50  # ウォーターマークの透明度（100=完全不透明、0=透明）
SHADOW_OFFSET = 2  # 影のオフセット（ピクセル）
SHADOW_ENABLED = True  # 影を有効にするかどうか
SHADOW_TRANSPARENCY = 70  # 影の透明度（100=完全不透明、0=透明）
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp']  # 処理対象の画像ファイル拡張子

def add_watermark_with_shadow(image_path, output_path):
    """指定された画像にウォーターマークを追加する関数"""
    with Image.open(image_path).convert("RGBA") as base:
        # ウォーターマークを追加するための透明レイヤーを作成
        watermark_layer = Image.new("RGBA", base.size)
        draw = ImageDraw.Draw(watermark_layer)
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

        # 影を描画する場合
        if SHADOW_ENABLED:
            shadow_position = (position[0] + SHADOW_OFFSET, position[1] + SHADOW_OFFSET)
            shadow_color = (0, 0, 0, int(255 * SHADOW_TRANSPARENCY / 100))
            draw.text(shadow_position, WATERMARK_TEXT, font=font, fill=shadow_color)

        # メインのテキストを描画
        text_color = (255, 255, 255, int(255 * TRANSPARENCY / 100))
        draw.text(position, WATERMARK_TEXT, font=font, fill=text_color)
        
        # 透明レイヤーを基本画像に合成し、RGB形式に変換
        combined = Image.alpha_composite(base, watermark_layer).convert("RGB")
        # 処理後の画像を保存
        combined.save(output_path, 'JPEG')

def process_directory(directory_path):
    """指定されたディレクトリ内の全画像にウォーターマークを追加する関数"""
    output_directory = os.path.join(directory_path, "watermarked_images")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # 出力ディレクトリが存在しない場合は作成

    # ディレクトリ内の全ファイルを処理
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        file_ext = os.path.splitext(filename)[1].lower()  # 拡張子を小文字で取得
        if os.path.isfile(file_path) and any(file_ext == ext for ext in IMAGE_EXTENSIONS):
            output_path = os.path.join(output_directory, f"wm_{filename}")
            add_watermark_with_shadow(file_path, output_path)
            print(f"Processed {filename}")

if __name__ == '__main__':
    # ユーザーから画像が格納されたディレクトリのパスを入力させる
    directory_path = input("画像が保存されているディレクトリのパスを入力してください: ")
    process_directory(directory_path)
