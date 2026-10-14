"""Format retrieved sources for display."""


def format_sources_markdown(sources: list[dict]) -> str:
    """Return a markdown string listing sources."""
    if not sources:
        return ""

    lines = ["**Sources:**"]
    for i, s in enumerate(sources, 1):
        page = s.get("page", "?")
        filename = s.get("filename", "?")
        lines.append(f"{i}. `{filename}` — page **{page}**")
    return "\n".join(lines)


def format_evidence(sources: list[dict]) -> str:
    """Return markdown with evidence snippets."""
    if not sources:
        return ""

    lines = ["**Evidence:**"]
    for i, s in enumerate(sources, 1):
        snippet = s.get("text", "").strip().replace("\n", " ")
        if len(snippet) > 200:
            snippet = snippet[:200] + "..."
        lines.append(f"\n*Chunk {i} (page {s.get('page')}):* {snippet}")
    return "\n".join(lines)