# swiftlint-linux

Minimal composite action that uses the SwiftLint static Linux binary, runs it on Ubuntu runners, and publishes a short summary in job outputs.

# Usage

```yaml
- name: Run SwiftLint
  uses: ainame/swiftlint-linux@main
```

To make warnings fail the job, enable SwiftLint's `--strict` mode:

```yaml
- name: Run SwiftLint (strict)
  uses: ainame/swiftlint-linux@main
  with:
    strict: true
```

The action exposes three outputs:
- `lint-report`: Multi-line summary suitable for `GITHUB_STEP_SUMMARY`.
- `issue-count`: Number of violations detected.
- `exit-code`: SwiftLint exit status for downstream logic.

This is what the summary block can look like when a violation is present:

```
### SwiftLint Summary
/home/runner/work/swiftlint-linux/swiftlint-linux/Sources/Greeting.swift:8: [Error] force_cast - Force casts should be avoided

Total violations: 1
```
