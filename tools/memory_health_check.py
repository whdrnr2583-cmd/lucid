#!/usr/bin/env python3
"""Memory directory self-health audit.

Checks:
1. inventory (file count, MEMORY.md line count vs 200 cap)
2. self-declared LEGACY (frontmatter or body marker)
3. broken [[wiki-style]] cross-refs (name slug ↔ file name)
4. orphan files (no [[link]] from any other file or MEMORY.md)
5. duplicate descriptions (similar slugs)
6. frontmatter convention split (top-level vs nested metadata)
"""
import re
from collections import defaultdict, Counter
import os
from pathlib import Path

MEM_DIR = Path(
    os.environ.get('CLAUDE_MEMORY_DIR', '~/.claude/projects/CHANGE-ME/memory')
).expanduser()
if not MEM_DIR.exists():
    raise SystemExit(
        f'Memory dir not found: {MEM_DIR}\n'
        f'Set CLAUDE_MEMORY_DIR env var to your Claude Code memory directory '
        f'(e.g., ~/.claude/projects/<your-sanitized-cwd>/memory)'
    )
MEM_FILES = sorted(p for p in MEM_DIR.glob('*.md') if p.name != 'MEMORY.md')
INDEX = MEM_DIR / 'MEMORY.md'

def parse_frontmatter(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if not text.startswith('---'):
        return {}, text, None
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text, None
    fm_raw = parts[1]
    body = parts[2].lstrip('\n')
    # very loose YAML-ish parser
    fm = {}
    cur_key = None
    nested = False
    for line in fm_raw.split('\n'):
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if not v:
                cur_key = k
                fm[k] = {}
                nested = True
                continue
            fm[k] = v
            nested = False
        elif nested and line.strip().startswith(('node_type', 'type', 'originSessionId')):
            sm = re.match(r'^\s+(\w+):\s*(.*)$', line)
            if sm and isinstance(fm.get(cur_key), dict):
                fm[cur_key][sm.group(1)] = sm.group(2).strip()
    return fm, body, fm_raw

def extract_name(fm, fallback):
    name = fm.get('name')
    if isinstance(name, str):
        return name
    return fallback

def is_self_declared_legacy(body):
    return bool(re.search(r'🛑\s*LEGACY|^LEGACY\b|\bLEGACY\s*\(', body[:2000], re.M))

def extract_wiki_links(text):
    return set(re.findall(r'\[\[([^\]]+)\]\]', text))

# main
inventory = {'count': len(MEM_FILES), 'index_lines': len(INDEX.read_text().splitlines())}

frontmatter_convention = {'top_level': [], 'nested': [], 'unknown': []}
self_legacy = []
slugs = {}  # name slug → file
descs = {}  # description → file
wiki_links_in = defaultdict(set)  # name → set of files that link to it

index_text = INDEX.read_text(encoding='utf-8')
index_links = extract_wiki_links(index_text)
# also detect markdown-style [text](file.md) links from index
index_md_links = set(re.findall(r'\(([a-zA-Z0-9_-]+)\.md\)', index_text))

for f in MEM_FILES:
    fm, body, fm_raw = parse_frontmatter(f)
    name = extract_name(fm, f.stem)
    slugs[f.stem] = name
    desc = fm.get('description', '') if isinstance(fm.get('description'), str) else ''
    if desc:
        descs.setdefault(desc[:80], []).append(f.name)

    # frontmatter convention
    if isinstance(fm.get('metadata'), dict):
        frontmatter_convention['nested'].append(f.name)
    elif 'type' in fm and isinstance(fm.get('type'), str):
        frontmatter_convention['top_level'].append(f.name)
    else:
        frontmatter_convention['unknown'].append(f.name)

    if is_self_declared_legacy(body):
        self_legacy.append(f.name)

    # collect wiki links found in this file
    for link in extract_wiki_links(body):
        wiki_links_in[link].add(f.name)

# orphan: a file whose name slug is not referenced by any other file or by MEMORY.md
referenced_names = set()
for name in wiki_links_in:
    referenced_names.add(name)
referenced_names.update(index_links)
referenced_names.update(index_md_links)

orphans = []
for f in MEM_FILES:
    name = slugs[f.stem]
    if (name not in referenced_names) and (f.stem not in referenced_names):
        orphans.append(f.name)

# broken cross-refs: [[link]] in any file pointing to a non-existent slug
all_slugs = set(slugs.keys()) | set(slugs.values())
broken_refs = defaultdict(list)
for link, sources in wiki_links_in.items():
    if link not in all_slugs and link.lower() not in {s.lower() for s in all_slugs}:
        broken_refs[link] = sorted(sources)

# duplicate descriptions (first 80 chars same)
dup_descs = {d: files for d, files in descs.items() if len(files) > 1}

# OUTPUT
print(f"=== Inventory ===")
print(f"memory files: {inventory['count']}")
print(f"MEMORY.md lines: {inventory['index_lines']} / 200 cap ({inventory['index_lines']*100//200}%)")
print()
print(f"=== Frontmatter convention split ===")
print(f"top_level (옛): {len(frontmatter_convention['top_level'])}")
print(f"nested metadata (신): {len(frontmatter_convention['nested'])}")
print(f"unknown: {len(frontmatter_convention['unknown'])}")
if frontmatter_convention['unknown']:
    for f in frontmatter_convention['unknown'][:5]:
        print(f"  ⚠ {f}")
print()
print(f"=== Self-declared LEGACY ===")
print(f"count: {len(self_legacy)}")
for f in self_legacy:
    print(f"  🛑 {f}")
print()
print(f"=== Broken [[cross-refs]] ===")
print(f"count: {len(broken_refs)}")
for link, sources in sorted(broken_refs.items())[:20]:
    print(f"  ⚠ [[{link}]] from {sources}")
print()
print(f"=== Orphan files (no link from anywhere) ===")
print(f"count: {len(orphans)}")
for f in orphans[:20]:
    print(f"  – {f}")
print()
print(f"=== Duplicate description (first 80 chars same) ===")
print(f"count: {len(dup_descs)}")
for d, files in list(dup_descs.items())[:5]:
    print(f"  ⚠ {files}")
    print(f"    desc: {d[:60]}…")
