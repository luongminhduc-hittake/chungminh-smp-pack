"""Fix the three models that inherit or omit a `particle` texture."""
import json, os

A = '/tmp/rpwork/merged/assets/minecraft'
B = os.path.join(A, 'models/block')


def load(name):
    with open(os.path.join(B, name + '.json'), encoding='utf-8-sig') as fh:
        return json.load(fh)


def save(name, d):
    with open(os.path.join(B, name + '.json'), 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write('\n')


# 1. template_wall_inventory_sand: inherits particle "#wall" from wall_inventory, but
#    the children only define 0/1/2, so #wall never resolves.
d = load('template_wall_inventory_sand')
d.setdefault('textures', {})['particle'] = '#1'
save('template_wall_inventory_sand', d)
print('template_wall_inventory_sand: particle -> #1')

# 2. short_grass_1: a root model with no parent and no particle key at all.
d = load('short_grass_1')
tex = d.setdefault('textures', {})
if 'particle' not in tex:
    tex['particle'] = tex.get('middle', 'block/short_grass_1_middle')
save('short_grass_1', d)
print('short_grass_1: particle ->', d['textures']['particle'])
