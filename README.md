# Resource pack cho ChungMinh SMP

Pack gộp từ **5 pack** (bỏ Modern Mizunos theo yêu cầu), đóng gói lại thành một file zip
duy nhất để host công khai cho Horizon server tải qua `resource-pack`.

## Thành phẩm

**URL công khai (GitHub Release):**
`https://github.com/luongminhduc-hittake/chungminh-smp-pack/releases/download/v1/ChungMinh-SMP-ResourcePack.zip`

| | |
|---|---|
| File | `ChungMinh-SMP-ResourcePack.zip` |
| Kích thước | 12,35 MiB (12.945.548 bytes) |
| SHA-1 | `15c9a5c4d14fa044d11ad36a8c93f87700302810` |
| SHA-256 | `dfd2dc6a2aad294379fd604aafdf57baacc01d7e4411e2e6765f4de7cf686aaf` |
| `pack_format` | `97` (= 26.3, khớp `RESOURCE_PACK_FORMAT` của Horizon) |
| Số file | 8.237 |

## Thứ tự đè (theo ảnh Cậu Chủ gửi, dưới thấp → trên cao)

1. **Better Leaves** — PandaDEV *(nền, bị đè nhiều nhất nhưng model lá vẫn thắng)*
2. **Mizuno's 16 Craft JE 1.20.4-1.0** — Mizuno
3. **Mizuno's 16 Craft JE CIT pack 1.20.1-1.0** — Mizuno
4. **Fresh Animations v1.11.2 BASE** — FreshLX
5. **Mizuno x Fresh Animations 5.2** — ShorkBee *(trên cùng, đè 505 file)*

Bỏ **Modern Mizunos v0.5.2** (Kchem/GardenGals). Xem mục "Đã bỏ gì" bên dưới.

## Đã sửa gì so với copy tay

Gộp bằng `cp` thường sẽ ra pack lỗi. Năm vấn đề đã xử lý:

| Vấn đề | Cách xử lý |
|---|---|
| `pack.mcmeta` của 6 pack xung đột (`pack_format` 15 → 75, `min_format` 84, 77...) | Ghi lại một `pack.mcmeta` duy nhất: `pack_format`/`min_format`/`max_format` = 97 |
| 24 model chết từ thời 1.12 (`lit_pumpkin`, `door_bottom`, `orientable_sf`, `generated_cit`...) trỏ tới texture `blocks/...` không còn tồn tại | Xoá, sau khi kiểm tra không blockstate nào với tới |
| 1 model (`cake_slice3_0`) còn đường dẫn kiểu cũ `blocks/cake_side_0` | Đổi thành `block/cake_side_0` |
| `Thumbs.db` lọt vào `textures/block/` | Lọc bỏ |
| 3 model thiếu key `particle` (`template_wall_inventory_sand`, `short_grass_1`) | Thêm `particle`, hết warning khi load |
| Mỗi pack có `readme.txt` / `pack.png` riêng | Giữ `pack.png` của pack trên cùng, gộp credit vào `CREDITS.txt` |

## Host công khai

Dùng **GitHub Release**, không dùng MediaFire:

| | GitHub Release | MediaFire |
|---|---|---|
| Link trực tiếp | cố định vĩnh viễn | **hết hạn sau ~120 s** |
| Sau khi hết hạn | vẫn 200 + đúng file | 302 → `download_repair.php` (HTML) |
| `Content-Type` | `application/octet-stream` | `application/zip` |
| Redirect | 1 (ổn định) | 0, nhưng token chết |
| Kiểm chứng từ 3 IP | ✅ | ✅ (trong 120 s) |

**MediaFire không dùng được** làm `resource-pack` URL: Horizon client nhận URL một lần
lúc start, client tải lúc join. Nếu player join sau ~2 phút kể từ lúc lấy link, họ nhận
trang HTML thay vì zip → pack fail.

## Kiểm chứng

`verify_pack.py` chạy trên file zip thành phẩm:

