Conditional Branches Tutorial
===========================

Learn how to execute different paths based on data conditions with the Condition class.

.. contents::
   :local:
   :depth: 3

1. Introduction
---------------

Conditional branches allow your pipeline to:

- **Execute different steps** based on data values
- **Build decision trees** with multiple paths
- **Handle multiple scenarios** in one pipeline
- **Skip steps** when conditions aren't met

The ``Condition`` class evaluates Python expressions against the pipeline data and routes execution accordingly.

1.1 When to Use Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use conditions when:

- Processing different data types requires different logic
- You need to validate input before processing
- Different user types or configurations require different flows
- Error recovery paths are needed
- Optional processing steps should be skipped

1.2 Basic Concept
~~~~~~~~~~~~~~~~

::

    ┌─────────────────────────────────────────────────────────────────┐
    │                     CONDITION FLOW                              │
    └─────────────────────────────────────────────────────────────────┘
    
    ┌──────────┐     ┌─────────────────┐
    │  Data   │────▶│   Condition    │
    └──────────┘     │  (expression) │
                      └───────┬────────┘
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
        ┌───────────┐               ┌───────────┐
        │   TRUE    │               │   FALSE   │
        │ branch    │               │ branch    │
        └───────────┘               └───────────┘

2. Condition Class Reference
---------------------------

.. code-block:: python

    from wpipe.pipe import Condition

    condition = Condition(
        expression="data_key == 'expected_value'",
        branch_true=[(step_a, "Step A", "v1.0")],
        branch_false=[(step_b, "Step B", "v1.0")],
    )

**Parameters:**

- **expression**: Python expression evaluated against pipeline data
- **branch_true**: List of steps executed when expression is True
- **branch_false**: (Optional) List of steps executed when expression is False

3. Basic Examples
-----------------

3.1 Simple Boolean Check
~~~~~~~~~~~~~~~~~~~~~~~

The most common use case - check if a value is greater than a threshold:

.. code-block:: python

    from wpipe import Pipeline, Condition

    def check_score(data):
        return {"score": 85}

    def process_high_score(data):
        return {"grade": "A", "message": "Excellent!"}

    def process_low_score(data):
        return {"grade": "B", "message": "Good job!"}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (check_score, "Check Score", "v1.0"),
        Condition(
            expression="score >= 80",
            branch_true=[(process_high_score, "High Score", "v1.0")],
            branch_false=[(process_low_score, "Low Score", "v1.0")],
        ),
    ])

    result = pipeline.run({})
    # Output: {'score': 85, 'grade': 'A', 'message': 'Excellent!'}

3.2 String Matching
~~~~~~~~~~~~~~~~~~~

Check for specific string values:

.. code-block:: python

    def detect_status(data):
        return {"status": "active"}

    def handle_active(data):
        return {"action": "Process normally"}

    def handle_inactive(data):
        return {"action": "Reactivate account"}

    condition = Condition(
        expression="status == 'active'",
        branch_true=[(handle_active, "Active", "v1.0")],
        branch_false=[(handle_inactive, "Inactive", "v1.0")],
    )

3.3 Without Else Branch
~~~~~~~~~~~~~~~~~~~~~~~

Execute steps only when condition is true, skip otherwise:

.. code-block:: python

    def check_premium(data):
        return {"user_type": "premium"}

    def apply_premium_features(data):
        return {"features": ["advanced", "exclusive", "priority"]}

    condition = Condition(
        expression="user_type == 'premium'",
        branch_true=[(apply_premium_features, "Apply Premium", "v1.0")],
        # No branch_false - steps are skipped if condition is False
    )

4. Complex Conditions
---------------------

4.1 Multiple Comparisons
~~~~~~~~~~~~~~~~~~~~~~~

Combine multiple conditions:

.. code-block:: python

    Condition(
        expression="age >= 18 and status == 'active'",
        branch_true=[(grant_access, "Grant Access", "v1.0")],
        branch_false=[(deny_access, "Deny Access", "v1.0")],
    )

4.2 Numeric Ranges
~~~~~~~~~~~~~~~~~

Check if values fall within ranges:

.. code-block:: python

    Condition(
        expression="0 <= temperature <= 30",
        branch_true=[(comfortable, "Comfortable", "v1.0")],
        branch_false=[(extreme, "Extreme Temp", "v1.0")],
    )

4.3 In Operator
~~~~~~~~~~~~~~~

Check if value is in a list:

.. code-block:: python

    Condition(
        expression="role in ['admin', 'moderator', 'editor']",
        branch_true=[(allow_edit, "Allow Edit", "v1.0")],
        branch_false=[(read_only, "Read Only", "v1.0")],
    )

