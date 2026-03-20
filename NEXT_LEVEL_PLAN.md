# BetterBeeswarm: Simple plan to become a community tool

This plan is intentionally lightweight: keep the package small, but make it easier for people to trust, adopt, and contribute.

## 1) Clarify the core promise
- Keep the main value proposition explicit: BetterBeeswarm provides drop-in `seaborn` swarm behavior with configurable overflow handling (`gutters`, `shrink`, `random`).
- Add one short “When to use each overflow mode” table in the README.

## 2) Make output reproducible by default
- Add a `random_state` option for `overflow='random'` so users can get deterministic plots for notebooks, papers, and CI docs.
- Keep current behavior as default (`None`) to preserve simplicity.

## 3) Add confidence through minimal tests
- Add a tiny test suite with 3-5 focused tests:
  - import/monkeypatch smoke test
  - `overflow='gutters'` stays in bounds
  - `overflow='shrink'` resolves gutter overflow cases
  - `overflow='random'` is deterministic with a seed
- Run tests against a small matrix of seaborn/matplotlib versions.

## 4) Improve contribution ergonomics
- Add `CONTRIBUTING.md` with:
  - local setup
  - how to run tests
  - release checklist (version bump + changelog)
- Add issue templates for bug report + feature request.

## 5) Publish practical examples
- Keep examples focused on real workflows:
  - dense-category scientific plots
  - publication-friendly style setup
  - before/after comparisons with same data and marker size
- Keep one “quickstart snippet” and one “advanced customization snippet”.

## 6) Stabilize the public API (small surface)
- Treat these as stable user-facing knobs: `overflow`, `warn_thresh`, and new `random_state`.
- Avoid exposing internal seaborn patching internals in docs unless needed.

## Suggested implementation order (2-3 short releases)
1. **Release 1:** docs refresh + contribution guide + minimal CI tests.
2. **Release 2:** `random_state` support + deterministic random overflow test.
3. **Release 3:** small benchmark/example refresh and compatibility matrix update.

