###1 node deployment
#Inspired from this tutorial : https://sarinsuriyakoon.medium.com/deploy-ollama-on-local-kubernetes-microk8s-6ca22bfb7fa3

Once Usernetes is up, follow these instructions:
```
kubectl create namespace ollama
kubectl apply -f ollama.yaml
kubectl apply -f ollama_service.yaml
kubectl -n ollama port-forward service/ollama 11434:80 &
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"Why is the sky blue?"
}'
```


```
time curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"When and where was Linus Torvalds born?"
}'
Handling connection for 11434
{"model":"llama2","created_at":"2025-02-15T15:45:10.610575329Z","response":"Lin","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:13.62523913Z","response":"us","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:19.950126286Z","response":" Tor","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:25.631028756Z","response":"val","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:40.796892252Z","response":"ds","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:42.855247406Z","response":" was","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:48.356937421Z","response":" born","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:58.456003501Z","response":" on","done":false}
{"model":"llama2","created_at":"2025-02-15T15:45:59.487858706Z","response":" December","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:07.161334267Z","response":" ","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:09.026162334Z","response":"2","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:12.68798439Z","response":"6","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:18.454064201Z","response":",","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:20.916924476Z","response":" ","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:28.750862582Z","response":"1","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:31.064869326Z","response":"9","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:44.783824135Z","response":"6","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:57.254898024Z","response":"9","done":false}
{"model":"llama2","created_at":"2025-02-15T15:46:58.814638342Z","response":",","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:02.448540194Z","response":" in","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:10.555487249Z","response":" Hels","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:12.195218441Z","response":"ink","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:23.168144083Z","response":"i","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:29.759940436Z","response":",","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:36.144613052Z","response":" Finland","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:49.923992663Z","response":".","done":false}
{"model":"llama2","created_at":"2025-02-15T15:47:54.291307611Z","response":"","done":true,"done_reason":"stop","context":[518,25580,29962,3532,14816,29903,29958,5299,829,14816,29903,6778,13,13,10401,322,988,471,4342,375,4794,791,6289,6345,29973,518,29914,25580,29962,13,11667,375,4794,791,6289,471,6345,373,5846,29871,29906,29953,29892,29871,29896,29929,29953,29929,29892,297,23278,682,29875,29892,18312,29889],"total_duration":198897951698,"load_duration":9086177,"prompt_eval_count":31,"prompt_eval_duration":35206000000,"eval_count":27,"eval_duration":163681000000}

real	3m18.990s
user	0m0.004s
sys	0m0.014s
```

###2 nodes deployment
TODO
