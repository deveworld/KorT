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


class GeneratedExample(BaseModel):
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
    generated_examples: list[GeneratedExample]


# TODO: Hardcoded-dict is workaround for now. Will be replaced with other format as like jsonl.
EVAL_DATA: dict[LangCode, dict[Categories, list[Example]]] = {}

EVAL_DATA[LangCode.ENG] = {
    Categories.IDIOM_PROVERB: [
        Example(
            source="You're barking up the wrong tree.",
            translation={LangCode.KOR: "너 완전 헛다리 짚고 있는 거야."},
        ),
        Example(
            source="It's raining cats and dogs.",
            translation={LangCode.KOR: "비가 억수같이 내린다."},
        ),
        Example(
            source="Don't put all your eggs in one basket.",
            translation={LangCode.KOR: "한 우물만 파지 마라."},
        ),
        Example(
            source="Yeah, when pigs fly. You know.",
            translation={LangCode.KOR: "아니, 절대로. 너도 알잖아."},
        ),
        Example(
            source="Break a leg for your presentation tonight!",
            translation={LangCode.KOR: "오늘밤에 발표 잘 해!"},
        ),
        Example(
            source="What a pencil fest! Typical engineering school.",
            translation={LangCode.KOR: "완전 고추밭이네! 전형적인 공대야."},
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
            source="I'm reading a book about anti-gravity. It's impossible to put down!",
            translation={
                LangCode.KOR: "무중력에 관한 책을 읽고 있는데, 못 내려놓고 끝까지 읽게 돼!"
            },
        ),
        Example(
            source="A boiled egg every morning is hard to beat.",
            translation={LangCode.KOR: "매일 아침 삶은 계란만한 게 없다."},
        ),
        Example(
            source="I used to be a baker, but I couldn't make enough dough.",
            translation={LangCode.KOR: "예전에 제빵사였는데, 벌이가 영 시원찮았어요."},
        ),
        Example(
            source="Need an ark? I Noah guy.",
            translation={
                LangCode.KOR: "방주 필요해? 나 아는 노아라고 있어.",
            },
        ),
        Example(
            source="Atheism is a non-prophet organization.",
            translation={
                LangCode.KOR: "무신론은 선지자가 없는 조직이다. / 무신론은 비영리 단체다."
            },
        ),
    ],
    Categories.CULTURE: [
        Example(
            source="He's a real Scrooge.",
            translation={LangCode.KOR: "그는 정말 구두쇠야."},
        ),
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
            translation={LangCode.KOR: "사장님한테 '네 다음 틀딱'이라고 하고 싶어."},
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
            translation={LangCode.KOR: "이것은 진퇴양난의 상황이다."},
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
            source="끌 모아 태산이라는 말이 있듯이, 나도 매일 돈을 모으고 있어.",
            translation={
                LangCode.ENG: "Just like the saying 'Little drops of water make a mighty ocean,' I am also saving money every day."
            },
        ),
        Example(
            source="소 잃고 외양간 고치지 말고, 지금부터 보안 작업을 꼼꼼히 해두자.",
            translation={
                LangCode.ENG: "Let's not wait to lock the stable door after the horse has bolted. We should meticulously implement our security measures starting now."
            },
        ),
        Example(
            source="빈대 잡으려다 초가삼간 다 태운 격이지 뭐..",
            translation={
                LangCode.ENG: "It's like using a sledgehammer to crack a nut.."
            },
        ),
        Example(
            source="요즘 일 구하기가 하늘에 별 따기야.",
            translation={
                LangCode.ENG: "Getting a job nowadays feels like mission impossible."
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
            source="이 다음에 이 닦고 자자.",
            translation={
                LangCode.ENG: "Let's brush our teeth after this, then go to bed."
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
            source="마그마는 내가 막으마. 어서 도망가거라.",
            translation={LangCode.ENG: "Magma? Ma' gonna stop it. Hurry and run."},
        ),
        Example(
            source="수박을 먹을 수밖에.",
            translation={
                LangCode.ENG: "Well, I guess I have no choice but to eat the watermelon."
            },
        ),
        Example(
            source="세상에서 제일 적은 금은 바로, '조금'입니다.",
            translation={
                LangCode.ENG: "The smallest amount of gold in the world is, 'a little bit'."
            },
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
            source="오늘 회식 있습니다.",
            translation={LangCode.ENG: "There's a company dinner today."},
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
    ],
    Categories.SLANG: [
        Example(
            source="미친 이거 존나 미쳤다, 개 쩔잖아!",
            translation={
                LangCode.ENG: "Holy shit, this is fucking insane! This is dope!"
            },
        ),
        Example(
            source="그 사람 완전 꿀벅지야. 미쳤어!",
            translation={
                LangCode.ENG: "Damn, that person has killer thighs! It's insane!"
            },
        ),
        Example(
            source="자, 그럼 스킵하고 다음으로 넘어갑시다.",
            translation={
                LangCode.ENG: "Okay then, let's skip this and move on to the next thing."
            },
        ),
        Example(
            source="좀 똘끼 있는 애가 노잼 드립쳐서 갑분싸된 상황이야.",
            translation={
                LangCode.ENG: "So, this kinda eccentric person told a really lame joke, and it just completely killed the mood."
            },
        ),
        Example(
            source="아 진짜 더럽게 귀찮은데... 좀 닥쳐 볼래?",
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
            source="그는 충무공의 기개를 본받아 어려운 상황에서도 결코 물러서지 않았다.",
            translation={
                LangCode.ENG: "Inspired by the unwavering courage of the great admiral (Chungmugong), he refused to yield even when facing adversity.",
            },
        ),
        Example(
            source="그 시인의 글에는 청산유수와 같은 맑고 흐르는 아름다움이 담겨 있었다.",
            translation={
                LangCode.ENG: "There was a lucid and flowing beauty in the poet's work, like effortlessly running water (Cheongsanyusu).",
            },
        ),
        Example(
            source="현대 사회에서도 심청이처럼 효를 실천하는 사람들의 이야기가 종종 뉴스에 나온다.",
            translation={
                LangCode.ENG: "Even today, news outlets sometimes feature stories of people showing extraordinary devotion to their parents, reminiscent of the legendary Sim Cheong.",
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
