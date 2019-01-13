# 概要
**SenbayKit-CLI** は、**SenbayVideo** の生成と解析をコマンドライン、またはPythonプログラム内から利用するためのライブラリである。SenbayVideoとは、動画の各フレームにセンサデータ（QRコード）が埋め込まれた動画のことであり、動画と共に容易にセンサデータの記録と配信を可能にする。

## 開発環境
本ライブラリは、Python3をベースに構築されており、以下の外部ライブラリに依存している。
 * NumPy
 * OpenCV 3
 * fastzbarlight
 * qrcode

ライブラリの開発はmacOS 10.12 (Sierra)で行なったが、他のUNIX系OSでも動作する。

### pip を使った依存ライブラリのインストール
```
pip install numpy
pip install opencv-python
pip install fastzbarlight
pip install qrcode
```

### setup.py を使った **SenbayKit** のインストール
SenbayKit-CLIのホームディレクトリに移動し、以下のコマンドを実行する。`senbay`パッケージがインストールされる。
```
python setup.py install
```

## 使用方法
### SenbayCamera
**SenbaCamera** は、(1)カメラモジュールから映像を読み込み、(2)各フレームにセンサデータ（=SenbayFormat）が保存されたQRコードを埋め込み、(3)動画ファイル（Senbay Video）として出力するアプリケーションである。

コマンドラインからの起動は以下のコマンドで実行できる。
```
$ ./sample_camera.py
```

オプションは以下の通り指定できる。

|短縮オプションキー|オプションキー|デフォルト値|
|-w| --width        |640 |
|-h| --height       |360 |
|-o| --video-output |'senbay_video_output.m4v' |
|-i| --camera-input |0  |
|-f| --fps          |30 |
|-t| --threads      |10 |

pythonコード内で利用する場合には、まず`senbay`パッケージから`SenbayCamera`モジュールをインポートし初期化する。起動時にコードバック関数を与えることで、QRコードの生成と、終了イベントをハンドルできる。

```python
from senbay import SenbayCamera

def generateContent:
  return "generate and return a QRcode content"

def complete():
  print("done")

camera = SenbayCamera()
camera.start(generateContent,complete)
```

#### NOTE
* CPU+シングルスレッドでは、10FPSが限界。
* パフォーマンス向上の為にマルチスレッド化を行い、「映像撮影」と「映像合成+動画ファイルへの書き込み」部分は切り分けたが、少し不安定（フレームの時々順番が入れ替わる）。スレッド数の上限（デフォルトでは10）を設定しないと、スレッドは無限に増え続け、300を超えたところでクラッシュする。
* macOS Mojave では、QRコード合成済みの動画を出力しようとするとクラッシュする。どうやら画面に画像表示する場合は、メインスレッドで `cv2.imshow` を実行する必要がある。一時的に、カメラインプットをそのまま表示している。
* スレッド管理は、順番が保証される `queue` が適切。今後修正予定。

#### TODO
- [x] マルチスレッド化
- [x] 各種設定をオプションで指定
- [ ] Queueの利用
- [ ] GPUの利用
- [ ] UIの修正
- [ ] 他プラットフォームでのテスト（Raspberry Piなど）

### SenbayReader
**Senbay Reader** は、Senbay Video内に埋め込まれたQRコードから、センサデータを取り出すアプリケーションである。

以下のコードでコマンドラインからSenbay Readerを起動できる。
第一引数にSenbay Videoのパスをしていることで、ビデオを再生しながら、QRコード内に保存されているセンサデータをリアルタイムに取得できる。

```
$ ./sample_reader.py video_path
```

Pythonコード内で利用する場合には、`senbay`パッケージから`SenbayReader`モジュールをインポートし、`SenbayReader`の初期化する。初期化時に、Senbay Videoのパスを指定する。`start`関数実行時に、コールバック関数を与えることで、SenbayReaderが検出したデータをその都度受け取ることができる。

```python
from senbay import SenbayReader

def showResult(self, data):
  print(data)

reader = SenbayReader(video_path)
reader.start(showResult)
```

#### TODO
 - [ ] マルチスレッド化
 - [x] 各種設定をオプションで指定
 - [ ] GPUの利用
 - [ ] UIの修理
 - [ ] 他プラットフォームでのテスト（Raspberry Piなど）

### SenbayFormat
SenbayFormatデータの生成
```
from senbay import SenbayData

sd = SenbayData()
sd.addNumber('key',value);
sd.addText('key','value');
sampleData = sd.getSenbayFormattedData(False); # or True (= with Base-122 Data Compression)
print(sampleData);

```

### SenbayFormat
SenbayFormatデータの解析
```
from senbay import SenbayData
sd = SenbayData()
senbayFormatText = 'V:3,TIME:123456,ACCX:1234,ACCY:56789';
dictData = sd.getSenbayDataAsDect(senbayFormatText);
print(dictData)
```


## Author and Contributors
**SenbayKit-CLI** is authord by [Yuuki Nishiyama](http://www.yuukinishiyama.com). In addition, [Takuro Yonezawa](https://www.ht.sfc.keio.ac.jp/~takuro/), [Denzil Ferreira](http://www.oulu.fi/university/researcher/denzil-ferreira), [Anind K. Dey](http://www.cs.cmu.edu/~anind/), [Jin Nakazawa](https://keio.pure.elsevier.com/ja/persons/jin-nakazawa) are deeply contributing this project. Please see more detail information on our [website](http://www.senbay.info).

## Related Links
* [Senbay Platform Website](http://www.senbay.info)
* [Senbay YouTube Channel](https://www.youtube.com/channel/UCbnQUEc3KpE1M9auxwMh2dA/videos)

## Citation
Please cite these papers in your publications if it helps your research:

```
@inproceedings{Nishiyama:2018:SPI:3236112.3236154,
author = {Nishiyama, Yuuki and Dey, Anind K. and Ferreira, Denzil and Yonezawa, Takuro and Nakazawa, Jin},
title = {Senbay: A Platform for Instantly Capturing, Integrating, and Restreaming of Synchronized Multiple Sensor-data Stream},
booktitle = {Proceedings of the 20th International Conference on Human-Computer Interaction with Mobile Devices and Services Adjunct},
series = {MobileHCI '18},
year = {2018},
location = {Barcelona, Spain},
publisher = {ACM},
}
```

## License

SenbayKit-CLI is available under the Apache License, Version 2.0 license. See the LICENSE file for more info.
