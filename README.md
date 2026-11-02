# API Lab

## Installation and running

Requirements: Python 3.10 or newer, Git, and `curl`.

Create and activate a virtual environment, then install dependencies.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the test suite from repository root:

```bash
pytest -v
```

Generate the HTML run report:

```bash
pytest -v --html=report.html --self-contained-html
```

Tests call QuickPizza at `https://quickpizza.grafana.com`. Tests that create ratings use a fresh
made-up user and that user's login token. Do not create, update, or delete shared ratings with the
public token.

## Step A1: Input domain model for `POST /api/ratings`

The request body contains `pizza_id` and `stars`; the request also needs an `Authorization` token.
Blocks come from API rules: stars must be an integer from 1 through 5, the pizza must exist, and the
token must belong to a logged-in user. Base choice uses the ordinary valid value for each
characteristic, then changes one characteristic at a time.

| Characteristic | Blocks | Values in tests | Coverage mapping |
|---|---|---|---|
| C1: value of `stars` | below 1; 1 to 5 (base); above 5 | `0`; `3`; `6` | `test_stars_out_of_range`; `test_base_choice_is_saved` |
| C2: type of `stars` | whole number (base); decimal; text; missing | `3`; `3.5`; `"3"`; no field | `test_base_choice_is_saved`; `test_decimal_stars_is_refused_with_empty_body`; `test_text_stars_is_refused_with_empty_body`; `test_missing_stars_is_refused_with_empty_body` |
| C3: pizza | exists (base); does not exist | newly created pizza; `999999999` | `test_base_choice_is_saved`; `test_nonexistent_pizza_is_refused_with_empty_body` |
| C4: token | user's own (base); none; wrong length | token from `auth`; no `Authorization` header (omitted); short made-up token | `test_base_choice_is_saved`; intentionally omitted for safety; `test_short_token_is_refused_with_empty_body` |

The complete base-choice model requires `1 + 2 + 3 + 1 + 2 = 9` test cases. The safe implemented
subset has 8 cases because the C4 missing-token mutation is intentionally omitted: the live API
unexpectedly creates an orphaned rating without authorization, violating the shared-service safety
rule. A safe made-up-token GET is tested separately as security-defect evidence in `RESULTS.md` Part B,
question 7. All other mapped tests keep non-target characteristics at their base values.
