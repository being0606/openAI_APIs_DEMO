from openai import OpenAI
client = OpenAI()

# file upload
batch_input_file = client.files.create(
  file=open("./data/ch02_batchinput.jsonl", "rb"),
  purpose="batch"
)

# Create a new batch
client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)

# {
#   "id": "batch_abc123",
#   "object": "batch",
#   "endpoint": "/v1/chat/completions",
#   "errors": null,
#   "input_file_id": "file-abc123",
#   "completion_window": "24h",
#   "status": "validating",
#   "output_file_id": null,
#   "error_file_id": null,
#   "created_at": 1714508499,
#   "in_progress_at": null,
#   "expires_at": 1714536634,
#   "completed_at": null,
#   "failed_at": null,
#   "expired_at": null,
#   "request_counts": {
#     "total": 0,
#     "completed": 0,
#     "failed": 0
#   },
#   "metadata": null
# }



# Retrieve a batch
client.batches.retrieve("batch_abc123")
# 상태 : 설명
# validating : 배치가 시작되기 전에 입력 파일이 검증되고 있습니다.
# failed : 입력 파일이 유효성 검사 과정에 실패했습니다
# in_progress : 입력 파일이 성공적으로 검증되었고 배치가 현재 실행 중입니다
# finalizing : 배치가 완료되었고 결과가 준비 중입니다
# completed : 배치가 완료되었고 결과가 준비되었습니다
# expired : 배치는 24시간 내에 완료될 수 없었습니다.
# cancelling : 배치가 취소되고 있습니다 (최대 10분 정도 걸릴 수 있음)
# cancelled : 배치가 취소되었습니다



# Retrieve a file
file_response = client.files.content("file-xyz123")
print(file_response.text)
# {"id": "batch_req_123", "custom_id": "request-2", "response": {"status_code": 200, "request_id": "req_123", "body": {"id": "chatcmpl-123", "object": "chat.completion", "created": 1711652795, "model": "gpt-3.5-turbo-0125", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hello."}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 22, "completion_tokens": 2, "total_tokens": 24}, "system_fingerprint": "fp_123"}}, "error": null}
# {"id": "batch_req_456", "custom_id": "request-1", "response": {"status_code": 200, "request_id": "req_789", "body": {"id": "chatcmpl-abc", "object": "chat.completion", "created": 1711652789, "model": "gpt-3.5-turbo-0125", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hello! How can I assist you today?"}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 20, "completion_tokens": 9, "total_tokens": 29}, "system_fingerprint": "fp_3ba"}}, "error": null}


# Cancel a batch
client.batches.cancel("batch_abc123")


# List batches
client.batches.list(limit=10)