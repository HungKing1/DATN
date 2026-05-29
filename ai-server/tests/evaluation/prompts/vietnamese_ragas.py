"""Vietnamese prompt overrides for Ragas metrics.

Ragas uses English prompts by default. When evaluating Vietnamese texts
(especially legal documents), we need to override the prompts to prevent
translation loss and improve evaluation accuracy.
"""

from ragas.prompt import Prompt

# ─────────────────────────────────────────────────────────
# 1. Faithfulness (Độ trung thực - Hallucination check)
# ─────────────────────────────────────────────────────────

VIETNAMESE_FAITHFULNESS_PROMPT = Prompt(
    name="vietnamese_faithfulness",
    instruction="""Bạn là một chuyên gia pháp lý và kiểm định thông tin.
Cho một câu hỏi (question), ngữ cảnh (context) và câu trả lời (answer).
Nhiệm vụ của bạn là kiểm tra xem TẤT CẢ các mệnh đề/khẳng định trong câu trả lời có được suy ra hoặc hỗ trợ bởi phần ngữ cảnh hay không.
Nếu một mệnh đề có thông tin không xuất hiện trong ngữ cảnh (bịa đặt, ảo giác), hãy đánh giá là không trung thực.

Định dạng trả về phải là JSON với cấu trúc:
{
    "statements": [
        {
            "statement": "Mệnh đề 1 từ câu trả lời",
            "reason": "Giải thích mệnh đề này có được hỗ trợ bởi ngữ cảnh không",
            "verdict": 1 hoặc 0 (1 nếu được hỗ trợ, 0 nếu không được hỗ trợ)
        }
    ]
}
""",
    input_keys=["question", "context", "answer"],
    output_key="output",
    output_type="json",
)

# ─────────────────────────────────────────────────────────
# 2. Answer Relevancy (Độ liên quan của câu trả lời)
# ─────────────────────────────────────────────────────────

VIETNAMESE_ANSWER_RELEVANCY_PROMPT = Prompt(
    name="vietnamese_answer_relevancy",
    instruction="""Bạn là một giám khảo đánh giá sự logic của văn bản.
Cho một câu trả lời (answer) đã được sinh ra cho một câu hỏi ẩn.
Nhiệm vụ của bạn là cố gắng suy luận (reverse-engineer) ra câu hỏi ban đầu dựa trên câu trả lời này.
Hãy đưa ra 3 câu hỏi khả thi nhất mà câu trả lời này đang cố gắng giải đáp.

Định dạng trả về phải là JSON:
{
    "questions": [
        "Câu hỏi suy luận 1",
        "Câu hỏi suy luận 2",
        "Câu hỏi suy luận 3"
    ]
}
""",
    input_keys=["answer"],
    output_key="output",
    output_type="json",
)

# ─────────────────────────────────────────────────────────
# 3. Context Precision (Độ chính xác ngữ cảnh)
# ─────────────────────────────────────────────────────────

VIETNAMESE_CONTEXT_PRECISION_PROMPT = Prompt(
    name="vietnamese_context_precision",
    instruction="""Cho một câu hỏi (question), đáp án chuẩn (ground_truth) và một danh sách các ngữ cảnh (contexts).
Nhiệm vụ của bạn là đánh giá xem ngữ cảnh này có thực sự hữu ích để suy ra đáp án chuẩn cho câu hỏi đó hay không.
Nếu ngữ cảnh cung cấp đủ thông tin để trả lời, verdict là 1. Nếu ngữ cảnh không liên quan hoặc vô ích, verdict là 0.

Định dạng trả về phải là JSON:
{
    "reason": "Giải thích vì sao ngữ cảnh hữu ích hoặc vô ích",
    "verdict": 1 hoặc 0
}
""",
    input_keys=["question", "ground_truth", "context"],
    output_key="output",
    output_type="json",
)

# ─────────────────────────────────────────────────────────
# 4. Context Recall (Độ phủ ngữ cảnh)
# ─────────────────────────────────────────────────────────

VIETNAMESE_CONTEXT_RECALL_PROMPT = Prompt(
    name="vietnamese_context_recall",
    instruction="""Cho một câu hỏi (question), đáp án chuẩn (ground_truth) và một danh sách các ngữ cảnh (contexts).
Nhiệm vụ của bạn là phân tích đáp án chuẩn thành các mệnh đề nhỏ, sau đó kiểm tra xem mỗi mệnh đề có thể được tìm thấy trong ngữ cảnh đã cho hay không.
Điều này giúp đo lường xem hệ thống tìm kiếm có bỏ sót thông tin quan trọng nào không.

Định dạng trả về phải là JSON:
{
    "statements": [
        {
            "statement": "Mệnh đề 1 từ đáp án chuẩn",
            "reason": "Giải thích vì sao ngữ cảnh có hoặc không chứa thông tin này",
            "verdict": 1 hoặc 0 (1 nếu tìm thấy, 0 nếu bị thiếu)
        }
    ]
}
""",
    input_keys=["question", "ground_truth", "context"],
    output_key="output",
    output_type="json",
)


