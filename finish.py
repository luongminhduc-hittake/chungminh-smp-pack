import json, os

M = '/tmp/rpwork/merged'
A = os.path.join(M, 'assets/minecraft')
MODELS = os.path.join(A, 'models')

# 1.1-era "blocks/..." texture paths the CIT pack still carries.
fixed = []
for root, _, fs in os.walk(MODELS):
    for f in fs:
        if not f.endswith('.json'):
            continue
        p = os.path.join(root, f)
        raw = open(p, encoding='utf-8', newline='').read()
        new = raw.replace('"blocks/', '"block/')
        if new != raw:
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(new)
            fixed.append(os.path.relpath(p, MODELS))
print('legacy paths rewritten:', fixed)

# pack.mcmeta: 26.3 only.
with open(os.path.join(M, 'pack.mcmeta'), 'w', encoding='utf-8') as fh:
    json.dump({'pack': {'description': 'ChungMinh SMP\nMizunos x Fresh Animations',
                        'pack_format': 97, 'min_format': 97, 'max_format': 97}},
              fh, ensure_ascii=False, indent=2)
    fh.write('\n')

with open(os.path.join(M, 'CREDITS.txt'), 'w', encoding='utf-8') as fh:
    fh.write("""ChungMinh SMP - resource pack

Bundled packs, overlay order (bottom is overridden first, top wins):

  1. Better Leaves - PandaDEV
  2. Mizuno's 16 Craft JE 1.20.4-1.0 - Mizuno (https://mizunomcmemo.blogspot.com/)
  3. Mizuno's 16 Craft JE CIT pack 1.20.1-1.0 - Mizuno
  4. Fresh Animations v1.11.2 BASE - FreshLX
  5. Mizuno x Fresh Animations 5.2 - ShorkBee

All credit belongs to the original authors. This bundle exists only as the
server resource pack of ChungMinh SMP, not as a standalone redistribution.

Fresh Animations Terms & Conditions:
- You MAY include this pack in your mod pack or server.
- You MAY NOT redistribute it as a resource pack of its own, nor include
  unedited assets in your own publicly released pack.
- FreshLX is the creator and copyright owner.
""")
print('pack.mcmeta and CREDITS.txt written')
