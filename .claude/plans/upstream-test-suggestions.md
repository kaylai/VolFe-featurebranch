# Tests VolFe could add (motivated by volcatenate integration)

These tests would have caught the issues we hit while wrapping VolFe,
and would prevent regressions. None require external dependencies
beyond VolFe itself plus pytest.

These pair with the fixes proposed in
`upstream-fix-suggestions.md` in this directory — read that first
for context.

---

## 1. Every default option string resolves through its lookup function

**Why:** catches the class of bug where an internal model is renamed
in VolFe but the corresponding entry in
`make_df_and_add_model_defaults` (or some downstream consumer's
default) still uses the old name. This is exactly what happened with
the `Ar_Basalt_HughesIP` → `Ar_Basalt_Hughes25` rename in v1.0.1 —
volcatenate's default broke silently with a cryptic
`could not convert string to float` error.

```python
import math
import pytest
import VolFe.model_dependent_variables as mdv

# (option_name, default_value, lookup_callable)
DEFAULT_LOOKUPS = [
    ("species X solubility", "Ar_Basalt_Hughes25", mdv.C_X),
    ("water",                "Basalt_Hughes24",    mdv.C_H2O),
    ("carbon dioxide",       "MORB_Dixon95",       mdv.C_CO2),
    # … one entry per option resolved by an if/elif chain in mdv
]

@pytest.mark.parametrize("opt_name,default,lookup_fn", DEFAULT_LOOKUPS)
def test_default_resolves(opt_name, default, lookup_fn):
    """Every default model name must be recognized by its lookup."""
    PT = {"P": 1000.0, "T": 1200.0}      # canonical PT
    melt_wf = canonical_basalt_melt_wf()  # canonical composition
    models = {"option": default}          # adapt to actual signature
    K = lookup_fn(PT, melt_wf, models)
    assert math.isfinite(K) and K > 0, (
        f"Default {opt_name!r}={default!r} did not resolve through "
        f"{lookup_fn.__name__}"
    )
```

Cheap parametric test, runs in milliseconds. Failure mode is
unmistakable: "default `species X solubility = 'Ar_Basalt_HughesIP'`
did not resolve."

---

## 2. Unknown model names raise informative ValueError

**Why:** locks in the contract once fix #1 from
`upstream-fix-suggestions.md` is applied. Prevents regressions where
someone re-introduces the `float(model)` fall-through.

```python
def test_unknown_X_model_is_informative():
    """An unknown solubility-model string must error clearly."""
    with pytest.raises(ValueError, match="Unknown species-X solubility model"):
        mdv.C_X(PT, melt_wf, {"species X solubility": "not_a_real_model"})

def test_unknown_water_model_is_informative():
    with pytest.raises(ValueError, match="Unknown water"):
        mdv.C_H2O(PT, melt_wf, {"water": "totally_made_up"})
```

One test per lookup function. Mechanical to add once fix #1 lands.

---

## 3. Deprecated aliases still work (with warning)

**Why:** if fix #2 from `upstream-fix-suggestions.md` is adopted,
this test enforces that deprecated names keep functioning during
the deprecation window. Eases migration for downstream libraries.

```python
import warnings

def test_deprecated_alias_still_works():
    """Renamed models keep working for one release with a warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        K = mdv.C_X(PT, melt_wf, {"species X solubility": "Ar_Basalt_HughesIP"})
        assert math.isfinite(K)
        assert any(
            issubclass(warning.category, DeprecationWarning)
            and "HughesIP" in str(warning.message)
            and "Hughes25" in str(warning.message)
            for warning in w
        )
```

---

## 4. Assembled `models_df` validates options upfront

**Why:** pairs with fix #3 in `upstream-fix-suggestions.md`. Catches
typos at the moment the user constructs the models_df, not deep
inside a solver hours later.

```python
import VolFe as vf

def test_make_df_rejects_unknown_water_model():
    """make_df_and_add_model_defaults should fail loudly on typos."""
    with pytest.raises(ValueError, match="water.*definitely_not"):
        vf.make_df_and_add_model_defaults([
            ["water", "definitely_not_a_real_solubility_model"],
        ])

def test_make_df_aggregates_multiple_errors():
    """Multiple bad options should be reported together, not one at a time."""
    with pytest.raises(ValueError) as exc_info:
        vf.make_df_and_add_model_defaults([
            ["water", "fake_water"],
            ["carbon dioxide", "fake_co2"],
        ])
    assert "fake_water" in str(exc_info.value)
    assert "fake_co2" in str(exc_info.value)
```

The aggregation test (`test_make_df_aggregates_multiple_errors`)
keeps the UX nice — fail once with a complete list rather than
fail-fix-fail-fix.
