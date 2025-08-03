# AGENTS.md

## 🎯 プロジェクト概要

### 名前
Stream Topic Detector

### 概要
配信者が話している内容をリアルタイムで音声認識し、話題の切り替わりを自動検出してOBSにテロップ表示するツール。加えて、話題が変わるタイミングでタイムスタンプ付きログを保存し、後から見返せるようにする。

CSSによるテロップの見た目調整は、OBSに読み込ませるブラウザ表示用のCSSを編集するGUIアプリ（デスクトップ用）で行う。

---

## 🔧 開発対象と構成

以下の2つの主要コンポーネントを実装対象とする：

1. `display_server/`  
   - FlaskベースのローカルWebサーバー  
   - 音声認識、話題検出、OBSに読み込ませるHTMLページの生成、タイムスタンプの記録を担当

2. `css_editor/`  
   - PyQt5ベースのGUIスタイルエディター  
   - `static/css/style.css` を編集・保存可能
   - ローカルのフォント一覧から選択し、プレビュー表示付き

---

## 📁 ディレクトリ構成（初期）

stream-topic-detector/
├── display_server/
│ ├── main.py # Flask起動と処理ループ
│ ├── audio_listener.py # 音声入力処理
│ ├── transcriber.py # Whisperなどで音声→テキスト
│ ├── topic_detector.py # 話題の切り替わり検出
│ ├── timestamp_logger.py # タイムスタンプログ記録
│ └── config.py # 各種パラメータ
│
├── templates/
│ ├── display.html # OBS表示用HTML
│
├── static/
│ └── css/
│ ├── style.css # 現在使用中のCSS（OBS表示用）
│ ├── dark.css # テンプレート例
│ ├── light.css # テンプレート例
│ └── fun.css # テンプレート例
│
├── css_editor/
│ ├── editor.py # PyQt5製CSSスタイルエディターGUI
│ ├── themes/ # CSSテンプレート
│ │ ├── dark.css
│ │ ├── light.css
│ │ └── fun.css
│ └── assets/
│ └── icon.png
│
├── logs/
│ └── topics_YYYY-MM-DD.txt # 話題ごとのタイムスタンプログ
│
├── requirements.txt # Python依存パッケージ
├── run_display.bat # OBS用ローカルサーバー起動用
├── run_editor.bat # CSSエディター起動用
└── README.md # プロジェクト説明


---

## 🧠 システム仕様

### 音声認識
- `audio_listener.py`：マイクや仮想オーディオデバイスから音声取得
- `transcriber.py`：Whisper API（またはローカル）でリアルタイム文字起こし
- 分割処理：5〜15秒ごとに区切る

### 話題検出
- `topic_detector.py`：
  - 直前の発話と比較して類似度が低い場合に話題変更と判断
  - LLM APIまたはTF-IDFで比較
- 切り替えが発生したら：
  - `topic_box` に新しい話題を表示
  - `timestamp_logger.py` により `logs/` に記録

### テロップ表示
- Flaskの `/` にアクセスで `display.html` を提供
- `display.html` は常に `/static/css/style.css` を読み込む
- OBSでは `http://localhost:5000/` をブラウザソースとして追加

---

## 🎨 CSSエディター仕様（`css_editor/editor.py`）

### 使用ライブラリ
- `PyQt5`

### 画面構成
| 要素          | 機能                                                         |
|---------------|--------------------------------------------------------------|
| テーマ選択    | `themes/` のCSSを選んで読み込み（ドロップダウン）           |
| CSSエディタ   | 編集用のテキストエリア                                       |
| フォント選択  | PC内のフォント一覧を取得し選択（`QFontComboBox`）           |
| プレビュー    | 指定フォント＆CSSで `QLabel` にリアルタイム表示              |
| 保存ボタン    | `static/css/style.css` にCSSを保存                           |

---

## 📦 exe化

- `display_server/main.py` → `run_display.exe`
- `css_editor/editor.py` → `run_editor.exe`
- `PyInstaller` を想定した `.spec` ファイルを用意する（任意）

---

## ✅ 完了条件（Done Criteria）

1. FlaskサーバーがOBS用ブラウザ出力と音声認識・話題切り替え・タイムスタンプ記録を実装済み
2. CSSファイルを選択・編集・保存できるGUIが完成している
3. GUIから保存されたCSSがOBSに即時反映される構造になっている
4. ディレクトリ構成が上記通りで再現性がある

---

## 📝 備考・注意点

- 音声認識は基本的にローカル動作前提（Whisper.cppやVosk）
- 話題抽出精度は重要視せず、実用的な閾値ベースでもOK
- `display.html` は背景透過にし、OBS上で自然に表示できるスタイルに

---


## 改善提案

- Flaskアプリがモジュールレベルのグローバル変数 `_current_topic` と `_previous_text` を直接参照しており、並列アクセス時に状態が競合する恐れがある。アプリコンテキストや永続ストレージを用いた状態管理が望ましい
- 表示ページは `setInterval` による1秒ごとのポーリングで話題取得を行っているが、Server-Sent Events や WebSocket を導入するとよりリアルタイム性と効率が向上する
- 話題判定は単語集合のジャッカード係数のみを用いた簡易比較であり、形態素解析や埋め込みベクトルを利用したセマンティック類似度を活用すれば精度を高められる
- 音声認識部は入力バイト列をそのままテキスト化するだけで実質的な認識処理が行われていない。実際の音声認識ライブラリ（Whisper 等）を組み込み、失敗時の例外処理も追加した方が良い
- CSS エディターは標準入力からCSSを保存する簡易CLIであり、仕様にあるGUI機能（プレビュー・フォント選択・テーマ選択など）の実装が未完了である
- 依存パッケージが `flask` しか記載されておらず、将来的に必要となる PyQt5 やテスト用ライブラリ等を明記し、バージョンも固定して再現性を確保するべきである
- テストは2ファイルのみで対象範囲が狭く、音声入力やCSSエディタ、異常系などのケースが不足しているため、モジュールごとに網羅的なテストを追加して品質を担保する必要がある
- ログ出力や設定値が散在しており、標準 `logging` モジュールや環境変数ベースの設定を導入することで運用時の拡張性・保守性を高められる


