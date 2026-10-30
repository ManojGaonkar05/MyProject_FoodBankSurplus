# Reflection

The handout refers to reflection questions but does not list the questions themselves. These responses cover the reflection topics implied by its learning outcomes.

1. **What is static analysis, and what did the tools contribute?**
   Static analysis inspects source code without running it. Pylint checks code quality and maintainability, Flake8 checks formatting and common style rules, and Bandit looks for risky security patterns. Used together, they provide different views of the same code.

2. **Which issue was most important, and why?**
   The unrestricted `eval` call was the most important issue because promo input could execute arbitrary Python code. A discount feature should parse a small, defined expression language instead of executing input as code.

3. **What did fixing the findings improve?**
   Input validation prevents nonsensical sales totals, using `None` avoids sharing receipt state across calls, and context-managed file access makes receipt logging safer. A main guard also makes the module importable without triggering prompts or file writes.

4. **What are the limits of static analysis?**
   Tools can identify suspicious patterns but cannot decide every business rule or prove that behavior is correct. Reviewing the output and considering edge cases still matters. After the fixes, Pylint scored 10.00/10 and Bandit and Flake8 reported no findings. The README supplies commands to rerun all three tools.
