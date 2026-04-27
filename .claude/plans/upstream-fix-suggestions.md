# VolFe upstream fixes suggested by volcatenate integration

This file documents VolFe improvements that came up while wiring VolFe
into the [volcatenate](https://github.com/kaylai/volcatenate) wrapper.
Each entry lists the location, the problem, and a concrete suggested
fix. **None of these have been PR'd yet** — this is a planning doc.

This clone has `origin` → `kaylai/VolFe-featurebranch` (your fork) and
`upstream` → `eryhughes/VolFe`. PRs go via `origin` to `upstream`.

---

## 1. Cryptic ValueError on unknown model names

**Location:** `src/VolFe/model_dependent_variables.py:2118` (inside
`C_X`), and the same pattern in similar lookup functions throughout
the file (`C_CO2`, `C_H2O`, `C_S`, `C_OH`, `y_*`, etc. — search for
`if model == "..." ... elif ...` chains without an `else: raise`
clause).

**Problem.** The lookup pattern is:

```python
if model == "Ar_Basalt_Hughes25":
    K = 0.7000
elif model == "Ar_Rhyolite_Hughes25":
    K = 0.4400
...
else:
    K = float(model)   # cryptic fallback
```

If the user (or a downstream library) supplies an unknown name like
`"Ar_Basalt_HughesIP"` (the old name from a previous release),
`float(model)` raises:

```
ValueError: could not convert string to float: 'Ar_Basalt_HughesIP'
```

This is not actionable. The user has no idea which option string is
wrong, what the valid choices are, or that they passed a model name
to a Henry-constant fallback at all.

**Real-world impact.** This is exactly how `Ar_Basalt_HughesIP` →
`Ar_Basalt_Hughes25` (renamed in VolFe v1.0.1) silently broke every
VolFe call in volcatenate — the `species X solubility` default still
pointed at the old name, and every saturation-pressure / degassing
call failed with the cryptic error above.

**Suggested fix.**

```python
_VALID_X_MODELS = {
    "Ar_Basalt_Hughes25":   0.7000,
    "Ar_Rhyolite_Hughes25": 0.4400,
    "Ne_Basalt_Hughes25":   0.1504,
    "Ne_Rhyolite_Hughes25": 0.8464,
    "test":                 35.0,
}

def C_X(PT, melt_wf, models):
    model = ...  # look up the option string from `models`
    if model in _VALID_X_MODELS:
        return _VALID_X_MODELS[model]
    try:
        return float(model)
    except ValueError:
        raise ValueError(
            f"Unknown species-X solubility model: {model!r}. "
            f"Valid options: {sorted(_VALID_X_MODELS)} "
            f"or a numeric Henry constant."
        ) from None
```

Same shape for every other lookup in `model_dependent_variables.py`.
Each function should surface its own valid-option set.

---

## 2. Backwards-compatible aliasing for renamed models

**Problem.** When VolFe renames a model (e.g. `HughesIP` →
`Hughes25`), downstream consumers' configs break with no migration
path beyond "manually update the string." Releases become
silently breaking for anyone with a saved config.

**Suggested fix.** Keep the old name as a deprecated alias for one
release with a `DeprecationWarning`:

```python
_X_ALIASES = {
    "Ar_Basalt_HughesIP":   "Ar_Basalt_Hughes25",
    # add others as renames occur
}

if model in _X_ALIASES:
    new_name = _X_ALIASES[model]
    warnings.warn(
        f"Model name {model!r} is deprecated; use {new_name!r}. "
        f"This alias will be removed in a future release.",
        DeprecationWarning, stacklevel=2,
    )
    model = new_name
```

This eases the migration path for downstream libraries (volcatenate
in particular).

---

## 3. Validate model names at construction time

**Location:** `make_df_and_add_model_defaults` (or wherever the
`models_df` is assembled — `src/VolFe/batch_calculations.py` or
similar).

**Problem.** Model names are validated lazily — at the point of use,
deep inside the solver. By then, an unknown name surfaces as a
solver failure (or the cryptic `float()` ValueError) rather than a
config failure. The user has to dig into a stack trace to discover
they typed a model name wrong.

**Suggested fix.** At construction time, validate every option
string against the set of valid choices for that option, raising a
single `ValueError` listing all unknown names so the user sees the
full problem in one shot:

```python
def make_df_and_add_model_defaults(model_opts):
    df = ...  # build the DataFrame
    errors = []
    for opt_name, valid_set in OPTION_VALIDATORS.items():
        value = df.loc[opt_name, "option"]
        if value not in valid_set:
            errors.append(
                f"  {opt_name}={value!r} (valid: {sorted(valid_set)})"
            )
    if errors:
        raise ValueError("Unknown model options:\n" + "\n".join(errors))
    return df
```

Pairs naturally with fix #1 — the same valid-option sets feed both
the construction-time validator and the runtime lookups.

---

## How to PR these

1. PRs go to `eryhughes/VolFe` via your fork
   `kaylai/VolFe-featurebranch`.
2. **Items 1 and 3 are independent** and can be PR'd separately.
   Item 2 (aliases) builds on the data table from Item 1.
3. **Item 1 alone** would have prevented the bug we hit in
   volcatenate. Start there.
