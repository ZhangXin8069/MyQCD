---
name: myqcd-release
description: |
  当用户要求发布或核验 `myqcd` 的 PyPI 包、更新 Read the Docs 中英文站点、
  维护英文默认 README 与 `README.zh-CN.md`、补全 PyPI Project links，或把
  gitlab.itp.ac.cn 与 gitee.com 双远端同步时使用。也用于排查“本地能构建、
  全新克隆不能构建”“PyPI 上传成功但 pip 装不到”“安装包入口 traceback”
  这类发布缺陷。
metadata:
  openclaw:
    emoji: 🚀
---

# myqcd-release — PyPI / Read the Docs / 双语文档发布

## 目的与边界

本技能负责 `myqcd` 的发布闭环：版本与打包元数据、sdist 构建与内容审计、
twine 上传、PyPI 远程安装复验、双远端推送、Read the Docs 双语言构建，以及
面向用户的算符/费曼图文档。它不判断物理正确性，也不修改核心算法；物理
结论由 `myqcd.operator_audit`、`myqcd.pyqcd_theory_audit` 与测试给出。

## 已实测事实

| 项 | 值 |
|---|---|
| 分发名 / 导入名 | `myqcd` / `myqcd` |
| 上传物 | 仅 sdist；不传 wheel |
| 凭据 | `PYPI_ZHANGXIN8069_API_KEY`，只从 `~/env-key.sh` 读取，不打印 |
| PyPI | <https://pypi.org/project/myqcd/> |
| 文档 | `docs/en/`、`docs/zh/`；RTD 项目 `myqcd`、`myqcd-zh` |
| 站点 | <https://myqcd.readthedocs.io/en/latest/>、`/zh-cn/latest/` |
| 主仓库 | <https://gitlab.itp.ac.cn/zhangxin8069/MyQCD> |
| 国内镜像 | <https://gitee.com/zhangxin8069/MyQCD> |
| 国外镜像 | <https://github.com/zhangxin8069/MyQCD>（Gitee 自动同步） |
| 双推 | `gpush.sh`（GitLab）与 `gpush.sh -t gitee.com`（Gitee） |

## 发布门禁

| # | 门 | 判据 |
|---|---|---|
| 1 | 版本一致 | `pyproject.toml` 的 `version` == `myqcd/__init__.py` 的 `__version__` |
| 2 | 打包配置已跟踪 | `git ls-files pyproject.toml MANIFEST.in myqcd/py.typed` 全部非空；全新克隆能构建 |
| 3 | sdist 内容 | 含 `py.typed` 与两个 README；无 `myqcd/testing`、无 `AGENTS.md`、`SOURCES.txt` 无 `/home/` |
| 4 | 元数据 | `python -m twine check dist/*` 为 PASSED；无弃用/绝对路径告警 |
| 5 | 干净安装 | 新 venv 从 sdist 安装；`myqcd.__file__` 含 `site-packages` |
| 6 | CLI 降级 | 安装环境 `python -m myqcd` 在缺 `refer/papers/INDEX.md` 时返回 `verified_core_without_inventory`，不 traceback |
| 7 | 文档构建 | `python -m sphinx -b html -W docs/en ...` 与 `docs/zh` 均 `build succeeded.` |
| 8 | 双语一致 | 两份 toctree 相同；同名页面的围栏代码块逐字节一致；`usage` 的 python 块可执行 |
| 9 | 文档内容 | 有算符表（16 个 Dirac 双线性、宇称/C/量纲/PyQCD 索引）与费曼图 SVG，并与标准 Dirac/SU(3)/QCD 值对照；公式用 LaTeX |
| 10 | PyPI 远程 | `pip install --index-url https://pypi.org/simple myqcd==<ver>` 成功；JSON 只有 sdist，`project_urls` 含 6 项 |
| 11 | RTD 远程 | builds API 最新 commit 为本地 HEAD 且 `state=finished`；中英文页面 200；静态图可访问 |
| 12 | 双推 | 本地、GitLab、Gitee 三端 HEAD 相同；GitHub 镜像随 Gitee 同步 |

## 工作流

1. 改版本：只改 `pyproject.toml` 与 `myqcd/__init__.py` 两处。
2. 构建前清理：`rm -rf build dist myqcd.egg-info`。
3. `python -m build --sdist` → `python -m twine check dist/*`。
4. sdist 审计：

   ```bash
   T=dist/myqcd-<ver>.tar.gz
   tar -tzf "$T" | grep -c 'myqcd/py.typed'        # 1
   tar -tzf "$T" | grep -c 'myqcd/testing/'        # 0
   tar -tzf "$T" | grep -c 'AGENTS.md'             # 0
   tar -xzOf "$T" */myqcd.egg-info/SOURCES.txt | grep -c '/home/'   # 0
   tar -tzf "$T" | grep -E 'README(\.zh-CN)?\.md$|pyproject.toml$|MANIFEST.in$'
   ```

5. 干净 venv 安装本地 sdist，验证 `python -m myqcd`、`myqcd`、`python -m myqcd.operator_audit`。
6. 上传：`TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_ZHANGXIN8069_API_KEY" python -m twine upload --non-interactive dist/myqcd-<ver>.tar.gz`。
7. 轮询 `https://pypi.org/simple/myqcd/` 出现新 tar.gz；若 pip 仍报 no matching，重试（CDN 边缘滞后），不要重传。
8. 新 venv 从 PyPI 安装并复验；检查 PyPI JSON 的 `project_urls` 与 `info.description` 首行。
9. 双推：`gpush.sh` → `gpush.sh -t gitee.com`；核对三端 HEAD。
10. 等 RTD builds API 出现新 commit 且 finished，再 `curl` 中英文页面与 `_static` 图。

