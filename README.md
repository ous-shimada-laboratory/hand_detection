<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク一覧 -->
  <!-- バックエンドのフレームワーク一覧 -->
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- ミドルウェア一覧 -->
  <!-- インフラ一覧 -->
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)
5. [トラブルシューティング](#トラブルシューティング)

<!-- READMEの作成方法のドキュメントのリンク -->
<br />
<div align="right">
    <a href="READMEの作成方法のリンク"><strong>READMEの作成方法 »</strong></a>
</div>
<br />
<!-- Dockerfileのドキュメントのリンク -->
<div align="right">
    <a href="Dockerfileの詳細リンク"><strong>Dockerfileの詳細 »</strong></a>
</div>
<br />
<!-- プロジェクト名を記載 -->

## 肌色検出アプリケーション

 <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">を用いた肌色検出アプリケーションです。

<!-- プロジェクトについて -->

## プロジェクトについて

島田研究室2025/05/16提出分。
1. OpenCVを用いたプログラムを開発できる環境を整えなさい。PythonまたはVisual Cとする。

2. 次のプログラムを作成し，ソースコードを印刷して提出しなさい。
　(1) 実行すると，Webカメラからの動画像がリアルタイムに表示される。
　(2) 手をかざした状態でスペースバーを押すと，そのカラー画像がキャプチャされる。
　(3) キャプチャしたカラー画像について，肌色部分を白，それ以外の部分を黒に変換する。
　(4) 変換された画像を "hand.png" というPNGフォーマット画像で保存する。

<!-- プロジェクトの概要を記載 -->

  <p align="left">
    <br />
    <!-- プロジェクト詳細にBacklogのWikiのリンク -->
    <a href="https://classroom.google.com/c/NzE2MTUxMDc4NjY1/a/Nzc4Nzk2MTA5MjQy/details"><strong>プロジェクト詳細 »</strong></a>
    <br />
    <br />

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python3                | 3.12.3     |




<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->

--hand_dection.py<br>
--README.md<br>
--skin_detection_results

<p align="right">(<a href="#top">トップへ</a>)</p>

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

### 必要条件
- Python 3.6以上
- OpenCV 4.x
- NumPy

```bash
pip3 install opencv-python numpy
```

## 実行方法
```bash
 python3 hand_detection.py 
```

## 問い合わせ先

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝<br>
株式会社アニメツーリズム<br>
取締役CTO　担当：川上<br>
sota@jam-info.com<br>

株式会社アニメツーリズム・JapanAnimeMaps運営<br>
お問い合わせ<br>
contact@animetourism.co.jp<br>

公式サイト<br>
https://animetourism.co.jp<br>

お問い合わせフォーム<br>
https://animetourism.co.jp/contact.html<br>

アプリはこちら<br>
https://apps.apple.com/jp/app/japananimemaps/id6608967051<br>

〒150-0043<br>
東京都 渋谷区道玄坂1丁目10番8号渋谷道玄坂東急ビル2F-C<br>
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝<br>
※本文に掲載された記事を許可なく転載することを禁じます。<br>
(c)2024 JapanAnimeMaps.All Rights Reserved.<br>

<p align="right">(<a href="#top">トップへ</a>)</p>
