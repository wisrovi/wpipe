# Stop Mixing Orchestration with Your Business Logic! 🛑

We've all seen that "God Script". You know the one: a 2,000-line Python file where API calls, database queries, error handling, and business logic are all tangled up in a giant `try/except` block.

It works... until it doesn't. And when it fails, good luck finding where the "Business Logic" ends and the "Infrastructure Plumbing" begins.

Today, I want to talk about how to separate these concerns using **wpipe** to keep your code clean, testable, and maintainable.

## The Problem: The "Spaghetti" Pipeline

In a typical script, your core logic (e.g., "Calculate Discount") is buried under infrastructure concerns:
*   How do I retry if the DB is down?
*   How do I log the input/output of this specific step?
*   How do I save progress so I don't restart from zero?

When you mix these, your business logic becomes untestable.

## The Solution: Declarative Orchestration

**wpipe** allows you to keep your functions "Pure". Your business logic stays as simple Python functions, while wpipe handles the "Plumbing".

### Step 1: Define Pure Business Logic
```python
# No infrastructure code here!
def calculate_premium(user_age, base_price):
    if user_age < 25:
        return base_price * 1.5
    return base_price
```

### Step 2: Decorate and Orchestrate
By adding the `@step` decorator, you give this function "Superpowers" without changing its core logic.

```python
from wpipe import Pipeline, step

@step(name="PremiumCalculation")
def calculate_premium_step(data):
    # Unwrap data, call pure logic, wrap result
    price = calculate_premium(data['age'], data['base'])
    return {"premium": price}

pipeline = Pipeline(pipeline_name="InsuranceBot")
pipeline.set_steps([calculate_premium_step])
```

## Why This Matters

### 1. Unit Testing is a Breeze
Since your core logic is in a pure function, you can test it without worrying about pipelines, databases, or environment variables.

### 2. Forensic Tracking
wpipe automatically logs the input and output of every `@step`. If a "Premium Calculation" looks wrong, you don't need to add `print()` statements. Just check the wpipe tracker.

### 3. Readability (The YAML advantage)
You can even define your pipeline structure in a YAML file. This means anyone (even a non-dev) can look at the YAML and understand the business flow, while the developers focus on the Python code.

```yaml
# pipeline_config.yaml
pipeline_name: InsuranceBot
steps:
  - name: FetchUser
  - name: PremiumCalculation
  - name: SendQuote
```

## Conclusion

Clean code isn't just about aesthetics; it's about reducing the cognitive load of your team. By delegating orchestration, retries, and persistence to **wpipe**, you free your brain to focus on what actually matters: **The Business Logic.**

Join the +117k developers who are cleaning up their Python stacks with wpipe. 🐍

#CleanCode #Python #SoftwareEngineering #BestPractices #Automation
