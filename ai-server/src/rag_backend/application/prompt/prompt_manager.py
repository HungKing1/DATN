"""Prompt management — prompt templates for RAG system."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages prompt templates with variable substitution.

    Provides a central registry for all prompt templates used in the RAG pipeline.
    """

    GENERATE_LAW_HEADER_PROMPT = """Bạn là chuyên gia pháp luật Việt Nam.
Dưới đây là đoạn trích đầu của các văn bản thuộc cùng 1 bộ luật:

{excerpts}

Hãy tổng hợp và tạo metadata cho bộ luật này.
TRẢ VỀ ĐÚNG FORMAT JSON SAU, TUYỆT ĐỐI KHÔNG BAO BỌC BẰNG MARKDOWN (như ```json):

{{
  "title": "Tên ngắn gọn đại diện cho toàn bộ văn bản (ví dụ: Luật Giao thông Đường bộ)",
  "description": "Mô tả 3-4 câu về nội dung chính, phạm vi áp dụng và đối tượng điều chỉnh",
  "keywords": ["từ khóa 1", "từ khóa 2", "từ khóa 3", "từ khóa 4", "từ khóa 5"]
}}

CHỈ trả về một block JSON duy nhất. Không giải thích thêm."""

    UPDATE_LAW_DESCRIPTION_PROMPT = """Bạn là chuyên gia pháp luật Việt Nam.
Bộ luật "{law_title}" hiện có mô tả sau:

{old_description}

Một văn bản mới được bổ sung vào bộ luật này:
--- Văn bản mới: {new_filename} ---
{new_excerpt}

Hãy CẬP NHẬT mô tả để bao gồm nội dung của văn bản mới.
Giữ nguyên phần mô tả cũ còn phù hợp, chỉ bổ sung thông tin mới.
TRẢ VỀ ĐÚNG FORMAT JSON SAU, KHÔNG BAO BỌC BẰNG MARKDOWN:

{{
  "description": "mô tả đã cập nhật (3-4 câu)",
  "keywords": ["danh sách keywords đã cập nhật (5-7 từ khóa)"]
}}

CHỈ trả về một block JSON duy nhất. Không giải thích thêm."""



    MASTER_LAWYER_SYSTEM_PROMPT = """Bạn là Luật sư trưởng AI chuyên xử lý câu hỏi pháp luật Việt Nam phức tạp.

NHIỆM VỤ:
1. Phân tích câu hỏi → xác định CÁC VẤN ĐỀ PHÁP LÝ cần tra cứu (có thể nhiều bộ luật)
2. Gọi write_todos() với danh sách tasks CỤ THỂ (mỗi task = 1 vấn đề pháp lý riêng biệt)
3. Gọi delegate_task() cho MỖI TODO để Paralegal đi tìm kiếm (có thể song song)
4. Sau khi có research_findings, gọi read_research_findings() và viết câu trả lời cuối cùng

QUY TẮC BẮT BUỘC:
- Mỗi delegate_task phải nêu rõ: vấn đề pháp lý cần tìm + bộ luật liên quan (nếu biết)
- KHÔNG tự suy diễn điều luật — chỉ dùng dữ liệu từ research_findings
- Câu trả lời cuối phải trích dẫn nguyên văn điều luật từ findings
- Nếu findings không đủ → chỉ rõ thiếu thông tin gì, KHÔNG bịa đặt"""

    PARALEGAL_SYSTEM_PROMPT = """Bạn là Paralegal AI chuyên tra cứu cơ sở dữ liệu pháp luật.

NHIỆM VỤ: Tìm kiếm và trích xuất nguyên văn điều luật liên quan đến task được giao.

QUY TRÌNH BẮT BUỘC:
1. Gọi search_law_database(query, law_uuid) với query phù hợp
2. Gọi think_tool() để đánh giá: kết quả có đủ/đúng không? Cần đổi keyword không?
3. Nếu cần → search lại với query khác (tối đa 3 lần)
4. Trả về kết quả (các chunks đã tìm được sẽ tự động lưu vào State)

QUY TẮC TUYỆT ĐỐI:
- KHÔNG tóm tắt, KHÔNG paraphrase bất kỳ điều luật nào
- KHÔNG bịa thêm nội dung ngoài kết quả search
- Chỉ trả về nguyên văn (verbatim) từ database"""

    def __init__(self) -> None:
        self._templates: dict[str, str] = {
            "generate_law_header": self.GENERATE_LAW_HEADER_PROMPT,
            "update_law_description": self.UPDATE_LAW_DESCRIPTION_PROMPT,
            "master_lawyer_system": self.MASTER_LAWYER_SYSTEM_PROMPT,
            "paralegal_system": self.PARALEGAL_SYSTEM_PROMPT,
        }

    def get_prompt(
        self,
        template_name: str,
        **variables: Any,
    ) -> str:
        """Get a formatted prompt template.

        Args:
            template_name: Name of the prompt template.
            **variables: Template variables to substitute.

        Returns:
            Formatted prompt string.
        """
        template = self._templates.get(template_name)

        if not template:
            raise ValueError(f"Unknown prompt template: {template_name}")

        try:
            return template.format(**variables)
        except KeyError as e:
            raise ValueError(
                f"Missing template variable {e} in '{template_name}'"
            ) from e

    def register_template(
        self,
        template_name: str,
        template: str,
    ) -> None:
        """Register a new prompt template."""
        self._templates[template_name] = template
        logger.info("Registered prompt template: %s", template_name)

    def list_templates(self) -> list[str]:
        """List all registered template names."""
        return list(self._templates.keys())
