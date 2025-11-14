# Blog Translation Script

Script Python để dịch blog posts sang tiếng Việt sử dụng Google Gemini AI.

## Tính năng

### Core Features
- ✅ **Content transformation** (không chỉ dịch từng từ)
- ✅ **Lead nurture optimized**: Xây dựng niềm tin, tạo kết nối cảm xúc
- ✅ **Email marketing ready**: Scannable, có CTA, value-focused
- ✅ **Frontmatter preserved 100%**: Metadata giữa `---` KHÔNG bị thay đổi
- ✅ Giữ nguyên technical terms (theo `content/english.md`)
- ✅ Giữ nguyên markdown formatting, code blocks, links
- ✅ Tùy chọn cập nhật ngày `updated`

### Frontmatter Protection 🔒

Script tách riêng và bảo vệ frontmatter:

```yaml
---
title: "Original Title"        # ✅ KHÔNG đổi
slug: "original-slug"           # ✅ KHÔNG đổi
description: "Original desc"    # ✅ KHÔNG đổi
tags: ["Tag1", "Tag2"]         # ✅ KHÔNG đổi
updated: "2025-01-01"          # ⚠️ CHỈ đổi nếu --update-date
---

Nội dung blog post...           # ✅ DỊCH phần này
```

**Cơ chế hoạt động:**
1. Script tách frontmatter ra riêng (dùng `python-frontmatter`)
2. Chỉ pass content (sau `---`) vào Gemini AI
3. AI chỉ nhận và dịch content
4. Ghép lại: frontmatter gốc + content đã dịch

### Creative Freedom
Model được phép:
- ✅ Thêm hooks, questions, mini-stories
- ✅ Thêm bullet points để dễ scan
- ✅ Thêm emoji phù hợp (⚡ 🎯 ✅)
- ✅ Viết lại câu cho tự nhiên
- ✅ Thêm transitions, quick wins
- ✅ Làm rõ value propositions

### Privacy Protection
- ⚠️ **Anonymize company names** trong case studies
- ⚠️ Không nêu tên cụ thể: Tiki, VinID, Sendo, etc.
- ✅ Thay bằng descriptors: "công ty e-commerce top 3", "startup fintech Series B"
- ✅ Giữ metrics để credible nhưng anonymous

## Cài đặt

```bash
cd tools/image-generator
/home/tan/.local/bin/uv sync
```

## Sử dụng

### Cú pháp cơ bản

```bash
# Dịch blog post (không cập nhật ngày)
.venv/bin/python translate_to_vietnamese.py <filename>

# Ví dụ
.venv/bin/python translate_to_vietnamese.py modern-data-stack-2025.mdx
```

### Cập nhật ngày "updated"

```bash
# Dịch và cập nhật ngày "updated" thành hôm nay
.venv/bin/python translate_to_vietnamese.py <filename> --update-date

# Ví dụ
.venv/bin/python translate_to_vietnamese.py modern-data-stack-2025.mdx --update-date
```

## Ví dụ output

```
============================================================
🇻🇳 BLOG POST TRANSLATION TO VIETNAMESE
============================================================
File: modern-data-stack-2025.mdx
Update date: True
============================================================
📖 Reading: modern-data-stack-2025.mdx
📚 Loaded 189 technical terms to keep in English
🤖 Calling Gemini API for translation...
✅ Translation completed
📅 Updated 'updated' field to: 2025-11-10
✅ Successfully translated and saved: modern-data-stack-2025.mdx
   Updated date: 2025-11-10
============================================================
🎉 Translation complete!
============================================================
```

## Prompt Strategy

Script sử dụng prompt **content marketing-focused** thay vì literal translation:

### 1. Creative Freedom ✨
- **Không cứng nhắc**: Model được phép thêm/sửa nội dung
- **Goal-oriented**: Focus vào lead nurture & email marketing
- **Storytelling**: Thêm hooks, scenarios, mini-stories
- **Engagement**: Thêm emoji, bullet points, CTAs

### 2. Privacy First 🔒
- **Anonymize companies**: "Tiki" → "công ty e-commerce top 3 VN"
- **Keep credibility**: Giữ industry, scale, metrics
- **Examples**:
  - "VinID" → "Platform loyalty program lớn nhất VN"
  - "CEO của Sendo" → "CEO của startup e-commerce Series C"

### 3. Technical Accuracy 🎯
- Giữ ~190 technical terms (Data Platform, ML, API, etc.)
- Giữ 100% code blocks, SQL, YAML
- Giữ metrics: ROI, MAU, KPI

### 4. Nurture & Marketing 📧
- Conversational tone (dùng "bạn")
- Pain point-driven hooks
- Social proof & urgency
- Clear CTAs
- Before/After comparisons
- Quick wins highlighted

## Lưu ý quan trọng

- ⚠️ Script sẽ **ghi đè** file gốc
- ⚠️ Nên backup hoặc commit vào git trước khi chạy
- ⚠️ Kiểm tra kết quả sau khi dịch (AI có thể không hoàn hảo 100%)
- ⚠️ File phải tồn tại trong `content/blog/`

## Requirements

- Python 3.10+
- Google Gemini API key trong `.env`:
  ```
  GEMINI_API_KEY=your_api_key_here
  ```

## Model sử dụng

- **Model**: `gemini-2.5-pro-preview-03-25` (Gemini 2.5 Pro)
- **Temperature**: 0.3 (thấp để dịch nhất quán)
- **Max tokens**: 32,768 (hỗ trợ blog posts dài)

