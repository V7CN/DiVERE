# DiVERE - 胶片校色工具

[![Python](https://img.shields.io/badge/Python-3.9~3.11-blue.svg)](https://www.python.org/downloads/) ![Version](https://img.shields.io/badge/Version-v0.1.27-orange)
[![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

胶片数字化后期处理工具，为胶片摄影师提供专业的硬件校正和负片校色解决方案。
该分支修改了色卡顺序，使得“扫描仪光谱锐化”可以适用于datacolor色卡用户。
## 🌟 功能特性

- 基于密度的反相、类似彩色暗房的操作、多种相纸/拷贝片的曲线预设、接触印相/裁剪模式、批量导出功能、方便的快捷键功能。
- 基于开源机器学习算法的自动校色功能。
- 推荐使用任何三色窄光谱光源进行翻拍/扫描。DiVERE使用了严谨的胶片数字化的硬件校正方案：IDT色彩转换和数字Mask。
- IDT转换和数字Mask可由日光直射的24色色卡校正。参考色（实际上是参考密度）由光谱物理模拟+官方数据计算所得。
- 底层工作空间提供三个：ACEScg（AP1）、Kodak Endura Premier相纸基色、Kodak 2383拷贝片基色。
- 特别支持imacon的fff文件。fff的特殊之处是需要进行一个1.8的gamma反校正。


## 🔧 技术原则
- 0：正视科学和美学的功能，科学提供必要的约束，美学在科学的约束下自由发挥。对科学了解得越多，美学的自由度就越高。
- 1：负片的色罩（Mask）专门设计用来消除相纸的串扰。而数码传感器光谱响应与相纸不同，导致色罩无法正确工作，产生严重的色偏和色彩失真，需要用数字Mask来补偿。
- 2：负片在串扰被正确补偿时，灰阶是无偏色的，校色不需要调整通道gamma，仅需要调整RGB曝光。

## 🎨 硬件校正算法核心原理和教程

[相关理论讲解&视频教程](https://drive.google.com/drive/folders/1mLxYPEhc7-zsOA2uG3n_qg3ngztglzZe?usp=sharing)

相关文字讨论：
- [彩色负片：色罩的原理，如何科学胶转数](https://zhuanlan.zhihu.com/p/1951558820087177534)
- [胶卷到底是扫描仪扫描出来的图片最接近真实的胶片色彩还是暗房光学放大最接近胶卷的真实色彩呢？](https://www.zhihu.com/question/1970096195973154804/answer/1971928008962056543)


## ☕ 支持作者

如果这个工具对您的胶片摄影工作有切实帮助，欢迎请作者V777喝杯饮料或买一卷胶片！或者将拍摄的色卡+您的线性扫描件通过邮箱发给他，99元帮您做一次有偿校准。
当然，这个校准工作本来就可以100%通过所发布的DiVERE进行。
您的支持是开源项目持续发展的动力 😊

<img src="donate.png" alt="donate" width="30%">

## 快捷键表：

### 🎯 参数调整快捷键
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Q` | R通道降曝光 | 减少红色，增加青色 (-0.01) |
| `E` | R通道增曝光 | 增加红色，减少青色 (+0.01) |
| `A` | B通道降曝光 | 减少蓝色，增加黄色 (-0.01) |
| `D` | B通道增曝光 | 增加蓝色，减少黄色 (+0.01) |
| `W` | 降低最大密度 | 提升整体曝光，图像变亮 (-0.01) |
| `S` | 增大最大密度 | 降低整体曝光，图像变暗 (+0.01) |
| `R` | 增加密度反差 | 增强对比度，图像更有层次 (+0.01) |
| `F` | 降低密度反差 | 减弱对比度，图像更平坦 (-0.01) |

### 🔍 精细调整模式
在上述任意快捷键前加上 `Shift`，调整步长变为精细模式 (0.001)
- 例如：`Shift+Q` = 精细调整R通道 (-0.001)

### 🤖 AI校色功能
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `空格` | AI校色一次 | 执行一次自动色彩校正 |
| `Shift+空格` | AI校色多次 | 执行多次迭代自动色彩校正 |

### 🔄 图像操作
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `[` 或 `【` | 左旋转 | 将图像逆时针旋转90度 |
| `]` 或 `】` | 右旋转 | 将图像顺时针旋转90度 |

### 🔍 导航功能
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `←` | 上一张照片 | 切换到上一张图片，支持循环浏览 |
| `→` | 下一张照片 | 切换到下一张图片，支持循环浏览 |
| `↑` | 向上切换裁剪 | 在裁剪区域间向上循环切换 |
| `↓` | 向下切换裁剪 | 在裁剪区域间向下循环切换 |
| `Ctrl/Cmd+=` | 添加新裁剪 | 添加新的裁剪区域 |

### 🔧 参数的复制粘贴
| 快捷键 | 功能     | 说明 |
|--------|--------|------|
| `Ctrl/Cmd+V` | 从默认值粘贴 | 将所有调色参数重置为默认值 |
| `Ctrl/Cmd+C` | 复制到默认值 | 将当前参数保存为文件夹默认设置 |

### ⚡ 分层反差 (Channel Gamma)
| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Option/Alt+E` | R Gamma升高 | 亮部变红，暗部不变 (+0.01) |
| `Option/Alt+Q` | R Gamma降低 | 亮部变青，暗部不变 (-0.01) |
| `Option/Alt+D` | B Gamma升高 | 亮部变蓝，暗部不变 (+0.01) |
| `Option/Alt+A` | B Gamma降低 | 亮部变黄，暗部不变 (-0.01) |

**精细调整模式**：在上述快捷键基础上加 `Shift`，步长变为 0.001
- 例如：`Option/Alt+Shift+E` = 精细调整 R Gamma (+0.001)

> 💡 **提示**: 状态栏会实时显示参数值和操作反馈，所有调整都会实时预览更新

## 📦 安装部署

### 系统要求

- Python 3.9–3.11（推荐 3.11）
- 操作系统：macOS 12+（Intel/Apple Silicon）、Windows 10/11、Ubuntu 20.04+
- 显卡：非必须。GPU 加速（可选）：
  - macOS Metal（推荐）：通过 PyObjC 访问 Metal（Apple Silicon/Intel）
  - OpenCL（可选）：跨平台（Windows/macOS/Linux）
  - CUDA（可选）：NVIDIA 显卡
- 包管理：pip 或 conda

### 🚀 快速开始

#### 方法零：手动下载
- .首先点Code -> Download ZIP 下载本项目源码（400多MB，大多是校色示例图片）
- .安装python
- .安装依赖、运行程序：
```bash
# 安装依赖
pip install -r requirements.txt

# 如需 macOS Metal 加速（可选）
pip install pyobjc-framework-Metal pyobjc-framework-MetalPerformanceShaders

# 如需 OpenCL（可选）
# pip install pyopencl  # 已在 requirements.txt 中包含

# 运行应用
python -m divere
```

#### 方法一：使用pip

```bash
# 克隆项目
git clone https://github.com/V7CN/DiVERE.git
cd DiVERE

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
python -m divere
```

#### 方法二：使用conda

```bash
# 克隆项目
git clone https://github.com/V7CN/DiVERE.git
cd DiVERE

# 创建conda环境（推荐 Python 3.11）
conda create -n divere python=3.11 -y
conda activate divere

# 安装依赖
pip install -r requirements.txt

# 运行应用
python -m divere
```

### 依赖包说明

#### 必需依赖
```
PySide6>=6.5.0          # GUI框架
numpy>=1.24.0           # 数值计算
opencv-python>=4.8.0    # 图像处理
pillow>=10.0.0          # 图像I/O
scipy>=1.11.0           # 科学计算
imageio>=2.31.0         # 图像格式支持
colour-science>=0.4.2   # 色彩科学计算
onnxruntime>=1.15.0     # ONNX推理（AI自动校色）
pyopencl>=2024.1        # GPU加速计算
tifffile>=2024.2.12     # 高级TIFF处理（ICC支持）
imagecodecs>=2024.1.1   # TIFF压缩编解码器
cma>=3.3.0              # CMA-ES优化器（CCM参数优化）
```

- 可选（GPU 加速）
```
### ICC 内嵌与 16-bit TIFF 支持

自 v0.1.10 起，导出 JPEG/TIFF 支持自动嵌入 ICC（位于 `config/colorspace/icc/`）。

- JPEG：使用 Pillow 保存并嵌入 ICC。
- TIFF：使用 `tifffile` 写入 16-bit/多通道，并通过 tag 34675 写入 ICC（默认 LZW 压缩）。

注：TIFF 的 LZW 压缩和 ICC 嵌入功能依赖 `tifffile` 和 `imagecodecs`，已在 requirements.txt 中包含。这些包是必需的，确保 TIFF 导出功能正常工作。

ICC 存放位置：`divere/config/colorspace/icc/`

默认映射：
- sRGB → `sRGB Profile.icc`
- Display P3 → `Display P3.icc`
- ACEScg_Linear/ACEScg → `ACESCG Linear.icc`
（若需 Adobe RGB，请将 `Adobe RGB (1998).icc` 放入上述目录）
# macOS Metal
pyobjc-framework-Metal
pyobjc-framework-MetalPerformanceShaders

# OpenCL（跨平台）
pyopencl

# CUDA（NVIDIA，可选）
cupy-cuda11x  # 按你的CUDA版本选择
```

- macOS Apple Silicon（arm64）：直接使用 `pip install onnxruntime`，官方已原生支持 arm64，不需要 `onnxruntime-silicon`。
- 可用以下命令简单验证环境：
```bash
python -c "import platform, onnxruntime as ort; print(platform.machine(), ort.__version__)"
```

## 🤝 致谢

### 深度学习自动校色

本项目的学习型自动校色基于以下优秀的开源研究成果：

#### Deep White Balance
- 论文: "Deep White-Balance Editing" (CVPR 2020)
- 作者: Mahmoud Afifi, Konstantinos G. Derpanis, Björn Ommer, Michael S. Brown
- GitHub: https://github.com/mahmoudnafifi/Deep_White_Balance
- 许可证: MIT License
- 说明: 模型来源于上述研究，已转换为 ONNX 并随项目分发使用（`divere/models/net_awb.onnx`）。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**V7** - vanadis@yeah.net

## 🐛 问题反馈

如果您发现任何问题或有功能建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/V7CN/DiVERE/issues)
- 发送邮件至：vanadis@yeah.net

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

**DiVERE** - 胶片校色工具 
