"""
快捷键帮助对话框
显示所有可用的键盘快捷键和功能说明
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QPushButton, QGroupBox, QSplitter, QHeaderView,
    QAbstractItemView, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ShortcutHelpDialog(QDialog):
    """快捷键帮助对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("快捷键参考")
        self.setGeometry(200, 200, 800, 600)
        self.setModal(True)
        
        self._setup_ui()
        self._populate_shortcuts()
    
    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("DiVERE 快捷键参考")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 搜索框
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入快捷键或功能名称进行搜索...")
        self.search_input.textChanged.connect(self._filter_shortcuts)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 主要内容区域
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 快捷键表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["快捷键", "功能", "说明"])
        
        # 设置表格属性
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 150)  # 快捷键列
        header.resizeSection(1, 200)  # 功能列
        
        splitter.addWidget(self.table)
        
        # 详细说明区域
        detail_group = QGroupBox("详细说明")
        detail_layout = QVBoxLayout(detail_group)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumWidth(300)
        
        # 默认说明文本
        default_text = """
<h3>快捷键使用指南</h3>

<h4>基本操作:</h4>
<ul>
<li>直接按键：标准调整 (0.01)</li>
<li>Shift + 按键：精细调整 (0.001)</li>
</ul>

<h4>参数范围:</h4>
<ul>
<li>RGB通道：-3.0 至 3.0</li>
<li>最大密度：0.0 至 4.8</li>
<li>密度反差：0.1 至 4.0</li>
<li>分层反差 (Channel Gamma)：0.5 至 2.0</li>
</ul>

<h4>快捷功能:</h4>
<ul>
<li>空格键：AI单次校色</li>
<li>Shift+空格：AI多次校色</li>
<li>Ctrl/Cmd+V：快速重置所有参数</li>
<li>Ctrl/Cmd+=：添加新裁剪区域</li>
<li>Ctrl/Cmd+鼠标选中：删除选中裁切区域</li>
<li>↑/↓箭头：切换裁剪区域</li>
<li>支持全角和半角括号进行旋转操作</li>
</ul>

<h4>提示:</h4>
<ul>
<li>状态栏会显示当前参数值和操作反馈</li>
<li>所有调整都会实时预览</li>
<li>裁剪功能需要在预览界面中使用</li>
</ul>
        """
        self.detail_text.setHtml(default_text.strip())
        
        detail_layout.addWidget(self.detail_text)
        splitter.addWidget(detail_group)
        
        # 设置分割器比例
        splitter.setSizes([500, 300])
        layout.addWidget(splitter)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        print_button = QPushButton("打印参考卡")
        print_button.clicked.connect(self._print_shortcuts)
        
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        
        button_layout.addWidget(print_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # 连接表格选择变化事件
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
    
    def _populate_shortcuts(self):
        """填充快捷键数据"""
        shortcuts_data = [
            # 参数调整快捷键 (标准步长 0.01)
            ("Q", "R通道降曝光", "减少红色，增加青色 (-0.01)"),
            ("E", "R通道增曝光", "增加红色，减少青色 (+0.01)"),
            ("A", "B通道降曝光", "减少蓝色，增加黄色 (-0.01)"),
            ("D", "B通道增曝光", "增加蓝色，减少黄色 (+0.01)"),
            ("W", "降低最大密度", "提升整体曝光，图像变亮 (-0.01)"),
            ("S", "增大最大密度", "降低整体曝光，图像变暗 (+0.01)"),
            ("R", "增加密度反差", "增强对比度，图像更有层次 (+0.01)"),
            ("F", "降低密度反差", "减弱对比度，图像更平坦 (-0.01)"),

            # 分层反差快捷键 (标准步长 0.01)
            ("Option/Alt+E", "R Gamma升高", "亮部变红，暗部不变 (+0.01)"),
            ("Option/Alt+Q", "R Gamma降低", "亮部变青，暗部不变 (-0.01)"),
            ("Option/Alt+D", "B Gamma升高", "亮部变蓝，暗部不变 (+0.01)"),
            ("Option/Alt+A", "B Gamma降低", "亮部变黄，暗部不变 (-0.01)"),

            # 精细调整快捷键 (精细步长 0.001)
            ("Shift+Q", "R通道精细降曝光", "精细调整红色通道 (-0.001)"),
            ("Shift+E", "R通道精细增曝光", "精细调整红色通道 (+0.001)"),
            ("Shift+A", "B通道精细降曝光", "精细调整蓝色通道 (-0.001)"),
            ("Shift+D", "B通道精细增曝光", "精细调整蓝色通道 (+0.001)"),
            ("Shift+W", "精细降低最大密度", "精细调整整体曝光 (-0.001)"),
            ("Shift+S", "精细增大最大密度", "精细调整整体曝光 (+0.001)"),
            ("Shift+R", "精细增加密度反差", "精细调整对比度 (+0.001)"),
            ("Shift+F", "精细降低密度反差", "精细调整对比度 (-0.001)"),

            # 分层反差精细调整
            ("Option/Alt+Shift+E", "R Gamma精细升高", "精细调整亮部红色 (+0.001)"),
            ("Option/Alt+Shift+Q", "R Gamma精细降低", "精细调整亮部青色 (-0.001)"),
            ("Option/Alt+Shift+D", "B Gamma精细升高", "精细调整亮部蓝色 (+0.001)"),
            ("Option/Alt+Shift+A", "B Gamma精细降低", "精细调整亮部黄色 (-0.001)"),


            # AI校色功能
            ("空格", "AI校色一次", "执行一次自动色彩校正"),
            ("Shift+空格", "AI校色多次", "执行多次迭代自动色彩校正"),

            # 中性色取色功能
            ("I", "设定中性点", "仅定义中性点"),
            ("N", "应用中性点", "执行中性点迭代"),
            
            # 旋转功能
            ("[ 或 【", "左旋转", "将图像逆时针旋转90度"),
            ("] 或 】", "右旋转", "将图像顺时针旋转90度"),
            
            # 裁剪功能
            ("↑ 上箭头", "向上切换裁剪", "在裁剪区域间向上循环切换"),
            ("↓ 下箭头", "向下切换裁剪", "在裁剪区域间向下循环切换"),
            ("Ctrl/Cmd+=", "添加新裁剪", "添加新的裁剪区域（相当于点击+按钮）"),
            ("Ctrl/Cmd+鼠标选中", "删除选中裁切", "删除鼠标所选的裁切区域")
            
            # 参数管理
            ("Ctrl/Cmd+V", "重置参数", "将所有调色参数重置为默认值"),
            ("Ctrl/Cmd+C", "设为文件夹默认", "将当前参数保存为文件夹默认设置"),
            
            
            # 导航功能
            ("← 左箭头", "上一张照片", "切换到上一张图片，支持循环浏览"),
            ("→ 右箭头", "下一张照片", "切换到下一张图片，支持循环浏览"),
        ]
        
        self.table.setRowCount(len(shortcuts_data))
        
        for row, (shortcut, function, description) in enumerate(shortcuts_data):
            # 快捷键列
            shortcut_item = QTableWidgetItem(shortcut)
            shortcut_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            
            # 设置快捷键列字体为等宽字体
            font = QFont("Courier New", 10)
            shortcut_item.setFont(font)
            
            self.table.setItem(row, 0, shortcut_item)
            
            # 功能列
            function_item = QTableWidgetItem(function)
            function_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table.setItem(row, 1, function_item)
            
            # 说明列
            description_item = QTableWidgetItem(description)
            description_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.table.setItem(row, 2, description_item)
        
        # 调整行高
        self.table.resizeRowsToContents()
    
    def _filter_shortcuts(self):
        """过滤快捷键表格"""
        filter_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            should_show = False
            
            # 检查每一列是否包含搜索文本
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and filter_text in item.text().lower():
                    should_show = True
                    break
            
            self.table.setRowHidden(row, not should_show)
    
    def _on_selection_changed(self):
        """处理表格选择变化"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        
        # 获取选中行的数据
        shortcut = self.table.item(row, 0).text()
        function = self.table.item(row, 1).text()
        description = self.table.item(row, 2).text()
        
        # 更新详细说明
        detail_html = f"""
<h3>{function}</h3>
<p><strong>快捷键:</strong> <code>{shortcut}</code></p>
<p><strong>功能说明:</strong></p>
<p>{description}</p>

<h4>使用提示:</h4>
        """
        
        # 根据快捷键类型添加特定提示
        if "通道" in function:
            detail_html += """
<ul>
<li>RGB通道调整范围：-3.0 至 3.0</li>
<li>负值向相反色彩偏移，正值向本色彩偏移</li>
<li>可以与其他通道组合使用</li>
<li>状态栏会显示当前通道的精确数值</li>
</ul>
            """
        elif "密度" in function:
            detail_html += """
<ul>
<li>最大密度范围：0.0 至 4.8</li>
<li>密度反差范围：0.1 至 4.0</li>
<li>调整会影响整体亮度和对比度</li>
<li>状态栏会显示当前参数的精确数值</li>
</ul>
            """
        elif "Gamma" in function:
            detail_html += """
<ul>
<li>分层反差范围：0.5 至 2.0</li>
<li>主要调整亮部色彩，对暗部影响较小</li>
<li>R Gamma: 控制亮部红青平衡</li>
<li>B Gamma: 控制亮部蓝黄平衡</li>
<li>状态栏会显示当前参数的精确数值</li>
</ul>
            """
        elif "旋转" in function:
            detail_html += """
<ul>
<li>每次旋转90度</li>
<li>可以连续使用达到所需角度</li>
<li>旋转不会影响调色参数</li>
<li>支持半角括号 [ ] 和全角括号【】</li>
<li>状态栏会显示旋转操作确认信息</li>
</ul>
            """
        elif "重置" in function:
            detail_html += """
<ul>
<li>重置所有调色参数为默认值</li>
<li>不会影响图像旋转角度</li>
<li>操作不可撤销，请谨慎使用</li>
<li>状态栏会显示操作确认信息</li>
</ul>
            """
        elif "AI校色" in function:
            detail_html += """
<ul>
<li>基于深度学习的自动色彩校正</li>
<li>单次校色适合大部分情况</li>
<li>多次校色用于复杂色偏场景</li>
<li>状态栏会显示操作确认信息</li>
<li>校色结果会自动更新到参数面板</li>
</ul>
            """
        elif "文件夹默认" in function:
            detail_html += """
<ul>
<li>将当前参数保存为该文件夹的默认设置</li>
<li>新打开该文件夹内的图像会自动应用</li>
<li>便于批量处理同一场景的多张照片</li>
<li>状态栏会显示操作确认信息</li>
</ul>
            """
        elif "照片" in function:
            detail_html += """
<ul>
<li>自动扫描当前文件夹内的所有图像</li>
<li>支持常见图像格式 (JPG, PNG, TIFF等)</li>
<li>支持循环浏览</li>
<li>状态栏会显示切换进度信息</li>
</ul>
            """
        elif "裁剪" in function:
            detail_html += """
<ul>
<li>裁剪功能允许你在一张图上创建多个独立的区域</li>
<li>每个裁剪区域可以有独立的调色参数</li>
<li>使用↑/↓键在裁剪区域间切换</li>
<li>使用Ctrl/Cmd+=添加新的裁剪区域</li>
<li>在预览界面中可看到裁剪区域的编号按钮</li>
</ul>
            """
        elif "精细" in function:
            detail_html += """
<ul>
<li>精细调整步长为0.001，是标准步长的十分之一</li>
<li>适用于需要微调的场景</li>
<li>所有参数调整都支持Shift精细模式</li>
<li>状态栏会显示精确到小数点后三位的数值</li>
</ul>
            """
        
        self.detail_text.setHtml(detail_html.strip())
    
    def _print_shortcuts(self):
        """打印快捷键参考卡"""
        try:
            from PySide6.QtPrintSupport import QPrinter, QPrintDialog
            from PySide6.QtGui import QTextDocument
            
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # 创建打印文档
                doc = QTextDocument()
                
                # 生成打印内容
                html_content = self._generate_print_html()
                doc.setHtml(html_content)
                
                # 打印
                doc.print(printer)
                
        except ImportError:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(
                self, 
                "打印功能不可用", 
                "打印功能需要 QtPrintSupport 模块。\n请手动截图或复制文本内容。"
            )
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "打印失败", f"打印时出现错误：{str(e)}")
    
    def _generate_print_html(self):
        """生成用于打印的HTML内容"""
        html = """
<html>
<head>
    <title>DiVERE 快捷键参考卡</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; color: #333; }
        h2 { color: #666; border-bottom: 1px solid #ccc; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f5f5f5; font-weight: bold; }
        .shortcut { font-family: 'Courier New', monospace; font-weight: bold; }
        .section { page-break-inside: avoid; }
    </style>
</head>
<body>
    <h1>DiVERE 快捷键参考卡</h1>
    
    <div class="section">
        <h2>参数调整快捷键</h2>
        <table>
            <tr><th>快捷键</th><th>功能</th><th>说明</th></tr>
            <tr><td class="shortcut">Q</td><td>R通道降曝光</td><td>减少红色，增加青色 (-0.01)</td></tr>
            <tr><td class="shortcut">E</td><td>R通道增曝光</td><td>增加红色，减少青色 (+0.01)</td></tr>
            <tr><td class="shortcut">A</td><td>B通道降曝光</td><td>减少蓝色，增加黄色 (-0.01)</td></tr>
            <tr><td class="shortcut">D</td><td>B通道增曝光</td><td>增加蓝色，减少黄色 (+0.01)</td></tr>
            <tr><td class="shortcut">W</td><td>降低最大密度</td><td>提升整体曝光，图像变亮 (-0.01)</td></tr>
            <tr><td class="shortcut">S</td><td>增大最大密度</td><td>降低整体曝光，图像变暗 (+0.01)</td></tr>
            <tr><td class="shortcut">R</td><td>增加密度反差</td><td>增强对比度，图像更有层次 (+0.01)</td></tr>
            <tr><td class="shortcut">F</td><td>降低密度反差</td><td>减弱对比度，图像更平坦 (-0.01)</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>精细调整快捷键</h2>
        <p>在上述快捷键前加上 <span class="shortcut">Ctrl/Cmd</span>，调整步长变为 0.001</p>
    </div>
    
    <div class="section">
        <h2>AI校色快捷键</h2>
        <table>
            <tr><th>快捷键</th><th>功能</th><th>说明</th></tr>
            <tr><td class="shortcut">空格</td><td>AI校色一次</td><td>执行一次自动色彩校正</td></tr>
            <tr><td class="shortcut">Shift+空格</td><td>AI校色多次</td><td>执行多次迭代自动色彩校正</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>操作功能快捷键</h2>
        <table>
            <tr><th>快捷键</th><th>功能</th><th>说明</th></tr>
            <tr><td class="shortcut">[ 或 【</td><td>左旋转</td><td>将图像逆时针旋转90度</td></tr>
            <tr><td class="shortcut">] 或 】</td><td>右旋转</td><td>将图像顺时针旋转90度</td></tr>
            <tr><td class="shortcut">Ctrl/Cmd + V</td><td>重置参数</td><td>将所有调色参数重置为默认值</td></tr>
            <tr><td class="shortcut">Ctrl/Cmd + C</td><td>设为文件夹默认</td><td>将当前参数保存为文件夹默认设置</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>导航快捷键</h2>
        <table>
            <tr><th>快捷键</th><th>功能</th><th>说明</th></tr>
            <tr><td class="shortcut">← 左箭头</td><td>上一张照片</td><td>切换到上一张图片</td></tr>
            <tr><td class="shortcut">→ 右箭头</td><td>下一张照片</td><td>切换到下一张图片</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>参数范围</h2>
        <ul>
            <li>RGB通道：-3.0 至 3.0</li>
            <li>最大密度：0.0 至 4.8</li>
            <li>密度反差：0.1 至 4.0</li>
        </ul>
    </div>
</body>
</html>
        """
        return html.strip()
