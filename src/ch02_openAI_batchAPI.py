import time
from openai import OpenAI

client = OpenAI()

# file upload
batch_input_file = client.files.create(
  file=open("../data/ch02_batchinput.jsonl", "rb"),
  purpose="batch"
)

# Create a new batch
client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "테스트를 위한 배치",
    }
)
start_time = time.time()

# Batch 객체들의 리스트를 가져옵니다.
batches = client.batches.list().data

# 각 배치의 상세 정보를 출력합니다.
for batch in batches[:5]:
    print(f"Batch ID: {batch.id}")
    print(f"Status: {batch.status}")
    print(f"Created At: {batch.created_at}")
    print(f"input_file_id: {batch.input_file_id}")
    print(f"output_file_id: {batch.output_file_id}")
    print("------")
    

# status를 15초에 한번씩 확인하고 'completed'일때까지 로그를 출력
# status가 'completed'가 되면 루프를 탈출합니다.
# 총 걸린 시간을 추가로 출력합니다.
while True:
  status = client.batches.retrieve(client.batches.list().data[0].id).status
  print("time: ", time.strftime('%X', time.localtime()), "   |    status: ", status)
  if status == "completed":
    break
  time.sleep(60) # 60초에 한번씩 확인

print("Total time: ", time.time() - start_time)


# output file을 다운로드 받아서 출력
file_response = client.files.content(client.batches.list().data[0].output_file_id)
print(file_response.text.encode('utf-8').decode('unicode-escape'))

file_response.text.encode('utf-8').decode('unicode-escape').split("\n")[0].split(",")[10]