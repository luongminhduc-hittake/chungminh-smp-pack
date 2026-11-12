> **URL pack:** `https://github.com/luongminhduc-hittake/chungminh-smp-pack/releases/download/v1/ChungMinh-SMP-ResourcePack.zip`
> **SHA-1:** `15c9a5c4d14fa044d11ad36a8c93f87700302810`

# Resource pack trên Fabric 26.3 — cần gì để "trơn tru"

Pack [ChungMinh-SMP-ResourcePack.zip](ChungMinh-SMP-ResourcePack.zip) **55% là định dạng
OptiFine**, không phải pack vanilla thường. Vanilla 26.3 (và Fabric trần) sẽ chỉ dùng được
45% còn lại. Đây là danh sách mod cần thiết, đã đối chiếu với instance thực tế.

## Pack cần gì (số liệu đo trên file zip)

| Tính năng OptiFine | Đường dẫn trong pack | Số lượng | Không có mod thì sao |
|---|---|---|---|
| **CEM** — custom entity models | `optifine/cem/*.jem` | **194** | Mob giữ model vanilla → Fresh Animations mất trắng |
| **CEM animations** | `optifine/cem/*.jpm` | **72** | Cử động (tai, đuôi, cánh) đứng yên |
| **CEM block entity** | `shulker.jem`, `head_*.jem` | 4 | Shulker/đầu mob không animate |
| **CTM** — connected textures | `optifine/ctm/` | **113 props / 1249 png** | Kính, đá, đất mất viền nối, thấy rõ mối nối từng block |
| **CIT** — custom item textures | `optifine/cit/` | **966 props / 1014 model / 810 png** | 218 item mất hình riêng (biển ghi tên, kiếm custom...) |
| **Random entity** | `optifine/random/` | 2 props / 38 png | Villager/bò/heo chỉ 1 kiểu thay vì nhiều biến thể |
| **Emissive** | `*_e.png` | 15 (10 block + 4 entity + 1 particle) | Đuốc, lò, rail không phát sáng trong tối |
| **Colormap** | `optifine/colormap/` | 2 + `color.properties` | Màu cỏ/patch lilypad sai |

Phần **thuần vanilla** (45%): texture block/item/entity, GUI, model block, model item,
`blockstates`, `particles` — chạy được ngay, không cần mod nào.

## Mod cần cài

Đã chép sẵn 4 file vào `mods/` của thư mục tham chiếu:

| Mod | File | sha512 (32 ký tự đầu) | Cần cho |
|---|---|---|---|
| **EMF** Entity Model Features | `entity_model_features-3.3.12-26.3-fabric.jar` | `4572fc065e757264947aff35a96d17d5` | 194 `.jem` + 72 `.jpm` |
| **ETF** Entity Texture Features | `entity_texture_features-7.2.7-26.3-fabric.jar` | `69193c58d4d05e08fea9afa34cc47563` | `optifine/random/` + emissive entity |
| **Continuity** | `continuity-3.0.1+26.3.jar` | `1ec1e3b2f73c26b19445d664822a8936` | 113 CTM props + emissive block |
| **CIT Resewn fork** | `citresewn-continuation-1.2.2-fork.14+26.3.jar` | `c053a0f8693b37e1f4e1663914056d77` | 966 CIT props |
| **Polytone** | `polytone-26.3-6.8.6-fabric.jar` | `f50370557e24f5404f17b6c055d35a3e` | `optifine/colormap/` + `color.properties` |

Tải: `https://modrinth.com/mod/entity-model-features`, `/entitytexturefeatures`,
`/continuity`, `/cit-resewn-fork`, `/polytone`.

### Quan hệ phụ thuộc

```
EMF  ──requires──▶  ETF >= 7.2
ETF  ──breaks──────▶  EMF < 3.3   (đã đúng: 3.3.12)
Continuity  ──requires──▶  Fabric API
CIT Resewn  ──requires──▶  Fabric API, Java >= 25
Polytone  ──requires──▶  Fabric API >= 0.162.0, Fabric Loader >= 0.19.3
Polytone  ──breaks──────▶  Sodium < 0.9  (đã đúng: 0.9.3)
```

Fabric API `0.165.0+26.3` và Loader `0.20.1` trong instance đã thoả mọi yêu cầu.
Sodium `0.9.3` **tự `provides: indium`** → không cần cài Indium riêng.

### Cảnh báo: ETF 7.2.6 trong instance là bản cũ

Thư mục tham chiếu đang có `entity_texture_features-7.2.6`. EMF 3.3.12 cần `>= 7.2` nên
chạy được, nhưng nên lên **7.2.7** (bản 26.3 mới nhất, 2026-11-03). Chỉ cần **một** trong
hai file, đừng để cả hai.

## Ba warning đã tìm ra và đã sửa

