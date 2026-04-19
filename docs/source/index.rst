.. wpipe documentation master file

.. include:: <isonum.txt>

.. raw:: html

    <style>
        .hero-section {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            padding: 80px 40px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            pointer-events: none;
        }
        .hero-section h1 {
            font-size: 4em;
            margin-bottom: 20px;
            color: white;
            font-weight: 800;
            letter-spacing: -0.02em;
            position: relative;
        }
        .hero-section h1 .logo {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero-section p.lead {
            font-size: 1.4em;
            margin-bottom: 30px;
            color: #a0aec0;
            position: relative;
        }
        .hero-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
            position: relative;
        }
        .hero-buttons a {
            padding: 16px 36px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .hero-buttons a:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: white;
            border: 2px solid rgba(255,255,255,0.2);
        }
        .btn-secondary:hover {
            background: rgba(255,255,255,0.2);
            border-color: rgba(255,255,255,0.4);
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }
        .feature-card {
            padding: 30px;
            border-radius: 12px;
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        .feature-card h3 {
            color: #2d3748;
            font-size: 1.3em;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .feature-card h3 span {
            font-size: 1.4em;
        }
        .feature-card p {
            color: #718096;
            line-height: 1.7;
        }
        .code-block {
            background: #1a1a2e;
            color: #e2e8f0;
            padding: 25px;
            border-radius: 12px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9em;
            line-height: 1.6;
            margin: 20px 0;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 40px 0;
        }
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
        }
        .stat-box .value {
            font-size: 3em;
            font-weight: 800;
        }
        .stat-box .label {
            font-size: 0.95em;
            opacity: 0.9;
            margin-top: 5px;
        }
        @media (max-width: 768px) {
            .stat-grid { grid-template-columns: repeat(2, 1fr); }
            .hero-section { padding: 40px 20px; }
            .hero-section h1 { font-size: 2.5em; }
            .hero-buttons { flex-direction: column; }
        }
    </style>

.. raw:: html

    <div class="hero-section">
        <h1><span class="logo">wpipe</span></h1>
        <p class="lead">Python Pipeline Library for Industrial-Grade Orchestration</p>
        <p style="font-size: 1.15em; color: #cbd5e0; max-width: 800px; margin: 0 auto; position: relative;">
            Build powerful, production-ready data processing pipelines with native parallelism, intelligent recovery, and deep observability.<br>
            <strong>No web UI required</strong> | <strong>High-Performance</strong> | <strong>Resilient by Design</strong>
        </p>
        <div class="hero-buttons">
            <a href="getting_started.html" class="btn-primary">🚀 Get Started</a>
            <a href="https://github.com/wisrovi/wpipe" class="btn-secondary" target="_blank">⭐ GitHub</a>
            <a href="installation.html" class="btn-secondary">📦 Install</a>
            <a href="https://pypi.org/project/wpipe/" class="btn-secondary" target="_blank">PyPI</a>
        </div>
    </div>

.. image:: https://img.shields.io/pypi/v/wpipe.svg
   :target: https://pypi.org/project/wpipe/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/wpipe.svg
   :target: https://pypi.org/project/wpipe/
   :alt: Python Versions

.. image:: https://img.shields.io/github/license/wisrovi/wpipe.svg
   :target: https://github.com/wisrovi/wpipe/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/badge/tests-625%20passing-10b981
   :alt: Tests

.. image:: https://img.shields.io/badge/LTS-1.6.1-green
   :alt: LTS

wpipe |version| Documentation
=============================

**wpipe** is a powerful, industrial-grade Python library for orchestrating high-performance data processing pipelines with native support for parallelism, intelligent recovery, and deep observability.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: 📚 Documentation

   getting_started
   installation
   usage
   user_guide/index
   tutorials
   api_reference
   examples/index
   architecture
   best_practices
   faq
   glossary
   contributing
   changelog

🎯 Why wpipe?
--------------

Traditional workflow tools like Apache Airflow, Prefect, or Dagster are excellent but often introduce **significant complexity**. **wpipe** provides a refreshing alternative for high-performance engineering:

.. raw:: html

    <div class="feature-grid">
        <div class="feature-card">
            <h3><span>⚡</span> Lightning Mode</h3>
            <p>Optimized SQLite architecture with WAL mode and non-blocking monitoring. Designed for high-frequency bursts.</p>
        </div>
        <div class="feature-card">
            <h3><span>🧵</span> Native Parallelism</h3>
            <p>Execute steps using Threading or Process pooling with a single command. Full GIL bypass for CPU-heavy tasks.</p>
        </div>
        <div class="feature-card">
            <h3><span>🛡️</span> Intelligent Checkpoints</h3>
            <p>Define milestones using logical expressions. Auto-resume exactly where you left off after system failures.</p>
        </div>
        <div class="feature-card">
            <h3><span>🔍</span> Forensic Error Capture</h3>
            <p>Get the exact file path and line number of any failure with automatic notification hooks (Telegram/Slack ready).</p>
        </div>
        <div class="feature-card">
            <h3><span>🧬</span> Data Contracts</h3>
            <p>Strict schema validation for your data context using <code>PipelineContext</code> and <code>TypeValidator</code>.</p>
        </div>
        <div class="feature-card">
            <h3><span>🔄</span> Async/Sync Parity</h3>
            <p>Choose between <code>Pipeline</code> or <code>PipelineAsync</code> with 100% feature parity and coroutine support.</p>
        </div>
    </div>

🚀 Quick Start
--------------

Get up and running in under 2 minutes:

Installation
~~~~~~~~~~~~

.. code-block:: bash

    # Install wpipe from PyPI
    pip install wpipe

Your First Pipeline
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline, step

    @step(name="Process", retry_count=3)
    def my_step(data):
        return {"result": data.get("x", 0) * 2}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([my_step])

    result = pipeline.run({"x": 10})
    # Output: {'x': 10, 'result': 20}

📊 Key Statistics
-----------------

.. raw:: html

    <div class="stat-grid">
        <div class="stat-box">
            <div class="value">625</div>
            <div class="label">Tests Passing</div>
        </div>
        <div class="stat-box">
            <div class="value">200+</div>
            <div class="label">Verified Examples</div>
        </div>
        <div class="stat-box">
            <div class="value">100%</div>
            <div class="label">Type Hints</div>
        </div>
        <div class="stat-box">
            <div class="value">LTS</div>
            <div class="label">1.6.1</div>
        </div>
    </div>

📝 License & Author
-------------------

**License**: MIT License
**Author**: William Steve Rodriguez Villamizar

- GitHub: https://github.com/wisrovi
- LinkedIn: https://linkedin.com/in/wisrovi-rodriguez

If you find wpipe useful, please ⭐ star the repository on GitHub!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
