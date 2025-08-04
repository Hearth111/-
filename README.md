# Stream Topic Detector

Flaskサーバーと簡易CSSエディターからなるツール。POSTされたテキストを音声認識結果とみなし、話題の切り替わりを検出してOBSに表示します。

## 使い方

### サーバー

```
python run_display.py
```

- `POST /submit` にテキストを送信すると話題が更新され、必要に応じて `logs/` にタイムスタンプ付きで記録されます。
- `GET /topic` で現在の話題をJSON形式で取得できます。

### CSSエディター

PyQt5製のGUIでCSSを編集します。以下のコマンドでエディターを起動します。

```
python run_editor.py
```

1. 起動後、テーマ選択ドロップダウンでテンプレートを読み込みます。
2. フォントやCSSを編集すると右側のプレビューに即時反映されます。
3. 「保存」ボタンで `static/css/style.css` に書き込みます。

> 補足: CLIからCSSファイルを読み込ませる場合は `python run_editor.py < my_style.css` を実行できます。

## ビルド

PyInstaller を使用して実行ファイルを作成できます。

```
pip install pyinstaller
pip install -r requirements.txt
pyinstaller run_display.spec
pyinstaller run_editor.spec
```

`dist/` ディレクトリにそれぞれの実行ファイルが生成されます。
