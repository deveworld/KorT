from enum import Enum
from hashlib import sha256

from pydantic import BaseModel

from .lang_code import LangCode


class Categories(Enum):
    IDIOM_PROVERB = "Idioms and Proverbs"
    WORDPLAY_PUN = "Wordplay and puns"
    CULTURE = "Cultural references"
    SLANG = "Slang and colloquialisms"
    LITERATURE = "Historical and literary allusions"


class GenerationMetadata(BaseModel):
    model_type: str
    model_name: str
    model_org: str
    timestamp: str


class Example(BaseModel):
    source: str
    translation: dict[LangCode, str]


class GenerationExample(BaseModel):
    source: str
    translated: str
    source_lang: LangCode
    target_lang: LangCode
    category: Categories
    reference_translation: str

    def get_hash(self) -> str:
        """Get the hash of the example."""
        return sha256(self.model_dump_json().encode("utf-8")).hexdigest()


class Generated(BaseModel):
    metadata: GenerationMetadata
    generated_examples: list[GenerationExample]


# TODO: Hardcoded-dict is workaround for now. Will be replaced with other format as like jsonl.
EVAL_DATA: dict[LangCode, dict[Categories, list[Example]]] = {}

EVAL_DATA[LangCode.ENG] = {
    Categories.IDIOM_PROVERB: [
        Example(
            source="You're barking up the wrong tree.",
            translation={LangCode.KOR: "너 완전 헛다리 짚고 있는 거야."},
        ),
        Example(
            source="Yeah, when pigs fly. You know.",
            translation={
                LangCode.KOR: "아니, 절대로. 너도 알잖아. (pigs fly를 제대로 번역하지 못하면 점수를 낮게 줄 것)"
            },
        ),
        Example(
            source="What a pencil fest! Typical engineering school.",
            translation={
                LangCode.KOR: "완전 고추밭이네! 전형적인 공대야. (pencil fest를 제대로 번역하지 못하면 점수를 낮게 줄 것)."
            },
        ),
    ],
    Categories.WORDPLAY_PUN: [
        Example(
            source="Time flies like an arrow; fruit flies like a banana.",
            translation={
                LangCode.KOR: "시간은 쏜살같이 빠르게 지나가고, 초파리는 바나나를 좋아한다."
            },
        ),
        Example(
            source="A boiled egg every morning is hard to beat.",
            translation={LangCode.KOR: "매일 아침 삶은 계란만한 게 없다."},
        ),
    ],
    Categories.CULTURE: [
        Example(
            source="It's his fifteen minutes of fame.",
            translation={LangCode.KOR: "잠깐 유명세를 타는 중이다."},
        ),
        Example(
            source="That's the elephant in the room.",
            translation={LangCode.KOR: "그건 모두가 알지만 언급하지 않는 문제이다."},
        ),
        Example(
            source="He threw me under the bus.",
            translation={LangCode.KOR: "그가 나를 희생양으로 삼았다."},
        ),
        Example(
            source="Looks like someone woke up on the wrong side of the bed.",
            translation={LangCode.KOR: "오늘 기분이 안 좋아 보이네."},
        ),
    ],
    Categories.SLANG: [
        Example(
            source="Let's Netflix and chill.",
            translation={LangCode.KOR: "넷플릭스 보면서 쉴까? / 라면 먹고 갈래?"},
        ),
        Example(
            source="Stop ghosting me!",
            translation={LangCode.KOR: "대답 좀 해! / 읽씹 좀 그만해!"},
        ),
        Example(
            source="I want to say 'OK Boomer' to my boss.",
            translation={
                LangCode.KOR: "사장님한테 '네 다음 틀딱'이라고 하고 싶어. (OK Boomer를 제대로 번역하지 못한 경우 점수를 매우 낮게 줄 것)"
            },
        ),
        Example(
            source="I got some tea to spil, anybody wanna listen?",
            translation={LangCode.KOR: "나 풀 소식 있는데, 들어볼래?"},
        ),
        Example(
            source="How do you lock in for a long time?",
            translation={LangCode.KOR: "어떻게 오랫동안 집중하나요?"},
        ),
        Example(
            source="Hey, Stay in your lane.",
            translation={LangCode.KOR: "야, 선 넘지마."},
        ),
    ],
    Categories.LITERATURE: [
        Example(
            source="Don't be such a Hamlet about it - just decide!",
            translation={LangCode.KOR: "그만 좀 고민하고, 그냥 결정해!"},
        ),
        Example(
            source="To be or not to be, that is the question.",
            translation={LangCode.KOR: "사느냐 죽느냐, 그것이 문제로다."},
        ),
        Example(
            source="She's gone down the rabbit hole researching conspiracy theories.",
            translation={
                LangCode.KOR: "그녀는 음모론을 연구하는 데 완전히 빠져들었다."
            },
        ),
        Example(
            source="A rose by any other name would smell as sweet.",
            translation={LangCode.KOR: "다른 이름으로 불려도 장미는 여전히 향기롭다."},
        ),
        Example(
            source="This is a real Catch-22 situation.",
            translation={
                LangCode.KOR: "이것은 진퇴양난의 상황이다. (Catch-22를 제대로 번역하지 못하면 점수를 낮게 줄 것)"
            },
        ),
        Example(
            source="He's a bit of a Jekyll and Hyde character.",
            translation={LangCode.KOR: "그는 이중적인 성격을 가지고 있다."},
        ),
        Example(
            source="Don't go all Big Brother on me.",
            translation={LangCode.KOR: "나 좀 그만 감시해."},
        ),
    ],
}


