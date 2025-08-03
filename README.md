# Stream Topic Detector

Flaskサーバーと簡易CSSエディターからなるツール。POSTされたテキストを音声認識結果とみなし、話題の切り替わりを検出してOBSに表示します。

## 使い方

### サーバー

```
python -m display_server.main
```

- `POST /submit` にテキストを送信すると話題が更新され、必要に応じて `logs/` にタイムスタンプ付きで記録されます。
- `GET /topic` で現在の話題をJSON形式で取得できます。

### CSSエディター

標準入力からCSSを読み取り `static/css/style.css` に保存します。

```
python -m css_editor.editor < my_style.css
```
