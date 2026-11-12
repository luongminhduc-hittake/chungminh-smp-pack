"""End-to-end checks on the built resource pack zip."""
import hashlib
import json
import os
import zipfile

Z = '/tmp/rpwork/ChungMinh-SMP-ResourcePack.zip'
V = '/tmp/rpwork/van'
fails = []


def ok(cond, what):
    print(('  ok   ' if cond else '  FAIL ') + what)
    if not cond:
        fails.append(what)


z = zipfile.ZipFile(Z)
ok(z.testzip() is None, 'zip archive is intact')

names = z.namelist()
ok(len(names) == len(set(names)), 'no duplicate entries')

bad = [n for n in names if n.startswith('/') or '..' in n.split('/')]
ok(not bad, 'no absolute or traversing paths')

mc = json.loads(z.read('pack.mcmeta'))
pack = mc['pack']
ok(pack['pack_format'] == 97, 'pack_format is 97 (26.3 resource format)')
ok(pack['min_format'] == 97 and pack['max_format'] == 97, 'min_format/max_format both 97')
ok('description' in pack and pack['description'], 'description present')
ok('pack.png' in names, 'pack.png present')
ok('CREDITS.txt' in names, 'CREDITS.txt present')

# every JSON parses
broken = []
for n in names:
    if n.endswith('.json'):
        try:
            json.loads(z.read(n).decode('utf-8-sig'))
        except Exception as e:
            broken.append((n, str(e)))
ok(not broken, f'all {sum(1 for n in names if n.endswith(".json"))} JSON files parse')
for b in broken[:5]:
    print('        ', b)

# every PNG is really a PNG
notpng = []
for n in names:
    if n.endswith('.png'):
        if z.read(n)[:8] != b'\x89PNG\r\n\x1a\n':
            notpng.append(n)
ok(not notpng, f'all {sum(1 for n in names if n.endswith(".png"))} PNG files have a valid header')
for n in notpng[:5]:
    print('        ', n)

# the pack's own model universe vs vanilla 26.3
universe = {}
for base in (V, '/tmp/rpwork/merged'):
    root = os.path.join(base, 'models')
    for r, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.json'):
                rel = os.path.relpath(os.path.join(r, f), root).replace(os.sep, '/')[:-5]
                universe[rel] = os.path.join(r, f)

pack_models = {n[len('assets/minecraft/models/'):-5] for n in names
               if n.startswith('assets/minecraft/models/') and n.endswith('.json')}


def refs(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ('model', 'parent') and isinstance(v, str):
                out.add(v.split(':')[-1])
            else:
                refs(v, out)
    elif isinstance(obj, list):
        for v in obj:
            refs(v, out)


missing = set()
for m in pack_models:
    d = json.loads(z.read(f'assets/minecraft/models/{m}.json').decode('utf-8-sig'))
    out = set()
    refs(d, out)
    for r in out:
        if r not in universe and r not in pack_models:
            missing.add((m, r))
ok(not missing, 'every model parent resolves in the pack or in vanilla 26.3')
for m in sorted(missing)[:8]:
    print('        ', m)

# every texture a pack model names exists in the pack or vanilla
vtex = set()
for line in open('/tmp/rpwork/van_tex.txt', encoding='utf-8'):
    p = line.strip()
    if p.startswith('textures/'):
        p = p[len('textures/'):]
    if p:
        vtex.add(p)
        vtex.add(p.rsplit('.', 1)[0])
ptex = set()
for n in names:
    if n.startswith('assets/minecraft/textures/'):
        rel = n[len('assets/minecraft/textures/'):]
        ptex.add(rel)
        ptex.add(rel.rsplit('.', 1)[0])
missing_tex = []
for m in pack_models:
    d = json.loads(z.read(f'assets/minecraft/models/{m}.json').decode('utf-8-sig'))
    for key, val in (d.get('textures') or {}).items():
        if isinstance(val, str) and not val.startswith('#'):
            tid = val.split(':')[-1]
            if tid not in vtex and tid not in ptex:
                missing_tex.append((m, key, val))
ok(not missing_tex, 'every texture a model names exists in the pack or vanilla')
for m in missing_tex[:8]:
    print('        ', m)

# the overlay order actually survived
ok('assets/minecraft/textures/block/oak_leaves_bushy_top.png' in names,
   'Better Leaves bushy texture survives the merge')
ok('assets/minecraft/textures/block/oak_leaves.png' in names,
   'Mizuno leaf texture still there')
ok(len([n for n in names if n.startswith('assets/minecraft/optifine/cem/')]) > 50,
   'Fresh Animations .jem models present')
ok(len([n for n in names if n.startswith('assets/minecraft/optifine/cit/')]) > 500,
   'Mizuno CIT definitions present')

print()
print('RESULT:', 'PASS' if not fails else f'FAIL ({len(fails)} problem(s))')
