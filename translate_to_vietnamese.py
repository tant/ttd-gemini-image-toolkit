#!/usr/bin/env python3
"""
Translate blog posts to Vietnamese using Google Gemini AI.
Keeps technical terms in English for clarity.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from google import genai
from google.genai import types
import frontmatter

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

# Create client
client = genai.Client(api_key=GEMINI_API_KEY)

# Model configuration
MODEL_NAME = "gemini-2.5-pro-preview-03-25"  # Gemini 2.5 Pro with higher quota
GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0.3,  # Lower temperature for more consistent translations
    top_p=0.95,
    top_k=40,
    max_output_tokens=32768,  # Increased for longer blog posts
)


def load_english_terms():
    """Load list of technical terms to keep in English."""
    english_file = Path(__file__).parent.parent.parent / "content" / "english.md"

    if not english_file.exists():
        print(f"⚠️  Warning: {english_file} not found. Will translate all terms.")
        return []

    terms = []
    with open(english_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Extract terms from markdown list (e.g., "* Data Platform")
            if line.startswith('*'):
                term = line[1:].strip()
                # Remove any parenthetical explanations
                if '(' in term:
                    term = term.split('(')[0].strip()
                terms.append(term)

    return terms


def create_translation_prompt(content, english_terms):
    """Create prompt for Gemini to translate content to Vietnamese."""
    terms_list = "\n".join(f"- {term}" for term in english_terms[:50])  # Show first 50 terms

    prompt = f"""Bạn là một chuyên gia content marketing và copywriting chuyên về nội dung Data/Tech tiếng Việt.

⚠️ **QUAN TRỌNG**: Bạn chỉ nhận CONTENT của blog post (không có frontmatter metadata giữa ---).
Frontmatter đã được xử lý riêng và SẼ KHÔNG thay đổi. Bạn CHỈ cần chuyển đổi nội dung bài viết.

NHIỆM VỤ:
Chuyển đổi nội dung blog post bên dưới thành tiếng Việt với mục tiêu:
- **Lead Nurture**: Xây dựng niềm tin, tạo kết nối cảm xúc với độc giả
- **Email Marketing Ready**: Nội dung hấp dẫn, dễ scan, có CTA rõ ràng
- **Chuyên nghiệp nhưng gần gũi**: Như đang tư vấn cho bạn bè
- **Action-oriented**: Khuyến khích độc giả hành động

QUYỀN SÁNG TẠO:
✅ **BẠN ĐƯỢC PHÉP**:
- Thêm câu hỏi mở đầu để thu hút (hook)
- Thêm mini-stories hoặc scenarios relatable
- Thêm bullet points để dễ scan
- Thêm emoji phù hợp (⚡ 🎯 ✅ ❌ 💡) nếu tăng engagement
- Viết lại câu cho tự nhiên, không dịch từng từ
- Thêm transitions giữa sections
- Thêm quick wins/tips nổi bật
- Làm rõ value propositions

⚠️ **NHƯNG GIỮ**:
- Core message và technical accuracy
- Cấu trúc markdown (headings, lists, code blocks)
- Độ dài tương đương (±20%)
- Professional tone (không quá casual)

QUY TẮC QUAN TRỌNG:

1. **GIỮ NGUYÊN CÁC THUẬT NGỮ KỸ THUẬT SAU ĐÂY (không dịch)**:
{terms_list}
... và các thuật ngữ kỹ thuật tương tự khác.

2. **PHONG CÁCH VIẾT - Lead Nurture Focus**:
- Dùng "bạn" (conversational, tạo kết nối 1-1)
- Câu ngắn, punchy (dễ scan trong email)
- Bắt đầu sections với hooks (pain points, questions, bold claims)
- Ví dụ: "Marketing team của bạn có chờ 2 tuần cho mỗi report không?" thay vì "Nhiều team gặp vấn đề chậm"
- Thêm social proof: "Hơn 80% doanh nghiệp gặp vấn đề này..."
- Tạo urgency nhẹ nhàng: "Càng sớm bắt đầu, càng nhanh thấy kết quả"
- Kết thúc mỗi section với quick win hoặc next step

3. **CASE STUDIES - Privacy First** ⚠️:
- **KHÔNG BAO GIỜ** nêu tên công ty cụ thể (VD: "Tiki", "VinID", "Sendo")
- Thay bằng descriptors:
  - "Một công ty e-commerce top 3 Việt Nam..."
  - "Startup fintech Series B..."
  - "Ngân hàng thương mại top 10..."
  - "Doanh nghiệp retail với 200+ cửa hàng..."
