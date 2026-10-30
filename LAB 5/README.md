# Lab 5: Static Code Analysis

The cleaned script is `pos_system.py`. The original file came from the supplied `L5_02_retail_pos-main.zip`.

## Install and run the analyzers

```powershell
python -m pip install pylint bandit flake8
python -m pylint --persistent=n pos_system.py > reports/after_pylint_report.txt
python -m bandit -r pos_system.py > reports/after_bandit_report.txt
python -m flake8 pos_system.py > reports/after_flake8_report.txt
```

The `reports/` folder contains the actual before and after output. Pylint uses `--persistent=n` so it does not need to write a cache outside this project.

Run the program with:

```powershell
python pos_system.py
```

Enter `total * 0.9` or `total - 50` at the promo prompt. Other expressions are rejected.
