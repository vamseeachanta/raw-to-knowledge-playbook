# Contributing

This playbook grows by **appending evidence-backed practices**, not by
rewriting theory. The bar for an entry:

1. **It happened.** Every practice/failure mode must come from a real
   incident or a measured comparison — not from first principles.
2. **One practice per PR**, formatted as:

   ```
   **GP-NN — <imperative rule>.**
   Why: <the incident or measurement, 1–3 sentences>.
   Apply: <concrete steps / checks>.
   ```

3. **Failure modes** go in `docs/04-failure-modes.md` with all four columns
   (manifestation, root cause, detection, mitigation).
4. **Sanitize.** No client names, project codes, internal hostnames, or
   private mount paths. Publisher/standards-body names are fine. If a story
   needs a confidential detail to make sense, abstract it ("a client
   project", "the vendor archive").
5. **Numbering is append-only.** Never renumber or repurpose a GP-ID; if a
   practice is superseded, mark it *Superseded by GP-MM* in place.
6. Update the *Next ID* line at the bottom of the catalog.

## Review

Practice PRs get the same treatment the pipeline got: at least one
adversarial review asking "is this actually supported by the stated
evidence, and is it stated so a stranger could apply it?"
