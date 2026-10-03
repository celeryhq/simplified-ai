#!/usr/bin/env python3
"""Validate every skill's structure and client metadata; no network or API calls."""
from pathlib import Path
import argparse
import re
import yaml


def validate_tree(root: Path) -> list[str]:
    root=root.resolve();errors=[];folders=sorted((root/'skills').glob('*'))
    if not folders:return ['No skills found']
    for folder in folders:
        if not folder.is_dir():continue
        prefix=folder.name
        def error(message):errors.append(f'{prefix}: {message}')
        doc=folder/'SKILL.md';meta=folder/'agents'/'openai.yaml'
        if not doc.is_file():error('SKILL.md missing');continue
        content=doc.read_text();match=re.match(r'^---\n(.*?)\n---(?:\n|$)',content,re.S)
        if not match:error('YAML frontmatter missing');continue
        try:data=yaml.safe_load(match[1])
        except yaml.YAMLError:error('Invalid frontmatter YAML');continue
        if not isinstance(data,dict):error('Frontmatter must be an object');continue
        name=data.get('name');description=data.get('description')
        if not isinstance(name,str) or name!=prefix or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>64:error('Invalid name or folder/name mismatch')
        if not isinstance(description,str) or not description.strip() or len(description)>1024 or '<' in description or '>' in description:error('Invalid description (required, at most 1024 characters)')
        if set(data)-{'name','description','license','allowed-tools','metadata','compatibility'}:error('Unsupported frontmatter keys')
        if re.search(r'^\s*\[TODO:[^\n]*\]\s*$',content,re.M):error('Unfinished scaffold')
        if not meta.is_file():error('agents/openai.yaml missing')
        else:
            try:m=yaml.safe_load(meta.read_text())
            except yaml.YAMLError:m=None
            if not isinstance(m,dict):error('Invalid client metadata YAML')
            else:
                interface=m.get('interface',{})
                if not isinstance(interface,dict):error('interface must be an object');interface={}
                short=interface.get('short_description');prompt=interface.get('default_prompt')
                if not isinstance(interface.get('display_name'),str) or not interface['display_name'].strip():error('display_name required')
                if not isinstance(short,str) or not 25<=len(short)<=64:error('short_description must be 25–64 characters')
                if not isinstance(prompt,str) or f'${prefix}' not in prompt:error('default_prompt must invoke this skill')
                policy=m.get('policy',{})
                if not isinstance(policy,dict) or ('allow_implicit_invocation' in policy and not isinstance(policy['allow_implicit_invocation'],bool)):error('Invalid invocation policy')
                for key in ['icon_small','icon_large']:
                    value=interface.get(key)
                    if value and (not isinstance(value,str) or not (folder/value).is_file()):error(f'{key} path missing')
                dependencies=m.get('dependencies',{})
                if not isinstance(dependencies,dict) or not isinstance(dependencies.get('tools',[]),list):error('Invalid dependencies')
                else:
                    for tool in dependencies.get('tools',[]):
                        if not isinstance(tool,dict) or tool.get('type')!='mcp' or not tool.get('value') or not tool.get('url','').startswith('https://'):error('Invalid MCP dependency')
        for md in folder.rglob('*.md'):
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',md.read_text()):
                if re.match(r'^(https?://|#|mailto:|/)',target):continue
                path=target.split('#')[0]
                if path and not (md.parent/path).exists():error(f'{md.relative_to(folder)}: missing reference {path}')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args()
    errors=validate_tree(args.root)
    for error in errors:print('FAIL:',error)
    if not errors:print(f'PASS: {len(list((args.root/"skills").glob("*/SKILL.md")))} skills validated (structure and metadata only)')
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