Tôi đã chạy thử pack trong instance PrismLauncher `MacOS Optimized` (Fabric 26.3,
Loader 0.20.1). Log `latest.log` ghi đúng 3 warning — đều do **Mizuno's 16 Craft 1.20.4**
mang model từ thời 1.12:

```
[Worker-Main-6/WARN]: Missing texture references in model minecraft:block/red_sandstone_wall_inventory: particle
[Worker-Main-6/WARN]: Missing texture references in model minecraft:block/sandstone_wall_inventory: particle
[Worker-Main-6/WARN]: Missing texture references in model minecraft:block/short_grass_1: particle
```

Nguyên nhân: `template_wall_inventory_sand` kế thừa `particle: "#wall"` từ
`wall_inventory` của vanilla, nhưng model con chỉ khai báo `0/1/2` nên `#wall` không bao
giờ resolve. `short_grass_1` là model gốc không có parent và không có key `particle`.

Đã sửa: `particle = "#1"` cho template, `particle = block/short_grass_1_middle` cho
`short_grass_1`. **Zip đã build lại**, sha1 mới `15c9a5c4d14fa044d11ad36a8c93f87700302810`.

## Những thứ KHÔNG cần cài

| Mod | Vì sao không cần |
|---|---|
| **Indium** | Sodium 0.9.3 đã `provides: indium` |
| **CIT List** | Chỉ để *xem* danh sách CIT, không cần để chạy |
| **Continuity 2.x / OptiFabric** | OptiFabric xung đột với EMF (`breaks: optifabric`) |
| **Iris** | Pack không có shader; Iris chỉ cần nếu Cậu Chủ dùng shaderpack riêng |

## Hai tinh chỉnh nên làm

### 1. `broken_paths` — nếu CIT hiện không đủ

CIT Resewn fork có option **"Allow broken paths in resourcepacks"**, mặc định **tắt**.
Pack này dùng **997/1014 model CIT có `"parent": "./cit_handheld"`** — đường dẫn tương
đối, kiểu OptiFine cũ. Với `broken_paths=false`, các parent này có thể không resolve.

Bật trong `config/citresewn.json`:

```json
{
  "enabled": true,
  "mute_errors": false,
  "mute_warns": false,
  "cache_ms": 100,
  "broken_paths": true
}
```

Log sẽ in `[citresewn] Caution! Broken paths is enabled!` — bình thường.

Tôi **chưa kiểm chứng được** liệu CIT Resewn fork có resolve `./` trong trường `parent`
hay không (bytecode không có xử lý `./` rõ ràng; `broken_paths` là cơ chế duy nhất liên
quan). Vì vậy: bật `broken_paths`, vào game xem biển gỗ đổi tên có ra hình riêng không.
Nếu **vẫn không** ra, báo tôi — lúc đó cần viết script chuyển 997 model sang đường dẫn
tuyệt đối, và phải xác định đúng namespace mà fork đăng ký model CIT.

### 2. MoreCulling — tắt culling lá

Instance đang đặt `leavesCullingMode = "DEFAULT"` + `leavesCullingAmount = 2`. Model lá
của Better Leaves là **cross 5 element**, nhìn từ nhiều góc vẫn thấy mặt lá; culling của
MoreCulling có thể làm lá biến mất khi ở gần. Nếu thấy lá "nhấp nháy" hoặc mất mặt:

```toml
# config/moreculling.toml
leavesCullingMode = "OFF"
```

Đổi lại, FPS giảm nhẹ ở rừng rậm.

## Kiểm chứng sau khi cài

1. **Mods** → phải thấy EMF, ETF, Continuity, CIT Resewn, Polytone (không đỏ).
2. **Resource Packs** → pack hiện **không** có dòng "incompatible" và **không** có
   "(Contains broken paths)" *(nếu đã bật broken_paths thì dòng này là bình thường)*.
3. Vào world, đứng cạnh **kính màu** → phải thấy viền nối liền, không có đường kẻ giữa
   các block.
4. Cầm **biển gỗ** đổi tên thành `*_0` → phải ra hình biển riêng của Mizuno (CIT).
5. Nhìn **bò/heo** → phải thấy chân cử động (Fresh Animations).
6. Đứng trong tối cạnh **lò nung đang cháy** → mặt trước phải phát sáng.
7. `logs/latest.log` → **không** còn `Missing texture references`.

## Nếu vẫn chưa trơn

```bash
# Đếm lỗi CIT
grep -i "citresewn" logs/latest.log | head -20

# Đếm lỗi CEM
grep -i "entity_model_features\|EMF" logs/latest.log | grep -i -E "error|fail" | head

# Đếm lỗi CTM
grep -i "continuity" logs/latest.log | grep -i -E "error|fail" | head
```

Nếu EMF báo lỗi nhiều: bật `entity_model_features.cfg` → `allowed_cem = known_only`
(mặc định `all`) để tránh EMF đụng vào model của mod khác.
