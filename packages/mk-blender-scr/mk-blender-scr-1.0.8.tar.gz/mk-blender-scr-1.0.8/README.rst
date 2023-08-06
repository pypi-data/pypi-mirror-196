
====================================================
化学構造をBlender上で作成するためのライブラリ
====================================================

| cif,xyz,VASPの構造ファイルをBeldnerに取り込むためのライブラリ
| Blender上で動作するPythonスクリプトを生成する.

Webアプリ版
------------------------------------
基本的には ``mk-blender-scr`` をインストールせずともWebアプリのみを使用すれば良い.

| `アプリはこちら <https://shimi-lab-makeblenderscriptapp-app-vrendi.streamlit.app/>`_
| `MakeBlenderScriptApp(GitHub) <https://github.com/shimi-lab/MakeBlenderScriptApp>`_

インストール
-----------------------

>>> pip install mk-blender-scr

ドキュメント
-------------------------
`ドキュメントはこちら <https://shimi-lab.github.io/mk-blender-scr_Document/>`_ .

基本的な使用方法
-------------------------

  .. code-block:: python

      from mk_blender_src import create,BallAndStick,SpaceFilling,Stick,Animation
      from ase.io import read

      atoms = read("CONTCAR") # CONTCAR is vasp-format file
      create("BallAndStick.py",BallAndStick(atoms))
      
`BallAndStick.py` をBlender上で実行すると,Ball-Stickスタイルの3Dモデルが作成される.

スタイルは

- BallAndStick (球棒)
- SpaceFilling (空間充填)
- Stick (棒)
- Animation (アニメーション(空間充填で再現される))

より詳細な使用方法は `ドキュメント <https://shimi-lab.github.io/mk-blender-scr_Document/>`_ を参照する.


インポート可能な構造ファイル
------------------------------

| ASEのAtomsオブジェクトを作成する必要があるため,VASP(POSCAR,CONTCAR), xyz, cif等を読み込むことができる.
| 詳細なフォーマットは以下を参照
| https://wiki.fysik.dtu.dk/ase/ase/io/io.html

Pythonバージョン
------------------

Python3.8,Python3.10での動作確認済

依存ライブラリ
----------------

| 以下の条件下で安定的な動作が確認されている.
| nglview==3.0.3の場合,ipywidgetsは8.0以下である必要があることが知られている.

- `ase==3.22.1 <https://wiki.fysik.dtu.dk/ase/>`_
- `Jinja2==3.1.2 <https://jinja.palletsprojects.com/en/3.1.x/>`_
- `ipywidgets==7.7.2 <https://ipywidgets.readthedocs.io/en/stable/index.html>`_
- `nglview==3.0.3 <https://pypi.org/project/nglview/>`_

Blenderバージョン
--------------------
Blender2.9, Blender3.0 での動作確認済