EVAL_DATA[LangCode.KOR] = {
    Categories.IDIOM_PROVERB: [
        Example(
            source="밥 한 그릇 뚝딱 해치웠어.",
            translation={LangCode.ENG: "I wolfed down a bowl of rice."},
        ),
        Example(
            source="이야, 오랜만이다. 밥은 먹고 다니냐?",
            translation={LangCode.ENG: "Wow, long time no see! How have you been?"},
        ),
        Example(
            source="아직 정해진 것도 아닌데, 너무 김칫국부터 마시는 거 아니야?",
            translation={
                LangCode.ENG: "Nothing's been decided yet, aren't you getting ahead of yourself?"
            },
        ),
        Example(
            source="사람이 빽이 있어야지. 어디 낙하산 꽂아 줄 사람 없나...",
            translation={
                LangCode.ENG: "A person's gotta have connections. Isn't there anyone who can pull some strings and place me in a position..."
            },
        ),
        Example(
            source="소 잃고 외양간 고치지 말고, 지금부터 보안 작업을 꼼꼼히 해두자.",
            translation={
                LangCode.ENG: "Let's not wait to lock the stable door after the horse has bolted. We should meticulously implement our security measures starting now."
            },
        ),
        Example(
            source="이미 엎질러진 물이야. 포기해.",
            translation={
                LangCode.ENG: "It's no use crying over spilled milk. Just give up."
            },
        ),
    ],
    Categories.WORDPLAY_PUN: [
        Example(
            source="저 대학원생이 머리는 휑 하지만 머리는 좋아서 교수도 될 거 같아.",
            translation={
                LangCode.ENG: "His head's getting bare up there, but his head's got smarts to spare; he could be a professor, I swear. (머리라는 단어의 언어유희를 제대로 살리지 못한 경우 점수를 매우 낮게 줄 것)"
            },
        ),
        Example(
            source="눈에 눈이 들어가면 눈물일까, 눈물일까?",
            translation={
                LangCode.ENG: "If snow gets in your eye, are the resulting drops tears or melted snow?"
            },
        ),
        Example(
            source="전 부드러운 남자입니다. 아뇨, 전부 드러운 남자 뿐이라고요.",
            translation={
                LangCode.ENG: "I'm a tender man. Oh wait, no, I meant all men are pretenders."
            },
        ),
        Example(
            source="난 눈이 높아서 그런지, 눈 맞는 일이 없더라.",
            translation={
                LangCode.ENG: "Maybe it's because my standards are high, but I rarely meet someone I click with."
            },
        ),
        Example(
            source="훈훈한 훈남 훈녀네.",
            translation={LangCode.ENG: "What a lovely guy and lovely girl."},
        ),
        Example(
            source="은근히 은근한 매력이 있네.",
            translation={LangCode.ENG: "It has a subtle, subtle charm."},
        ),
    ],
    Categories.CULTURE: [
        Example(
            source="이래서 눈치 빠른 아이는 싫다니까...",
            translation={
                LangCode.ENG: "This is why kids who catch on too quickly can be annoying..."
            },
        ),
        Example(
            source="한개만 주면 정 없으니까 여러개 주는게 한국인이죠.",
            translation={
                LangCode.ENG: "It's typical for Koreans to give several items instead of just one, as giving only one feels a bit ungenerous."
            },
        ),
        Example(
            source="나한테 악감정 있니? 그럼 말을 해. 한 서린 눈빛 하지 말고.",
            translation={
                LangCode.ENG: "Got a problem with me? Then spit it out. Don't just give me that look full of resentment."
            },
        ),
        Example(
            source="빨간 날이라서 회사 안가도 된다!",
            translation={
                LangCode.ENG: "Since it's a public holiday today, no work for me!"
            },
        ),
        Example(
            source="오늘 수능이라서 그런지 도로가 한산하네.",
            translation={
                LangCode.ENG: "Maybe it's because today is the Suneung (CSAT), but the roads are really clear."
            },
        ),
        Example(
            source="빨리빨리 좀 해. 이러다 해 지겠다.",
            translation={
                LangCode.ENG: "Hurry up, chop chop! At this rate, the sun will set."
            },
        ),
    ],
    Categories.SLANG: [
        Example(
            source="미친 이거 존나 미쳤다, 개 쩔잖아!",
            translation={
                LangCode.ENG: "Holy shit, this is fucking insane! This is dope!"
            },
        ),
        Example(
            source="좀 똘끼 있는 애가 노잼 드립쳐서 갑분싸된 상황이야.",
            translation={
                LangCode.ENG: "So, this kinda eccentric person told a really lame joke, and it just completely killed the mood."
            },
        ),
        Example(
            source="아 진짜 더럽게 귀찮게 하네... 좀 닥쳐 볼래?",
            translation={
                LangCode.ENG: "Seriously, you're pissing me off... Just shut your mouth?"
            },
        ),
        Example(
            source="진짜 좇같은 상황이네. 존나 빡친다.",
            translation={
                LangCode.ENG: "This is total bullshit. Fucking furious right now."
            },
        ),
    ],
    Categories.LITERATURE: [
        Example(
            source="진짜 홍길동마냥 막 여기저기서 나오네.",
            translation={
                LangCode.ENG: "Wow, they're really popping up all over the place, just like Hong Gildong."
            },
        ),
        Example(
            source="그 사람의 미소에 봄이 내려앉았다.",
            translation={LangCode.ENG: "Spring seemed to settle upon their smile."},
        ),
        Example(
            source="아이고, 누렇다 못해 누리끼리 해졌네.",
            translation={
                LangCode.ENG: "Oh dear, it's not just yellow, it's turned all dingy."
            },
        ),
        Example(
            source="그 시인의 글에는 청산유수와 같은 맑고 흐르는 아름다움이 담겨 있었다.",
            translation={
                LangCode.ENG: "There was a lucid and flowing beauty in the poet's work, like effortlessly running water (Cheongsanyusu).",
            },
        ),
        Example(
            source="그들의 동맹은 견원지간처럼 시작했지만, 결국 공동의 목표를 위해 손을 잡았다.",
            translation={
                LangCode.ENG: "Their alliance started off like cats and dogs (Gyeonwonjigan), but they eventually joined forces for a common goal.",
            },
        ),
    ],
}
