import json, os

M = '/tmp/rpwork/merged'
A = os.path.join(M, 'assets/minecraft')
MODELS = os.path.join(A, 'models')
V = '/tmp/rpwork/van'


def load(p):
    try:
        with open(p, 'rb') as fh:
            return json.loads(fh.read().decode('utf-8-sig'))
    except Exception:
        return None


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


# Entry points: every blockstate and every item definition, the pack's and vanilla's.
roots = set()
for base in (A, V):
    for sub in ('blockstates', 'items'):
        d = os.path.join(base, sub)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith('.json'):
                refs(load(os.path.join(d, f)) or {}, roots)

# Model universe: vanilla first, the pack on top.
universe = {}
for base in (V, A):
    root = os.path.join(base, 'models')
    for r, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.json'):
                rel = os.path.relpath(os.path.join(r, f), root).replace(os.sep, '/')[:-5]
                universe[rel] = os.path.join(r, f)

pack_models = set()
root = os.path.join(MODELS)
for r, _, fs in os.walk(root):
    for f in fs:
        if f.endswith('.json'):
            pack_models.add(os.path.relpath(os.path.join(r, f), root).replace(os.sep, '/')[:-5])

live = set()
frontier = list(roots)
while frontier:
    cur = frontier.pop()
    if cur in live:
        continue
    live.add(cur)
    p = universe.get(cur)
    if not p:
        continue
    d = load(p)
    if isinstance(d, dict):
        before = set()
        refs(d, before)
        frontier.extend(x for x in before if x not in live)

dead = sorted(pack_models - live)
print(f'pack models: {len(pack_models)} | reachable: {len(pack_models & live)} | dead: {len(dead)}')
for d in dead:
    print('   dropping', d)
    os.remove(os.path.join(MODELS, *d.split('/')) + '.json')