4.4 String Contains
~~~~~~~~~~~~~~~~~~~

Check if string contains substring:

.. code-block:: python

    Condition(
        expression="'error' in message.lower()",
        branch_true=[(log_error, "Log Error", "v1.0")],
        branch_false=[(log_info, "Log Info", "v1.0")],
    )

5. Nested Conditions
--------------------

5.1 Chained Conditions
~~~~~~~~~~~~~~~~~~~~~~

Create decision trees with multiple conditions:

.. code-block:: python

    from wpipe import Pipeline, Condition

    def classify(data):
        return {"score": 75, "category": "math"}

    def excellent_path(data):
        return {"path": "honors"}

    def good_path(data):
        return {"path": "standard"}

    def needs_improvement(data):
        return {"path": "remedial"}

    def math_path(data):
        return {"path": "advanced_math"}

    condition = Condition(
        expression="score >= 90",
        branch_true=[(excellent_path, "Excellent", "v1.0")],
        branch_false=[(Condition(
            expression="score >= 70",
            branch_true=[(good_path, "Good", "v1.0")],
            branch_false=[(needs_improvement, "Needs Help", "v1.0")],
        )],
    )

5.2 Multiple Independent Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple conditions at the same level:

.. code-block:: python

    def analyze_data(data):
        return {"has_error": False, "is_complete": True}

    def handle_error(data):
        return {"status": "error_handled"}

    def handle_complete(data):
        return {"status": "complete"}

    def handle_incomplete(data):
        return {"status": "incomplete"}

    # First check for errors
    error_condition = Condition(
        expression="has_error == True",
        branch_true=[(handle_error, "Handle Error", "v1.0")],
    )

    # Then check completion
    complete_condition = Condition(
        expression="is_complete == True",
        branch_true=[(handle_complete, "Complete", "v1.0")],
        branch_false=[(handle_incomplete, "Incomplete", "v1.0")],
    )

6. Real-World Examples
-----------------------

6.1 User Registration Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline, Condition

    def validate_registration(data):
        return {
            "email": "user@example.com",
            "age": 16,
            "country": "US"
        }

    def register_standard(data):
        return {"account_type": "standard"}

    def register_minor(data):
        return {"account_type": "restricted", "requires_guardian": True}

    def block_registration(data):
        return {"status": "blocked", "reason": "Age requirements not met"}

    def send_verification(data):
        return {"verification_sent": True}

    def flag_for_review(data):
        return {"flagged": True}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (validate_registration, "Validate", "v1.0"),
        # Check age first
        Condition(
            expression="age >= 18",
            branch_true=[(register_standard, "Register Adult", "v1.0")],
            branch_false=[(register_minor, "Register Minor", "v1.0")],
        ),
        # Then check country for additional verification
        Condition(
            expression="country in ['US', 'UK', 'CA']",
            branch_true=[(send_verification, "Send Verification", "v1.0")],
            branch_false=[(flag_for_review, "Flag for Review", "v1.0")],
        ),
    ])

6.2 Order Processing
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def process_order(data):
        return {
            "order_total": 150.00,
            "customer_type": "premium",
            "items_in_stock": True
        }

    def apply_premium_discount(data):
        return {"discount": 0.20, "final_total": data["order_total"] * 0.80}

    def apply_standard_discount(data):
        return {"discount": 0.10, "final_total": data["order_total"] * 0.90}

    def no_discount(data):
        return {"discount": 0, "final_total": data["order_total"]}

    def ship_immediately(data):
        return {"shipping": "priority"}

    def ship_when_available(data):
        return {"shipping": "standard", "backorder": True}

    def hold_order(data):
        return {"status": "on_hold"}

    discount_condition = Condition(
        expression="customer_type == 'premium'",
        branch_true=[(apply_premium_discount, "Premium Discount", "v1.0")],
        branch_false=[(apply_standard_discount, "Standard Discount", "v1.0")],
    )

    shipping_condition = Condition(
        expression="items_in_stock == True",
        branch_true=[(ship_immediately, "Ship Now", "v1.0")],
        branch_false=[(ship_when_available, "Ship Later", "v1.0")],
    )

