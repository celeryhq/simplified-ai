#!/usr/bin/env python3
"""Check skill tool names and literal smp examples against an installed apikit source.

Run with apikit's Python environment; checks are read-only and make no API calls.
This validates names/flags, not prose semantics, permissions, or live deployment.
"""
import argparse
import re
import shlex
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apikit', type=Path, required=True, help='Current simplified-apikit checkout')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1], help='Skill repository root')
    args = parser.parse_args()
    sys.path.insert(0, str(args.apikit.resolve()))
    import yaml
    from smp.apikit.server import _SPECS
    from smp.apikit.cli import cli, _camel_to_kebab
    root = args.root.resolve()
    if not list((root / 'skills').rglob('SKILL.md')):
        parser.error('root contains no skill files')
    tools = {'smp_callApi'}
    enums = {}

    def resolve(schema, spec):
        while '$ref' in schema:
            ref = schema['$ref'].split('/')[1:]
            schema = spec
            for key in ref: schema = schema[key]
        return schema
    for filename, namespace, _ in _SPECS:
        spec = yaml.safe_load((args.apikit / 'smp/apikit/specs' / filename).read_text())
        for item in spec.get('paths', {}).values():
            for op in item.values():
                if isinstance(op, dict) and 'operationId' in op:
                    tools.add(f'{namespace}_{op["operationId"]}')
                    command = (namespace, _camel_to_kebab(op['operationId']))
                    choices = {}
                    for param in op.get('parameters', []):
                        param = resolve(param, spec)
                        schema = resolve(param.get('schema', {}), spec)
                        if 'enum' in schema: choices['--' + param['name'].replace('_', '-')] = schema['enum']
                    body = op.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
                    body = resolve(body, spec)
                    for name, schema in body.get('properties', {}).items():
                        schema = resolve(schema, spec)
                        if 'enum' in schema: choices['--' + name.replace('_', '-')] = schema['enum']
                    enums[command] = choices
    errors = []
    command_count = 0
    for path in sorted((root / 'skills').rglob('*.md')):
        content = path.read_text()
        label = str(path.relative_to(root))
        for tool in sorted(set(re.findall(r'\b(?:api|pm|social|media|flows|agents|notify|smp)_[a-z][A-Za-z]*[A-Z][A-Za-z]*\b', content))):
            if tool not in tools:
                errors.append(f'{label}: unknown tool {tool}')
        for block in re.findall(r'```(?:bash|sh)\n(.*?)```', content, re.S):
            block = block.replace('\\\n', ' ')
            for line in block.splitlines():
                match = re.search(r'\bsmp\s+(.*)', line)
                if not match: continue
                text = match.group(1).split(' | ')[0].split(' #')[0]
                try: words = shlex.split(text)
                except ValueError: continue  # Multiline JSON; other checks cover tool names.
                if not words: continue
                # Root options can precede the group, e.g. smp --raw api list-assets.
                while words and words[0].startswith('--'):
                    opt = words.pop(0)
                    if opt in {'--help', '--version'}: break
                    param = next((p for p in cli.params if opt in p.opts), None)
                    if param is None:
                        errors.append(f'{label}: unknown root option {opt}'); break
                    if not param.is_flag and words: words.pop(0)
                if not words: continue
                group_name = words.pop(0)
                if ':' in group_name:
                    group_name, command = group_name.split(':', 1)
                    words.insert(0, command)
                if group_name.startswith('<'): continue  # Explicit discovery template.
                group = cli.commands.get(group_name)
                if group is None:
                    errors.append(f'{label}: unknown group {group_name}'); continue
                if not words or words[0].startswith('--'): continue
                if not hasattr(group, 'commands'): continue
                command_name = words.pop(0)
                if command_name.startswith('<'): continue
                command = group.commands.get(command_name)
                if command is None:
                    errors.append(f'{label}: unknown command {group_name} {command_name}'); continue
                command_count += 1
                if '--help' not in words:
                    supplied = {w.split('=')[0] for w in words if w.startswith('--')}
                    for param in command.params:
                        if param.required and not supplied.intersection(param.opts):
                            errors.append(f'{label}: missing required option {group_name} {command_name} {param.opts[0]}')
                    for index, word in enumerate(words[:-1]):
                        values = enums.get((group_name, command_name), {}).get(word)
                        value = words[index + 1]
                        if values and not value.startswith(('<', '$')) and value not in [str(v) for v in values]:
                            errors.append(f'{label}: invalid enum {group_name} {command_name} {word} {value}')
                options = {'--help'} | {o for p in command.params for o in p.opts}
                for word in words:
                    if word.startswith('--') and word.split('=')[0] not in options:
                        errors.append(f'{label}: unknown option {group_name} {command_name} {word}')
    if errors:
        for err in sorted(set(errors)): print('FAIL', err)
        print(f'{len(set(errors))} source contract errors')
        return 1
    print(f'PASS: tool names and {command_count} CLI examples match source. No live calls made.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