### Why Gemini 2.5 Pro?

- ✅ **Higher quota**: Không bị 429 quota errors như 2.0-pro-exp
- ✅ **Better quality**: Improved translation & content transformation
- ✅ **Better anonymization**: Hiểu và thực hiện privacy rules tốt hơn
- ✅ **Context understanding**: Handle long blog posts (up to 32K tokens)
- ✅ **Creative capability**: Excellent at adding hooks, engagement elements
- ⏱️ Processing time: ~30-60s per blog post
- 💰 Cost: ~$0.20-0.30 per translation (worth it for marketing content)

## Troubleshooting

### Lỗi: GEMINI_API_KEY not found
- Kiểm tra file `.env` có `GEMINI_API_KEY`

### Lỗi: File not found
- Đảm bảo filename đúng và file tồn tại trong `content/blog/`
- Bao gồm extension `.mdx`

### ⚠️ Lỗi: MDX Compile Error - "Unexpected character before name"

**Error message:**
```
[next-mdx-remote] error compiling MDX:
Unexpected character `1` (U+0031) before name, expected a character that can start a name
Unexpected character `5` (U+0035) before name, expected a character that can start a name
```

**Nguyên nhân:**
- **Lỗi 1 - Hash symbol `#`**: Model tạo heading level 1 hoặc dùng `#` trong tables
  - `# 1. Title`, `# 5. Conclusion` → MDX không chấp nhận H1
  - `| **#1: Phase** |` → MDX hiểu nhầm thành heading trong table!
- **Lỗi 2 - Less-than symbol `<`**: Model dùng `<` trước số
  - `<10 người`, `<5 phút`, `<1%` → MDX hiểu nhầm thành JSX tag `<10>`, `<5>`!
  - MDX cố parse như `<10>` nhưng tag name không thể bắt đầu bằng số → CRASH!

**Giải pháp:**
1. ✅ Script đã được update với rules **CỰC KỲ RÕ RÀNG** về MDX syntax
2. ✅ **HASH SYMBOL**: Model được instruct **TUYỆT ĐỐI KHÔNG DÙNG `#`** (H1) trong content
   - ✅ **CHỈ ĐƯỢC DÙNG** `##`, `###`, `####` (H2, H3, H4)
   - ✅ **KHÔNG DÙNG `#` TRONG TABLES** - dùng `1.`, `2.` thay vì `#1:`, `#2:`
3. ✅ **LESS-THAN SYMBOL**: Model được instruct dùng escape character hoặc Vietnamese
   - ✅ **OPTION 1**: Dùng HTML entity `&lt;` (ví dụ: `&lt;10 người`)
   - ✅ **OPTION 2**: Dùng Vietnamese words (ví dụ: `dưới 10 người`)
4. ✅ Prompt yêu cầu model kiểm tra output trước khi trả về

**Nếu vẫn gặp lỗi:**
Run commands sau để tìm và sửa:
```bash
# Tìm H1 headings (ngoài code blocks)
grep -n "^# " content/blog/your-file.mdx

# Tìm `#` trong tables
grep -n "| \*\*#[0-9]" content/blog/your-file.mdx

# Tìm `<` trước số (ngoài code blocks)
grep -n '<[0-9]' content/blog/your-file.mdx

# Sửa thủ công:
# - Đổi `# ` thành `## ` trong headings
# - Đổi `| **#1: Phase** |` thành `| **1. Phase** |` trong tables
# - Đổi `<10` thành `&lt;10` hoặc `dưới 10`
```

**Ví dụ sửa lỗi:**

**1. Hash symbol trong tables:**
```markdown
❌ SAI:  | **#1: Startup** | 2010-2014 | ...
✅ ĐÚNG: | **1. Startup** | 2010-2014 | ...

❌ SAI:  | **#5: Growth** | 2020-2025 | ...
✅ ĐÚNG: | **5. Growth** | 2020-2025 | ...
```

**2. Less-than symbol trước số:**
```markdown
❌ SAI:  **Quy mô team**: <10 người
✅ ĐÚNG: **Quy mô team**: &lt;10 người       (HTML entity)
✅ ĐÚNG: **Quy mô team**: dưới 10 người     (Vietnamese)

❌ SAI:  Thời gian: <5 phút
✅ ĐÚNG: Thời gian: &lt;5 phút              (HTML entity)
✅ ĐÚNG: Thời gian: dưới 5 phút             (Vietnamese)

❌ SAI:  | Query time | <2 giây |
✅ ĐÚNG: | Query time | &lt;2 giây |        (HTML entity - recommended cho tables)
✅ ĐÚNG: | Query time | dưới 2 giây |       (Vietnamese - OK nhưng less technical)
```

**Lưu ý:**
- Code comments (như `# Python comment`) trong code blocks là OK
- Color codes (như `#189eff`) trong text cũng OK
- Comparison operators trong code blocks (`if x < 10:`) là OK
- **HTML entity `&lt;`** sẽ hiển thị thành `<` khi render (giữ ký hiệu toán học)

### Kết quả dịch không như mong đợi
- Kiểm tra prompt trong script
- Có thể chỉnh `temperature` (hiện tại: 0.3)
- Chạy lại với file khác để so sánh

## Related Scripts

- `generate_image.py` - Tạo cover image cho blog
- `../scripts/add-updated-date.js` - Thêm trường updated cho tất cả posts