6.3 Data Validation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def validate_input(data):
        return {
            "email": "test@example.com",
            "username": "validuser",
            "password": "short"
        }

    def validate_email_format(data):
        return {"email_valid": "@" in data["email"] and "." in data["email"]}

    def validate_username(data):
        return {"username_valid": len(data["username"]) >= 3}

    def validate_password(data):
        return {"password_valid": len(data["password"]) >= 8}

    def accept_registration(data):
        return {"registration": "accepted"}

    def reject_email(data):
        return {"registration": "rejected", "reason": "Invalid email format"}

    def reject_username(data):
        return {"registration": "rejected", "reason": "Username too short"}

    def reject_password(data):
        return {"registration": "rejected", "reason": "Password too weak"}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (validate_input, "Get Input", "v1.0"),
        (validate_email_format, "Check Email", "v1.0"),
        (validate_username, "Check Username", "v1.0"),
        (validate_password, "Check Password", "v1.0"),
        Condition(
            expression="email_valid == True",
            branch_true=[],
            branch_false=[(reject_email, "Reject Email", "v1.0")],
        ),
        Condition(
            expression="username_valid == True",
            branch_true=[],
            branch_false=[(reject_username, "Reject Username", "v1.0")],
        ),
        Condition(
            expression="password_valid == True",
            branch_true=[(accept_registration, "Accept", "v1.0")],
            branch_false=[(reject_password, "Reject Password", "v1.0")],
        ),
    ])

7. Best Practices
------------------

7.1 Keep Expressions Simple
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Good:**

.. code-block:: python

    Condition(
        expression="age >= 18 and verified == True",
        branch_true=[(allow, "Allow", "v1.0")],
        branch_false=[(deny, "Deny", "v1.0")],
    )

**Avoid:**

.. code-block:: python

    # Too complex - hard to debug
    Condition(
        expression="(age >= 18 if verified else False) and (country in allowed)",
        ...
    )

7.2 Use Meaningful Variable Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The expression has access to all data keys:

.. code-block:: python

    # Good - clear what we're checking
    Condition(
        expression="user_age >= 18",
        branch_true=[(allow_adult, "Allow Adult", "v1.0")],
    )

7.3 Order Conditions Strategically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Put most likely conditions first:

.. code-block:: python

    # If most users are standard, check premium first and invert
    Condition(
        expression="user_type != 'premium'",
        branch_true=[(process_standard, "Standard", "v1.0")],
        branch_false=[(process_premium, "Premium", "v1.0")],
    )

7.4 Test Both Branches
~~~~~~~~~~~~~~~~~~~~~~

Always verify both paths work:

.. code-block:: python

    # Test TRUE path
    result_true = pipeline.run({"value": 100})
    assert result_true["branch"] == "high"

    # Test FALSE path
    result_false = pipeline.run({"value": 50})
    assert result_false["branch"] == "low"

8. Troubleshooting
-----------------

8.1 Condition Not Evaluating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure the data key exists:

.. code-block:: python

    # Check the key exists first
    Condition(
        expression="'key' in data and data['key'] > 0",
        ...
    )

8.2 Type Mismatch
~~~~~~~~~~~~~~~~

Ensure types match your comparison:

.. code-block:: python

    # String comparison
    Condition(expression="status == 'active'", ...)
    
    # Numeric comparison
    Condition(expression="count > 0", ...)

9. Complete Example
------------------

.. code-block:: python

    from wpipe import Pipeline, Condition

    def fetch_user(data):
        return {"user_type": "admin", "permissions": ["read", "write", "delete"]}

    def grant_full_access(data):
        return {"access_level": "full"}

    def grant_read_only(data):
        return {"access_level": "read_only"}

    def grant_basic_with_write(data):
        return {"access_level": "basic"}

    def log_access_denied(data):
        return {"logged": True, "event": "access_denied"}

    # Determine access level based on user type
    access_condition = Condition(
        expression="user_type == 'admin'",
        branch_true=[(grant_full_access, "Full Access", "v1.0")],
        branch_false=[],
    )

    # Check permissions for non-admins
    permission_condition = Condition(
        expression="'delete' in permissions",
        branch_true=[(grant_read_only, "Read/Write", "v1.0")],
        branch_false=[(grant_basic_with_write, "Basic", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (fetch_user, "Fetch User", "v1.0"),
        access_condition,
        permission_condition,
    ])

    result = pipeline.run({})
    print(result)
    # {'user_type': 'admin', 'permissions': [...], 'access_level': 'full'}

10. Next Steps
-------------

Now you understand conditional branching:

- Explore :doc:`retry_logic` - Add automatic retries for unreliable operations
- Learn :doc:`nested_pipelines` - Compose complex workflows
- Check :doc:`advanced_patterns` - Advanced usage patterns
- Read :doc:`../user_guide/conditions` - Detailed reference guide