```
ok  zip archive is intact
ok  no duplicate entries
ok  no absolute or traversing paths
ok  pack_format is 97 (26.3 resource format)
ok  min_format/max_format both 97
ok  all 1450 JSON files parse
ok  all 5278 PNG files have a valid header
ok  every model parent resolves in the pack or in vanilla 26.3
ok  every texture a model names exists in the pack or vanilla
ok  Better Leaves bushy texture survives the merge
ok  Mizuno leaf texture still there
ok  Fresh Animations .jem models present
ok  Mizuno CIT definitions present
RESULT: PASS
```

Hai phép kiểm tra nặng hơn, chạy trên cây file đã giải nén, đối chiếu với
`~/horizon/srv/resources/assets/minecraft` của server:

- **84/84 blockstate** có tập `variants` **giống hệt** vanilla 26.3 (không pack nào
  còn khai báo biến thể mà 26.3 đã bỏ, cũng không thiếu biến thể mới).
- **0** model có parent chain gãy; **0** vòng lặp parent; **0** texture reference
  không giải được (tính cả texture của vanilla).

## Đã bỏ gì khi loại Modern Mizunos

Modern Mizunos chỉ có **279 file riêng** (94 texture block, 69 texture item, 34 model
block, 31 texture entity, 17 `.jem`) và **đè 44 file** của pack bên dưới. Bỏ nó nghĩa là:

- block/item quay về texture Mizuno gốc (16x, phong cách cũ hơn)
- 17 `.jem` của nó nhường chỗ cho `.jem` của Fresh Animations / Mizuno x FA
- mất `texts/credits.json`, `blockstates/wildflowers.json`, `resin_brick_slab.json`

Nếu sau này muốn thêm lại: chèn `x5` vào cuối `ORDER` trong `merge.py` rồi chạy lại
4 script theo thứ tự dưới đây.

## Build lại

```bash
cd services/homelab1/resourcepack
python3 merge.py      # gộp 5 pack (low → high priority)
python3 cleanup2.py   # xoá model chết
python3 finish.py     # sửa path cũ, ghi pack.mcmeta + CREDITS.txt
python3 fix_particle.py  # thêm key particle còn thiếu
python3 zip.py        # đóng zip, in sha1/sha256
python3 verify_pack.py
```

Input là các thư mục `x6 x2 x3 x1 x4 x5` (đã giải nén từ zip gốc) trong `/tmp/rpwork`.
Script không tự giải nén; nếu dựng lại từ đầu thì giải nén 5 zip vào đúng tên thư mục đó.

## Chạy trên Fabric

Pack 55% là định dạng OptiFine (CEM/CTM/CIT). Cần 5 mod để dùng đủ, và có một lưu ý về
CIT + MoreCulling. Xem [FABRIC-26.3.md](FABRIC-26.3.md).

## Ràng buộc phía Horizon

- `resource-pack` là **key `[properties]`**, không phải key typed trong `server.toml`.
- `resource-pack-id` **phải là UUID hợp lệ**; sai định dạng thì `server_pack_info()`
  trả `None` và pack bị **bỏ im lặng**. Để trống thì server tự sinh UUID từ URL.
- Thiếu `resource-pack-sha1` vẫn chạy nhưng client chỉ cập nhật khi *đổi tên file*.
- **Horizon server không tự host file pack** — chỉ có route `/api/v1/*`. URL phải do
  một HTTP server khác phục vụ.
- Client Horizon giới hạn pack **250 MiB**; 12,35 MiB là thoải mái.

## Giấy phép

- **Fresh Animations**: được phép "include this resource pack in your mod pack or
  **server**", nhưng **không được redistribute** nó như một pack riêng, và không được
  đưa asset chưa sửa vào pack công khai khác. Đây là lý do `CREDITS.txt` ghi rõ bundle
  chỉ dùng làm server pack của ChungMinh SMP, không phát hành độc lập.
  Nguồn: điều khoản trong `FAterms&conditions.txt` của pack gốc.
- **Modern Mizunos**: CC-BY-NC-SA-4.0 (đã bỏ khỏi bundle).
- **Mizuno's 16 Craft**: điều khoản tại `https://bit.ly/3rdruE2`, yêu cầu đọc trước
  khi dùng.
