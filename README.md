# ppt-image2-editable-rebuild

一个基于截图 / 参考图重建可编辑 PowerPoint 的 Codex skill。

它的核心思路是：先用 image2 / imagegen 生成单页 PPT 视觉参考图，再以局部截图保留复杂插图、图标、地图等视觉资产，同时用 PPT 文本框和形状重建标题、正文、卡片、箭头、标签、结论条等可编辑元素。
！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
下面的内容一定！一定！要看啊，不然做出来会很烂，理解了原理才能做好！！！
简单说：**image2 负责视觉定稿，Presentations 负责可编辑重建。**

## 这个 skill 解决什么问题

image2 很适合生成漂亮的 PPT 视觉稿，但生成结果本质上是一张图片。直接把整页图放进 PPT，会导致：

- 文字无法编辑
- 图表无法修改
- 卡片、箭头、说明框不能调整
- 中文可能有错字或变形
- 后续扩展整套 PPT 很困难

`ppt-image2-editable-rebuild` 的目标不是把整页图片贴进 PPT，而是把参考图拆成两部分：

- **复杂视觉**：插图、地图、图标、徽章、纹理等，用局部截图保留视觉效果。
- **可编辑结构**：标题、正文、数字卡、卡片、箭头、标签、结论条等，用 PPT 原生文本框和形状重建。

## 非常重要：参考图背景不要太复杂

使用 image2 生成 PPT 参考图时，强烈建议背景保持干净。

推荐：

- 纯白背景
- 极浅灰背景
- 极浅纹理背景
- 低透明装饰元素
- 简洁母版线条
- 卡片和文字区域底色清晰

不推荐：

- 大面积复杂纹理
- 强烈渐变背景
- 背景上叠太多装饰图案
- 文字区域后面有复杂插画
- 卡片、文字、背景混在一起
- 整页都是海报式视觉而不是 PPT 页面

原因很简单：这个 skill 的可编辑重建是以 **局部截图 + PPT 可编辑元素** 为基础的。如果 image2 参考图背景太花，截图时很容易把背景、文字、图标、卡片边框混在一起，导致后续 PPT 页面变脏、裁图带残影、文字难以拆分，最终可编辑效果会明显下降。

最佳做法是：让 image2 负责整体布局、插图和视觉中心，但让文字区域、卡片区域、图表区域尽量干净。

## 推荐工作流

### 第一步：用 image2 生成单页参考图

如果你有一份逐页提示词文档，例如本仓库示例中的：

```text
examples/Codex_image2_presentation_29页逐页极详细提示词_统一母版版_修正版.docx
```

可以先让 Codex 读取该文档，并逐页调用 image2 / imagegen 生成参考图：

```text
slide01_reference.png
slide02_reference.png
slide03_reference.png
...
```

注意：

- 每次只生成一页。
- 不要把多页拼成一张合集图。
- 不要把 contact sheet 当作单页参考图。
- 每页参考图应使用统一母版和统一风格。
- 背景尽量干净，方便后续裁图和可编辑重建。

### 第二步：用本 skill 重建可编辑 PPT

当单页参考图已经存在后，使用：

```text
/ppt-image2-editable-rebuild
```

如果你的 Codex 客户端使用 skill chip 或 `$` 语法，也可以使用：

```text
$ppt-image2-editable-rebuild
```

然后按页重建 PPT：

```text
slide06_reference.png -> 第 6 页可编辑 PPT
```

重建阶段应以单页 PNG 为视觉依据，不再使用合集图，也不要把整页参考图直接铺进 PPT。

## 示例文件

本仓库会持续补充示例，展示从 image2 参考图到可编辑 PPT 的实际效果。当前先放入逐页 image2 提示词文档：

```text
examples/Codex_image2_presentation_29页逐页极详细提示词_统一母版版_修正版.docx
```

配套 PPT 示例为《环境成本视角_跨界流域生态补偿标准量化研究_第1-29页可编辑.pptx》。由于完整 PPT 文件体积较大，建议通过 GitHub Releases、网盘或单独示例包提供，避免安装 skill 时把大文件一起拉取。

这套示例展示了：

- 如何用逐页提示词生成 image2 参考图。
- 如何裁取参考图中的复杂插图和图标。
- 如何把标题、正文、卡片、箭头、说明框、结论条重建为可编辑元素。
- 如何逐页导出预览并检查文字出框、裁图缺边、图层遮挡等问题。

后续会继续补充截图版使用教程。

## 支持作者

这个项目会保持免费使用。如果这个 skill 帮你节省了制作可编辑 PPT 的时间，可以自愿支持作者继续维护，也可以添加微信交流使用反馈。

如果你不会安装、不会调用 image2、不会按参考图重建可编辑 PPT，或者对裁图和排版流程不熟，也可以扫码添加微信咨询。我可以提供一次基础教学 / 答疑；如果问题确实帮你解决，希望自愿支持 20 元人民币，用于项目维护。

<p align="center">
  <img src="assets/wechat-pay.jpg" width="220" alt="微信支付打赏码">
  <img src="assets/wechat-contact.jpg" width="220" alt="作者微信二维码">
</p>

二维码仅用于自愿支持、教学答疑和交流，不影响 skill 的安装和免费使用。

## 安装方式

从 GitHub 安装：

```bash
python <skill-installer>/install-skill-from-github.py \
  --repo wwe-dog/ppt-image2-editable-rebuild \
  --path skills/ppt-image2-editable-rebuild
```

安装后重启 Codex，让 skill 被识别。

## 仓库结构

```text
skills/
  ppt-image2-editable-rebuild/
    SKILL.md
    agents/
      openai.yaml
    scripts/
      crop_reference_assets.py

examples/
  Codex_image2_presentation_29页逐页极详细提示词_统一母版版_修正版.docx
```

## 核心原理

```text
文档 / 提示词
  -> image2 生成单页参考图
  -> 从参考图中裁取局部复杂视觉
  -> 用 Presentations 重建可编辑 PPT 结构
  -> 导出预览
  -> 对照参考图修正
  -> 输出可编辑 PPT
```

它不是自动 OCR 转 PPT，也不是整页截图粘贴工具。

它是一套 **截图辅助的高保真可编辑 PPT 重建流程**。

## 适合的场景

适合：

- 学术答辩 PPT
- 商业计划书 PPT
- 路演 PPT
- 高信息密度中文 PPT
- 需要先用 image2 出视觉稿，再做可编辑 PPT 的任务
- 需要保留复杂插图风格，同时又要修改文字和结构的 PPT

不适合：

- 只想快速生成粗糙 PPT
- 完全不需要可编辑性的海报图
- 要求所有插图也必须矢量可编辑
- 背景极复杂、文字和图像无法拆分的参考图

## 质量检查

每一页都应检查：

- 是否误用了整页截图
- 文字是否可编辑
- 文字是否出框
- 裁图是否缺边
- 图标是否完整
- 背景是否太脏
- 是否有截图残影
- 是否有手动硬换行
- PPT 预览是否接近参考图

最终交付时建议同时提供：

- 可编辑 PPTX
- 每页预览 PNG
- contact sheet 总览图
- 简短 QA 报告
