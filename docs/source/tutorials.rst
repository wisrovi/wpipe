WPipe Academy: Master Your Pipelines
====================================

.. meta::
   :description: Complete learning path for wpipe, from basic concepts to advanced enterprise patterns.
   :keywords: tutorials, learning, academy, pipeline, wpipe, automation

Welcome to the **WPipe Academy**. This section is your definitive guide to becoming a master of industrial-grade pipeline orchestration. Whether you are building simple ETL scripts or complex, distributed microservices, these tutorials will guide you through every feature of |wpipe|.

.. raw:: html

    <div class="hero-section" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 40px; border-radius: 16px; margin-bottom: 40px; border-left: 8px solid #00f2fe;">
        <h2 style="color: #00f2fe; margin-top: 0;">🚀 The Learning Path</h2>
        <p style="color: #94a3b8; font-size: 1.1em;">
            Our curriculum is designed to take you from a curious beginner to a senior pipeline architect. 
            Follow the 130-level tour for a deep dive, or jump into specific tutorials to solve your immediate problems.
        </p>
    </div>

.. toctree::
   :maxdepth: 2
   :hidden:

   tutorials/tour/index
   tutorials/basic_pipeline
   tutorials/class_steps
   tutorials/api_integration
   tutorials/error_handling
   tutorials/retry_logic
   tutorials/nested_pipelines
   tutorials/sqlite_integration
   tutorials/yaml_config
   tutorials/conditions
   tutorials/advanced_patterns
   tutorials/production_deployment

The Learning Tour
-----------------

.. raw:: html

    <div class="feature-grid">
        <div class="feature-card" style="grid-column: span 2; background: rgba(0, 242, 254, 0.05); border: 2px solid rgba(0, 242, 254, 0.3);">
            <h3><span>🏆</span> The 130-Level Tour de Aprendizaje</h3>
            <p>A massive, step-by-step journey through every single capability of the engine. Each level introduces one new concept, building upon the last.</p>
            <p><strong>Status:</strong> Available (Levels 1-130)</p>
            <a href="tutorials/tour/index.html" class="btn-primary" style="display: inline-block; margin-top: 15px; text-decoration: none;">Start The Tour →</a>
        </div>
    </div>

Core Curriculum
---------------

.. raw:: html

    <div class="feature-grid">
        <div class="feature-card">
            <h3><span>🌱</span> 1. Basic Foundations</h3>
            <p>Learn the core mental model of wpipe: Pipelines, Steps, and Context. Ideal for your first 30 minutes.</p>
            <ul>
                <li><a href="tutorials/basic_pipeline.html">Basic Pipeline</a></li>
                <li><a href="tutorials/class_steps.html">Class-based Steps</a></li>
                <li><a href="tutorials/yaml_config.html">YAML Configuration</a></li>
            </ul>
        </div>
        <div class="feature-card">
            <h3><span>🛡️</span> 2. Resiliency & Reliability</h3>
            <p>Master the features that keep your pipelines running when things go wrong in production.</p>
            <ul>
                <li><a href="tutorials/error_handling.html">Error Handling</a></li>
                <li><a href="tutorials/retry_logic.html">Retry Strategies</a></li>
                <li><a href="tutorials/sqlite_integration.html">SQLite Persistence</a></li>
            </ul>
        </div>
        <div class="feature-card">
            <h3><span>🧩</span> 3. Advanced Orchestration</h3>
            <p>Combine pipelines, use logic, and scale with parallelism for complex enterprise workflows.</p>
            <ul>
                <li><a href="tutorials/nested_pipelines.html">Nested Pipelines</a></li>
                <li><a href="tutorials/conditions.html">Conditional Logic</a></li>
                <li><a href="tutorials/advanced_patterns.html">Advanced Patterns</a></li>
            </ul>
        </div>
        <div class="feature-card">
            <h3><span>🌐</span> 4. Integration & Operations</h3>
            <p>Connect your pipelines to the world and monitor them like a pro.</p>
            <ul>
                <li><a href="tutorials/api_integration.html">API & Dashboard</a></li>
                <li><a href="tutorials/production_deployment.html">Production Ready</a></li>
            </ul>
        </div>
    </div>

Recommended Learning Plan
-------------------------

We've structured this academy to fit into your busy schedule.

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Phase
     - Focus
     - Estimated Time
   * - **Phase 1**
     - :doc:`tutorials/basic_pipeline`, :doc:`tutorials/class_steps`, :doc:`tutorials/yaml_config`
     - 2 hours
   * - **Phase 2**
     - :doc:`tutorials/error_handling`, :doc:`tutorials/sqlite_integration`, :doc:`tutorials/api_integration`
     - 4 hours
   * - **Phase 3**
     - :doc:`tutorials/retry_logic`, :doc:`tutorials/conditions`, :doc:`tutorials/nested_pipelines`
     - 4 hours
   * - **Phase 4**
     - :doc:`tutorials/advanced_patterns`, :doc:`tutorials/production_deployment`
     - 3 hours

Troubleshooting During Tutorials
--------------------------------

If you encounter issues during the tutorials:

.. raw:: html

    <div style="background: rgba(245, 158, 11, 0.1); border-left: 5px solid #f59e0b; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <p style="margin: 0;"><strong>Common Pitfalls:</strong></p>
        <ul style="margin: 10px 0 0 0;">
            <li><strong>Step Output:</strong> Ensure every step returns a dictionary. Returning <code>None</code> or a non-dict will break the chain.</li>
            <li><strong>Context Keys:</strong> Be careful with key naming to avoid overwriting data from previous steps unless intentional.</li>
            <li><strong>Async Mismatch:</strong> Don't mix <code>Pipeline</code> with async steps, use <code>PipelineAsync</code> instead.</li>
        </ul>
    </div>

Next Steps
----------

After completing these tutorials:

- Explore the :doc:`user_guide/index` for in-depth technical deep dives.
- Check the :doc:`api_reference` for the complete specification.
- Review :doc:`best_practices` to write idiomatic and clean code.