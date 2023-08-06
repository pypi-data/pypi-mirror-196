# propositional_logic_expr_parser
命題論理の論理式を構文解析してASTをつくり、可視化します。また解析した論理式に対してそれぞれの命題変数に真理値の代入を行い計算する機能をvisitor patternを用いて作成しました。論理式のAST可視化かつてからやってみたかったのでできてうれしい。

# BNF

```
expression :=  term | term "|" expression
term := factor | factor & term
factor := unit | ~ factor
unit := atom | (expression)
atom := アルファベットで構成された文字列
```

なおspaceは構文解析の際には無視される。

# 使い方(適当)

```
pip install -r requirements.txt
```

もしかしたらgraphvizを入れるように言われるかもしれないのでそのときは以下を実行。

```
sudo apt-get install graphviz graphviz-dev
```


各logic_tokenizer.py(tokenize),logic_parser.py(AST表示),truth_value_assignment.py(真理値代入)を適当に実行すると指定すべき引数がでてくる（はず）

# 動作確認

top directoryでpytest実行

# example

![ASTexample1](https://user-images.githubusercontent.com/46624038/218297175-9b00232d-b2f8-4534-8980-443f530ab657.png)
![ASTexample2](https://user-images.githubusercontent.com/46624038/218297181-466dc30c-576f-4ac3-b300-8fb80a2abd00.png)
![ASTexample3](https://user-images.githubusercontent.com/46624038/218297183-e12fcc5d-14d6-470d-9be2-1b7fe8c5abe5.png)
![ASTexample4](https://user-images.githubusercontent.com/46624038/218297187-c7427ce3-fbe1-41f1-b0a5-4ec5b15a5a45.png)

# 参考文献

四則演算のところまではCで書いたことがあったのでそれを思い出しながらかきました。

[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)
