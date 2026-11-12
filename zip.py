import hashlib, os, zipfile

M = '/tmp/rpwork/merged'
OUT = '/tmp/rpwork/ChungMinh-SMP-ResourcePack.zip'
EPOCH = (2026, 1, 1, 0, 0, 0)

if os.path.exists(OUT):
    os.remove(OUT)

files = []
for root, dirs, fs in os.walk(M):
    dirs.sort()
    for f in sorted(fs):
        p = os.path.join(root, f)
        rel = os.path.relpath(p, M).replace(os.sep, '/')
        files.append((rel, p))

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for rel, p in files:
        info = zipfile.ZipInfo(rel, EPOCH)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        with open(p, 'rb') as fh:
            z.writestr(info, fh.read())

size = os.path.getsize(OUT)
sha1 = hashlib.sha1(open(OUT, 'rb').read()).hexdigest()
sha256 = hashlib.sha256(open(OUT, 'rb').read()).hexdigest()
print(f'entries: {len(files)}')
print(f'file:    {OUT}')
print(f'size:    {size} bytes ({size/1048576:.2f} MiB)')
print(f'sha1:    {sha1}')
print(f'sha256:  {sha256}')