## 文档要求

- 根 `README.md` 默认英文，顶部 `**English** | [中文](...)`；`README.zh-CN.md` 中文，顶部反向链接。语言链接用 GitLab 绝对 URL。
- PyPI Project links 对齐 PyQCD 六项：Documentation、Homepage、国内开发 (GitLab)、国内发布 (Gitee)、国外发布 (GitHub)、Issues。
- RTD 每侧：`index.rst` + `overview/usage/operators/diagrams/install.md` + `conf.py` + `.readthedocs.yaml` + `requirements.txt`。两侧 toctree 与页面集合必须一致。
- 图放在 `docs/<lang>/_static/*.svg`，用 Markdown `![...](_static/name.svg)` 引用；`conf.py` 设 `html_static_path = ["_static"]`。Sphinx 会把图片节点输出到 `_images/name.svg`；README/PyPI 的绝对图片 URL 必须用 `https://myqcd.readthedocs.io/<lang>/latest/_images/name.svg`，不要写 `_static`。
- 算符页必须给出 16 个结构的表：结构、类别、宇称、C、量纲、PyQCD 索引；说明 `T13` 无精确 PyQCD 索引的原因；至少给出一个非平凡分解、介子插值算符和导数算符实例。
- 图页必须给出图的 `V`、`E_int`、`C`、`L=E_int-V+C`，并与树图/单圈/两圈标准值对照；至少包含两点链、三角形、单圈自能、两圈 sunset；QCD 顶点表列出颜色因子与耦合幂次。
- 对照表只写可复现的精确值（Dirac 迹、`C_F=4/3`、`C_A=3`、`T_F=1/2`、`f_123=1`、`d_118=1/sqrt(3)`、`sum f^2=24`、`sum d^2=40/3`），不写未验证的数值。
- 公式用 LaTeX：`conf.py` 加 `sphinx.ext.mathjax`，`myst_enable_extensions = ["dollarmath", "amsmath"]`；页面中的物理量写 `$...$`。PyPI README 不渲染 MathJax，README 用 Unicode（γ、δ、√）并链接到 RTD 公式页。
- 导出器布局：树图水平链、纯环图圆周、平行边二次曲线、外部腿短桩；新增复杂图后同时更新 `_static` 与 `diagrams.md`。

## 踩坑清单（全部实测）

| 现象 | 根因 | 处置 |
|---|---|---|
| 本地 sdist 正常，全新克隆不能 `pyproject.toml` | 根 `.gitignore` 是白名单，漏了 `!pyproject.toml`、`!MANIFEST.in` | 补例外，`git ls-files` 验证，克隆后重建 |
| 全新克隆 sdist 缺 `py.typed` | `py.typed` 无扩展名，同样被白名单忽略 | 补 `!myqcd/py.typed`，`git ls-files myqcd/py.typed` 非空 |
| 刚改 `.gitignore` 后 `git add` 仍报 ignored | 同一 shell 中读取了旧规则/输出误导 | 重新 `git status --short` 与 `git check-ignore -v --no-index` 确认 |
| PyPI 上传成功但 pip 装不到 | simple index 边缘滞后 | 重试 pip；以 simple index 出现文件为准，不重传同版本 |
| 安装包 `python -m myqcd` traceback | 缺 `refer/papers/INDEX.md` 未捕获 | 捕获 `FileNotFoundError`，无 paper id 时降级为 `verified_core_without_inventory`；指定 `--paper-id`/`--inventory-json` 时退出码 2 |
| 安装包默认写 `site-packages/logs` | 默认 root 取 `__file__.parents[1]` | 入口默认 root 改为 `Path.cwd()` |
| 外部腿被算成圈 | `loop_count` 用了总边数 | 改用 `internal_edge_count`（两端点都 >=0） |
| TikZ 引用未声明的 `external` | 外部腿边端点 `-1` | 输出 `\vertex (external) at (-2.4,0) {};` |
| RTD 页面没有新内容 | 只查了首页 | 查 `install.html`/`operators.html` 等独立页；查 builds API 的 commit 与 state |
| README 图片 404 | 用了 `_static/` 绝对 URL | 改用 `_images/name.svg`（Sphinx 图片节点输出目录） |
| Sphinx 在 `/tmp` 满时 exit 2 | 构建输出/静态文件写入 `/tmp` 失败 | 把 `-d` 与输出目录放到仓库 `data/runs/`；检查 `df -h /tmp` |
| gpush 拒绝提交 | 有已暂存 submodule gitlink | 先显式提交 gitlink，再 `gpush.sh` |
| 日志索引末尾空行 | `write-log.sh` 追加索引 | 修掉 `logs/AGENTS.md` 的 blank line at EOF，再 `git diff --check` |

## 交接

- 物理正确性：`myqcd.operator_audit`、`myqcd.pyqcd_theory_audit` 与 `myqcd/testing/`。
- 目录/命名/数据边界：`~form`。
- 日志归档：常驻 `~log`，最终日志写入 `logs/v<timestamp>.txt` 并登记 `logs/AGENTS.md`。
