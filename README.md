#  インパルス応答  

非線形系を評価するため、非線形の出力と　仮にそれを線形に当てはめたとき出力（インパルス応答から計算）の差を計算するもの。   

## 内容 

- make_test_signal.py インパルス応答を求めるための入力信号の作成。パルスの前後に1秒間の無音あり。
- ola_convolve.py オーバーラップアド法で、そのインパルス応答をもった系に入れたときの出力を計算する。仮に線形に当てはめたときの出力を計算する。
- comparion.py 両者を比べるため、出力信号の差分を求める。 

 