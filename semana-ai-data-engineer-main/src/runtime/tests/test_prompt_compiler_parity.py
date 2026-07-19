from pathlib import Path
from difflib import unified_diff
from itertools import zip_longest

from src.runtime.prompt.markdown import MarkdownPromptCompiler
from src.runtime.prompt_compiler.compiler import PromptCompiler
from src.runtime.tests.test_runtime import build_test_runtime


# =============================================================================
# Build runtime
# =============================================================================

runtime = build_test_runtime()

context = runtime.build_context(
    capability_id="domain.shopagent-builder",
    objective="Create Pydantic models",
)

old = MarkdownPromptCompiler()
new = PromptCompiler()

old_prompt = old.compile(context)
new_prompt = new.compile(context)


# =============================================================================
# Artifacts
# =============================================================================

artifacts = Path("artifacts") / "runtime" / "parity"
artifacts.mkdir(
    parents=True,
    exist_ok=True,
)

old_file = artifacts / "markdown_prompt.txt"
new_file = artifacts / "compiled_prompt.txt"
diff_file = artifacts / "prompt_parity.diff"

old_file.write_text(
    old_prompt,
    encoding="utf-8",
)

new_file.write_text(
    new_prompt,
    encoding="utf-8",
)

diff = list(
    unified_diff(
        old_prompt.splitlines(),
        new_prompt.splitlines(),
        fromfile="MarkdownPromptCompiler",
        tofile="PromptCompiler",
        lineterm="",
    )
)

diff_file.write_text(
    "\n".join(diff) if diff else "No differences found.",
    encoding="utf-8",
)


# =============================================================================
# Helpers
# =============================================================================

def normalize(text: str) -> str:
    """
    Ignore trailing whitespace and blank lines at EOF.
    """

    lines = [line.rstrip() for line in text.splitlines()]

    while lines and not lines[-1]:
        lines.pop()

    return "\n".join(lines)


def first_difference(a: str, b: str) -> int:
    limit = min(len(a), len(b))

    for i in range(limit):
        if a[i] != b[i]:
            return i

    if len(a) != len(b):
        return limit

    return -1


def print_difference_context(
    old_text: str,
    new_text: str,
    index: int,
    context: int = 250,
):
    start = max(0, index - context)
    end = index + context

    print("\n" + "=" * 100)
    print(f"FIRST DIFFERENCE @ CHAR {index}")
    print("=" * 100)

    print("\nOLD (repr):")
    print(repr(old_text[start:end]))

    print("\nNEW (repr):")
    print(repr(new_text[start:end]))

    print("\nOLD:")
    print(old_text[start:end])

    print("\nNEW:")
    print(new_text[start:end])

    print("=" * 100)


def print_line_differences(
    old_text: str,
    new_text: str,
    limit: int = 20,
):
    print("\n" + "=" * 100)
    print("FIRST DIFFERENT LINES")
    print("=" * 100)

    count = 0

    for lineno, (old_line, new_line) in enumerate(
        zip_longest(
            old_text.splitlines(),
            new_text.splitlines(),
            fillvalue="",
        ),
        start=1,
    ):
        if old_line == new_line:
            continue

        print(f"\nLine {lineno}")
        print(f"OLD: {repr(old_line)}")
        print(f"NEW: {repr(new_line)}")

        count += 1

        if count >= limit:
            print(f"\n... truncated after {limit} differing lines ...")
            break

    if count == 0:
        print("No differing lines found.")


def print_diff_statistics(diff_lines: list[str]):
    added = 0
    removed = 0

    for line in diff_lines:
        if line.startswith("+++") or line.startswith("---"):
            continue

        if line.startswith("+"):
            added += 1

        elif line.startswith("-"):
            removed += 1

    print("\n" + "=" * 100)
    print("DIFF STATISTICS")
    print("=" * 100)

    print(f"Added lines   : {added}")
    print(f"Removed lines : {removed}")
    print(f"Net delta     : {added - removed:+}")


# =============================================================================
# Report
# =============================================================================

print("\n=== PROMPT PARITY TEST ===")

print(f"Old prompt size : {len(old_prompt):,} characters")
print(f"New prompt size : {len(new_prompt):,} characters")

print(f"Old prompt      : {old_file.resolve()}")
print(f"New prompt      : {new_file.resolve()}")
print(f"Diff            : {diff_file.resolve()}")

print()

print(f"Old lines       : {len(old_prompt.splitlines()):,}")
print(f"New lines       : {len(new_prompt.splitlines()):,}")
print(f"Diff lines      : {len(diff):,}")

print()
print(f"Knowledge docs  : {len(context.knowledge)}")

for doc in context.knowledge:
    print(
        f"- {doc.document.id} "
        f"({len(doc.document.content):,} chars)"
    )


# =============================================================================
# Diagnostics
# =============================================================================

index = first_difference(old_prompt, new_prompt)

if index == -1:
    print("\n✓ Prompts are byte-identical.")

else:
    print(f"\nFirst difference at character: {index}")

    print_difference_context(
        old_prompt,
        new_prompt,
        index,
    )

    print_line_differences(
        old_prompt,
        new_prompt,
        limit=20,
    )

    print_diff_statistics(diff)

    print("\n" + "=" * 100)
    print("SIZE")
    print("=" * 100)

    print(f"Old length : {len(old_prompt):,}")
    print(f"New length : {len(new_prompt):,}")
    print(f"Delta      : {len(new_prompt) - len(old_prompt):+}")


# =============================================================================
# Assertions
# =============================================================================

normalized_old = normalize(old_prompt)
normalized_new = normalize(new_prompt)

if normalized_old != normalized_new:
    print("\n❌ Normalized prompts still differ.")
else:
    print("\n✓ Normalized prompts are identical.")

assert normalized_old == normalized_new