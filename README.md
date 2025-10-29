# linux-swiftlint-action

Minimal composite action that uses the SwiftLint static Linux binary, runs it on Ubuntu runners, and publishes a short summary in job outputs.

# Usage

```yaml
- name: Run SwiftLint
  uses: ainame/linux-swiftlint-action@main
```

The action exposes three outputs:
- `lint-report`: Multi-line summary suitable for `GITHUB_STEP_SUMMARY`.
- `issue-count`: Number of violations detected.
- `exit-code`: SwiftLint exit status for downstream logic.

This is an example of what this action will report to GITHUB_STEP_SUMMARY.

```
### SwiftLint Summary
/home/runner/work/linux-swiftlint-action/linux-swiftlint-action/Sources/Greeting.swift:8: [Error] force_cast - Force casts should be avoided

Total violations: 1
```
