import os, shutil, json, hashlib

SRC = '/tmp/rpwork'
# low -> high priority, mirroring the screenshot (bottom pack first)
ORDER = ['x6', 'x2', 'x3', 'x1', 'x4']
NAMES = {
    'x1': 'FreshAnimations v1.11.2 BASE (FreshLX)',
    'x2': "Mizuno's 16 Craft JE 1.20.4-1.0 (Mizuno)",
    'x3': "Mizuno's 16 Craft JE CIT 1.20.1-1.0 (Mizuno)",
    'x4': 'Mizuno x Fresh Animations 5.2 (ShorkBee)',
    'x5': 'Modern Mizunos v0.5.2 (Kchem / GardenGals)',
    'x6': 'Better Leaves (PandaDEV)',
}
OUT = os.path.join(SRC, 'merged')
SKIP_ROOT = {'readme.txt', 'README.md', 'changelog1.11.2.txt',
             'FAterms&conditions.txt', 'pack.mcmeta', 'pack.png'}
SKIP_ANY = {'Thumbs.db', '.DS_Store', 'desktop.ini'}

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

counts = {}
override = {}
for d in ORDER:
    src = os.path.join(SRC, d)
    n = 0
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        for f in files:
            if rel == '.' and f in SKIP_ROOT:
                continue
            if f in SKIP_ANY:
                continue
            r = (f if rel == '.' else os.path.join(rel, f)).replace(os.sep, '/')
            dst = os.path.join(OUT, *r.split('/'))
            if os.path.exists(dst):
                override[d] = override.get(d, 0) + 1
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(root, f), dst)
            n += 1
    counts[d] = n
print('copied per pack:', counts)
print('files overwritten by each pack:', override)

# highest-priority pack.png
shutil.copyfile(os.path.join(SRC, 'x4', 'pack.png'), os.path.join(OUT, 'pack.png'))

mcmeta = {
    'pack': {
        'description': 'ChungMinh SMP\nMizunos x Fresh Animations',
        'pack_format': 97,
        'min_format': 15,
        'max_format': 999,
    }
}
with open(os.path.join(OUT, 'pack.mcmeta'), 'w', encoding='utf-8') as fh:
    json.dump(mcmeta, fh, ensure_ascii=False, indent=2)
    fh.write('\n')

total = sum(len(fs) for _, _, fs in os.walk(OUT))
print('merged file count:', total)
