# data-qd-220 · 质谱同位素峰簇归组

根据 1/电荷 的同位素峰间距，从有序 m/z 峰中选择连续峰簇，保留电荷、单同位素峰、强度总和、最大间距误差及未归组峰。

Python 3.11+；运行只用标准库，构建固定 setuptools 80.9.0 与 wheel 0.45.1。

    uv venv --python 3.12 .venv
    uv pip install --python .venv/bin/python --offline -r requirements-build.lock
    uv pip install --python .venv/bin/python --offline --no-build-isolation -e .
    .venv/bin/python -m unittest discover -s tests -v
    .venv/bin/python examples/run_sample.py

样例完全合成。本仓不读取仪器原始文件、不鉴定化合物，也不生成可视化看板。

