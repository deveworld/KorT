# KorT
Korean Translation Benchmark, LLM-as-a-judge

## Abstract
KorT는 대규모 언어 모델(LLM)을 바탕으로 번역 품질을 정량적으로 평가합니다.

<details>
<summary>배경</summary>
현재 많은 번역 앱이 존재하지만 번역 품질을 정량적으로 평가하고, 제대로 비교한 경우가 없습니다.
게다가, 기존의 BLEU와 같은 자동 평가 지표들은 은어나 문화적 적절성과 같은 미묘한 차이를 정확히 포착하지 못하는 경우가 많으며, 인간 평가는 비용과 시간이 많이 소요됩니다. 그래서 본 연구를 통해 한국어-다국어 번역 역량을 엄격하게 평가하기 위해 설계된 새로운 벤치마크인 <bold>KorT</bold>를 제안합니다. 

KorT는 "LLM 기반 평가 (LLM-as-a-judge)" 패러다임을 통해 대규모 언어 모델(LLM)의 정교한 언어 이해 능력을 활용합니다. 이를 위해, 번역하기 어려운 것으로 알려진 다양한 문장들로 구성된 데이터셋을 구축합니다. 이 데이터셋은 여러 도메인과 언어적 현상(예: 중의성, 관용 표현, 문화적 참조 등)을 포괄합니다. 다양한 MT 모델과 LLM 모델이 생성한 번역 결과물은, 평가 프롬프트를 사용하여 고성능 LLM에 의해 평가됩니다.

핵심 목표는 기존 자동 평가 지표보다 인간의 판단과 높은 상관관계를 가지면서도, 신뢰할 수 있고 확장 가능하며 정교한 평가 체계를 구축하는 것입니다. 이를 위해, KorT 벤치마크에서의 결과를 기반으로 MT 시스템의 순위를 보여주는 공개 리더보드를 공개할 예정입니다. 이를 통해 현재 번역 기술의 강점과 약점에 대한 힌트를 제공하고, 특히 한국어와 관련된 까다로운 언어적 맥락에서의 번역 성능 향상을 촉진해, 궁극적으로 고품질 다국어 기계 번역 분야의 발전에 기여할 것으로 기대됩니다.
</details>

## Usage

### Install
KorT 설치하기
```
git clone https://github.com/deveworld/kort
cd kort
pip install .
```

### Generate
이용 가능한 번역기 리스트 보기
```
python -m kort.scripts.generate -l
```

하나를 선택하여 생성
```
python -m kort.scripts.generate \
    -t openai \
    -n gpt-4.1-mini \
    --api_key sk-xxx
```

### Evaluation
평가 가능한 모델 리스트 보기
```
python -m kort.scripts.evaluate -l
```

Generate 된 파일을 input으로 받아 평가
```
python -m kort.scripts.evaluate \
    -t gemini \
    -n gemini-2.5-pro-preview-03-25 \
    --api_key AIzaxxx \
    --input generated/openai_gpt-4.1-mini.json
```

또는 Batch를 사용하여 평가할 경우: 먼저 Batch 등록한 후
```
python -m kort.scripts.eval_batch \
    -t claudebatch \
    -n claude-3-7-sonnet-20250219 \
    --api_key sk-ant-api03-xxx \
    --input generated/openai_gpt-4.1-mini.json
```
Batch가 끝난 뒤에 Job ID를 입력하여 평가 완료
```
python -m kort.scripts.eval_batch \
    -t claudebatch \
    -n claude-3-7-sonnet-20250219 \
    --api_key sk-ant-api03-xxx \
    --input generated/openai_gpt-4.1-mini.json \
    --job_id msgbatch_xxx
```

### LeaderBoard
아래 명령으로 리더보드 실행
```
python -m kort.scripts.leaderboard
```