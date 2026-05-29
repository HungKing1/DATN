import asyncio
import json
import logging
from pathlib import Path

from rag_backend.config.settings import get_settings
from rag_backend.di.container import init_container

logger = logging.getLogger(__name__)

# Prompt để LLM tự sinh câu hỏi từ ngữ cảnh (PDF/Law chunks)
DATA_GENERATOR_PROMPT = """Bạn là một chuyên gia Red Teamer và AI Evaluator xuất sắc trong mảng Pháp luật Việt Nam.
Tôi sẽ cung cấp cho bạn một đoạn văn bản (context). Nhiệm vụ của bạn là đọc và tạo ra 1 cặp câu hỏi - câu trả lời (QA pair) để đánh giá (test) một hệ thống AI tư vấn luật.

Hãy chọn NGẪU NHIÊN 1 trong 3 loại câu hỏi (chiến thuật test) sau để tạo ra QA pair:

1. Fact-check (Kiểm chứng): Tạo câu hỏi hóc búa, yêu cầu suy luận từ nhiều chi tiết trong context. 
   - Ground_truth: Câu trả lời chính xác dựa trên context.
2. Out of Context (Ngoài lề - Chống Hallucination): Tạo một câu hỏi liên quan đến chủ đề pháp luật nhưng thông tin để trả lời KHÔNG HỀ CÓ trong context.
   - Ground_truth: Bắt buộc phải là "Tôi không biết do thông tin không có trong tài liệu cung cấp" hoặc tương tự.
3. Ambiguous (Mập mờ): Đặt một câu hỏi pháp lý chung chung, thiếu chủ ngữ, điều kiện hoặc ngữ cảnh cụ thể.
   - Ground_truth: Nêu rõ AI cần phải hỏi ngược lại người dùng để làm rõ thông tin gì.

MỘT SỐ YÊU CẦU CHUNG:
- Cố gắng sử dụng ngôn ngữ tự nhiên như cách một người dân bình thường hỏi luật sư.
- Không tiết lộ cho AI biết bạn đang dùng chiến thuật test nào trong câu hỏi.

Context: {context}

Định dạng trả về là JSON hợp lệ:
{
    "attack_type": "Tên chiến thuật đã chọn (Fact-check, Out of Context, hoặc Ambiguous)",
    "question": "Câu hỏi test của bạn...",
    "ground_truth": "Câu trả lời chuẩn xác (hoặc câu từ chối trả lời) theo đúng chiến thuật..."
}
"""

async def generate_dataset(num_samples: int = 10):
    """Lấy ngẫu nhiên các chunk từ Weaviate và sinh ra câu hỏi."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Khởi tạo môi trường...")
    
    settings = get_settings()
    container = init_container(settings)
    
    vector_repo = container.vector_repository()
    llm_provider = container.llm_provider()
    
    logger.info("Đang lấy ngẫu nhiên các chunk từ Weaviate...")
    # Lấy các chunks ngẫu nhiên (chúng ta sẽ lấy giới hạn 50 chunk đầu tiên rồi chọn ngẫu nhiên)
    chunks = await vector_repo.search_chunks(
        query_vector=[0.0] * settings.embedding_dimension, # Vector dummy để query
        top_k=num_samples * 2,
    )
    
    if not chunks:
        logger.error("Không tìm thấy dữ liệu trong Weaviate. Hãy chắc chắn bạn đã Ingest tài liệu.")
        return
        
    import random
    selected_chunks = random.sample(chunks, min(num_samples, len(chunks)))
    
    dataset = []
    
    logger.info(f"Bắt đầu sinh câu hỏi cho {len(selected_chunks)} chunks...")
    for idx, chunk in enumerate(selected_chunks):
        logger.info(f"Đang sinh câu hỏi {idx + 1}/{len(selected_chunks)}...")
        prompt = DATA_GENERATOR_PROMPT.replace("{context}", chunk.content)
        
        try:
            response = await llm_provider.generate(
                prompt=prompt,
                system_prompt="Bạn là một AI assistant hữu ích trả về JSON hợp lệ."
            )
            
            # Xử lý chuỗi JSON an toàn (loại bỏ markdown block nếu có)
            json_text = response.text.replace("```json", "").replace("```", "").strip()
            qa_pair = json.loads(json_text)
            
            dataset.append({
                "attack_type": qa_pair.get("attack_type", "Unknown"),
                "question": qa_pair.get("question"),
                "ground_truth": qa_pair.get("ground_truth"),
            })
            
        except Exception as e:
            logger.warning(f"Lỗi khi sinh câu hỏi cho chunk {idx}: {e}")
            continue
            
    # Lưu ra file JSON
    output_dir = Path("tests/evaluation/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "golden_dataset.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
        
    logger.info(f"Đã lưu thành công {len(dataset)} câu hỏi vào {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_dataset(num_samples=10))
