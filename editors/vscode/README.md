# 🚀 WPipe VS Code Tools

[![Version](https://img.shields.io/visual-studio-marketplace/v/wpipe.wpipe-vscode?style=flat-square&color=blue)](https://marketplace.visualstudio.com/items?itemName=wpipe.wpipe-vscode)
[![Author](https://img.shields.io/badge/Author-wisrovi-orange?style=flat-square)](https://github.com/wisrovi)
[![License](https://img.shields.io/github/license/wisrovi/wpipe?style=flat-square&color=green)](https://github.com/wisrovi/wpipe/blob/main/LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-William_Rodriguez-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/wisrovi/)

<img width="1682" height="943" alt="image" src="https://github.com/user-attachments/assets/9618bcca-4253-43b1-a483-7941a1130edf" />

**The Swiss Army Knife for Pipeline Orchestration with WPipe.**

Elevate your Python data engineering with intelligent tools designed to maximize speed, clarity, and resilience. This extension provides a deep, seamless integration of the **WPipe** engine directly into your favorite editor, turning complex orchestration into a visual and intuitive experience.

---

## 💎 Why WPipe Tools?

Traditional pipeline development can be opaque and error-prone. **WPipe Tools** changes the game by giving you visual superpowers and intelligent automation.

### 📊 Real-Time DAG Visualization & Interaction
Stop guessing how your data flows. Watch your architecture come to life as you write code.
- **Instant Insights:** Generate high-fidelity Directed Acyclic Graphs (DAG) from your `.py` and `.yaml` configurations.
- **Bi-directional Navigation:** Click any node in the DAG to jump directly to its definition in the code.
- **Live Feedback:** The visualization panel refreshes instantly on save, helping you catch logic errors before they hit production.
- **Interactive Exploration:** Zoom, pan, and navigate through complex architectures with professional-grade controls.
- **Pro Exports:** Download your architecture as high-quality **SVG** or **PNG** for documentation.

### 🔍 Step Registry & Impact Analysis
Master your ecosystem of reusable components.
- **Centralized Hub:** A dedicated sidebar view maps every `@step` across your entire workspace.
- **Precision Navigation:** Click any step to teleport directly to its implementation.
- **Impact Analysis:** Right-click a step to see exactly which pipelines and files across your workspace will be affected if you change its logic.
- **One-Click Testing:** Run and validate individual steps in isolation without launching the full pipeline.

### 🐞 Debugging & Observability
Understand failures faster than ever.
- **Integrated Dashboard:** Access the WPipe real-time monitoring dashboard natively within a VS Code tab—no external browser needed.
- **Log Replay:** Load any WPipe log file to automatically highlight failed steps in the editor and the DAG view. See exactly where the data stopped flowing.

### 🤖 AI Pipeline Assistant
Accelerate your development with artificial intelligence.
- **AI Scaffolding:** Describe your pipeline in natural language (e.g., "A pipeline with parallel tasks that saves to SQLite") and get a production-ready structure instantly.
- **Optimization Tips:** The DAG panel automatically suggests performance improvements, like where you can use `Parallel` blocks to speed up execution.

### 🧠 Intelligent snippets (The "Pro" Way)
Don't just write code—write *excellent* code.
- **`wpstep` / `wpstepadv`**: Create everything from simple functions to robust classes with built-in retries and timeouts.
- **`wppipe` / `wppipeadv`**: Scaffold production-ready pipelines with metric tracking and persistence in seconds.
- **Quick Fixes:** Hover over any standard Python function and click the lightbulb to instantly convert it into a WPipe Step.

### 🛡️ World-Class YAML Validation
Safety first. Eliminate configuration errors before they happen.
- **Smart Autocomplete:** Intelligent schema-aware suggestions for your `*.wpipe.yaml` files.
- **Validation Engine:** Real-time warnings if you use a step that doesn't exist in your workspace or the official catalog.

---

## 🚀 Getting Started

1. **Install:** Search for `WPipe Tools` in the VS Code Marketplace or press `Ctrl+P` and type `ext install wpipe.wpipe-vscode`.
2. **Activate:** Open any Python (`.py`) or WPipe YAML (`.yaml`) file.
3. **Visualize:** Open the Command Palette (`Ctrl+Shift+P`) and run `WPipe: Preview Pipeline DAG`.

---

## 🛠️ Key Commands

| Command | Action |
|---------|--------|
| `WPipe: Preview Pipeline DAG` | Open the interactive graph visualizer with bi-directional navigation. |
| `WPipe: Open Web Dashboard` | Launch the native real-time monitoring dashboard inside VS Code. |
| `WPipe: Replay Log Errors` | Load a log file to highlight errors in code and DAG. |
| `WPipe: AI Pipeline Assistant` | Generate pipeline structures using natural language. |
| `WPipe: Search & Import Steps` | Browse the global component library. |
| `WPipe: Show Cheat Sheet / Help` | Instant access to the pro-tips guide. |

---

## 📄 License

MIT License - Crafted with ❤️ by **William Rodriguez** (wisrovi).

---

**Built for engineers who demand excellence in data orchestration.**
[Visit the official WPipe repository](https://github.com/wisrovi/wpipe)
