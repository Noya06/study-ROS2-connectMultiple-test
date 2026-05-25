# study-ROS2-connectMultiple-test
2026年度にHR研で行われたROS2勉強会用リポジトリ
「ネットワークを介した複数台ロボット/機器の接続」の実装例

## 概要
このリポジトリはROS2 Humbleで複数PC/機器間のトピック通信を行うための最小構成サンプルを含みます。

パッケージ: `multi_comm`（Python, ament_python）

## ファイル構成
- `multi_comm/` - パッケージ本体
	- `multi_comm/talker.py` - 単純なパブリッシャ（`chatter`）
	- `multi_comm/listener.py` - 単純なサブスクライバ（`chatter`）
	- `package.xml`, `setup.py`, `setup.cfg`, `resource/multi_comm`

## 必要環境
- ROS2 Humble が各マシンにインストールされていること
- 同一ネットワーク上でICMP（ping）やUDPマルチキャストが許可されていること（ファイアウォール確認）

## ビルドと実行
ワークスペースルート（このREADMEがあるディレクトリ）で:

```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

ノード実行例:

```bash
# パブリッシャ（PC A）
ros2 run multi_comm talker

# サブスクライバ（PC B）
ros2 run multi_comm listener
```

同一ネットワーク内であれば、`talker`が送る`chatter`メッセージを別のPC上の`listener`が受信します。

## マルチPCでの接続手順（要点）
1. 各マシンでROS2 Humbleをインストール・セットアップする。
2. ネットワークで相互に疎通確認（`ping`）。
3. 必要に応じてファイアウォールでUDPポートやマルチキャストを許可する。
4. 同じROS_DOMAIN_IDを使う（デフォルト0で問題ないことが多い）。
	 例: `export ROS_DOMAIN_ID=0`
5. （DDS実装に依存）`RMW_IMPLEMENTATION`を揃える。
	 例: `export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` または `rmw_fastrtps_cpp`

## トラブルシューティング
- メッセージが届かない場合:
	- `ROS_DOMAIN_ID`が一致しているか確認。
	- ファイアウォールを一時的に無効化して確認。
	- `RMW_IMPLEMENTATION`を揃える。
	- `ifconfig`/`ip addr`で正しいインターフェースが使われているか確認（マルチキャストがローカルネットワークでブロックされることがある）。

## 参考実行例
PC A:
```bash
export ROS_DOMAIN_ID=0
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run multi_comm talker
```

PC B:
```bash
export ROS_DOMAIN_ID=0
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run multi_comm listener
```

以上が最小構成の説明です。必要ならCyclone DDSの設定例やSystemdでのサービス化スクリプトも追加できます。
