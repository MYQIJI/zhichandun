#!/usr/bin/env python3
"""
知产盾™ 道统自指版 V2.5 · 师门铸剑炉出品
整合功能：零困惑导航、智能路径防护、自指加冕仪式、快捷操作面板
"""
import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from datetime import datetime
from pathlib import Path
import time
import sys

# ==================== 道统配色体系 ====================
class ShimenColors:
    """师门道统配色 · 玄黑为底，鎏金镶边"""
    BG_OUTER = "#0f0b07"
    BG_MAIN = "#1a1410"
    BG_CARD = "#231f1a"
    BG_INPUT = "#2c2620"
    BG_LOG = "#16120e"
    
    BORDER_GOLD = "#8b7a5e"
    BORDER_DARK = "#3a3028"
    BORDER_LIGHT = "#a89870"
    BORDER_RITUAL = "#c9a96e"
    
    TEXT_GOLD = "#d4b95a"
    TEXT_LIGHT = "#e8d8a8"
    TEXT_MUTED = "#7a6d5b"
    TEXT_WHITE = "#f0e6d0"
    TEXT_RED = "#d04040"
    TEXT_GREEN = "#5a9a5a"
    TEXT_BLUE = "#5a8ba9"
    
    BTN_PRIMARY = "#2c1e10"
    BTN_PRIMARY_HOVER = "#3c2e20"
    BTN_ACCENT = "#3a2418"
    BTN_RITUAL = "#5a4a2e"
    BTN_SUCCESS = "#2a4a2a"
    
    CARD_SUCCESS = "#1a2a1a"
    CARD_TIP = "#2a241a"
    CARD_RITUAL = "#3a2e1a"
    CARD_WARNING = "#4a2a1a"

# ==================== 道统字体配置 ====================
FONT_TITLE = ("仿宋", 18, "bold")
FONT_HEADING = ("仿宋", 13, "bold")
FONT_BODY = ("仿宋", 11)
FONT_SMALL = ("仿宋", 10)
FONT_MINI = ("仿宋", 9)
FONT_LOG = ("宋体", 10)
FONT_BUTTON = ("仿宋", 12, "bold")
FONT_BUTTON_BIG = ("仿宋", 14, "bold")

class CreatorProtectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("知产盾™ · 道统自指版 V2.5")
        
        # 屏幕居中
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width, window_height = 920, 720
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.resizable(True, True)
        self.root.configure(bg=ShimenColors.BG_OUTER)
        
        # 隐藏主窗口，先显示启动画面
        self.root.withdraw()
        
        # 变量初始化
        self.watch_dir = tk.StringVar()
        self.owner_name = tk.StringVar(value="")
        self.processed_files = []
        self.scanned_files = []
        self.ritual_in_progress = False
        self.path_history = []  # 路径历史记录
        self.current_breadcrumb = "🏠 知产盾 > 待命"
        
        # 显示启动画面
        self.show_splash_screen()
        
        # 稍后构建主界面
        self.root.after(2500, self.build_main_ui)
    
    def show_splash_screen(self):
        """显示道统启动画面"""
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        
        splash_width, splash_height = 400, 300
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        
        self.splash.configure(bg=ShimenColors.BG_OUTER)
        
        border_frame = tk.Frame(self.splash, bg=ShimenColors.BORDER_GOLD, padx=2, pady=2)
        border_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        main_frame = tk.Frame(border_frame, bg=ShimenColors.BG_MAIN)
        main_frame.pack(fill="both", expand=True)
        
        seal_frame = tk.Frame(main_frame, bg=ShimenColors.BG_MAIN)
        seal_frame.pack(fill="both", expand=True, pady=30)
        
        tk.Frame(seal_frame, bg=ShimenColors.BORDER_GOLD, height=2).pack(fill="x", padx=40, pady=(0, 20))
        
        self.splash_text = tk.Label(seal_frame, text="", font=FONT_TITLE, 
                                   bg=ShimenColors.BG_MAIN, fg=ShimenColors.TEXT_GOLD)
        self.splash_text.pack(pady=10)
        
        tk.Frame(seal_frame, bg=ShimenColors.BORDER_GOLD, height=2).pack(fill="x", padx=40, pady=(20, 0))
        
        tk.Label(main_frame, text="知产盾™ · 道统自指版 V2.5", font=FONT_SMALL,
                bg=ShimenColors.BG_MAIN, fg=ShimenColors.TEXT_MUTED).pack(pady=10)
        
        tk.Label(main_frame, text="师门铸剑炉 · 出品", font=FONT_MINI,
                bg=ShimenColors.BG_MAIN, fg=ShimenColors.TEXT_MUTED).pack()
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate', 
                                          length=200, style="Ritual.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=20)
        
        self.setup_progressbar_style()
        self.progress_bar.start(15)
        
        self.animate_splash_text([
            "道统结界初始化...",
            "加载自指加冕模块...",
            "构筑智能防护...",
            "启动零困惑导航..."
        ])
    
    def setup_progressbar_style(self):
        """设置道统风格进度条"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Ritual.Horizontal.TProgressbar", 
                       background=ShimenColors.BORDER_GOLD,
                       troughcolor=ShimenColors.BG_CARD,
                       bordercolor=ShimenColors.BORDER_DARK,
                       lightcolor=ShimenColors.TEXT_GOLD,
                       darkcolor=ShimenColors.BORDER_GOLD)
    
    def animate_splash_text(self, texts, index=0):
        """启动画面文字动画"""
        if index < len(texts):
            current_text = ""
            full_text = texts[index]
            
            def type_effect(char_index=0):
                if char_index < len(full_text):
                    current_text = full_text[:char_index+1]
                    self.splash_text.config(text=current_text)
                    self.splash.after(50, lambda: type_effect(char_index+1))
                else:
                    self.splash.after(500, lambda: self.animate_splash_text(texts, index+1))
            
            type_effect()
        else:
            self.splash.after(800, self.splash.destroy)
    
    def build_main_ui(self):
        """构建道统主界面"""
        # 显示主窗口
        self.root.deiconify()
        
        # ===== 顶部道统标题栏 =====
        title_bar = tk.Frame(self.root, bg=ShimenColors.BG_OUTER, height=75)
        title_bar.pack(fill="x", padx=3, pady=(3, 0))
        title_bar.pack_propagate(False)
        
        tk.Frame(title_bar, bg=ShimenColors.BORDER_GOLD, height=2).pack(fill="x", side="top")
        
        title_inner = tk.Frame(title_bar, bg=ShimenColors.BG_OUTER)
        title_inner.pack(fill="both", expand=True, padx=25)
        
        left_deco = tk.Frame(title_inner, bg=ShimenColors.BG_OUTER)
        left_deco.pack(side="left", fill="y")
        tk.Label(left_deco, text="╰┄┄┄", font=("仿宋", 16), 
                bg=ShimenColors.BG_OUTER, fg=ShimenColors.BORDER_GOLD).pack(side="left")
        
        center_title = tk.Frame(title_inner, bg=ShimenColors.BG_OUTER)
        center_title.pack(side="left", expand=True, fill="y")
        
        tk.Label(center_title, text="知产盾™", 
                font=FONT_TITLE, bg=ShimenColors.BG_OUTER, fg=ShimenColors.TEXT_GOLD).pack()
        tk.Label(center_title, text="道统自指版 V2.5", 
                font=FONT_HEADING, bg=ShimenColors.BG_OUTER, fg=ShimenColors.TEXT_LIGHT).pack()
        
        right_deco = tk.Frame(title_inner, bg=ShimenColors.BG_OUTER)
        right_deco.pack(side="right", fill="y")
        tk.Label(right_deco, text="┄┄┄╯", font=("仿宋", 16), 
                bg=ShimenColors.BG_OUTER, fg=ShimenColors.BORDER_GOLD).pack(side="right")
        
        tk.Frame(title_bar, bg=ShimenColors.BORDER_GOLD, height=2).pack(fill="x", side="bottom")
        
        # ===== 【新增】零困惑导航栏 =====
        self.create_navigation_bar()
        
        # ===== 主内容区 =====
        main_frame = tk.Frame(self.root, bg=ShimenColors.BG_OUTER)
        main_frame.pack(fill="both", expand=True, padx=15, pady=(10, 5))
        
        # ===== 第一步：确立道主 =====
        step1 = self.create_ritual_frame(main_frame, "第一步：确立道主 · 知产归属")
        step1.pack(fill="x", pady=(0, 10))
        
        owner_frame = tk.Frame(step1, bg=ShimenColors.BG_MAIN)
        owner_frame.pack(fill="x", pady=8)
        
        self.create_ritual_label(owner_frame, "道主尊号：").pack(side="left", padx=(0, 10))
        self.owner_entry = self.create_ritual_entry(owner_frame, self.owner_name, width=30)
        self.owner_entry.pack(side="left", padx=5)
        
        tip_label = self.create_ritual_label(owner_frame, "※ 请输入您的姓名或笔名，此名将镌刻于所有知产法印", 
                                            font=FONT_SMALL, fg=ShimenColors.TEXT_MUTED)
        tip_label.pack(side="left", padx=(20, 0))
        
        self.add_breathing_effect(self.owner_entry)
        
        # ===== 第二步：选择道场 =====
        step2 = self.create_ritual_frame(main_frame, "第二步：选择道场 · 守护之地")
        step2.pack(fill="x", pady=(0, 10))
        
        dir_frame = tk.Frame(step2, bg=ShimenColors.BG_MAIN)
        dir_frame.pack(fill="x", pady=8)
        
        self.create_ritual_label(dir_frame, "守护道场：").pack(side="left", padx=(0, 10))
        self.dir_entry = self.create_ritual_entry(dir_frame, self.watch_dir, width=35)
        self.dir_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        choose_btn = self.create_ritual_button(dir_frame, "择地", self.choose_dir, 
                                              font=FONT_SMALL, width=8)
        choose_btn.pack(side="left", padx=5)
        self.add_button_ritual_feedback(choose_btn)
        
        # ===== 第三步：启坛行仪 =====
        step3 = self.create_ritual_frame(main_frame, "第三步：启坛行仪 · 一键守护")
        step3.pack(fill="x", pady=(0, 10))
        
        ritual_btn_frame = tk.Frame(step3, bg=ShimenColors.BG_MAIN)
        ritual_btn_frame.pack(fill="x", pady=12)
        
        self.ritual_button = self.create_ritual_button(
            ritual_btn_frame, "🛡️  启 坛 · 一 键 守 护", 
            self.ritual_one_click_protect,
            font=FONT_BUTTON_BIG, bg=ShimenColors.BTN_RITUAL, 
            fg=ShimenColors.TEXT_GOLD, width=24, height=2
        )
        self.ritual_button.pack()
        self.add_button_ritual_feedback(self.ritual_button, scale_effect=True)
        
        ritual_tip = """道主择地后，点击上方按钮，本结界将自动完成：
        神识探查 → 真名烙印 → 归藏入府 → 法旨封存
        全程道统护持，无需额外操作"""
        
        ritual_tip_label = self.create_ritual_label(ritual_btn_frame, ritual_tip,
                                                   font=FONT_SMALL, fg=ShimenColors.TEXT_MUTED)
        ritual_tip_label.pack(pady=(8, 0))
        
        # ===== 第四步：道统日志 =====
        step4 = self.create_ritual_frame(main_frame, "道统行仪日志")
        step4.pack(fill="both", expand=True)
        
        log_toolbar = tk.Frame(step4, bg=ShimenColors.BG_MAIN)
        log_toolbar.pack(fill="x", padx=5, pady=(8, 5))
        
        self.create_ritual_button(log_toolbar, "清空", self.clear_log, 
                                 font=FONT_SMALL, width=6).pack(side="left", padx=2)
        self.create_ritual_button(log_toolbar, "保存", self.save_log, 
                                 font=FONT_SMALL, width=6).pack(side="left", padx=2)
        
        level_frame = tk.Frame(log_toolbar, bg=ShimenColors.BG_MAIN)
        level_frame.pack(side="right", padx=5)
        
        levels = [
            ("系统", ShimenColors.TEXT_MUTED),
            ("仪式", ShimenColors.TEXT_GOLD),
            ("成功", ShimenColors.TEXT_GREEN),
            ("警告", "#d4a017"),
            ("错误", ShimenColors.TEXT_RED)
        ]
        
        for level_text, color in levels:
            tk.Label(level_frame, text="●", font=FONT_SMALL, 
                    bg=ShimenColors.BG_MAIN, fg=color).pack(side="left", padx=(5, 2))
            tk.Label(level_frame, text=level_text, font=FONT_MINI, 
                    bg=ShimenColors.BG_MAIN, fg=ShimenColors.TEXT_MUTED).pack(side="left", padx=(0, 8))
        
        log_container = tk.Frame(step4, bg=ShimenColors.BORDER_DARK, relief="sunken", bd=1)
        log_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        self.log_area = scrolledtext.ScrolledText(
            log_container, font=FONT_LOG, height=12,
            bg=ShimenColors.BG_LOG, fg=ShimenColors.TEXT_LIGHT,
            relief="flat", bd=0, wrap="word",
            insertbackground=ShimenColors.TEXT_GOLD,
            padx=10, pady=10
        )
        self.log_area.pack(fill="both", expand=True)
        
        self.setup_log_tags()
        
        self.log("━" * 45, "ritual")
        self.log("知产盾™ · 道统自指版 V2.5 已就绪", "ritual")
        self.log("━" * 45, "ritual")
        self.log("", "system")
        self.log("道主，请先确立您的尊号，再择守护道场。", "system")
        self.log("点击「启坛·一键守护」，本结界将自动行仪。", "system")
        
        # ===== 【新增】快捷操作面板 =====
        self.create_quick_access_panel()
        
        # ===== 底部道统信息栏 =====
        bottom_bar = tk.Frame(self.root, bg=ShimenColors.BG_OUTER, height=32)
        bottom_bar.pack(fill="x", padx=3, pady=(0, 3))
        bottom_bar.pack_propagate(False)
        
        tk.Frame(bottom_bar, bg=ShimenColors.BORDER_GOLD, height=2).pack(fill="x", side="top")
        
        bottom_inner = tk.Frame(bottom_bar, bg=ShimenColors.BG_OUTER)
        bottom_inner.pack(fill="both", expand=True, padx=20)
        
        tk.Label(bottom_inner, text="师门™ 出品 | 道统护持 | 自指加冕 | 智能防护", 
                font=FONT_MINI, fg=ShimenColors.TEXT_MUTED, 
                bg=ShimenColors.BG_OUTER).pack(side="left")
        
        self.status_label = tk.Label(bottom_inner, text="⚪ 结界待命", 
                                    font=FONT_MINI, fg=ShimenColors.TEXT_MUTED, 
                                    bg=ShimenColors.BG_OUTER)
        self.status_label.pack(side="right")
        
        tk.Frame(bottom_bar, bg=ShimenColors.BORDER_GOLD, height=2).pack(fill="x", side="bottom")
    
    def create_navigation_bar(self):
        """【新功能】创建零困惑导航栏"""
        nav_frame = tk.Frame(self.root, bg=ShimenColors.BG_OUTER, height=30)
        nav_frame.pack(fill="x", padx=20, pady=(5, 0))
        
        # 面包屑导航
        self.breadcrumb_label = tk.Label(nav_frame, 
                                        text=self.current_breadcrumb,
                                        font=FONT_SMALL, 
                                        fg=ShimenColors.TEXT_MUTED, 
                                        bg=ShimenColors.BG_OUTER)
        self.breadcrumb_label.pack(side="left")
        
        # 全局返回按钮（初始隐藏）
        self.home_btn = self.create_ritual_button(nav_frame, "🏠 返回首页", 
                                                 command=self.return_to_home,
                                                 font=FONT_MINI, width=10)
        self.home_btn.pack(side="right", padx=5)
        self.home_btn.pack_forget()  # 初始隐藏
    
    def update_breadcrumb(self, new_crumb):
        """更新面包屑导航"""
        self.current_breadcrumb = new_crumb
        self.breadcrumb_label.config(text=new_crumb)
        
        # 如果不是在首页，显示返回按钮
        if "待命" not in new_crumb and "首页" not in new_crumb:
            self.home_btn.pack(side="right", padx=5)
        else:
            self.home_btn.pack_forget()
    
    def return_to_home(self):
        """返回首页功能"""
        self.update_breadcrumb("🏠 知产盾 > 待命")
        self.log("已返回首页", "system")
    
    def create_quick_access_panel(self):
        """【新功能】创建快捷操作面板"""
        quick_panel = tk.Frame(self.root, bg=ShimenColors.BG_CARD, width=60)
        quick_panel.pack(side="right", fill="y", padx=(0,5), pady=20)
        quick_panel.pack_propagate(False)
        
        # 绘制边框
        border_canvas = tk.Canvas(quick_panel, width=60, height=400, 
                                 bg=ShimenColors.BG_CARD, highlightthickness=0)
        border_canvas.pack(fill="both", expand=True)
        border_canvas.create_rectangle(1, 1, 58, 398, 
                                      outline=ShimenColors.BORDER_GOLD, width=1, fill='')
        
        # 快捷操作按钮列表
        quick_actions = [
            ("📁", "打开存证库", self.open_archive_dir),
            ("📋", "复制日志", self.copy_log_to_clipboard),
            ("⚙️", "快速设置", self.show_quick_settings),
            ("👑", "自我加冕", self.ritual_self_certify),
            ("❓", "即时帮助", self.show_context_help),
        ]
        
        for icon, text, command in quick_actions:
            btn_frame = tk.Frame(quick_panel, bg=ShimenColors.BG_CARD)
            btn_frame.pack(fill="x", pady=8)
            
            btn = tk.Button(btn_frame, text=icon, font=("Segoe UI Emoji", 16),
                           bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_GOLD,
                           relief="flat", bd=0, cursor="hand2",
                           activebackground=ShimenColors.BG_INPUT,
                           command=command)
            btn.pack()
            
            # 添加悬停提示
            self.create_tooltip(btn, text)
    
    def create_tooltip(self, widget, text):
        """创建悬停提示"""
        def on_enter(e):
            tip = tk.Toplevel(widget)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{e.x_root+10}+{e.y_root+10}")
            
            label = tk.Label(tip, text=text, font=FONT_MINI,
                            bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_GOLD,
                            relief="solid", bd=1)
            label.pack()
            
            widget.tip_window = tip
        
        def on_leave(e):
            if hasattr(widget, 'tip_window') and widget.tip_window:
                widget.tip_window.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def open_archive_dir(self):
        """打开存证库目录"""
        if hasattr(self, 'last_archive_dir') and os.path.exists(self.last_archive_dir):
            os.startfile(self.last_archive_dir)
            self.log(f"已打开存证库：{self.last_archive_dir}", "action")
        else:
            self.log("尚未生成存证库，请先执行一键守护", "warning")
    
    def copy_log_to_clipboard(self):
        """复制日志到剪贴板"""
        log_content = self.log_area.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(log_content)
        self.show_ritual_message("日志已复制到剪贴板", "success")
    
    def show_quick_settings(self):
        """显示快速设置"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("快速设置")
        settings_win.geometry("400x300")
        settings_win.configure(bg=ShimenColors.BG_OUTER)
        
        tk.Label(settings_win, text="快速设置", font=FONT_HEADING,
                bg=ShimenColors.BG_OUTER, fg=ShimenColors.TEXT_GOLD).pack(pady=10)
        
        # 文件类型设置
        type_frame = tk.Frame(settings_win, bg=ShimenColors.BG_CARD, padx=10, pady=10)
        type_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(type_frame, text="监控文件类型：", font=FONT_SMALL,
                bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_LIGHT).pack(anchor="w")
        
        file_types = [".py", ".md", ".txt", ".pdf", ".docx", ".jpg", ".png"]
        self.file_type_vars = {}
        
        for ft in file_types:
            var = tk.IntVar(value=1)
            cb = tk.Checkbutton(type_frame, text=ft, variable=var,
                               bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_LIGHT,
                               selectcolor=ShimenColors.BG_CARD)
            cb.pack(anchor="w", pady=2)
            self.file_type_vars[ft] = var
    
    def ritual_self_certify(self):
        """【新功能】自我加冕仪式"""
        self.update_breadcrumb("🏠 知产盾 > 自我加冕")
        
        self.log_area.delete(1.0, tk.END)
        self.log("━" * 45, "ritual")
        self.log("🫅 知产盾·自我加冕大典", "ritual")
        self.log("━" * 45, "ritual")
        
        # 获取自身所有相关文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self_files = []
        
        for file in os.listdir(current_dir):
            if file.endswith('.py') and not file.startswith('__'):
                self_files.append(os.path.join(current_dir, file))
        
        if not self_files:
            self.log("未找到自身文件", "warning")
            return
        
        success_count = 0
        for i, file_path in enumerate(self_files):
            self.log(f"为自身文件加冕 ({i+1}/{len(self_files)}): {os.path.basename(file_path)}", "ritual")
            
            evidence_path = self.create_evidence(file_path, "师门铸剑炉")
            if evidence_path:
                success_count += 1
                self.log(f"  ✅ 加冕完成: {os.path.basename(file_path)}", "success")
            else:
                self.log(f"  ❌ 加冕失败: {os.path.basename(file_path)}", "error")
        
        self.log("━" * 45, "ritual")
        self.log(f"👑 知产盾·自我加冕大典·礼成", "ritual")
        self.log(f"成功加冕 {success_count}/{len(self_files)} 个自身文件", "ritual")
        self.log("从此，盾护万物，亦能自护", "ritual")
        self.log("━" * 45, "ritual")
        
        self.update_breadcrumb("🏠 知产盾 > 待命")
    
    def show_context_help(self):
        """显示即时帮助"""
        help_text = """知产盾™ 道统自指版 V2.5 使用帮助：

1. 确立道主：填写您的姓名或笔名
2. 选择道场：选择要监控的文件夹
3. 启坛守护：点击一键保护按钮
4. 查看结果：在日志中查看保护详情

快捷操作：
📁 打开存证库 - 直接打开存证文件夹
📋 复制日志 - 复制操作日志到剪贴板
👑 自我加冕 - 为知产盾自身文件做存证
❓ 即时帮助 - 显示本帮助信息

师门™出品 · 道统永续"""
        
        messagebox.showinfo("即时帮助", help_text)
    
    def create_ritual_frame(self, parent, text):
        """创建道统仪式边框的LabelFrame"""
        frame = tk.LabelFrame(
            parent, text=f"  {text}  ",
            font=FONT_HEADING, bg=ShimenColors.BG_MAIN, fg=ShimenColors.TEXT_GOLD,
            relief="solid", bd=1, 
            highlightbackground=ShimenColors.BORDER_RITUAL,
            highlightthickness=1,
            padx=15, pady=12
        )
        return frame
    
    def create_ritual_button(self, parent, text, command, font=FONT_BUTTON, 
                           bg=None, fg=None, width=None, height=None):
        """创建道统仪式按钮"""
        if bg is None: bg = ShimenColors.BTN_PRIMARY
        if fg is None: fg = ShimenColors.TEXT_GOLD
        
        btn = tk.Button(
            parent, text=text, font=font, bg=bg, fg=fg,
            relief="ridge", bd=2, cursor="hand2",
            activebackground=ShimenColors.BTN_PRIMARY_HOVER,
            activeforeground=ShimenColors.TEXT_LIGHT,
            command=command
        )
        
        if width: btn.config(width=width)
        if height: btn.config(height=height)
        
        return btn
    
    def create_ritual_entry(self, parent, textvariable, width=None, font=FONT_BODY):
        """创建道统输入框"""
        entry = tk.Entry(
            parent, textvariable=textvariable, font=font,
            bg=ShimenColors.BG_INPUT, fg=ShimenColors.TEXT_LIGHT,
            relief="solid", bd=1, 
            insertbackground=ShimenColors.TEXT_GOLD,
            highlightbackground=ShimenColors.BORDER_DARK,
            highlightthickness=1
        )
        if width: entry.config(width=width)
        return entry
    
    def create_ritual_label(self, parent, text, font=FONT_BODY, fg=None, bg=None):
        """创建道统标签"""
        if bg is None: bg = ShimenColors.BG_MAIN
        if fg is None: fg = ShimenColors.TEXT_LIGHT
        
        return tk.Label(parent, text=text, font=font, bg=bg, fg=fg, justify="left")
    
    def add_breathing_effect(self, widget):
        """为部件添加呼吸灯效果"""
        base_bg = widget.cget("bg")
        
        def breath(alpha=0.1, direction=1):
            if hasattr(widget, '_breathing_active') and not widget._breathing_active:
                return
                
            r, g, b = int(base_bg[1:3], 16), int(base_bg[3:5], 16), int(base_bg[5:7], 16)
            r = min(255, int(r * (1 + alpha * 0.1)))
            g = min(255, int(g * (1 + alpha * 0.1)))
            b = min(255, int(b * (1 + alpha * 0.1)))
            
            new_color = f"#{r:02x}{g:02x}{b:02x}"
            widget.config(bg=new_color)
            
            alpha += 0.1 * direction
            if alpha >= 0.3 or alpha <= 0.1:
                direction *= -1
            
            widget.after(1000, lambda: breath(alpha, direction))
        
        widget._breathing_active = True
        breath()
    
    def add_button_ritual_feedback(self, button, scale_effect=False):
        """为按钮添加道统仪式反馈效果"""
        original_bg = button.cget("bg")
        original_fg = button.cget("fg")
        original_font = button.cget("font")
        
        def on_enter(e):
            button.config(bg=ShimenColors.BTN_PRIMARY_HOVER)
            if scale_effect:
                font_config = list(original_font)
                font_config[1] = font_config[1] + 1
                button.config(font=tuple(font_config))
        
        def on_leave(e):
            button.config(bg=original_bg)
            if scale_effect:
                button.config(font=original_font)
        
        def on_click(e):
            x, y = e.x, e.y
            ripple = tk.Frame(button, bg=ShimenColors.TEXT_GOLD + "80", width=1, height=1)
            ripple.place(x=x, y=y)
            
            def expand(size=1):
                if size < 100:
                    ripple.config(width=size*2, height=size*2)
                    ripple.place(x=x-size, y=y-size)
                    button.after(10, lambda: expand(size+5))
                else:
                    ripple.destroy()
            
            expand()
            button.config(relief="sunken")
            button.after(100, lambda: button.config(relief="ridge"))
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_click)
    
    def setup_log_tags(self):
        """设置日志标签样式"""
        self.log_area.tag_config("timestamp", foreground=ShimenColors.TEXT_MUTED)
        
        level_tags = {
            "system": {"fg": ShimenColors.TEXT_MUTED, "prefix": "📜 "},
            "ritual": {"fg": ShimenColors.TEXT_GOLD, "prefix": "🛡️ "},
            "action": {"fg": ShimenColors.TEXT_BLUE, "prefix": "🎯 "},
            "success": {"fg": ShimenColors.TEXT_GREEN, "prefix": "✅ "},
            "warning": {"fg": "#d4a017", "prefix": "⚠️ "},
            "error": {"fg": ShimenColors.TEXT_RED, "prefix": "❌ "},
            "process": {"fg": ShimenColors.TEXT_LIGHT, "prefix": "⏳ "}
        }
        
        for level, style in level_tags.items():
            self.log_area.tag_config(f"prefix_{level}", foreground=style["fg"])
            self.log_area.tag_config(f"text_{level}", foreground=style["fg"])
    
    def log(self, msg, level="system"):
        """增强版道统日志系统"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        level_styles = {
            "system": {"fg": ShimenColors.TEXT_MUTED, "prefix": "📜 "},
            "ritual": {"fg": ShimenColors.TEXT_GOLD, "prefix": "🛡️ "},
            "action": {"fg": ShimenColors.TEXT_BLUE, "prefix": "🎯 "},
            "success": {"fg": ShimenColors.TEXT_GREEN, "prefix": "✅ "},
            "warning": {"fg": "#d4a017", "prefix": "⚠️ "},
            "error": {"fg": ShimenColors.TEXT_RED, "prefix": "❌ "},
            "process": {"fg": ShimenColors.TEXT_LIGHT, "prefix": "⏳ "}
        }
        
        style = level_styles.get(level, level_styles["system"])
        
        self.log_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_area.insert(tk.END, style["prefix"], f"prefix_{level}")
        self.log_area.insert(tk.END, f"{msg}\n", f"text_{level}")
        
        self.log_area.see(tk.END)
        self.log_area.update_idletasks()
        
        if level in ["ritual", "success", "action"]:
            self.flash_log_area(style["fg"])
        
        if level in ["ritual", "process"]:
            self.update_status(f"🔄 {msg[:30]}...")
        elif level == "success":
            self.update_status(f"✅ 仪式完成")
    
    def flash_log_area(self, color):
        """日志区域轻微高亮反馈"""
        original_bg = self.log_area.cget("bg")
        
        def restore():
            self.log_area.configure(bg=original_bg)
        
        self.log_area.configure(bg=color + "20")
        self.root.after(80, restore)
    
    def update_status(self, text):
        """更新状态栏"""
        self.status_label.config(text=text)
    
    def clear_log(self):
        """清空日志"""
        self.log_area.delete(1.0, tk.END)
        self.log("日志已清空", "system")
    
    def save_log(self):
        """保存日志到文件"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("日志文件", "*.log"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    log_content = self.log_area.get(1.0, tk.END)
                    f.write(f"知产盾™ 道统行仪日志\n")
                    f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"="*50 + "\n")
                    f.write(log_content)
                
                self.log(f"日志已保存至：{file_path}", "success")
                self.show_ritual_message("日志保存成功", "success")
            except Exception as e:
                self.log(f"保存日志失败：{e}", "error")
    
    def validate_watch_path(self, path):
        """【新功能】智能路径校验"""
        if not path or not os.path.exists(path):
            return False, "❌ 路径不存在或无法访问"
        
        # 防止选择自身所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            if os.path.commonpath([os.path.abspath(path), current_dir]) == os.path.abspath(path):
                return False, "❌ 不能选择程序自身所在目录"
        except:
            pass
        
        # 防止选择父目录（避免循环）
        for prev_path in self.path_history:
            try:
                if os.path.commonpath([path, prev_path]) == prev_path:
                    return False, f"❌ 此目录已在监控历史中，请避免重复选择"
            except:
                pass
        
        # 防止选择系统目录
        system_dirs = ["Windows", "Program Files", "Program Files (x86)", "System32"]
        path_lower = path.lower()
        for dir_name in system_dirs:
            if dir_name.lower() in path_lower:
                return False, "⚠️ 不建议选择系统目录，可能存在权限问题"
        
        return True, "✅ 路径有效"
    
    def choose_dir(self):
        """选择守护道场（目录）"""
        path = filedialog.askdirectory()
        if path:
            # 验证路径
            is_valid, msg = self.validate_watch_path(path)
            if is_valid:
                self.watch_dir.set(path)
                self.path_history.append(path)  # 记录历史
                if len(self.path_history) > 10:  # 只保留最近10条
                    self.path_history.pop(0)
                self.log(f"已择守护道场：{path}", "action")
            else:
                self.show_ritual_message(msg, "warning")
    
    def ritual_one_click_protect(self):
        """道统一键守护仪式"""
        if self.ritual_in_progress:
            return
        
        # 更新导航
        self.update_breadcrumb("🏠 知产盾 > 守护仪式 > 准备中")
        
        owner = self.owner_name.get().strip()
        if not owner:
            self.show_ritual_message("请先确立道主尊号", "warning")
            return
        
        watch_path = self.watch_dir.get()
        if not watch_path or not os.path.exists(watch_path):
            self.show_ritual_message("请先择守护道场", "warning")
            return
        
        # 路径验证
        is_valid, msg = self.validate_watch_path(watch_path)
        if not is_valid:
            self.show_ritual_message(msg, "warning")
            return
        
        self.ritual_in_progress = True
        original_text = self.ritual_button.cget("text")
        self.ritual_button.config(text="🔄 仪式进行中...", state="disabled")
        
        try:
            self.log_area.delete(1.0, tk.END)
            
            self.log("━" * 45, "ritual")
            self.log("知产守护大典 · 启坛", "ritual")
            self.log(f"道主：{owner}", "ritual")
            self.log(f"道场：{watch_path}", "ritual")
            self.log("━" * 45, "ritual")
            
            ritual_steps = [
                ("第一步：神识探查", self.ritual_step_scan, [watch_path]),
                ("第二步：真名烙印", self.ritual_step_evidence, [watch_path, owner]),
                ("第三步：归藏入府", self.ritual_step_archive, [watch_path]),
                ("第四步：法旨封存", self.ritual_step_report, [watch_path])
            ]
            
            all_success = True
            for i, (step_name, step_func, args) in enumerate(ritual_steps):
                self.update_breadcrumb(f"🏠 知产盾 > 守护仪式 > {step_name}")
                self.log(f"\n✨ {step_name} ({i+1}/{len(ritual_steps)})", "ritual")
                step_success = step_func(*args)
                
                if not step_success:
                    all_success = False
                    self.log("❌ 此步受阻，仪式继续", "warning")
            
            self.log("\n" + "━" * 45, "ritual")
            if all_success:
                self.log("✅ 知产守护大典 · 圆满", "ritual")
                self.root.bell()
            else:
                self.log("⚠️ 仪式完成，但有步骤受阻", "warning")
            self.log("━" * 45, "ritual")
            
        finally:
            self.ritual_in_progress = False
            self.ritual_button.config(text=original_text, state="normal")
            self.update_breadcrumb("🏠 知产盾 > 待命")
    
    def ritual_step_scan(self, watch_path):
        """仪式化扫描"""
        self.log("展开神识，探查道场...", "process")
        
        try:
            scanned_files = self.scan_files(watch_path)
            if not scanned_files:
                self.log("道场清净，无真经需守护", "system")
                return False
            
            file_stats = {}
            for file in scanned_files:
                ext = os.path.splitext(file)[1].lower()
                file_stats[ext] = file_stats.get(ext, 0) + 1
            
            self.log(f"探查完成，发现 {len(scanned_files)} 卷待守护真经", "success")
            for ext, count in file_stats.items():
                self.log(f"  {ext} 真经：{count}卷", "system")
            
            self.scanned_files = scanned_files
            return True
            
        except Exception as e:
            self.log(f"探查失败：{e}", "error")
            return False
    
    def ritual_step_evidence(self, watch_path, owner):
        """仪式化确权"""
        if not hasattr(self, 'scanned_files') or not self.scanned_files:
            self.log("无真经可烙印", "warning")
            return False
        
        self.log("开始真名烙印...", "process")
        
        self.processed_files = []
        success_count = 0
        
        for i, file_path in enumerate(self.scanned_files):
            if i % 5 == 0:
                self.log(f"  正在烙印第 {i+1}/{len(self.scanned_files)} 卷...", "process")
            
            evidence_path = self.create_evidence(file_path, owner)
            if evidence_path:
                self.processed_files.append((file_path, evidence_path))
                success_count += 1
        
        if success_count > 0:
            self.log(f"真名烙印完成，成功守护 {success_count} 卷真经", "success")
            return True
        else:
            self.log("真名烙印失败", "error")
            return False
    
    def ritual_step_archive(self, watch_path):
        """仪式化归档"""
        if not self.processed_files:
            self.log("无真经可归档", "warning")
            return False
        
        self.log("开始归藏入府...", "process")
        
        try:
            archive_dir = os.path.join(watch_path, "版权存证库")
            subdirs = ["时间戳证书", "原版文档", "交付版文档", "授权协议", "维权记录"]
            
            for sub in subdirs:
                os.makedirs(os.path.join(archive_dir, sub), exist_ok=True)
            
            for original_path, evidence_path in self.processed_files:
                shutil.copy(evidence_path, os.path.join(archive_dir, "时间戳证书", os.path.basename(evidence_path)))
                shutil.copy(original_path, os.path.join(archive_dir, "原版文档", os.path.basename(original_path)))
            
            self.last_archive_dir = os.path.abspath(archive_dir)
            self.log(f"归藏完成！存证府库：{self.last_archive_dir}", "success")
            return True
            
        except Exception as e:
            self.log(f"归藏失败：{e}", "error")
            return False
    
    def ritual_step_report(self, archive_dir):
        """仪式化报告"""
        if not self.processed_files:
            return False
        
        self.root.after(1000, lambda: self.show_ritual_report(archive_dir))
        return True
    
    def show_ritual_report(self, archive_dir):
        """显示道统仪式报告"""
        report_win = tk.Toplevel(self.root)
        report_win.title("知产守护法旨 · 复盘真言")
        
        screen_width = report_win.winfo_screenwidth()
        screen_height = report_win.winfo_screenheight()
        window_width, window_height = 850, 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        report_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        report_win.resizable(False, False)
        report_win.configure(bg=ShimenColors.BG_OUTER)
        
        canvas = tk.Canvas(report_win, bg=ShimenColors.BG_OUTER, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        canvas.create_rectangle(25, 25, 825, 575, 
                              fill=ShimenColors.BG_CARD, 
                              outline=ShimenColors.BORDER_RITUAL, width=3)
        
        canvas.create_rectangle(10, 150, 25, 450, 
                              fill="#5a4532", outline="#3a2512", width=2)
        canvas.create_rectangle(825, 150, 840, 450, 
                              fill="#5a4532", outline="#3a2512", width=2)
        
        scroll_rect = canvas.create_rectangle(25, 25, 25, 575, 
                                            fill=ShimenColors.BG_CARD, 
                                            outline=ShimenColors.BORDER_RITUAL, width=3)
        
        def unroll_scroll(step=25):
            if step < 825:
                canvas.coords(scroll_rect, 25, 25, step, 575)
                report_win.after(10, lambda: unroll_scroll(step+20))
            else:
                show_content()
        
        def show_content():
            title_frame = tk.Frame(canvas, bg=ShimenColors.BG_CARD)
            canvas.create_window(425, 70, window=title_frame)
            
            tk.Label(title_frame, text="◆ 知产守护法旨 ◆", 
                    font=("篆书", 20, "bold"), 
                    bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_GOLD).pack()
            
            tk.Frame(title_frame, bg=ShimenColors.BORDER_GOLD, height=2, width=320).pack(pady=5)
            
            content_frame = tk.Frame(canvas, bg=ShimenColors.BG_CARD)
            canvas.create_window(425, 300, window=content_frame)
            
            left_frame = tk.Frame(content_frame, bg=ShimenColors.BG_CARD)
            left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
            
            tk.Label(left_frame, text="【守护成果】", font=FONT_HEADING,
                    bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_GOLD).pack(anchor="w", pady=(0, 10))
            
            result_card = tk.Frame(left_frame, bg=ShimenColors.CARD_SUCCESS, 
                                 relief="solid", bd=1, padx=15, pady=15)
            result_card.pack(fill="both", expand=True)
            
            result_text = f"""
╔════════ 道统战绩 ════════╗
  🎯 真经守护：{len(self.processed_files)}卷
  🛡️ 法印镌刻：{len(self.processed_files)}枚
  📚 归藏入府：已完成
  🔐 结界强度：金刚不坏
  📁 存证府库：版权存证库
╚══════════════════════════╝
            """
            
            result_display = tk.Text(result_card, height=8, width=30,
                                   bg=ShimenColors.CARD_SUCCESS, 
                                   fg=ShimenColors.TEXT_GREEN,
                                   font=FONT_BODY, relief="flat", wrap="word")
            result_display.pack(fill="both", expand=True)
            result_display.insert(1.0, result_text)
            result_display.config(state="disabled")
            
            right_frame = tk.Frame(content_frame, bg=ShimenColors.BG_CARD)
            right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)
            
            tk.Label(right_frame, text="【法印授权】", font=FONT_HEADING,
                    bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_GOLD).pack(anchor="w", pady=(0, 10))
            
            auth_text = """请选择真经使用法印：
            
🔐 仅个人参悟
   - 禁止外传
   - 禁止商用
   
📖 可传阅，需注吾名
   - 需注明出处
   - 需链接道主
   
⚔️ 可商用，需遵吾法
   - 需遵守协议
   - 可商议润格"""
            
            auth_label = tk.Label(right_frame, text=auth_text, font=FONT_BODY,
                                bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_LIGHT,
                                justify="left")
            auth_label.pack(anchor="w", pady=10)
            
            self.auth_var = tk.StringVar(value="仅个人参悟")
            
            auth_options = [
                ("🔐 仅个人参悟，禁传外道", "仅个人参悟"),
                ("📖 可传阅，需注吾名", "可传阅"),
                ("⚔️ 可商用，需遵吾法", "可商用"),
            ]
            
            for text, value in auth_options:
                frame = tk.Frame(right_frame, bg=ShimenColors.BG_INPUT, padx=10, pady=5)
                frame.pack(fill="x", pady=3)
                
                tk.Radiobutton(frame, variable=self.auth_var, value=value,
                              bg=ShimenColors.BG_INPUT, fg=ShimenColors.TEXT_LIGHT,
                              selectcolor=ShimenColors.BTN_GOLD,
                              activebackground=ShimenColors.BG_INPUT).pack(side="left", padx=5)
                tk.Label(frame, text=text, font=FONT_SMALL,
                        bg=ShimenColors.BG_INPUT, fg=ShimenColors.TEXT_LIGHT).pack(side="left")
            
            seal_button = tk.Button(content_frame, text="⚜️ 钤印确认", 
                                  font=("篆书", 14, "bold"),
                                  bg=ShimenColors.BTN_RITUAL, fg=ShimenColors.TEXT_GOLD,
                                  relief="ridge", bd=2,
                                  command=lambda: self.save_auth_and_close(archive_dir, report_win))
            canvas.create_window(425, 500, window=seal_button)
            
            tk.Label(canvas, 
                    text=f"道主：{self.owner_name.get()}\n法旨颁行：{datetime.now().strftime('%Y年%m月%d日 %H时%M分')}", 
                    font=FONT_SMALL, bg=ShimenColors.BG_CARD, fg=ShimenColors.TEXT_MUTED
                    ).place(x=425, y=540, anchor="center")
        
        unroll_scroll()
    
    def save_auth_and_close(self, archive_dir, window):
        """保存授权并关闭窗口"""
        auth_choice = self.auth_var.get()
        auth_texts = {
            "仅个人参悟": "仅个人参悟，不外传",
            "可传阅": "可传阅，需注明出处",
            "可商用": "可商用，需遵守授权协议"
        }
        
        auth_file = os.path.join(archive_dir, "授权协议", "法旨授权声明.txt")
        os.makedirs(os.path.dirname(auth_file), exist_ok=True)
        
        with open(auth_file, "w", encoding="utf-8") as f:
            f.write("【知产守护法旨】\n")
            f.write("═" * 35 + "\n")
            f.write(f"道主：{self.owner_name.get()}\n")
            f.write(f"授权法印：{auth_texts[auth_choice]}\n")
            f.write(f"钤印时间：{datetime.now().strftime('%Y年%m月%d日 %H时%M分')}\n")
            f.write("═" * 35 + "\n")
            f.write("此法旨由知产盾™道统守护结界自动生成\n")
            f.write("师门™出品 · 万法归宗 · 道统永续\n")
        
        canvas = window.winfo_children()[0]
        
        def roll_up_scroll(step=825):
            if step > 25:
                canvas.coords("scroll_rect", 25, 25, step, 575)
                window.update()
                window.after(10, lambda: roll_up_scroll(step-20))
            else:
                window.destroy()
                self.show_ritual_message(f"法旨已钤印：{auth_texts[auth_choice]}", "success")
        
        roll_up_scroll()
    
    def scan_files(self, watch_path):
        """扫描文件"""
        found = []
        file_types = [".md", ".txt", ".py", ".json", ".pdf", ".docx", 
                     ".jpg", ".png", ".gif", ".html", ".css", ".js",
                     ".ai", ".psd", ".fig", ".sketch", ".mp3", ".mp4",
                     ".wav", ".mov", ".avi", ".zip", ".rar"]
        
        for root, dirs, files in os.walk(watch_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "版权存证库"]
            
            for file in files:
                if any(file.lower().endswith(ft) for ft in file_types):
                    found.append(os.path.join(root, file))
        
        return found
    
    def create_evidence(self, file_path, author):
        """创建存证文件"""
        try:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                content_hash = str(hash(content))
            except:
                stat = os.stat(file_path)
                content_hash = f"bin_{stat.st_size}_{stat.st_mtime}"
            
            evidence = {
                "file_name": os.path.basename(file_path),
                "file_path": os.path.dirname(file_path),
                "file_size": os.path.getsize(file_path),
                "file_hash": content_hash,
                "owner": author,
                "create_time": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
                "modify_time": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "evidence_time": datetime.now().isoformat(),
                "evidence_tool": "知产盾™ V2.5 道统自指版"
            }
            
            output_path = file_path + ".evidence.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(evidence, f, indent=2, ensure_ascii=False)
            
            return output_path
            
        except Exception as e:
            self.log(f"创建存证失败 {os.path.basename(file_path)}: {e}", "error")
            return None
    
    def show_ritual_message(self, message, level="info"):
        """显示道统仪式消息"""
        colors = {
            "warning": ShimenColors.CARD_WARNING,
            "success": ShimenColors.CARD_SUCCESS,
            "error": ShimenColors.TEXT_RED,
            "info": ShimenColors.BG_CARD
        }
        
        bg_color = colors.get(level, ShimenColors.BG_CARD)
        fg_color = ShimenColors.TEXT_LIGHT if level != "success" else ShimenColors.TEXT_GREEN
        
        message_frame = tk.Frame(self.root, bg=ShimenColors.BG_OUTER, height=45)
        message_frame.place(relx=0.5, rely=0.12, anchor="center", width=450)
        
        inner_frame = tk.Frame(message_frame, bg=bg_color, relief="solid", bd=1,
                              highlightbackground=ShimenColors.BORDER_GOLD)
        inner_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        tk.Label(inner_frame, text=message, font=FONT_BODY, 
                bg=bg_color, fg=fg_color).pack(pady=10)
        
        def fade_out(step=10):
            if step > 0:
                new_rely = 0.12 - (0.015 * (10-step))
                message_frame.place_configure(relx=0.5, rely=new_rely, anchor="center")
                message_frame.after(50, lambda: fade_out(step-1))
            else:
                message_frame.destroy()
        
        self.root.after(1500, fade_out)

if __name__ == "__main__":
    root = tk.Tk()
    app = CreatorProtectionApp(root)
    root.mainloop()