- Giữ lại industry và scale để credible
- Giữ lại metrics cụ thể (vẫn impressive nhưng anonymous)

4. **MỤC TIÊU EMAIL MARKETING**:
- CTA rõ ràng ở cuối mỗi major section
- Highlight value propositions (bold, emoji)
- Số liệu cụ thể (ROI, time saved, cost reduction)
- Before/After comparisons
- Lists thay vì paragraphs dài
- Quotes/testimonials (anonymized)

5. **ĐỊNH DẠNG & MDX SYNTAX** ⚠️:

🚨 **CRITICAL - MDX HEADING RULES (BẮT BUỘC!):**

RULE #1: **TUYỆT ĐỐI KHÔNG ĐƯỢC** sử dụng `#` (single hash = H1) trong toàn bộ content
- ❌ SAI: `# Tiêu đề bất kỳ`
- ❌ SAI: `# 1. Giới thiệu`
- ❌ SAI: `# 5. Kết luận`
- ❌ SAI: Bất kỳ dòng nào bắt đầu bằng `# ` (dấu cách sau hash)

RULE #2: **CHỈ ĐƯỢC DÙNG** `##`, `###`, `####` cho headings (H2, H3, H4)
- ✅ ĐÚNG: `## Giới thiệu`
- ✅ ĐÚNG: `## 1. Giới thiệu về Data Platform`
- ✅ ĐÚNG: `## 5. Kết luận và khuyến nghị`
- ✅ ĐÚNG: `### Phân tích chi tiết`
- ✅ ĐÚNG: `#### Technical details`

RULE #3: Kiểm tra kỹ output - nếu có bất kỳ dòng nào bắt đầu `# ` thì XÓA hoặc đổi thành `##`

RULE #4: **KHÔNG DÙNG `#` TRONG TABLES** - MDX sẽ hiểu nhầm thành heading
- ❌ SAI: `| **#1: Phase** |` → Gây lỗi MDX!
- ✅ ĐÚNG: `| **1. Phase** |` hoặc `| **Phase 1** |`
- ❌ SAI: `| **#5: Conclusion** |`
- ✅ ĐÚNG: `| **5. Conclusion** |`

🚨 **CRITICAL - LESS-THAN SYMBOL `<` RULES (BẮT BUỘC!):**

RULE #5: **TUYỆT ĐỐI KHÔNG ĐƯỢC** dùng `<` trước số (MDX hiểu nhầm thành JSX tag)
- ❌ SAI: `<10 người`, `<5 phút`, `<1 giây`, `<2%`
- ❌ SAI: `**Quy mô team**: <10 người` → CRASH MDX!
- ❌ SAI: `Thời gian: <5 phút` → CRASH MDX!
- ❌ SAI: `GMV <1 triệu USD/tháng` → CRASH MDX!

✅ ĐÚNG - Dùng **HTML ENTITY** `&lt;` để escape (RECOMMENDED):
- ✅ **OPTION 1 - HTML Entity** (giữ ký hiệu toán học, professional):
  - `&lt;10 người` → hiển thị: "<10 người"
  - `&lt;5 phút` → hiển thị: "<5 phút"
  - `&lt;1 giây` → hiển thị: "<1 giây"
  - `&lt;2%` → hiển thị: "<2%"
  - `&lt;1M USD` → hiển thị: "<1M USD"

- ✅ **OPTION 2 - Vietnamese words** (tự nhiên hơn, dễ đọc):
  - "dưới 10 người"
  - "ít hơn 5 phút"
  - "chưa đến 1 giây"
  - "dưới 2%"
  - "chưa tới 1 triệu USD"

**Ưu tiên sử dụng:**
1. **Tables & Technical content**: Dùng `&lt;` (giữ format chuyên nghiệp)
2. **Running text**: Dùng Vietnamese words (tự nhiên hơn)

**Ví dụ chuyển đổi:**

| Context | ❌ SAI | ✅ ĐÚNG (Option 1) | ✅ ĐÚNG (Option 2) |
|---------|--------|-------------------|-------------------|
| Table cell | `<10 người` | `&lt;10 người` | `dưới 10 người` |
| Running text | Chỉ mất `<5 phút` | Chỉ mất `&lt;5 phút` | Chỉ mất dưới 5 phút |
| Metrics | `<1% false positive` | `&lt;1% false positive` | `dưới 1% false positive` |
| Technical | Query `<2 giây` | Query `&lt;2 giây` | Query dưới 2 giây |

