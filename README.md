# 概要
**SenbayKit-CLI** は、**SenbayVideo** の生成と解析をコマンドライン、またはPythonプログラム内から利用するためのライブラリです。SenbayVideoとは、動画の各フレームにセンサデータ（QRコード）が埋め込まれた動画のことであり、動画と共に容易にセンサデータの記録と配信を可能にします。


<p align="center">
    <img src="media/image/senbay_reader_demo.gif", width="640">
</p>

## 開発環境
本ライブラリは、Python3をベースに構築されており、以下の外部ライブラリに依存しています。
 * NumPy
 * OpenCV 3
 * fastzbarlight
 * qrcode
 * mss

ライブラリの開発はmacOS 10.12 (Sierra)で行なったが、他のUNIX系OSでも動作します。

### 依存ライブラリのインストール
```command
pip install numpy
pip install opencv-python
pip install fastzbarlight
pip install qrcode
pip install mss
```

### **SenbayKit** のインストール
SenbayKit-CLIのホームディレクトリに移動し、以下のコマンドを実行すると、`senbay`パッケージがインストールされます。
```command
python setup.py install
```

または、`pip`を使ってGitHubから直接インストールすることもできます。
```command
pip install git+https://github.com/tetujin/SenbayKit-CLI
```

## 使用方法
### SenbayCamera
**SenbaCamera** は、(1)カメラモジュールから映像を読み込み、(2)各フレームにセンサデータ（=SenbayFormat）が保存されたQRコードを埋め込み、(3)動画ファイル（Senbay Video）として出力するアプリケーションです。

ダウンロードしたSenbayKit-CLIのホームディレクトリに移動し、以下のコマンドで実行できます。
```command
./sample_camera.py
```

また、動画のサイズや、出力先、フレームレートなどは、以下のオプションを使って指定できます。

| オプション | デフォルト値 |
| ---- | ---- |
| -w --width        | 640 |
| -h --height       | 360 |
| -o --video-output | 'senbay_video_output.m4v' |
| -i --camera-input | 0  |
| -f --fps          | 30 |
| -t --threads      | 10 |

pythonコード内で利用する場合には、まず`senbay`パッケージから`SenbayCamera`モジュールをインポートし、初期化します。起動時にコードバック関数を与えることで、QRコードの生成と、終了イベントをハンドルできます。

```python
from senbay import SenbayCamera

def get_content():
  return "generate and return a QRcode content"

def complete():
  print("done")

camera = SenbayCamera()
camera.start(get_content,complete)
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
**Senbay Reader** は、Senbay Video内に埋め込まれたQRコードから、センサデータを取り出すアプリケーションです。

ダウンロードしたSenbayKit-CLIのホームディレクトリに移動し、以下のコマンドでSenbay Readerを起動する。第一引数にSenbay Videoへのパスを指定することで、ビデオを再生しながら、QRコード内に保存されているセンサデータをリアルタイムに取得できる。

```command
./sample_reader.py video_path
```

Pythonコード内で利用する場合には、`senbay`パッケージから`SenbayReader`モジュールをインポートし、`SenbayReader`の初期化する。SenbayReaderは、ビデオ(0)・カメラ(1)・スクリーン(2)の三通りの画像の取得先を選択できる。`start`関数実行時に、コールバック関数を与えることで、SenbayReaderが検出したデータをその都度受け取ることができる。

ビデオモードでは、指定したSenbay動画からQRコードを検出できる。ビデオの場合は、SenbayReaderモードを`mode='video'`（または`mode=0`）にし、ローカルのSenbay動画からパスを与える。

```python
# ビデオモード
from senbay import SenbayReader

def showResult(self, data):
  print(data)

reader = SenbayReader(mode='video', video_in='path_to_senbay_video')
reader.start(showResult)
```

カメラ・スクリーンモードでは、カメラまたはスクリーン上からQRコードを検出できる。SenbayReaderモードを、カメラの場合は`mode='camera'`（または`mode=1`）、スクリーンの場合には、`mode='screen'`（または`mode=2`）に設定する。スクリーンモードでは加えて、キャプチャ領域の指定が必要です。

```python
# カメラモード
from senbay import SenbayReader

def showResult(self, data):
    print(data)

reader = SenbayReader(mode='camera')
reader.start(showResult)
```

```python
# スクリーンモード
from senbay import SenbayReader

cap_area = {'top':200, 'left':200, 'width':200, 'height':200}

def showResult(self, data):
    print(data)

reader = SenbayReader(mode='screen', cap_area=cap_area)
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
```python
from senbay import SenbayData

sd = SenbayData()
sd.add_number('key',value);
sd.add_text('key','value');
print(sd.encode());
```

### SenbayFormat
SenbayFormatデータの解析
```python
from senbay import SenbayData
sd = SenbayData()
senbayFormatText = 'V:3,TIME:123456,ACCX:1234,ACCY:56789';
dict = sd.decode(senbayFormatText);
print(dict)
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
