def generate_summary(changes):
    counts={k:sum(c['change_type']==k for c in changes) for k in ('added','removed','modified')}
    lines=[f"Compared documents contain {len(changes)} detected changes: {counts['added']} added, {counts['removed']} removed, and {counts['modified']} modified.", 'This is a rule-based summary; it does not establish factual correctness.']
    for c in changes:
        if c.get('priority')=='High' or c.get('semantic_flag') or c.get('number_change'):
            lines.append(f"Change {c['id']} ({c['category']}, {c['priority']}) — old page(s) {c['old_pages']}; new page(s) {c['new_pages']}. Review required. Old: {c['old_text'][:240] or '—'} New: {c['new_text'][:240] or '—'}")
    if not any(c.get('priority')=='High' or c.get('semantic_flag') for c in changes): lines.append('No high-priority or semantic-review items were identified by the configured rules.')
    return '\n\n'.join(lines)