**LƯU Ý:** Điều này chỉ áp dụng cho văn bản thường. Trong code blocks thì `<` vẫn OK:
```python
if value < 10:  # OK - trong code block
    pass
```

**Các format khác:**
- ✅ Numbered lists: `1. Item`, `2. Item` (list format, không phải heading)
- ✅ Code blocks: ` ```python`, ` ```yaml`, etc.
- ✅ Tables OK - NHƯNG KHÔNG dùng `#` ở đầu cell hoặc `<` trước số
- ✅ Blockquotes OK
- ✅ Color codes OK: `#189eff`, `#0a1929` (trong code hoặc text)
- ❌ KHÔNG dùng HTML: `<div>`, `<span>`, etc.
- ❌ KHÔNG dùng JSX components
- Giữ nguyên URLs, links, code blocks hoàn toàn

6. **KHÔNG DỊCH (nhưng có thể ANONYMIZE)**:
- ✅ Tool/Platform names: BigQuery, Snowflake, AWS, GCP, Azure, Looker, etc.
- ✅ Code examples, SQL queries, YAML configs (giữ nguyên 100%)
- ✅ URLs và email addresses
- ✅ Technical metrics: MAU, DAU, ROI, KPI, etc.
- ✅ "Carptech" (brand name của chúng ta)
- ⚠️ **Tên công ty/doanh nghiệp khác**: PHẢI anonymize (xem rule #3)

VÍ DỤ VỀ ANONYMIZATION:

**Trước** (có tên công ty):
"Tiki đã triển khai Data Platform và giảm 50% thời gian xử lý"

**Sau** (anonymized):
"Một công ty e-commerce hàng đầu Việt Nam đã triển khai Data Platform và giảm 50% thời gian xử lý"

**Trước**:
"Case study: VinID với 15 million users"

**Sau**:
"Case study: Platform loyalty program lớn nhất Việt Nam với 15+ triệu users"

**Trước**:
"CEO của Sendo chia sẻ..."

**Sau**:
"CEO của một startup e-commerce Series C chia sẻ..."

---

NỘI DUNG CẦN CHUYỂN ĐỔI:

{content}

---

OUTPUT REQUIREMENTS:

🚨 **QUAN TRỌNG NHẤT - HEADING & TABLE FORMAT:**
Trước khi output, BẮT BUỘC kiểm tra:
1. Search toàn bộ output cho pattern `^# ` (dòng bắt đầu bằng `# ` + space)
2. Nếu tìm thấy BẤT KỲ dòng nào → ĐỔI NGAY thành `## ` (double hash)
3. Tuyệt đối KHÔNG được có `# ` ở đầu dòng nào (ngoài code blocks)
4. **TABLES**: Tìm pattern `| **#[0-9]` trong tables → Xóa `#` (ví dụ: `| **#1: Phase** |` → `| **1. Phase** |`)
5. **LESS-THAN SYMBOL**: Tìm pattern `<[0-9]` ngoài code blocks → ĐỔI thành:
   - **RECOMMENDED**: `&lt;` HTML entity (ví dụ: `<10 người` → `&lt;10 người`, `<5%` → `&lt;5%`)
   - **ALTERNATIVE**: Vietnamese words (ví dụ: `<10 người` → `dưới 10 người`, `<5%` → `dưới 5%`)

**Các yêu cầu khác:**
- CHỈ trả về nội dung đã chuyển đổi
- KHÔNG kèm ghi chú, giải thích, hoặc meta-commentary
- **VALID MDX SYNTAX**:
  - ❌ Không có `# ` ở đầu bất kỳ dòng nào
  - ❌ Không có `# 1. ...`, `# 5. ...`, `# Bất kỳ text nào`
  - ✅ Chỉ dùng `##`, `###`, `####` cho tất cả headings
  - ❌ Không HTML tags hoặc JSX
- Sẵn sàng để publish ngay
- Optimized cho email marketing và lead nurture

VÍ DỤ MDX VALID vs INVALID:

❌ INVALID (GÂY LỖI - TUYỆT ĐỐI TRÁNH):
```
# Giới thiệu
# 1. Giới thiệu về Data Platform
# 2. Kiến trúc hệ thống
# 5. Kết luận

| Giai đoạn | Mô tả |
|-----------|-------|
| **#1: Startup** | ... |     ← LỖI: `#` trong table cell!
| **#5: Growth** | ... |      ← LỖI: MDX sẽ crash!

**Quy mô team**: <10 người     ← LỖI: `<10` = JSX tag!
Thời gian: <5 phút             ← LỖI: `<5` = JSX tag!
GMV <1 triệu USD               ← LỖI: MDX crash!
```

✅ VALID (DÙNG FORMAT NÀY):
```
## Giới thiệu
## 1. Giới thiệu về Data Platform
## 2. Kiến trúc hệ thống
## 5. Kết luận

| Giai đoạn | Mô tả |
|-----------|-------|
| **1. Startup** | ... |      ← ĐÚNG: Không có `#`
| **5. Growth** | ... |       ← ĐÚNG: Chạy OK!

**Quy mô team**: &lt;10 người     ← ĐÚNG! (HTML entity)
Thời gian: &lt;5 phút             ← ĐÚNG! (HTML entity)
GMV dưới 1 triệu USD               ← ĐÚNG! (Vietnamese words)

| Chỉ số | Trước | Sau |
|--------|-------|-----|
| Query time | 30s | &lt;2 giây |  ← ĐÚNG! (HTML entity trong table)
| Team size | 50 | dưới 10 người |  ← ĐÚNG! (Vietnamese trong table)
```

**LƯU Ý:** Code comments trong code blocks có thể dùng `#`:
```python
# This is OK - đây là Python comment
def function():
    pass
```

**LƯU Ý 2:** Color codes cũng OK:
```
Color: #189eff  ← OK (trong text/code)
```"""

    return prompt


def translate_content(content, english_terms):
    """Translate content using Gemini API."""
    prompt = create_translation_prompt(content, english_terms)

    print("🤖 Calling Gemini API for translation...")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=GENERATION_CONFIG,
        )
        translated = response.text.strip()
        print("✅ Translation completed")
        return translated
    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        sys.exit(1)


def process_blog_post(filename, update_date=False):
    """
    Process a blog post: translate content while preserving frontmatter.

    IMPORTANT: This function:
    1. Extracts frontmatter (metadata between ---) separately
    2. Only translates the blog post CONTENT (after frontmatter)
    3. Preserves frontmatter 100% unchanged (title, description, slug, tags, etc.)
    4. Reconstructs the file with original frontmatter + translated content

    This ensures metadata like title, slug, SEO fields remain intact.
    """
    blog_dir = Path(__file__).parent.parent.parent / "content" / "blog"
    file_path = blog_dir / filename

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    print(f"📖 Reading: {filename}")

    # Load frontmatter and content separately
    # frontmatter library automatically separates:
    # - post.metadata (dict) = frontmatter between ---
    # - post.content (str) = actual blog content after ---
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # Load English terms
    english_terms = load_english_terms()
    print(f"📚 Loaded {len(english_terms)} technical terms to keep in English")

    # Translate ONLY the content (not frontmatter)
    # post.content = blog post body after frontmatter
    # Frontmatter (title, description, slug, etc.) is NOT passed to AI
    translated_content = translate_content(post.content, english_terms)

    # Update frontmatter field if needed (only 'updated' date)
    # This is a safe metadata update, not translation
    if update_date:
        today = date.today().strftime('%Y-%m-%d')
        post['updated'] = today
        print(f"📅 Updated 'updated' field to: {today}")

    # Write back: frontmatter (unchanged) + translated content
    # frontmatter.dump() reconstructs file with:
    # ---
    # [original frontmatter]
    # ---
    # [translated content]
    post.content = translated_content

    output_path = file_path
    with open(output_path, 'wb') as f:
        frontmatter.dump(post, f)

    print(f"✅ Successfully translated and saved: {filename}")
    if update_date:
        print(f"   Updated date: {post['updated']}")


def main():
    parser = argparse.ArgumentParser(
        description="Translate blog posts to Vietnamese using Gemini AI"
    )
    parser.add_argument(
        "filename",
        help="Blog post filename (e.g., 'modern-data-stack-2025.mdx')"
    )
    parser.add_argument(
        "--update-date",
        action="store_true",
        default=False,
        help="Update 'updated' field to today's date"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🇻🇳 BLOG POST TRANSLATION TO VIETNAMESE")
    print("=" * 60)
    print(f"File: {args.filename}")
    print(f"Update date: {args.update_date}")
    print("=" * 60)

    process_blog_post(args.filename, args.update_date)

    print("=" * 60)
    print("🎉 Translation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
