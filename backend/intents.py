import random

import random

def _pick_response(intent: dict, hint: str | None = None) -> dict:
    responses = intent["responses"]

    if responses and isinstance(responses[0], str):
        chosen = random.choice(responses)
        followup = intent.get("followup")
        return {
            "text": chosen,
            "followup_pergunta": followup if followup else None,
            "tag": intent["tag"],
            "imagem": None,
            "followup_data": {
                "pergunta": followup,
                "proxima_tag": None,
                "proximo_hint": None
            } if followup else None
        }

    matched = None

    if hint:
        hint_norm = hint.lower().strip()
        best_score = -1
        best_response = None

        for r in responses:
            hints = r.get("match_hints", [])
            score = 0

            for h in hints:
                h_norm = h.lower().strip()
                if h_norm and h_norm in hint_norm:
                    score = max(score, len(h_norm))

            if score > best_score:
                best_score = score
                best_response = r

        if best_score > 0:
            matched = best_response

    if not matched:
        matched = random.choice(responses)

    followup_data = matched.get("followup")
    followup_pergunta = followup_data.get("pergunta") if followup_data else None

    return {
        "text": matched["text"],
        "followup_pergunta": followup_pergunta,
        "tag": intent["tag"],
        "imagem": matched.get("imagem"),
        "followup_data": followup_data
    }


def get_response_for_tag(tag: str, hint: str | None = None) -> dict:
    for intent in INTENTS:
        if intent["tag"] == tag:
            return _pick_response(intent, hint)
    return _pick_response(next(i for i in INTENTS if i["tag"] == "default"))


def get_random_response(tag: str) -> dict:
    return get_response_for_tag(tag, hint=None)


INTENTS = [

    # -------------------------------------------------------------------------
    # SAUDACAO E DESPEDIDA
    # -------------------------------------------------------------------------
    {
        "tag": "saudacao",
        "patterns": [
            "oi", "ola", "olá", "hey", "e ai", "e aí",
            "bom dia", "boa tarde", "boa noite", "tudo bem"
        ],
        "responses": [
            {
                "match_hints": [],
                "text": "Oi! Que bom te ver por aqui. O universo é enorme e cheio de mistérios.\n\n",
                "followup": {
                    "pergunta": "Por onde você quer começar? Posso falar sobre buracos negros, planetas, estrelas, galáxias ou até vida extraterrestre.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": [],
                "text": "Olá! Sou a Stella, sua guia pelo cosmos.\n\n",
                "followup": {
                    "pergunta": "Tem algum canto do universo que sempre te deixou curioso?",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": [],
                "text": "Hey! Tô aqui prontinha pra embarcar numa viagem pelo espaço com você.\n\n",
                "followup": {
                    "pergunta": "O que você quer descobrir hoje?",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },
    {
        "tag": "despedida",
        "patterns": [
            "tchau", "ate mais", "até mais", "ate logo", "até logo",
            "adeus", "bye", "flw", "valeu", "obrigado", "obrigada"
        ],
        "responses": [
            {
                "match_hints": [],
                "text": "Até logo! Toda vez que você olhar para o céu à noite, lembra: está vendo o passado do universo.",
                "followup": None
            },
            {
                "match_hints": [],
                "text": "Tchau! Foi incrível explorar o cosmos com você. O universo vai continuar aqui esperando pelas suas perguntas.",
                "followup": None
            },
            {
                "match_hints": [],
                "text": "Até mais! Você é literalmente feito de poeira de estrelas. Pensa nisso hoje à noite.",
                "followup": None
            }
        ]
    },

    # -------------------------------------------------------------------------
    # BURACOS NEGROS
    # -------------------------------------------------------------------------
    {
        "tag": "buraco_negro",
        "patterns": [
            "buraco negro", "buracos negros", "singularidade",
            "horizonte de eventos", "hawking", "espaguetificacao",
            "sagitario", "gravidade extrema", "radiacao hawking", "buraco negro central", "sagitario a*", "centro",
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Um buraco negro é uma região do espaço onde a gravidade é tão intensa que nada consegue escapar, nem mesmo a luz.\n\n"
                    "Não é um buraco no sentido literal, mas um ponto onde a matéria foi esmagada a densidades absurdas.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber como um buraco negro se forma?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "como se forma"
                }
            },
            {
                "match_hints": ["perto de um buraco negro", "aproximo a um buraco negro", "ao redor de um buraco negro", "ao chegar perto de um buraco negro"],
                "text": (
                    "Perto de um buraco negro, o espaço e o tempo são distorcidos. O tempo passa mais devagar ali, um efeito previsto pela Teoria da Relatividade Geral de Einstein.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber como um buraco negro se forma?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "como se forma"
                }
            },
            {
                "match_hints": ["como se forma", "como nasce", "origem", "formacao", "forma", "surge"],
                "text": (
                    "Um buraco negro estelar se forma quando uma estrela com mais de 20 massas solares chega ao fim da vida. Ela colapsa sobre si mesma numa supernova e o núcleo é comprimido até virar uma singularidade.\n\n"
                    "Já os buracos negros supermassivos, com milhões ou bilhões de massas solares, têm origem ainda debatida pelos cientistas. A NASA acredita que podem ter se formado nos primeiros momentos do universo.\n\n"
                ),
                "followup": {
                    "pergunta": "No centro da nossa galáxia existe um desses supermassivos. Ficou curioso pra saber mais sobre ele?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "sagitario a*"
                }
            },
            {
                "match_hints": ["centro", "buraco negro central", "o que ha no centro", "o que tem no centro", "sagitario a*", "o que tem no centro da via lactea"],
                "text": (
                    "O buraco negro no centro da Via Láctea se chama Sagitário A*. Ele tem a massa de 4 milhões de sóis comprimidos numa região menor que nosso sistema solar.\n\n"
                    "Em 2022, o Event Horizon Telescope divulgou a primeira imagem real dele:"
                ),
                "imagem": ["img/sagitario-a.jpg", "img/via-lactea.jpeg"],
                "followup": {
                    "pergunta": "E se alguém caísse nele, quer descobrir o que aconteceria?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "dentro"
                }
            },
            {
                "match_hints": ["cair em um buraco negro", "caisse em um buraco negro", "entrar em um buraco negro", "dentro", "espaguetificacao"],
                "text": (
                    "Se alguém caísse em um buraco negro, passaria pelo processo de espaguetificação.\n\n"
                    "A diferença de gravidade entre a cabeça e os pés esticaria o corpo como um espaguete.\n\n"
                    "Para quem observa de fora, a pessoa pareceria congelar no horizonte de eventos e desaparecer lentamente. Para quem cai, atravessaria a fronteira sem perceber, mas seria destruído na singularidade."
                ),
                "imagem": "img/buraconegro.jpg",
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre estrelas, galáxias, planetas ou o Big Bang.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": ["engolir outro", "dois buracos negros", "fusao de buracos negros", "colisao de buracos negros", "buracos negros se unem"],
                "text": (
                    "Um buraco negro não engole o outro no sentido literal, mas os dois podem se unir formando um ainda maior.\n\n"
                    "Não existe limite teórico para o tamanho que um buraco negro pode atingir ao absorver matéria. Eles crescem conforme consomem.\n\n"
                    "Quando dois se fundem, liberam ondas gravitacionais, ondulações no tecido do espaço-tempo. Em 2015, o detector LIGO captou pela primeira vez esse fenômeno, confirmando uma previsão de Einstein de um século antes.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber mais sobre buracos negros ou gostaria de explorar outro tema?",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # CONTELAÇÕES
    # -------------------------------------------------------------------------
    {
        "tag": "constelacoes",
        "patterns": [
            "constelacao", "constelação", "constelacoes", "constelações", "constelacao de orion", "cinturao de orion", "cinturão de órion", "tres marias", "três marias", "alnitak", "alnilam", "mintaka", "betelgeuse", "cruzeiro do sul", "bandeira brasileira", "paises", "cruzeiro do sul na bandeira", "constelação do cruzeiro do sul na bandeira"
        ],
        "responses": [
            {
                "match_hints": ["constelacao", "constelação", "constelacoes", "constelações"],
                "text": (
                    "Constelações são grupos de estrelas que, vistas da Terra, formam desenhos no céu, mesmo estando a distâncias diferentes.\n\n"
                    "Existem 88 constelações oficiais que dividem todo o céu, como se fosse um mapa. Toda estrela que vemos faz parte de alguma delas.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber sobre o Cruzeiro do Sul, uma das mais famosas do nosso céu?",
                    "proxima_tag": "constelacoes",
                    "proximo_hint": "cruzeiro do sul"
                }
            },
            {
                "match_hints": ["cruzeiro do sul", "onde fica o cruzeiro do sul", "constelacao do cruzeiro do sul", "constelação do cruzeiro do sul", "onde esta o cruzeiro do sul", "onde está o cruzeiro do sul"],
                "text": (
                    "O Cruzeiro do Sul é a menor, porém mais famosa constelação da Via Láctea, facilmente visível no Hemisfério Sul.\n\n"
                    "Ele é usado há séculos para orientação, ajudando a localizar o sul no céu."
                ),
                "imagem": "img/cruzeiro-sul.jpg",
                "followup": {
                    "pergunta": "Curiosamente, o Cruzeiro do Sul não está só no céu. Ele também aparece na bandeira do Brasil. Quer entender isso?",
                    "proxima_tag": "constelacoes",
                    "proximo_hint": "bandeira brasileira"
                }
            },
            {
                "match_hints": ["bandeira", "cruzeiro do sul na bandeira", "cruzeiro do sul na bandeira brasileira", "cruzeiro do sul simbolo", "bandeira brasileira", "bandeira do brasil", "cruzeiro do sul na bandeira", "constelação do cruzeiro do sul na bandeira"],
                "text": (
                    "A constelação do Cruzeiro do Sul é o elemento central do círculo azul na bandeira brasileira, representando o céu do Rio de Janeiro em 19 de novembro de 1889 e simbolizando a localização austral do país.\n\n"
                    "Além do Brasil, outros países também têm o Cruzeiro do Sul em suas bandeiras, como Austrália, Nova Zelândia e Papua Nova Guiné, simbolizando sua posição no Hemisfério Sul."
                ),
                "imagem": ["img/bandeira.png", "img/bandeiras.png"],
                "followup": {
                    "pergunta": "Quer saber sobre as Três Marias na constelação de Órion, uma das mais famosas do nosso céu?",
                    "proxima_tag": "constelacoes",
                    "proximo_hint": "O Cinturão de Órion"
                }
            },
            {
                "match_hints": ["cinturao de orion", "cinturão de órion", "tres marias", "três marias", "alnitak", "alnilam", "mintaka"],
                "text": (
                    "O Cinturão de Órion, popularmente conhecido como Três Marias, é formado por três estrelas alinhadas na constelação de Órion.\n\n"
                    "Seus nomes são Alnitak, Alnilam e Mintaka. Elas estão a diferentes distâncias da Terra, variando de cerca de 800 a 2.000 anos-luz, e estão entre as estrelas mais brilhantes do céu noturno.\n\n"
                    "Embora pareçam pontos únicos no céu, Alnitak é um sistema triplo de estrelas, Alnilam é uma supergigante azul e Mintaka é um sistema quádruplo."
                ),
                "imagem": "img/cinturao-orion.jpg",
                "followup": {
                    "pergunta": "Quer saber mais sobre a Constelação de Órion e o que existe ao redor das Três Marias?",
                    "proxima_tag": "constelacoes",
                    "proximo_hint": "orion"
                }
            },
            {
                "match_hints": ["orion", "constelacao", "constelação", "constelacao de orion", "ao redor", "nebulosa de orion"],
                "text": (
                    "A Constelação de Órion é uma das mais reconhecíveis do céu e visível em quase todo o planeta.\n\n"
                    "Abaixo do cinturão fica a Nebulosa de Órion, uma das regiões de formação estelar mais ativas próximas da Terra, a cerca de 1.344 anos-luz de distância.\n\n"
                    "Duas das estrelas mais famosas de Órion são Betelgeuse, uma supergigante vermelha que pode explodir em supernova em qualquer momento em escala astronômica, e Rigel, uma das estrelas mais luminosas do céu noturno."
                ),
                "imagem": "img/orion.png",
                "followup": {
                    "pergunta": "Bora descobrir mais sobre a Betelgeuse e por que os astrônomos acompanham ela de perto?",
                    "proxima_tag": "constelacoes",
                    "proximo_hint": "betelgeuse"
                }
            },
            {
                "match_hints": ["betelgeuse", "supergigante", "vai explodir", "supernova"],
                "text": (
                    "Betelgeuse é uma supergigante vermelha localizada no ombro de Órion, a cerca de 700 anos-luz da Terra.\n\n"
                    "Ela é tão grande que, se estivesse no lugar do Sol, se estenderia até além da órbita de Júpiter\n\n"
                    "Em 2019, ela escureceu de forma incomum, o que gerou especulação sobre uma supernova iminente. Os astrônomos concluíram que foi uma ejeção de massa, mas Betelgeuse está mesmo no fim da vida e vai explodir em supernova, provavelmente nos próximos 100 mil anos.\n\n"
                ),
                "followup": {
                    "pergunta": "Tá a fim de explorar outros temas? Posso falar sobre constelações, signos ou qualquer tema do cosmos.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SIGNOS
    # -------------------------------------------------------------------------
    {
        "tag": "signos",
        "patterns": [
            "signos", "signo", "zodiaco", "zodíaco", "astrologia",
            "constelacoes do zodiaco", "constelações do zodíaco",
            "signo e astronomia", "astrologia e astronomia", "precessao dos equinocios", "precessão dos equinócios"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "signos", "zodiaco"],
                "text": (
                    "Os signos do zodíaco têm origem na astronomia antiga. As civilizações observaram que o Sol parece passar por diferentes grupos de estrelas ao longo do ano.\n\n"
                    "Esses grupos foram divididos em 12 constelações, que formam o zodíaco. A ideia era que a posição do Sol em relação a essas constelações no momento do nascimento de alguém influenciaria sua personalidade.\n\n"
                    "A astronomia e a astrologia caminharam juntas por séculos antes de se separarem como ciência e crença."
                ),
                "imagem": "img/constelacoes-zodiaco.jpg",
                "followup": {
                    "pergunta": "Quer saber a diferença entre astrologia e astronomia?",
                    "proxima_tag": "signos",
                    "proximo_hint": "diferenca"
                }
            },
            {
                "match_hints": ["diferenca", "diferença", "astronomia", "ciencia", "real", "verdade"],
                "text": (
                    "A astronomia e a astrologia divergem em um ponto fundamental, a posição do Sol nas constelações mudou desde que o zodíaco foi criado há 2.500 anos.\n\n"
                    "Isso acontece por causa da precessão dos equinócios, uma oscilação lenta do eixo da Terra. Hoje o Sol está numa constelação diferente da que a astrologia indica para cada signo.\n\n"
                    "Além disso, a astrologia usa 12 constelações, mas o Sol na verdade passa por 13, incluindo Ofiúco, que a astrologia tradicional simplesmente ignora."
                ),
                "imagem": "img/ofiúco.jpg",
                "followup": {
                    "pergunta": "Quer saber o que é a precessão dos equinócios e como ela afeta nossa visão do céu?",
                    "proxima_tag": "signos",
                    "proximo_hint": "precessao"
                }
            },
            {
                "match_hints": ["precessao", "precessão", "equinocio", "equinócio", "eixo da terra", "oscilacao"],
                "text": (
                    "A precessão dos equinócios é um movimento lento do eixo da Terra, parecido com o bambolear de um pião que está perdendo velocidade.\n\n"
                    "Um ciclo completo leva cerca de 26.000 anos. Por causa disso, a estrela que apontamos como norte muda ao longo dos milênios. Hoje é Polaris, mas daqui a 12.000 anos será Vega.\n\n"
                    "Os antigos egípcios e gregos já observavam esse fenômeno, e foi justamente essa mudança gradual que desconectou os signos astrológicos das constelações reais ao longo dos séculos."
                ),
                "imagem": "img/precessao.png",
                "followup": {
                    "pergunta": "Quer explorar as constelações de forma mais ampla?",
                    "proxima_tag": "constelacoes",
                    "proximo_hint": "constelacao"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # ESTRELAS
    # -------------------------------------------------------------------------
    {
        "tag": "estrelas",
        "patterns": [
            "estrela", "estrelas", "ciclo estelar", "fusão nuclear",
            "fusao nuclear", "vida de uma estrela", "como nasce uma estrela",
            "morte de uma estrela", "ana amarela", "gigante vermelha", "próxima centauri", "proxima centauri", "estrela mais proxima", "estrela mais próxima", "quantas estrelas", "escuro", "espaco escuro", "por que o espaço é escuro", "cores das estrelas", "cor", "estrela mais proxima da terra", "estrela mais próxima da terra", "feito de estrelas", "por que o espaco é escuro", "estrelas", "estrelas sao coloridas", "por que as estrelas são coloridas", "como morre", "ciclo de vida", "ciclo de vida de uma estrela", "tipos de estrelas", "tipos", "maior estrela", "menor estrela", "ana vermelha", "hipergigante", "ana branca", "Carl Sagan"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Estrelas são esferas de gás, principalmente hidrogênio e hélio, que brilham por fusão nuclear.\n\n"
                    "No núcleo, a temperatura passa de 15 milhões de graus Celsius."
                ),
                "imagem": "img/estrelas.jpg",
                "followup": {
                    "pergunta": "Quer saber como uma estrela nasce?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "como nasce"
                }
            },
            {
                "match_hints": [
                    "quantas estrelas", "numero de estrelas", "quantidade", "universo observavel",
                ],
                "text": (
                    "Estima-se que existam mais de 10 sextilhões (10^22) de estrelas no universo observável.\n\n"
                    "A NASA calcula que existem cerca de 200 a 400 bilhões de estrelas só na Via Láctea. No universo inteiro, há mais estrelas do que grãos de areia em todas as praias da Terra.\n\n"
                    "Um dos aglomerados mais densos e compactos já observados é o Messier 69, localizado próximo ao centro da Via Láctea. Ele contém cerca de 1 milhão de estrelas em uma região com apenas 50 anos-luz de diâmetro."
                ),
                "imagem": "img/Messier_69.jpg",
                "followup": {
                    "pergunta": "Mesmo com esse número absurdo, cada estrela pode ser bem diferente. Quer descobrir os tipos de estrelas?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "tipos"
                }
            },
            {
                "match_hints": ["como nasce", "nasce", "nascem", "origem", "formacao", "nebulosa"],
                "text": (
                    "Estrelas nascem em nebulosas, nuvens de gás e poeira que a gravidade vai comprimindo.\n\n"
                    "Quando a pressão e a temperatura no centro ficam altas o suficiente, a fusão nuclear acende.\n\n"
                    "O Sol passou por isso há 4,6 bilhões de anos. O processo de formação pode levar de 100 mil a 1 milhão de anos.\n\n"
                ),
                "followup": {
                    "pergunta": "O ciclo de vida de uma estrela depende do seu tamanho. Gostaria de entender o ciclo completo?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "como morre"
                }
            },
            {
                "match_hints": ["como morre", "morre", "morrem", "fim", "ciclo", "destino final", "ciclo de vida", "ciclo de vida de uma estrela"],
                "text": (
                    "O destino de uma estrela depende da sua massa.\n\n"
                    "Estrelas como o Sol viram gigantes vermelhas, depois nebulosas planetárias e, por fim, anãs brancas.\n\n"
                    "Estrelas muito massivas terminam em supernova e deixam para trás uma estrela de nêutrons ou um buraco negro. O Sol ainda tem cerca de 5 bilhões de anos de vida pela frente, segundo a NASA."
                ),
                "imagem": "img/ciclo-vida-estrelas.png",
                "followup": {
                    "pergunta": "Quer saber mais sobre os tipos de estrelas, como as anãs vermelhas ou as hipergigantes?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "tipos"
                }
            },
            {
                "match_hints": ["tipos", "maior", "menor", "ana vermelha", "hipergigante", "ana branca"],
                "text": (
                    "Existe uma enorme variedade de estrelas.\n\n"
                    "Anãs vermelhas, como o Sol, são as mais comuns e as mais longevas, podendo viver trilhões de anos.\n\n"
                    "Já a Antares, uma hipergigante, tem raio 883 vezes maior que o Sol.\n\n"
                    "Anãs brancas como Sirius B são núcleos de estrelas mortas, do tamanho da Terra mas com massa comparável à do Sol.\n\n"
                    "O Sol é gigantesco em comparação com a Terra. Mas é um pequeno grão de poeira quando comparado à outras estrelas:"
                ),
                "imagem": "img/tipos-estrelas.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre supernovas, o maior espetáculo do universo?",
                    "proxima_tag": "supernova",
                    "proximo_hint": "o que e"
                }
            },
            {
                "match_hints": ["proxima centauri", "próxima centauri", "estrela mais proxima", "estrela mais próxima", "vizinha do sol"],
                "text": (
                    "Próxima Centauri é a estrela mais próxima da Terra, localizada a cerca de 4,24 anos-luz de distância.\n\n"
                    "Ela é uma anã vermelha, menor e mais fria que o Sol, mas ainda assim muito ativa, com erupções frequentes.\n\n"
                    "Ao seu redor orbita pelo menos um planeta, Próxima Centauri b, que está na chamada zona habitável, onde poderia existir água líquida.\n\n"
                ),
                "followup": {
                    "pergunta": "Mesmo sendo a estrela mais próxima, chegar até ela ainda é um grande desafio. Quer entender por quê?",
                    "proxima_tag": "ano_luz",
                    "proximo_hint": "limite da luz"
                }
            },
            {
                "match_hints": ["stephenson 2-18", "maior estrela", "maior estrela do universo", "estrela mais enorme"
                ],
                "text": (
                    "Stephenson 2-18 é considerada uma das maiores estrelas já descobertas.\n\n"
                    "Ela é uma hipergigante vermelha com um raio cerca de 2.100 vezes maior que o do Sol.\n\n"
                    "Se estivesse no lugar do Sol, sua superfície ultrapassaria a órbita de Saturno.\n\n"
                    "Mesmo sendo tão gigantesca, é uma estrela instável e está nos estágios finais da sua vida."
                ),
                "imagem": "img/Stephenson_2-18.png",
                "followup": {
                    "pergunta": "Quer conhecer a estrela mais próxima da Terra?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "proxima centauri"
                }
            },
            {
                "match_hints": ["espaco escuro", "por que o espaco e escuro", "espaco escuro perto do sol", "espaco e escuro mesmo com o sol"],
                "text": (
                    "O universo é escuro porque não é eterno nem infinito. Com cerca de 13,8 bilhões de anos, a luz de estrelas muito distantes ainda não chegou até nós.\n\n"
                    "Mesmo próximo do Sol, o espaço é escuro porque não há atmosfera, e a luz solar não ilumina o vazio ao redor.\n\n"
                    "A luz azul que vemos na Terra durante o dia é resultado da difusão dos raios solares nas moléculas do ar. Sem esse meio, a luz viaja em linha reta, sem se espalhar.\n\n"

                ),
                "followup": {
                    "pergunta": "Quer entender por que as estrelas têm cores diferentes?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "estrelas sao coloridas"
                }
            },
            {
                "match_hints": ["coloridas", "estrelas sao coloridas", "por que as estrelas são coloridas", "cores diferentes", "cor", "cores"],
                "text": (
                    "A cor de uma estrela revela sua temperatura superficial.\n\n"
                    "• Estrelas vermelhas são as mais frias, com cerca de 3.000°C.\n"
                    "• Estrelas amarelas como o Sol têm cerca de 5.500°C.\n"
                    "• Estrelas azuis são as mais quentes, passando de 30.000°C.\n\n"
                    "A composição química também influencia. Diferentes elementos emitem luz em comprimentos de onda específicos, assim os astrônomos conseguem identificar do que cada estrela é feita."
                ),
                "imagem": "img/cores-das-estrelas.jpg",
                "followup": {
                    "pergunta": "Quer entender por que somos feitos de poeira de estrelas?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "somos feitos de estrelas"
                }
            },
                        {
                "match_hints": ["poeira estelar", "somos feitos de estrelas", "elementos das estrelas", "carl sagan", "poeira de estrelas"],
                "text": (
                    "Carl Sagan dizia que somos feitos de poeira estelar, e é literalmente verdade.\n\n"
                    "Os elementos químicos que formam nosso corpo, como carbono, nitrogênio, oxigênio e ferro, foram sintetizados no interior de estrelas bilhões de anos atrás.\n\n"
                    "Quando essas estrelas explodiram em supernovas, espalharam esses elementos pelo espaço. Eles se juntaram para formar novos sistemas solares, planetas e, eventualmente, vida. Somos o universo tentando se compreender.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender melhor as supernovas, as explosões que espalharam esses elementos pelo cosmos?",
                    "proxima_tag": "supernova",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SUPERNOVA
    # -------------------------------------------------------------------------
    {
        "tag": "supernova",
        "patterns": [
            "supernova", "supernovas", "explosão de estrela", "explosao de estrela", "estrela explode", "estrela explodindo"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Supernova é a explosão de uma estrela massiva no fim de sua vida.\n\n"
                    "Esse fenômeno libera uma energia gigantesca, dispersando elementos químicos pesados que formam novas estrelas e planetas.\n\n"
                    "O ferro no seu sangue foi forjado em uma supernova.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender como uma supernova acontece, passo a passo?",
                    "proxima_tag": "supernova",
                    "proximo_hint": "como acontece"
                }
            },
            {
                "match_hints": ["como acontece", "como ocorre", "processo", "colapsa", "combustivel"],
                "text": (
                    "Quando uma estrela massiva esgota o hidrogênio no núcleo, começa a fundir elementos mais pesados.\n\n"
                    "Quando chega ao ferro, a fusão deixa de gerar energia e o núcleo colapsa em menos de um segundo.\n\n"
                    "A onda de choque resultante explode as camadas externas com energia absurda. Em alguns casos, a explosão libera mais energia do que o Sol vai emitir em toda a sua vida.\n\n"
                ),
                "followup": {
                    "pergunta": "Ficou interessado em saber o que sobra depois de uma supernova?",
                    "proxima_tag": "supernova",
                    "proximo_hint": "sobra"
                }
            },
            {
                "match_hints": ["sobra", "sobra", "restos", "estrela de neutrons"],
                "text": (
                    "Depois da explosão, o que sobra depende da massa do núcleo.\n\n"
                    "Se o núcleo tiver entre 1,4 e 3 massas solares, vira uma estrela de nêutrons, incrivelmente densa.\n\n"
                    "Se for maior, o colapso não para e forma um buraco negro. A Nebulosa do Caranguejo, observada em 1054, é o resquício de uma supernova ainda visível hoje."
                ),
                "imagem": "img/nebulosa-caranguejo.jpg",
                "followup": {
                    "pergunta": "Além disso, uma supernova pode formar uma estrela de nêutrons, bora descobrir mais sobre?",
                    "proxima_tag": "estrela_neutrons",
                    "proximo_hint": "conceito"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # ESTRELAS DE NÊUTRONS
    # -------------------------------------------------------------------------
    {
        "tag": "estrela_neutrons",
        "patterns": [
            "estrela de neutrons", "estrela de nêutrons", "estrela de neutron", "neutron", "nêutrons", "colisão de estrelas de nêutrons", "choque de estrelas de nêutrons", "kilonova"],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Uma estrela de nêutrons é uma estrela extremamente densa, resultado do colapso de uma estrela massiva.\n\n"
                    "Elas têm a massa do Sol comprimida em apenas 20 km de diâmetro.\n\n"
                    "Uma colher de chá do material delas pesaria cerca de 10 milhões de toneladas. Isso acontece porque a gravidade do colapso é tão intensa que esmaga prótons e elétrons juntos, formando nêutrons.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber o que acontece quando dua estrelas de nêutrons colidem?",
                    "proxima_tag": "estrela_neutrons",
                    "proximo_hint": "colisão"
                }
            },
            {
                "match_hints": ["colisao", "colisão", "fusao", "fusão", "duas estrelas", "kilonova", "kilonova", "onda gravitacional"],
                "text": (
                    "Quando duas estrelas de nêutrons orbitam uma à outra, elas vão se aproximando lentamente ao longo de milhões de anos.\n\n"
                    "Quando finalmente colidem, liberam uma quantidade enorme de energia em ondas gravitacionais, ondulações no próprio tecido do espaço-tempo. Em 2017, o detector LIGO captou pela primeira vez esse evento, chamado kilonova.\n\n"
                    "Essa colisão também forja elementos pesados como ouro, platina e urânio. O ouro da sua aliança ou do seu celular provavelmente nasceu numa colisão como essa, bilhões de anos atrás."
                ),
                "imagem": "img/kilonova.jpg",
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre buracos negros, galáxias ou o Big Bang.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # NEBULOSAS
    # -------------------------------------------------------------------------
    {
        "tag": "nebulosa",
        "patterns": [
            "nebulosa", "nebulosas", "o que e nebulosa", "o que é nebulosa",
            "nuvem espacial", "nuvem de gas", "nuvem de gás",
            "orion nebulosa", "nebulosa de orion", "nebulosa de órion",
            "nebulosa colorida", "formacao de estrelas", "formação de estrelas", "hélix", "nebulosa mais proxima da terra", "tipos", "tipos de nebulosa"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "o que e nebulosa", "defin", "conceito", "explica", "nebulosa", "berçário"],
                "text": (
                    "Uma nebulosa é uma grande nuvem de gás e poeira no espaço. Elas podem ter formas e cores diferentes, dependendo dos elementos presentes e da luz das estrelas ao redor.\n\n"
                    "Muitas delas são chamadas de berçários estelares, pois é onde novas estrelas começam a se formar.\n\n"
                    "Algumas são densas e escuras, enquanto outras brilham intensamente, criando algumas das imagens mais impressionantes do universo."
                ),
                "imagem": ["img/nebulosa-helix.jpg", "img/nebulosa-borboleta.jpg"],
                "followup": {
                    "pergunta": "Tem uma nebulosa famosa bem perto de nós. Quer conhecer?",
                    "proxima_tag": "nebulosa",
                    "proximo_hint": "orion"
                }
            },
            {
                "match_hints": ["o que e", "o que é", "orion", "órion", "nebulosa de orion", "nebulosa de órion"],
                "text": (
                    "A Nebulosa de Órion é uma das mais famosas e fica na constelação de Órion, localizada na nossa galáxia. Ela está situada no mesmo braço espiral que o sistema solar.\n\n"
                    "Ela é um dos berçários estelares mais próximos da Terra e pode até ser vista a olho nu em noites escuras.\n\n"
                    "Ali, novas estrelas estão se formando ativamente."
                ),
                "imagem": "img/Orion_Nebula.jpg",
                "followup": {
                    "pergunta": "Nem todas as nebulosas formam estrelas. Posso te mostrar outro tipo?",
                    "proxima_tag": "nebulosa",
                    "proximo_hint": "tipos"
                }
            },
            {
                "match_hints": ["quais", "tipos", "tipos de nebulosa", "diferentes", "quais tipos"],
                "text": (
                    "Existem diferentes tipos de nebulosas.\n\n"
                    "Algumas são regiões de nascimento de estrelas, outras são restos de explosões de supernovas, e também existem as chamadas nebulosas planetárias, formadas quando estrelas como o Sol chegam ao fim da vida.\n\n"
                    "Cada tipo mostra uma fase diferente da vida das estrelas."
                ),
                "imagem": "img/cassiopeia-a.jpg",
                "followup": {
                    "pergunta": "Bora descobrir qual é a nebulosa mais proxima da terra?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "morte"
                }
            },
            {
                "match_hints": ["nebulosa mais proxima da terra", "hélix", "olho de deus", "olho de sauron"],
                "text": (
                    "A Nebulosa de Hélix (NGC 7293), também conhecida como \"Olho de Deus\" ou \"Olho de Sauron\", é uma nebulosa planetária localizada na constelação de Hélix.\n\n"
                    "Ela é formada por uma estrela que explodiu como supernova e deixou para trás uma camada de gás e poeira que se expande no espaço."
                ),
                "imagem": "img/nebulosa-helix.jpg",
                "followup": {
                    "pergunta": "Agora que sabemos sobre nebulosas, vamos descobrir mais sobre estrelas?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "formacao"
                }
            }
        ]
    },
    
    # -------------------------------------------------------------------------
    # GALAXIAS
    # -------------------------------------------------------------------------
    {
        "tag": "galaxias",
        "patterns": [
            "galaxia", "galáxia", "galaxias", "galáxias", "via lactea",
            "via láctea", "andromeda", "andrômeda", "grupo local",
            "aglomerado", "universo observavel", "quantas galaxias", "numero de galaxias", "formacao", "como se forma", "como se formaram","como se origina", "como se originaram", "como surgiu", "como surgiram", "tipos de galaxias", "tipos de galáxias"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "tipos", "galaxia", "galáxia"],
                "text": (
                    "Galáxias são sistemas de estrelas, gás, poeira e matéria escura mantidos unidos pela gravidade.\n\n"
                    "A maioria das grandes galáxias, incluindo a Via Láctea, tem um buraco negro central supermassivo.\n\n"
                    "Existem em formas diferentes: espirais, elípticas e irregulares."
                ),
                "imagem": "img/tipos-galaxias.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre a nossa galáxia, a Via Láctea?",
                    "proxima_tag": "galaxias",
                    "proximo_hint": "via lactea"
                }
            },
            {
                "match_hints": ["formaram", "surgiram", "originaram", "como se forma", "como se formaram","como se origina", "como se originaram", "como surgiu", "como surgiram"],
                "text": (
                    "As galáxias formaram-se há mais de 10 bilhões de anos, logo após o Big Bang, através do colapso gravitacional de nuvens gigantescas de gás (hidrogênio e hélio) e matéria escura.\n\n"
                    "O crescimento ocorreu de forma hierárquica, com galáxias menores colidindo e se fundindo para formar galáxias maiores.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender o Big Bang e como tudo isso começou?",
                    "proxima_tag": "big_bang",
                    "proximo_hint": "big bang"
                }
            },
            {
                "match_hints": ["via lactea", "nossa galaxia", "nossa galáxia"],
                "text": (
                    "A Via Láctea tem entre 100 e 400 bilhões de estrelas e cerca de 100 mil anos-luz de diâmetro.\n\n"
                    "Ela é uma galáxia espiral barrada, com um núcleo em forma de barra e braços espirais saindo.\n\n"
                    "O sistema solar fica num dos braços, a cerca de 26 mil anos-luz do centro."
                ),
                "imagem": "img/via-lactea-terra.jpg",
                "followup": {
                    "pergunta": "Nossa vizinha mais próxima é a Andrômeda. Sabia que ela vai colidir com a Via Láctea?",
                    "proxima_tag": "galaxias",
                    "proximo_hint": "andromeda"
                }
            },
            {
                "match_hints": ["andromeda", "andrômeda", "colisao", "vizinha", "galaxia mais proxima", "galáxia mais próxima da terra"],
                "text": (
                    "A Galáxia de Andrômeda está a 2,5 milhões de anos-luz da Terra.\n\n"
                    "Ela se aproxima da Via Láctea a cerca de 110 km por segundo.\n\n"
                    "Daqui a 4,5 bilhões de anos, as duas vão colidir e fundir numa galáxia elíptica gigante. Mas não precisa se preocupar, o espaço entre as estrelas é tão vasto que quase nenhuma vai realmente bater em outra."
                ),
                "imagem": "img/andromeda.jpg",
                "followup": {
                    "pergunta": "Quer entender como as galáxias se formaram?",
                    "proxima_tag": "galaxias",
                    "proximo_hint": "formaram"
                }
            },
            {
                "match_hints": [
                    "quantas galaxias", "numero de galaxias", "quantidade",
                    "universo observavel", "quantas existem"
                ],
                "text": (
                    "Estima-se que existam cerca de 2 trilhões de galáxias no universo observável.\n\n"
                    "Esse número é uma projeção baseada em imagens de campo profundo feitas por telescópios como o Hubble e o James Webb, que analisam pequenas áreas do céu e extrapolam para todo o cosmos.\n\n"
                    "Estudos recentes indicam que até 90% dessas galáxias ainda não foram observadas diretamente."
                ),
                "imagem": "img/galaxias.jpg",
                "followup": {
                    "pergunta": "Quer explorar nossa galáxia, a Via Láctea?",
                    "proxima_tag": "galaxias",
                    "proximo_hint": "via lactea"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # BIG BANG
    # -------------------------------------------------------------------------
    {
        "tag": "big_bang",
        "patterns": [
            "big bang", "origem do universo", "começo do universo",
            "inicio do universo", "como tudo começou", "antes do big bang",
            "inflacao cosmica", "radiacao cosmica de fundo", "universo surgiu", "universo se expandiu", "universo se expande", "evidencias do big bang", "provas do big bang", "sinais do big bang", "multiverso", "outros universos", "universos paralelos", "existem outros universos"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "big bang", "explica", "origem", "começo", "inicio", "como tudo começou", "como surgiu"],
                "text": (
                    "A teoria do Big Bang é a explicação mais aceita para a origem do nosso Universo.\n\n"
                    "De acordo com essa hipótese, todos os elementos conhecidos e desconhecidos que estão presentes no espaço vieram de um único ponto de altíssima temperatura e densidade infinita que era chamado então de “átomo primordial”.\n\n"
                    "Há aproximadamente 13,8 bilhões de anos, esse único ponto começou a se inflar, por uma pequena fração de tempo, e “explodiu” logo na sequência, isto é, começou o seu processo de expansão, que continua até o presente."
                ),
                "imagem": "img/big-bang.png",
                "followup": {
                    "pergunta": "Tá a fim de descobrir as evidências de que o Big Bang realmente aconteceu?",
                    "proxima_tag": "big_bang",
                    "proximo_hint": "evidencias"
                }
            },
            {
                "match_hints": ["evidencias", "provas", "como sabemos", "comprovacao", "sinais", "evidências", "aconteceu", "ocorreu"],
                "text": (
                    "O Big Bang aconteceu há bilhões de anos, mas deixou sinais que ainda conseguimos observar hoje.\n\n"
                    "Um dos principais sinais é a radiação cósmica de fundo. Em 1965, cientistas detectaram um sinal de micro-ondas vindo de todas as direções do céu. Esse sinal é uma luz muito antiga, formada quando o universo era extremamente quente. \n\n"
                    "Outro sinal é a expansão do universo. As galáxias estão se afastando umas das outras. Isso mostra que o universo está aumentando de tamanho. Ao analisar esse movimento ao contrário, tudo aponta para um passado em que estava muito mais concentrado.\n\n"
                ),
                "followup": {
                    "pergunta": "Ficou interessado em saber o que havia antes do Big Bang? É uma das perguntas mais profundas da física.",
                    "proxima_tag": "big_bang",
                    "proximo_hint": "antes"
                }
            },
            {
                "match_hints": ["antes", "antes do big bang", "o que havia", "anterior"],
                "text": (
                    "O tempo surgiu junto com o universo. Perguntar o que havia antes é como perguntar o que está ao sul do Polo Sul. A resposta é: nada, pois o próprio conceito de direção (ou tempo) começa ali.\n\n"
                    "Algumas teorias propõem um universo cíclico, ou um multiverso onde nosso universo seria apenas um bolso de espuma quântica. Mas são especulações e ainda não temos como testá-las.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber sobre o destino final do universo, como tudo isso vai terminar?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "o que e"
                }
            },
            {
                "match_hints": ["multiverso", "outros universos", "universos paralelos", "existem outros universos"],
                "text": (
                    "A ideia de múltiplos universos é matematicamente plausível em algumas teorias, mas ainda não é verificável.\n\n"
                    "O astrônomo Alan Guth propôs que nosso universo poderia ser apenas uma bolha numa árvore de infinitas bolhas, cada uma com suas próprias leis físicas.\n\n"
                    "A teoria das supercordas prevê até 10 dimensões e um vasto número de universos possíveis. Por enquanto, essas ideias estão na fronteira entre a física teórica e a especulação filosófica.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer explorar o destino do nosso universo, como ele vai terminar?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "fim do universo"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # DESTINO DO UNIVERSO
    # -------------------------------------------------------------------------
    {
        "tag": "destino_universo",
        "patterns": [
            "destino do universo", "fim do universo", "como o universo vai acabar", "morte do universo", "big rip", "big freeze", "big crunch",
            "universo se expande", "o universo vai parar", "universo vai colapsar", "universo vai congelar", "universo está se expandindo", "universo vai se expandir para sempre"
        ],
        "responses": [
            {
                "match_hints": ["qual", "qual e", "como o universo vai acabar", "universo vai acabar", "fim do universo", "destino", "fim", "morte", "big freeze", "congelamento"],
                "text": (
                    "O universo está se expandindo, e cada vez mais rápido, empurrado pela energia escura.\n\n"
                    "O cenário mais aceito hoje é o Big Freeze, ou Grande Congelamento.\n\n"
                    "Daqui a trilhões de anos, as estrelas vão se apagar, os buracos negros vão evaporar e o universo vai esfriar até o zero absoluto. Tudo para. Tudo esfria.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer conhecer os outros cenários possíveis, como o Big Rip e o Big Crunch?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "cenarios"
                }
            },
            {
                "match_hints": ["cenarios", "big rip", "big crunch", "possibilidades", "outros cenarios", "destino do universo"],
                "text": (
                    "Existem três cenários principais para o destino do universo.\n\n"
                    "Big Freeze: expansão eterna até o universo esfriar completamente. É o mais provável.\n\n"
                    "Big Rip: a energia escura fica forte demais e rasga o próprio tecido do espaço, até os átomos seriam destruídos.\n\n"
                    "Big Crunch: o universo para de se expandir, reverte e colapsa sobre si mesmo. Tudo depende da natureza da energia escura, que ainda não entendemos completamente."
                ),
                "imagem": "img/fim-universo.png",
                "followup": {
                    "pergunta": "Quer entender de onde vem a energia escura que está acelerando o universo?",
                    "proxima_tag": "materia_escura",
                    "proximo_hint": "energia escura"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MATERIA ESCURA E ENERGIA ESCURA
    # -------------------------------------------------------------------------
    {
        "tag": "materia_escura",
        "patterns": [
            "materia escura", "matéria escura", "dark matter",
            "energia escura", "dark energy", "o que e materia escura", "o que é matéria escura", "o que e energia escura", "o que é energia escura", "o que é o efeito lente gravitacional", "o que é a expansão acelerada do universo"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "materia escura"],
                "text": (
                    "Matéria escura é uma substância invisível que não emite, absorve nem reflete luz.\n\n"
                    "O nome 'escura' não significa que ela é negra ou sombria. Significa que ela é invisível para nós.\n\n"
                    "Sabemos que existe porque sua gravidade afeta galáxias e aglomerados de formas que a matéria visível não explica.\n\n"
                    "Segundo a NASA, ela compõe cerca de 27% do universo. Já tudo o que conseguimos observar, como estrelas, planetas e até nós mesmos, corresponde a apenas 5%."
                ),
                "imagem": "img/materia-escura-energia-escura-universo.jpg",
                "followup": {
                    "pergunta": "Quer saber como os cientistas detectam algo que não pode ser visto?",
                    "proxima_tag": "materia_escura",
                    "proximo_hint": "como detecta"
                }
            },
            {
                "match_hints": ["como detecta", "como sabemos", "evidencia", "prova", "lente gravitacional", "galaxias girando"],
                "text": (
                    "A matéria escura é detectada pelos seus efeitos gravitacionais.\n\n"
                    "Um dos métodos é o lente gravitacional: a matéria escura dobra a luz de objetos distantes, distorcendo sua imagem.\n\n"
                    "O Hubble e o telescópio James Webb já mapearam a distribuição da matéria escura com essa técnica. Outra evidência é que galáxias giram mais rápido do que deveriam se houvesse apenas matéria visível nelas."
                ),
                "imagem": "img/lente-gravitacional.jpg",
                "followup": {
                    "pergunta": "Quer entender a energia escura, que é diferente e ainda mais misteriosa?",
                    "proxima_tag": "materia_escura",
                    "proximo_hint": "energia escura"
                }
            },
            {
                "match_hints": ["energia escura", "dark energy", "expansao", "acelerando"],
                "text": (
                    "Energia escura representa cerca de 68% do universo e está acelerando sua expansão.\n\n"
                    "Em 1998, dois grupos de cientistas descobriram essa aceleração estudando supernovas distantes. Eles ganharam o Nobel de Física em 2011 por isso.\n\n"
                    "Não sabemos o que é a energia escura. É a maior questão em aberto da cosmologia moderna.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer explorar o destino do universo impulsionado por essa energia?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SOL
    # -------------------------------------------------------------------------
    {
        "tag": "sol",
        "patterns": [
            "o sol", "o que e o sol", "o que e sol", "me explica o sol", "estrela ana amarela", "nossa estrela", "como o sol funciona", "o que e vento solar", "tempestade solar", "corona", "aurora", "aurora boreal", "morte do sol", "como morre o sol", "futuro do sol", "maior tempestade solar", "maior tempestade registrada", "evento carrington", "carrington", "erupcao solar", "erupção solar", "mancha solar", "manchas solares", "cor do sol", "se atingisse a terra", "se fosse atingir a terra", "se atingisse a terra", "se fosse atingir a terra"
        ],
        "responses": [
            {
                "match_hints": ["sol", "nossa estrela", "estrela ana amarela", "explica"],
                "text": (
                    "O Sol é uma estrela anã amarela com 4,6 bilhões de anos de idade.\n\n"
                    "Tem 109 vezes o diâmetro da Terra e contém 99,8% de toda a massa do sistema solar.\n\n"
                    "No núcleo, a temperatura chega a 15 milhões de graus Celsius. A cada segundo, ele converte 600 milhões de toneladas de hidrogênio em hélio por fusão nuclear."
                ),
                "imagem": "img/Sol.png",
                "followup": {
                    "pergunta": "Quer entender os fenômenos da superfície do Sol, como manchas solares?",
                    "proxima_tag": "sol",
                    "proximo_hint": "mancha"
                }
            },
            {
                "match_hints": ["mancha solar", "manchas solares", "mancha", "corona",],
                "text": (
                    "Manchas solares são regiões mais frias causadas por campos magnéticos intensos e podem ser maiores que a Terra."
                ),
                "imagem": "img/mancha-solar.jpg",
                "followup": {
                    "pergunta": "Quer descobrir o que são erupções solares?",
                    "proxima_tag": "sol",
                    "proximo_hint": "erupcao"
                }
            },
            {
                "match_hints": ["erupcao solar", "erupcao", "erupcoes solares", "erupções solares", "explosao solar", "explosão solar"],
                "text": (
                    "Erupções solares são explosões que acontecem na superfície do Sol. Elas liberam em minutos mais energia do que a humanidade consumiu em toda a história."
                ),
                "imagem": "img/erupcao.jpg",
                "followup": {
                    "pergunta": "Quer descobrir o que é o vento solar, e como ele afeta a Terra?",
                    "proxima_tag": "sol",
                    "proximo_hint": "vento"
                }
            },
            {
                "match_hints": ["vento solar", "vento", "corona", "aurora", "aurora boreal"],
                "text": (
                    "O vento solar é um fluxo contínuo de partículas carregadas que o Sol emite o tempo todo. Elas podem atingir velocidades de até 800 km/s e são responsáveis pelas auroras na Terra."
                ),
                "imagem": "img/aurora-boreal.jpg",
                "followup": {
                    "pergunta": "Quer entender o que são tempestades solares, as explosões mais violentas do Sol?",
                    "proxima_tag": "sol",
                    "proximo_hint": "tempestade solar"
                }
            },
            {
                "match_hints": ["tempestade solar", "tempestades solares", "ejecao de massa coronal"],
                "text": (
                    "Uma tempestade solar ocorre quando o Sol lança uma nuvem de plasma magnetizado para o espaço.\n\n"
                    "Esse plasma viaja pelo espaço e, quando atinge a Terra, pode perturbar o campo magnético do planeta, causando falhas em satélites, GPS e até blecautes em redes elétricas.\n\n"
                    "O campo magnético e a atmosfera da Terra funcionam como escudo. Sem eles, as tempestades solares seriam letais para a vida na superfície.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer conhecer a maior tempestade solar já registrada, que aconteceu em 1859?",
                    "proxima_tag": "sol",
                    "proximo_hint": "carrington"
                }
            },
            {
                "match_hints": ["carrington", "evento carrington", "maior tempestade solar", "tempestade de 1859", "maior tempestade registrada"],
                "text": (
                    "O Evento Carrington, em 1859, foi a tempestade solar mais intensa já registrada.\n\n"
                    "Ela foi tão forte que sistemas de telégrafo pegaram fogo e funcionaram mesmo desligados.\n\n"
                    "Auroras foram vistas em regiões tropicais, algo extremamente raro.\n\n"
                ),
                "followup": {
                    "pergunta": "Mesmo com tecnologia moderna, ainda estamos vulneráveis. Quer saber o que poderia acontecer hoje?",
                    "proxima_tag": "sol",
                    "proximo_hint": "hoje"
                }
            },
            {
                "match_hints": ["atingir", "atingiria", "atingisse", "fosse atingir", "se fosse atingir", "se atingisse", "se atingisse a terra", "se fosse atingir a terra"],
                "text": (
                    "Se uma tempestade solar do nível do Evento Carrington atingisse a Terra hoje, os impactos seriam muito maiores.\n\n"
                    "Satélites poderiam ser danificados, sistemas de GPS ficariam imprecisos e redes elétricas poderiam sofrer apagões em larga escala.\n\n"
                    "Missões espaciais e até voos em alta altitude também seriam afetados pela radiação.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender como a Terra se protege dessas tempestades solares com seu campo magnético?",
                    "proxima_tag": "terra",
                    "proximo_hint": "campo magnetico"
                }
            },
            {
                "match_hints": ["cor do sol", "cor", "cor vermelho", "cor laranja", "cor amarela", "por que é vermelho", "por que é laranja", "por que é amarelo", "por do sol", "nascer do sol"],
                "text": (
                    "A verdadeira cor do Sol é branco. Embora pareça amarelo ou alaranjado da Terra, essa percepção é causada pela dispersão da luz na atmosfera terrestre.\n\n"
                    "O Sol emite todas as cores visíveis simultaneamente, o que, misturadas, resultam na luz branca, cor real observada por astronautas no espaço.\n\n"
                    "Por isso o céu é azul durante o dia, mas o Sol parece alaranjado quando está no horizonte.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber mais sobre o que o Sol vai se tornar quando morrer?",
                    "proxima_tag": "sol",
                    "proximo_hint": "morte do sol"
                }
            },
            {
                "match_hints": ["morte do sol", "morrer", "como morre", "futuro do sol", "gigante vermelha", "daqui a"],
                "text": (
                    "Daqui a cerca de 5 bilhões de anos, o Sol vai esgotar o hidrogênio no núcleo.\n\n"
                    "Ele vai se expandir e virar uma gigante vermelha, engolindo Mercúrio, Vênus e provavelmente a Terra.\n\n"
                    "Depois, as camadas externas serão expulsas formando uma nebulosa planetária colorida. O que sobra é uma anã branca, um núcleo quente do tamanho da Terra que vai esfriar por trilhões de anos.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer conhecer os planetas que orbitam o Sol, começando pelo mais próximo?",
                    "proxima_tag": "mercurio",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SISTEMA SOLAR
    # -------------------------------------------------------------------------
    {
        "tag": "sistema_solar",
        "patterns": [
            "o que e sistema solar", "nosso sistema solar", "como se formou o sistema solar", "origem do sistema solar", "planetas do sistema solar", "composicao do sistema solar", "como os planetas se movem", "orbitas dos planetas", "por que os planetas orbitam o sol", "qual a composição do sistema solar", "por que planetas sao redondos", "formato dos planetas", "por que esferico", "por que planetas proximos sao rochosos", "por que planetas distantes sao gasosos", "diferenca entre planetas", "eixo de rotação dos planetas", "por que os planetas tem o eixo de rotação"
        ],
        "responses": [
            {
                "match_hints": ["o que e sistema solar", "o que e o sistema", "como se formou", "origem"],
                "text": (
                    "O Sistema Solar se formou há cerca de 4,6 bilhões de anos a partir de uma nuvem de gás e poeira chamada nebulosa solar.\n\n"
                    "A gravidade fez essa nuvem colapsar, concentrando a maior parte da massa no centro, onde se formou o Sol.\n\n"
                    "O que sobrou desse material formou um disco em rotação, de onde surgiram os planetas, luas, asteroides e cometas. Hoje, o Sistema Solar tem 8 planetas oficiais, e Plutão foi reclassificado como planeta anão em 2006."
                ),
                "imagem": "img/sistema_solar.png",
                "followup": {
                    "pergunta": "Quer saber como a massa do Sistema Solar está distribuída?",
                    "proxima_tag": "sistema_solar",
                    "proximo_hint": "composicao"
                }
            },
            {
                "match_hints": ["composicao", "massa", "composicao do sistema solar", "quantidade de materia", "composição do sistema solar"],
                "text": (
                    "O Sol contém 99.85% de toda a matéria do Sistema Solar. \n\n"
                    "Os planetas, que se condensaram a partir do mesmo disco de matéria de onde se formou o Sol, contêm apenas 0,135% da massa do sistema solar. Júpiter contém mais do dobro da matéria de todos os outros planetas juntos.\n\n"
                    "Os satélites dos planetas, cometas, asteróides, meteoróides e o meio interplanetário constituem os restantes 0,015%."
                ),
                "imagem": "img/tamanho-sol.png",
                "followup": {
                    "pergunta": "Quer saber como os planetas se movem e por que não saem de suas órbitas?",
                    "proxima_tag": "sistema_solar",
                    "proximo_hint": "orbitas"
                }
            },
            {
                "match_hints": ["orbitas", "orbita", "por que os planetas orbitam o sol", "orbitam o sol", "orbitam", "giram", "movem", "gravitacao"],
                "text": (
                    "Os planetas orbitam o Sol porque herdaram o movimento giratório da nebulosa que formou o sistema solar.\n\n"
                    "Quando essa nuvem colapsou, começou a girar cada vez mais rápido, formando um disco em rotação.\n\n"
                    "A gravidade do Sol puxa os planetas para dentro, enquanto o movimento deles os mantém seguindo em frente. Esse equilíbrio faz com que eles permaneçam em órbita há anos\n\n"
                ),
                "followup": {
                    "pergunta": "Mercúrio vive no limite desse equilíbrio. Quer saber como ele consegue sobreviver tão perto do Sol?",
                    "proxima_tag": "mercurio", 
                    "proximo_hint": "o que e"
                }
            },
            {
                "match_hints": ["redondo", "redondos", "esferico", "planetas sao esfericos", "formato dos planetas", "por que esferico"],
                "text": (
                    "Planetas são redondos porque a gravidade puxa a matéria igualmente para todos os lados em direção ao centro.\n\n"
                    "A esfera é a única forma geométrica onde todos os pontos da superfície estão à mesma distância do núcleo. Qualquer saliência seria puxada de volta pela gravidade ao longo do tempo.\n\n"
                    "Na prática, nenhum planeta é perfeitamente esférico. A rotação os achata levemente nos polos. A Terra, por exemplo, tem 43 km a mais no equador do que nos polos.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber por que os primeiros planetas são rochosos e os mais distantes são gasosos?",
                    "proxima_tag": "sistema_solar",
                    "proximo_hint": "rochosos e gasosos"
                }
            },
            {
                "match_hints": ["rochosos e gasosos", "rochosos", "gasosos", "por que planetas proximos sao rochosos", "por que planetas distantes sao gasosos", "diferenca entre planetas"],
                "text": (
                    "Logo após o Sol se formar, o vento solar soprou os gases leves para longe, empurrando o hidrogênio e o hélio para regiões mais distantes.\n\n"
                    "Mais pesada, a poeira e os minerais ficaram próximos, formando os planetas rochosos. Nas regiões frias e distantes, os gases se acumularam formando os gigantes gasosos.\n\n"
                    "Por isso planetas gasosos tendem a ser maiores: é mais fácil acumular gás em grande quantidade do que rochas."
                ),
                "imagem": "img/planetas.png",
                "followup": {
                    "pergunta": "Quer conhecer Júpiter, o maior de todos, que tem massa maior que todos os outros planetas juntos?",
                    "proxima_tag": "jupiter",
                    "proximo_hint": "o que e"
                }
            },
            {
                "match_hints": ["eixo", "rotação", "giram", "todos os planetas giram", "planetas giram em torno do proprio eixo", "rotacao dos planetas", "qual planeta gira mais rapido"],
                "text": (
                    "Sim, todos os planetas giram em torno do próprio eixo, pois conservam o movimento angular da nebulosa que os formou.\n\n"
                    "O campeão de velocidade é Júpiter, que completa uma rotação em apenas 9h 55min, apesar de ser o maior. O mais lento é Vênus, com um dia de 243 dias terrestres.\n\n"
                    "Na translação, Mercúrio é o mais rápido, com um ano de 88 dias terrestres. Netuno é o mais lento, levando 165 anos para dar uma volta ao redor do Sol.\n\n"
                ),
                "followup": {
                    "pergunta": "Vênus tem uma rotação realmente estranha. Quer entender por quê?",
                    "proxima_tag": "venus",
                    "proximo_hint": "rotacao inversa"
                }
            }
        ]
    },
    
    # -------------------------------------------------------------------------
    # MERCURIO
    # -------------------------------------------------------------------------
    {
        "tag": "mercurio",
        "patterns": [
            "mercurio", "mercúrio", "planeta mercurio", "sobre mercurio",
            "primeiro planeta", "primeiro planeta do sistema solar", "planeta mais proximo do sol", "planeta mais próximo do sol", "menor planeta", "mais proximo", "mais perto do sol", "planeta mais perto do sol", "planeta proximo ao sol", "mais rapido", "planeta mais veloz"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "primeiro planeta", "primeiro planeta do sistema solar", "menor planeta", "planeta mais proximo do sol", "planeta mais próximo do sol", "planeta mais perto do sol", "mais rapido", "planeta mais veloz"],
                "text": (
                    "Mercúrio é o primeiro planeta do sistema solar, além de ser o menor e o mais próximo do Sol. Tem cerca de 4.879 km de diâmetro, sendo pouco maior que a Lua.\n\n"
                    "O planeta recebeu esse nome por causa do deus romano Mercúrio, o mensageiro veloz, já que ele é o planeta que se move mais rápido ao redor do Sol.\n\n"
                    "Apesar de ser o mais próximo do Sol, não é o mais quente. As temperaturas variam entre -180°C à noite e 430°C durante o dia."
                ),
                "imagem": "img/Mercúrio.png",
                "followup": {
                    "pergunta": "Quer saber por que um dia em Mercúrio é mais longo que um ano?",
                    "proxima_tag": "mercurio",
                    "proximo_hint": "dia e ano"
                }
            },
            {
                "match_hints": ["dia e ano", "rotacao", "orbita", "tempo", "lento", "planeta mais lento"],
                "text": (
                    "Mercúrio tem uma das rotações mais lentas do sistema solar. Um dia dura 176 dias terrestres.\n\n"
                    "Mas um ano mercuriano leva apenas 88 dias terrestres. Então um dia em Mercúrio é literalmente mais longo do que um ano lá.\n\n"
                    "A NASA estudou Mercúrio de perto com a missão MESSENGER, que orbitou o planeta de 2011 a 2015."
                ),
                "imagem": "img/mercurio-perto.jpg",
                "followup": {
                    "pergunta": "Quer conhecer Vênus, o vizinho seguinte?",
                    "proxima_tag": "venus",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # VENUS
    # -------------------------------------------------------------------------
    {
        "tag": "venus",
        "patterns": [
            "venus", "vênus", "planeta venus", "sobre venus", "segundo",
            "segundo planeta", "segundo planeta do sistema solar", "planeta mais brilhante", "planeta mais luminoso", "planeta mais quente", "mais quente do sistema solar", "planeta mais toxico"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "segundo", "segundo planeta", "segundo planeta do sistema solar", "planeta mais brilhante", "planeta mais luminoso", "planeta mais toxico"],
                "text": (
                    "Vênus é o segundo planeta do sistema solar e o mais brilhante no céu noturno. É quase do mesmo tamanho que a Terra, por isso é chamado de planeta irmão.\n\n"
                    "O planeta recebeu esse nome por causa da deusa romana Vênus, associada à beleza e ao brilho, já que ele é o objeto mais luminoso do céu depois do Sol e da Lua.\n\n"
                    "Sua atmosfera é 96% dióxido de carbono com nuvens de ácido sulfúrico. A pressão na superfície é 92 vezes maior que na Terra, equivalente a 900 metros de profundidade no oceano, tornando Vênus o planeta mais tóxicos e inóspitos do Sistema Solar."
                ),
                "imagem": "img/Vênus.png",
                "followup": {
                    "pergunta": "Vênus é o planeta mais quente do sistema solar. Quer entender por quê?",
                    "proxima_tag": "venus",
                    "proximo_hint": "mais quente"
                }
            },
            {
                "match_hints": ["mais quente", "planeta mais quente", "temperatura", "calor", "efeito estufa"],
                "text": (
                    "A temperatura na superfície de Vênus chega a 465°C, quente o suficiente para derreter chumbo.\n\n"
                    "E é constante, não importa o dia ou a noite, o polo ou o equador. A atmosfera densa de CO₂ aprisiona o calor do Sol. Isso faz de Vênus mais quente que Mercúrio, mesmo estando mais longe do Sol.\n\n"
                    "A sonda soviética Venera 13 conseguiu pousar no planeta em 1982 e resistiu por pouco mais de duas horas, enviando imagens e dados antes de ser destruída pelas condições extremas."
                ),
                "imagem": ["img/venus-venera-13.jpg", "img/venera13.jpg"],
                "followup": {
                    "pergunta": "Vênus gira ao contrário dos outros planetas e muito devagar, bora entender por quê?",
                    "proxima_tag": "venus",
                    "proximo_hint": "rotacao inversa"
                }
            },
            {
                "match_hints": ["rotacao inversa", "gira ao contrario", "dia longo", "rotacao"],
                "text": (
                    "Vênus é um planeta peculiar na sua rotação. Ele gira no sentido horário, ao contrário da maioria dos planetas.\n\n"
                    "Além disso, um dia em Vênus dura 243 dias terrestres, mais longo que o seu próprio ano, que dura 225 dias terrestres.\n\n"
                    "A razão dessa rotação invertida ainda é debatida e pode ter sido uma colisão catastrófica no passado.\n\n"
                ),
                "followup": {
                    "pergunta": "No meio de tantos extremos, existe um planeta único. Vamos explorar mais sobre nosso planeta?",
                    "proxima_tag": "terra",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # TERRA
    # -------------------------------------------------------------------------
    {
        "tag": "terra",
        "patterns": [
            "terra", "nosso planeta", "planeta terra", "sobre a terra",
            "campo magnetico da terra", "atmosfera da terra", "terceiro"
            "terceiro planeta", "terceiro planeta do sistema solar", "planeta com vida", "planeta habitável", "planeta azul", "terra parasse de girar", "e se a terra parasse", "sem rotacao", "terra sem rotacao", "rotacionar", "parar de rotacionar", "sobre a terra"
        ],
        "responses": [
            {
            "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "terra", "nosso planeta", "planeta terra", "terceiro", "terceiro planeta", "terceiro planeta do sistema solar", "planeta com vida", "planeta habitável", "planeta azul", "sobre a terra"],
                "text": (
                    "A Terra é o terceiro planeta do sistema solar, sendo o único com vida confirmada e o maior dos planetas rochosos.\n\n"
                    "71% da superfície é coberta por água líquida, o único planeta no sistema solar com esse fenômeno em abundância.\n\n"
                    "A NASA considera essa combinação de água, atmosfera e temperatura o motivo pelo qual a vida surgiu aqui."
                ),
                "imagem": "img/Terra.png",
                "followup": {
                    "pergunta": "Quer entender o que protege a vida na Terra?",
                    "proxima_tag": "terra",
                    "proximo_hint": "campo magnetico"
                }
            },
            {
                "match_hints": ["campo magnetico", "atmosfera", "protecao", "escudo"],
                "text": (
                    "A Terra tem dois escudos naturais para a vida.\n\n"
                    "O campo magnético, gerado pelo núcleo de ferro líquido, desvia o vento solar e a radiação cósmica. Sem ele, a atmosfera seria varrida como aconteceu com Marte.\n\n"
                    "A atmosfera em si, com sua camada de ozônio, bloqueia a radiação ultravioleta. A NASA monitora essas camadas com satélites como o Aura e o DSCOVR.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber como a lua influencia a Terra?",
                    "proxima_tag": "terra",
                    "proximo_hint": "lua"
                }
            },
            {
                "match_hints": ["parar de girar", "parasse de girar", "e se a terra parasse", "sem rotacao", "terra sem rotacao", "rotacionar", "parar de rotacionar"],
                "text": (
                    "Se a Terra parasse de girar, o dia duraria um ano inteiro, metade com sol, metade no escuro.\n\n"
                    "O lado iluminado ficaria tórrido como Vênus, acima de 400°C, enquanto o lado escuro gelaria como Júpiter, abaixo de -100°C.\n\n"
                    "Os oceanos se redistribuiriam para os polos, os ventos se tornariam extremos e a vida na superfície seria praticamente inviável. \n\n"
                ),
                "followup": {
                    "pergunta": "Esse é só um cenário extremo na Terra. Quer descobrir o que pode acontecer com o universo inteiro?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "destino"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # LUA
    # -------------------------------------------------------------------------
    {
        "tag": "lua",
        "patterns": [
            "lua", "mare", "maré", "eclipse", "missao apollo", "missão apollo",
            "armstrong", "lua cheia", "fases da lua", "crateras",
            "como a lua se formou", "origem da lua", "grande impacto", "formacao da lua", "artemis", "artemis 2", "artemis II", "o que e o programa artemis", "o que e artemis", "satelite da terra", "Como a Lua foi formada", "lua se formou", "o que e a lua", "influencia da lua", "qual a influencia da lua", "qual a importancia da lua", "formação da lua", "movimento da lua", "lua orbita a terra", "lua gira em torno da terra", "lua gira em volta da terra", "fases da lua", "como as fases da lua acontecem", "por que a lua tem fases", "lua nao tem atmosfera", "por que a lua nao tem ar", "atmosfera da lua", "ar na lua"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "lua", "o que e a lua", "defin", "conceito", "explica", "sobre", "satelite da terra"],
                "text": (
                    "A Lua é o único satélite natural da Terra e o quinto maior do sistema solar.\n\n"
                    "Tem 3.474 km de diâmetro, cerca de um quarto da Terra.\n\n"
                    "A Lua está em rotação síncrona com a Terra, ou seja, completa uma rotação no mesmo tempo que orbita o planeta. Por isso sempre vemos a mesma face dela."
                ),
                "imagem": "img/Lua.png",
                "followup": {
                    "pergunta": "Quer saber como a Lua se formou? A história é mais dramática do que parece.", 
                    "proxima_tag": "lua",
                    "proximo_hint": "formacao"
                }
            },
            {
                "match_hints": ["formacao", "formou", "surgiu", "como se formou", "como a Lua foi formada", "origem", "nasceu"],
                "text": (
                    "A hipótese mais aceita é a do Grande Impacto.\n\n"
                    "Há 4,5 bilhões de anos, um objeto do tamanho de Marte, chamado Theia, colidiu com a Terra jovem.\n\n"
                    "Os detritos da colisão foram ejetados para órbita e se acumularam formando a Lua.\n\n"
                    "A Lua está se afastando da Terra a 3,8 cm por ano. Quando os dinossauros viviam, os dias terrestres tinham 23 horas."
                ),
                "imagem": "img/formacao-lua.png",
                "followup": {
                    "pergunta": "Quer saber por que a Lua é tão importante para a vida na Terra?",
                    "proxima_tag": "lua",
                    "proximo_hint": "unico satelite"
                }
            },
            {
                "match_hints": ["satelite", "unico satelite", "quanto tempo", "formacao da lua", "influencia da lua", "qual a influencia da lua", "qual a importancia da lua"],
                "text": (
                    "A Terra é o único planeta rochoso do sistema solar com um satélite natural tão grande em proporção ao seu tamanho.\n\n"
                    "A Lua exerce uma influência enorme sobre a Terra, ajudando a estabiliza a inclinação do eixo terrestre e mantendo o clima previsível ao longo de milhões de anos.\n\n"
                    "Sem a Lua, o eixo da Terra oscilaria de forma caótica, tornando o clima extremamente instável e dificultando o surgimento de vida complexa."
                ),
                "imagem": "img/terra-lua.jpg",
                "followup": {
                "pergunta": "Quer entender o movimento da Lua e por que sempre vemos a mesma face?",
                    "proxima_tag": "lua",
                    "proximo_hint": "movimento da lua"
                }
            },
            {
                "match_hints": ["translação", "rotação", "movimento da lua", "lua orbita a terra", "girar em volta", "lua gira em torno da terra", "lua gira em volta da terra"],
                "text": (
                    "A Lua demora aproximadamente 27,3 dias (período sideral) para completar uma volta ao redor da Terra em relação às estrelas.\n\n"
                    "Esse movimento é chamado de translação. Durante esse período, a Lua também realiza uma rotação sobre seu próprio eixo, o que faz com que vejamos sempre a mesma face.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber como as fases da Lua acontecem e por que a vemos de formas diferentes ao longo do mês?",
                    "proxima_tag": "lua",
                    "proximo_hint": "fases da lua"
                }
            },
            {
                "match_hints": ["fases da lua", "como as fases da lua acontecem", "por que a lua tem fases"],
                "text": (
                    "As fases da Lua ocorrem porque ela orbita a Terra e não possui luz própria, refletindo a luz solar de ângulos diferentes.\n\n"
                    "À medida que a Lua se move, a porção de sua superfície iluminada pelo Sol que enxergamos muda, passando por fases como nova, crescente, cheia e minguante em um ciclo de 29,5 dias (Período Sinódico (ciclo de fases))."
                ),
                "imagem": "img/fases-lua.png",
                "followup": {
                    "pergunta": "Quer saber por que a Lua não tem atmosfera?",
                    "proxima_tag": "lua",
                    "proximo_hint": "lua nao tem atmosfera"
                }
            },
            {
                "match_hints": ["lua nao tem atmosfera", "por que a lua nao tem ar", "atmosfera da lua", "ar na lua"],
                "text": (
                    "A gravidade da Lua é cerca de um sexto da Terra, fraca demais para reter gases.\n\n"
                    "Na Terra, os gases precisam de 11 km/s para escapar para o espaço. Na Lua, basta 2,4 km/s. As moléculas dos gases se movem rápido o suficiente para simplesmente fugir.\n\n"
                    "A Lua tem uma exosfera extremamente tênue, com traços de hidrogênio, hélio e outros gases, mas nada comparável a uma atmosfera real.\n\n"
                ),
                "followup": {
                    "pergunta": "Sem atmosfera, a superfície da Lua fica exposta a impactos. Quer saber o que causou as crateras?",
                    "proxima_tag": "lua",
                    "proximo_hint": "crateras"
                }
            },
            {
                "match_hints": ["crateras", "lua cheia de crateras", "o que causou as crateras", "buraco na lua"],
                "text": (
                    "As crateras da Lua são resultado de bilhões de anos de bombardeio por asteroides e meteoritos.\n\n"
                    "Sem atmosfera, não há fricção para frear ou queimar os objetos antes do impacto. E sem placas tectônicas ou erosão, as crateras se preservam por bilhões de anos.\n\n"
                    "A maior cratera da Lua, a Bacia South Pole-Aitken, tem 2.500 km de diâmetro e 8 km de profundidade, uma das maiores do sistema solar.\n\n"
                ),
                "followup": {
                    "pergunta": "O programa Apollo foi um marco histórico. Quer saber o que os astronautas descobriram lá?",
                    "proxima_tag": "lua",
                    "proximo_hint": "apollo"
                }
            },
            {
                "match_hints": ["apollo", "missao", "armstrong", "astronauta", "caminharam", "amostras"],
                "text": (
                    "Entre 1969 e 1972, o programa Apollo da NASA enviou 12 astronautas à superfície lunar.\n\n"
                    "Eles trouxeram 382 kg de rochas que ainda são estudadas hoje.\n\n"
                    "Neil Armstrong e Buzz Aldrin pousaram na Lua em 20 de julho de 1969. A missão Apollo 17 em 1972 foi a última e até hoje nenhum humano voltou à superfície lunar."
                ),
                "imagem": "img/apollo.jpg",
                "followup": {
                    "pergunta": "A NASA está desenvolvendo o programa Artemis para retornar à Lua. Quer saber sobre ele?",
                    "proxima_tag": "lua",
                    "proximo_hint": "artemis"
                }
            },
            {
                "match_hints": ["artemis", "artemis II", "artemis 2", "o que e o programa artemis", "o que e artemis", "volta a lua", "retorno", "futuro da lua"],
                "text": (
                    "O programa Artemis, da NASA, pretende retomar a exploração da Lua, com uma série de missões planejadas para os próximos anos.\n\n"
                    "O Artemis I, lançado em 2022, foi um voo não tripulado que testou o foguete e a cápsula Orion.\n\n"
                    "O Artemis II, lançado em 2026, foi o primeiro voo tripulado do programa, levando astronautas ao redor da Lua.\n\n"
                    "O Artemis III, previsto para 2027, tem como objetivo levar humanos de volta à superfície lunar.\n\n"
                    "As missões seguintes, como Artemis IV e V, fazem parte do plano de estabelecer uma presença contínua na Lua, incluindo a construção da estação orbital Gateway e missões regulares à superfície, servindo como base para futuras viagens a Marte."
                ),
                "imagem": ["img/Artemis-II.jpg", "img/artemis-decolando.jpg"],
                "followup": {
                    "pergunta": "Quer descobrir qual nave pode tornar Marte uma realidade?",
                    "proxima_tag": "spacex",
                    "proximo_hint": "starship"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # MARTE
    # -------------------------------------------------------------------------
    {
        "tag": "marte",
        "patterns": [
            "marte", "planeta marte", "sobre marte", "planeta vermelho",
            "perseverance", "vida em marte", "colonizacao de marte",
            "quarto", "quarto planeta", "quarto planeta do sistema solar", "mais parecido com a terra", "planeta parecido com a terra"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "marte", "planeta marte", "quarto", "quarto planeta", "quarto planeta do sistema solar", "mais parecido com a terra", "planeta parecido com a terra"],
                "text": (
                    "Marte é o quarto planeta do sistema solar, chamado de Planeta Vermelho pela cor do óxido de ferro no solo. Tem metade do diâmetro da Terra e uma atmosfera mais fina.\n\n"
                    "O planeta recebeu esse nome por causa do deus romano Marte, associado à guerra, justamente por sua aparência avermelhada no céu.\n\n"
                    "Um dia marciano dura 24h 37min, bem parecido com o da Terra. Porém, um ano tem 687 dias terrestres."
                ),
                "imagem": "img/Marte.png",
                "followup": {
                    "pergunta": "Marte tem os maiores acidentes geográficos do sistema solar. Quer conhecê-los?",
                    "proxima_tag": "marte",
                    "proximo_hint": "geografia"
                }
            },
            {
                "match_hints": ["geografia", "vulcao", "olympus", "valles marineris", "canyon", "montanha"],
                "text": (
                    "Marte tem recordes geográficos impressionantes.\n\n"
                    "O Olympus Mons é o maior vulcão do sistema solar, com 22 km de altura e 600 km de diâmetro. Para comparar, o Everest tem 8,8 km.\n\n"
                    "Já o Valles Marineris é um sistema de canyons com 4.000 km de comprimento e até 7 km de profundidade. O Grand Canyon dos EUA caberia inteiro num dos seus braços laterais."
                ),
                "imagem": ["img/olympus-mons.jpg", "img/valles-marineris.jpg"],
                "followup": {
                    "pergunta": "As missões da NASA em Marte descobriram evidências de água no passado. Quer saber mais?",
                    "proxima_tag": "marte",
                    "proximo_hint": "agua e vida"
                }
            },
            {
                "match_hints": ["agua e vida", "agua", "vida", "passado", "habitavel", "missao", "perseverance", "curiosity"],
                "text": (
                    "Evidências sólidas mostram que Marte teve água líquida na superfície há bilhões de anos.\n\n"
                    "O rover Curiosity encontrou minerais que só se formam na presença de água. O rover Perseverance, lançado em 2020, coleta amostras de rochas de regiões que foram lagos ou rios.\n\n"
                    "Essas amostras serão trazidas à Terra numa missão futura para análise de possíveis biossinaturas. Hoje, água existe em Marte congelada nas calotas polares e possivelmente no subsolo."
                ),
                "imagem": "img/perseverance.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre os planos de colonização de Marte e os desafios de levar humanos até lá?",
                    "proxima_tag": "marte",
                    "proximo_hint": "colonizacao"
                }
            },
            {
                "match_hints": ["colonizacao", "colonização", "humanos em marte", "viagem a marte", "desafios"],
                "text": (
                    "Levar humanos a Marte é um dos maiores desafios da exploração espacial.\n\n"
                    "A viagem leva entre 6 e 9 meses dependendo do alinhamento orbital. Durante esse tempo, os astronautas são expostos à radiação cósmica sem proteção magnética.\n\n"
                    "Em Marte, a temperatura média é de -60°C, a atmosfera é irrespirável e as tempestades de poeira podem durar meses. A NASA planeja missões tripuladas para a década de 2030, mas ainda há muito a resolver.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber sobre o programa Artemis, que pretende levar humanos de volta à Lua como passo para futuras missões a Marte?",
                    "proxima_tag": "lua",
                    "proximo_hint": "artemis"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # JUPITER
    # -------------------------------------------------------------------------
    {
        "tag": "jupiter",
        "patterns": [
            "jupiter", "júpiter", "planeta jupiter", "sobre jupiter",
            "o que e a grande mancha vermelha", "mancha em jupiter", "luas de jupiter", "europa lua", "io lua", "ganimedes", "quinto", "quinto planeta", "quinto planeta do sistema solar", "maior planeta", "maior planeta do sistema solar", "planeta gigante", "gigante gasoso"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "quinto", "quinto planeta", "quinto planeta do sistema solar", "maior planeta", "maior planeta do sistema solar", "planeta gigante", "gigante gasoso"],
                "text": (
                    "Júpiter é o quinto e maior planeta do sistema solar, com 11 vezes o diâmetro da Terra e mais massivo que todos os outros planetas juntos. É um gigante gasoso composto principalmente de hidrogênio e hélio.\n\n"
                    "O planeta recebeu esse nome por causa de Júpiter, o rei dos deuses na mitologia romana, refletindo seu tamanho e importância no Sistema Solar.\n\n"
                    "Um dia em Júpiter dura apenas 9h 55min, sendo o planeta que gira mais rápido. Essa rotação rápida achata os polos e cria faixas de nuvens características."
                ),
                "imagem": "img/Júpiter.png",
                "followup": {
                    "pergunta": "A Grande Mancha Vermelha de Júpiter é uma tempestade que dura séculos. Quer saber mais?",
                    "proxima_tag": "jupiter",
                    "proximo_hint": "grande mancha"
                }
            },
            {
                "match_hints": ["o que é a mancha em jupiter", "mancha em jupiter", "grande mancha", "tempestade", "mancha vermelha"],
                "text": (
                    "A Grande Mancha Vermelha é uma tempestade anticiclônica que existe há pelo menos 350 anos.\n\n"
                    "Tem ventos de até 640 km/h e um tamanho maior que a Terra inteira.\n\n"
                    "Curiosamente, ela tem encolhido nas últimas décadas. A NASA acompanha esse fenômeno com a sonda Juno, que orbita Júpiter desde 2016."
                ),
                "imagem": ["img/jupiter-terra.jpeg", "img/mancha-jupiter.jpg"],
                "followup": {
                    "pergunta": "Júpiter é o segundo planeta com o maior número de luas. Algumas delas são mundos fascinantes. Quer conhecer?",
                    "proxima_tag": "jupiter",
                    "proximo_hint": "luas"
                }
            },
            {
                "match_hints": ["luas", "europa", "io", "ganimedes", "calisto"],
                "text": (
                    "Júpiter tem 95 luas confirmadas, entre elas as quatro maiores, descobertas por Galileu em 1610.\n\n"
                    "Io é o objeto mais vulcanicamente ativo do sistema solar, com mais de 400 vulcões ativos.\n\n"
                    "Europa tem um oceano líquido sob uma camada de gelo, aquecido pelas forças de maré de Júpiter. É um dos candidatos mais promissores na busca por vida fora da Terra.\n\n"
                    "Ganimedes é a maior lua do sistema solar, maior até que Mercúrio.\n\n"
                    "Calisto é a mais distante das quatro e tem uma superfície cheia de crateras, uma das mais antigas e preservadas do Sistema Solar."
                ),
                "imagem": "img/luas-jupiter.png",
                "followup": {
                    "pergunta": "Quer conhecer Saturno e seus famosos anéis?",
                    "proxima_tag": "saturno",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SATURNO
    # -------------------------------------------------------------------------
    {
        "tag": "saturno",
        "patterns": [
            "saturno", "planeta saturno", "sobre saturno",
            "aneis de saturno", "anéis de saturno", "titan lua", "sexto", 
            "sexto planeta", "sexto planeta do sistema solar", "segundo maior planeta", "segundo maior planeta do sistema solar", "gigante gasoso", "luas de saturno", "numero de luas de saturno", "planeta com mais luas", "tem mais luas", "mais luas", "aneis de saturno", "de que sao feitos os aneis de saturno", 
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "sexto", "sexto planeta", "sexto planeta do sistema solar", "segundo maior planeta", "segundo maior planeta do sistema solar", "gigante gasoso", "mais anéis", "planeta com mais aneis", "planeta com mais anéis"],
                "text": (
                    "Saturno é o sexto planeta e o segundo maior do sistema solar, famoso pelos seus impressionantes anéis.\n\n"
                    "É um gigante gasoso com densidade tão baixa que flutuaria na água, se houvesse um oceano grande o suficiente.\n\n"
                    "Um dia dura 10h 33min e um ano tem 29 anos terrestres. Saturno tem pelo menos 146 luas confirmadas, o maior número do sistema solar."
                ),
                "imagem": "img/Saturno.png",
                "followup": {
                    "pergunta": "Os anéis de Saturno são uma das maravilhas do sistema solar. Quer entendê-los?",
                    "proxima_tag": "saturno",
                    "proximo_hint": "aneis de saturno"
                }
            },
            {
                "match_hints": ["aneis de saturno", "anéis de saturno", "composicao dos aneis", "de que sao feitos"],
                "text": (
                    "Os anéis de Saturno são compostos de partículas de gelo e rocha, do tamanho de grãos até o de casas.\n\n"
                    "Se espalhados, cobriam a distância da Terra à Lua. Mas são incrivelmente finos, apenas 10 a 100 metros de espessura em relação ao diâmetro de 270.000 km.\n\n"
                    "A missão Cassini da NASA orbitou Saturno de 2004 a 2017 e revelou que os anéis são relativamente jovens, entre 10 e 100 milhões de anos."
                ),
                "imagem": "img/aneis-saturno.jpg",
                "followup": {
                    "pergunta": "Além dos anéis, Saturno tem um sistema de luas fascinante. Bora conhecer algumas delas?",
                    "proxima_tag": "saturno",
                    "proximo_hint": "luas de saturno"
                }
            },
            {
                "match_hints": ["luas", "luas de saturno", "numero de luas de saturno", "planeta com mais luas", "mais luas"],
                "text": (
                    "Saturno é o planeta com o maior número de luas confirmadas no Sistema Solar, com um total de 274 luas conhecidas após novas descobertas anunciadas em 2025.\n\n"
                    "Essas luas variam de tamanho, sendo Titã a maior e com atmosfera densa, enquanto muitas outras são pequenas e irregulares."
                ),
                "imagem": "img/luas-de-saturno.jpg",
                "followup": {
                    "pergunta": "A lua Titã é única, tem atmosfera densa e lagos de metano líquido. Quer saber mais?",
                    "proxima_tag": "saturno",
                    "proximo_hint": "titan"
                }
            },
            {
                "match_hints": ["tita", "titã", "lua titan"],
                "text": (
                    "Titã é a segunda maior lua do sistema solar e a única com atmosfera densa.\n\n"
                    "Sua atmosfera é principalmente nitrogênio, parecida com a da Terra primordial. Na superfície, existem lagos e rios de metano e etano líquidos.\n\n"
                    "A NASA enviou a missão Dragonfly para explorar Titan, uma espécie de drone nuclear que vai pousar lá na década de 2030."
                ),
                "imagem": ["img/titan-saturno.jpg", "img/titan-saturno2.jpg"],
                "followup": {
                    "pergunta": "Quer conhecer Urano, o planeta que gira de lado?",
                    "proxima_tag": "urano",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # URANO
    # -------------------------------------------------------------------------
    {
        "tag": "urano",
        "patterns": [
            "urano", "planeta urano", "sobre urano",
            "planeta gelado", "gigante de gelo urano",
            "setimo planeta", "sétimo", "sétimo planeta", "setimo planeta do sistema solar", "planeta azul esverdeado", "planeta mais frio", "planeta mais frio do sistema solar", "planeta que gira de lado", "aneis de urano", "luas de urano", "planeta mais frio"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "setimo", "sétimo", "sétimo planeta", "setimo planeta do sistema solar", "planeta gelado", "gigante de gelo", "planeta mais frio", "mais frio"],
                "text": (
                    "Urano é o sétimo planeta do Sistema Solar e o primeiro dos gigantes de gelo. Também é o mais frio, com temperaturas que podem chegar a cerca de -224°C.\n\n"
                    "Tem 4 vezes o diâmetro da Terra e é composto principalmente de água, metano e amônia no estado gelado.\n\n"
                    "O planeta recebeu esse nome por causa de Urano, o deus grego do céu, sendo o único planeta do Sistema Solar nomeado diretamente da mitologia grega, e não romana.\n\n"
                    "O metano na atmosfera absorve a luz vermelha e reflete a azul-esverdeada, por isso sua cor característica."
                ),
                "imagem": "img/Urano.png",
                "followup": {
                    "pergunta": "Urano tem uma peculiaridade única: ele gira praticamente de lado. Quer entender por quê?",
                    "proxima_tag": "urano",
                    "proximo_hint": "eixo inclinado"
                }
            },
            {
                "match_hints": ["eixo inclinado", "gira de lado", "inclinacao", "colisao"],
                "text": (
                    "O eixo de Urano é inclinado 98 graus em relação à sua órbita, ele praticamente rola ao redor do Sol.\n\n"
                    "A explicação mais aceita é que ele tenha sofrido uma grande colisão com um objeto do tamanho da Terra no passado distante.\n\n"
                    "Essa inclinação extrema cria estações únicas, cada polo passa cerca de 42 anos em luz contínua, seguidos por 42 anos de escuridão.\n\n"
                ),
                "followup": {
                    "pergunta": "Urano também tem bastantes luas. Quer conhecer mais sobre elas?",
                    "proxima_tag": "urano",
                    "proximo_hint": "luas de urano"
                }
            },
            {
                "match_hints": ["luas", "numero de luas de urano", "luas de urano"],
                "text": (
                    "Urano possui 28 luas conhecidas, com nomes inspirados em personagens das obras de Shakespeare e Alexander Pope.\n\n"
                    "As maiores são Titânia, Oberon, Umbriel, Ariel e Miranda. Miranda é especialmente interessante por suas formações geológicas extremas, como falésias de até 20 km de altura e regiões com terreno caótico, sugerindo um passado geologicamente ativo."
                ),
                "imagem": "img/luas-urano.jpeg",
                "followup": {
                    "pergunta": "Assim como Saturno, Urano tem um sistema de anéis. Quer conhecer mais sobre eles?",
                    "proxima_tag": "urano",
                    "proximo_hint": "anéis de urano"
                }
            },
            {
                "match_hints": ["anéis de urano", "aneis de urano", "sistema de anéis"],
                "text": (
                    "Urano também tem anéis, embora sejam muito mais tênues e escuros que os de Saturno.\n\n"
                    "Eles foram descobertos em 1977 e são compostos principalmente de partículas de gelo e rocha. Esses anéis são muito finos, com espessura de apenas alguns metros, e acredita-se que sejam relativamente jovens, formados por detritos de luas destruídas por impactos ou forças de maré."
                ),
                    "imagem": "img/aneis-urano.jpg",
                    "followup": {
                    "pergunta": "Quer conhecer Netuno, o planeta mais distante e ventoso do sistema solar?",
                    "proxima_tag": "netuno",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # NETUNO
    # -------------------------------------------------------------------------
    {
        "tag": "netuno",
        "patterns": [
            "netuno", "planeta netuno", "sobre netuno",
            "planeta mais distante", "tritao", "oitavo",
            "oitavo planeta", "oitavo planeta do sistema solar", "planeta ventoso", "gigante de gelo netuno", "planeta azul escuro", "planeta mais distante do sistema solar", "aneis de netuno", "luas de netuno", "numero de luas de netuno", "mais distante", "mais distante do sol", "mais longe do sol", "mais lento", "planeta mais lento"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e", "oitavo planeta", "planeta mais distante", "planeta azul escuro", "planeta mais distante do sistema solar", "planeta mais distante do sol", "planeta mais longe do sol", "mais distante", "mais distante do sol", "mais longe do sol", "mais lento", "planeta mais lento"],
                "text": (
                    "Netuno é o oitavo e mais distante planeta do sistema solar.\n\n"
                    "Ele fica a cerca de 30 vezes a distância entre a Terra e o Sol e leva 165 anos terrestres para completar uma órbita, sendo o planeta mais lento do Sistema Solar\n\n"
                    "O planeta recebeu esse nome por causa de Netuno, o deus romano dos mares, devido à sua cor azul intensa, que lembra os oceanos.\n\n"
                    "É um gigante de gelo azul-escuro, com ventos de até 2.100 km/h, os mais rápidos do sistema solar. A NASA visitou Netuno apenas uma vez, com a Voyager 2 em 1989."
                ),
                "imagem": "img/Netuno.png",
                "followup": {
                    "pergunta": "A lua Tritão de Netuno é uma das mais estranhas do sistema solar. Quer entender por quê?",
                    "proxima_tag": "netuno",
                    "proximo_hint": "tritao"
                }
            },
            {
                "match_hints": ["tritao", "tritão", "luas", "numero de luas de netuno", "luas de netuno", "quantas luas tem netuno", "lua retrograda"],
                "text": (
                    "Netuno possui 14 luas conhecidas, mas a mais famosa é Tritão, a maior delas. O que torna Tritão tão peculiar é que ele orbita Netuno no sentido contrário à rotação do planeta, um movimento chamado de órbita retrógrada.\n\n"
                    "Isso sugere que ele foi capturado pelo campo gravitacional de Netuno e não se formou junto com o planeta.\n\n"
                    "Tritão tem temperatura de -235°C e geysers de nitrogênio na superfície, os mais frios já observados no sistema solar. Com o tempo, a órbita de Tritão vai decair e ele será destruído pelas forças de maré, formando um anel."
                ),
                "imagem": "img/tritao.jpg",
                "followup": {
                    "pergunta": "Netuno tem um sistema de anéis tênues, assim como Urano. Quer conhecer mais sobre eles?",
                    "proxima_tag": "netuno",
                    "proximo_hint": "anéis de netuno"
                }
            },
            {
                "match_hints": ["aneis de netuno", "sistema de aneis"],
                "text": (
                    "Netuno também posui um sistema de anéis tênues, compostos principalmente de partículas de gelo e rocha.\n\n"
                    "Esses anéis são muito finos, com espessura de apenas alguns metros, e acredita-se que sejam relativamente jovens, formados por detritos de luas destruídas por impactos ou forças de maré.\n\n"
                ),
                "followup": {
                    "pergunta": "Além dos 8 planetas, existe Plutão e o cinturão de Kuiper. Quer explorar as fronteiras do sistema solar?",
                    "proxima_tag": "plutao",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # PLUTAO E CINTURAO DE KUIPER
    # -------------------------------------------------------------------------
    {
        "tag": "plutao",
        "patterns": [
            "plutao", "plutão", "planeta anao", "planeta anão", "o que e plutao", "sobre plutao", "planeta rebaixado", "alem de netuno", "cinturao de kuiper", "kuiper", "nuvem de oort", "oort", "borda do sistema solar"],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "plutão", "planeta anao", "planeta anão", "o que e plutao", "o que e um planeta anao", "planeta rebaixado"],
                "text": (
                    "Plutão foi considerado o nono planeta por 76 anos, até ser rebaixado a planeta anão em 2006.\n\n"
                    "Isso se deve ao fato de ele compartilhar a órbita com muitos outros objetos no Cinturão de Kuiper e não ter limpado sua órbita.\n\n"
                    "O nome Plutão vem do deus romano do submundo, associado à escuridão e ao frio, o que combina com sua localização distante e gelada.\n\n"
                    "Plutão tem 2.377 km de diâmetro, menor que a Lua. A missão New Horizons da NASA fez o sobrevoo histórico em 2015 e revelou montanhas de gelo e um coração gelado na superfície."
                ),
                "imagem": "img/Plutão.png",
                "followup": {
                    "pergunta": "Quer saber o que é o Cinturão de Kuiper e o que existe além dele?",
                    "proxima_tag": "plutao",
                    "proximo_hint": "cinturao de kuiper"
                }
            },
            {
                "match_hints": ["cinturao de kuiper", "kuiper", "alem de netuno", "fronteira"],
                "text": (
                    "O Cinturão de Kuiper é uma região além de Netuno com bilhões de objetos gelados.\n\n"
                    "É semelhante ao Cinturão de Asteroides, mas muito maior, 20 vezes mais largo e até 200 vezes mais massivo.\n\n"
                    "Além de Plutão, outros planetas anões como Éris, Makemake e Haumea vivem nessa região. Éris, descoberta em 2005, é ligeiramente menor que Plutão."
                ),
                "imagem": ["img/objetos-kuiper.png", "img/cinturao-kuiper.jpg"],
                "followup": {
                    "pergunta": "Além do Cinturão de Kuiper existe a Nuvem de Oort, a borda do sistema solar. Quer explorar?",
                    "proxima_tag": "plutao",
                    "proximo_hint": "nuvem de oort"
                }
            },
            {
                "match_hints": ["nuvem de oort", "oort", "borda", "limite do sistema solar"],
                "text": (
                    "A Nuvem de Oort é uma esfera de trilhões de objetos gelados que envolve todo o sistema solar.\n\n"
                    "Começa a cerca de 2.000 UA do Sol e se estende até 100.000 UA, quase um quarto do caminho até a estrela mais próxima.\n\n"
                    "É o lugar de origem da maioria dos cometas de longo período. Nenhuma sonda já chegou até lá. A Voyager 1, o objeto humano mais distante, ainda está a mais de 21.000 UA do Sol."
                ),
                "imagem": "img/nuvem-oort.jpg",
                "followup": {
                    "pergunta": "Quer explorar outros temas, como buracos negros, galáxias ou vida extraterrestre?",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EXOPLANETAS
    # -------------------------------------------------------------------------
    {
        "tag": "exoplanetas",
        "patterns": [
            "exoplaneta", "exoplanetas", "o que e exoplaneta",
            "planetas fora do sistema solar", "trappist", "trappist-1", "kepler", "planeta habitavel", "zona habitavel", "goldilocks", "detecta", "planetas distantes"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Exoplanetas são planetas que orbitam outras estrelas, fora do nosso sistema solar.\n\n"
                    "A NASA confirmou mais de 5.700 deles e estima que cada estrela da galáxia tenha em média um planeta.\n\n"
                    "Isso significa centenas de bilhões de planetas só na Via Láctea.\n\n"
                ),
                "followup": {
                    "pergunta": "Como detectamos planetas a anos-luz de distância sem conseguir vê-los diretamente?",
                    "proxima_tag": "exoplanetas",
                    "proximo_hint": "como detecta"
                }
            },
            {
                "match_hints": ["detecta", "metodo", "transito", "como encontra", "distantes", "telescopio"],
                "text": (
                    "O método mais usado é o de trânsito: quando um planeta passa na frente da estrela, a luz dela diminui ligeiramente.\n\n"
                    "O telescópio Kepler usou esse método e encontrou mais de 2.600 planetas.\n\n"
                    "O James Webb Space Telescope vai além e consegue analisar a atmosfera dos exoplanetas. Ao filtrar a luz da estrela que passa pela atmosfera do planeta, identifica moléculas como água, metano ou CO₂.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber sobre o sistema TRAPPIST-1, um dos candidatos mais promissores à vida fora da Terra?",
                    "proxima_tag": "exoplanetas",
                    "proximo_hint": "trappist"
                }
            },
            {
                "match_hints": ["trappist", "sistema", "sistema trappist", "sistema trappist-1","trappist-1"],
                "text": (
                    "TRAPPIST-1 é um sistema a 40 anos-luz da Terra com 7 planetas rochosos do tamanho da Terra.\n\n"
                    "Três deles estão na zona habitável, a distância ideal da estrela para ter água líquida na superfície.\n\n"
                    "A estrela é uma anã vermelha fria, muito menor que o Sol. O James Webb já detectou que pelo menos um dos planetas pode ter atmosfera, uma descoberta histórica.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender o que é a zona habitável e por que ela é crucial na busca por vida?",
                    "proxima_tag": "exoplanetas",
                    "proximo_hint": "zona habitavel"
                }
            },
            {
                "match_hints": ["zona habitavel", "goldilocks", "agua liquida", "vida"],
                "text": (
                    "A zona habitável, ou Goldilocks Zone, é a faixa de distância de uma estrela onde a água pode existir líquida na superfície.\n\n"
                    "Nem quente demais, nem fria demais. Mas estar nessa zona não garante vida.\n\n"
                    "Vênus está na zona habitável do Sol e é um inferno de 465°C. O que importa é a combinação de atmosfera, composição e geologia.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer explorar a possibilidade de vida extraterrestre de forma mais ampla?",
                    "proxima_tag": "vida_extraterrestre",
                    "proximo_hint": "o que e"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # VIDA EXTRATERRESTRE
    # -------------------------------------------------------------------------
    {
        "tag": "vida_extraterrestre",
        "patterns": [
            "vida extraterrestre", "alienigenas", "alienígenas", "aliens",
            "vida fora da terra", "fermi", "paradoxo de fermi", "seti",
            "biossinatura", "vida no universo", "somos sozinhos"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "somos sozinhos", "existe", "vida no universo", "vida extraterrestre"],
                "text": (
                    "A questão da vida extraterrestre é uma das mais profundas da ciência.\n\n"
                    "Matematicamente, parece impossível que sejamos sozinhos. Existem mais estrelas no universo observável do que grãos de areia em todas as praias da Terra.\n\n"
                    "A NASA catalogou mais de 5.700 exoplanetas, muitos em zonas habitáveis.\n\n"
                ),
                "followup": {
                    "pergunta": "O Paradoxo de Fermi pergunta: se há tanta possibilidade, onde estão todos? Quer explorar?",
                    "proxima_tag": "vida_extraterrestre",
                    "proximo_hint": "paradoxo de fermi"
                }
            },
            {
                "match_hints": ["paradoxo de fermi", "fermi", "onde estao", "silencio"],
                "text": (
                    "Em 1950, o físico Enrico Fermi fez uma pergunta simples: onde estão todos?\n\n"
                    "O universo é velho e enorme. Se vida inteligente é comum, deveríamos ter detectado sinais.\n\n"
                    "Algumas hipóteses para o silêncio: talvez vida inteligente seja rara, ou civilizações se autodestruam, ou as distâncias são grandes demais para comunicação.\n\n"
                ),
                "followup": {
                    "pergunta": "Marte, Europa e Encélado são os candidatos mais promissores à vida microbiana. Quer saber por quê?",
                    "proxima_tag": "vida_extraterrestre",
                    "proximo_hint": "onde buscar"
                }
            },
            {
                "match_hints": ["onde buscar", "marte", "europa", "enceladus", "candidatos", "candidatos mais promissores", "candidatos a vida", "candidatos a vida extraterrestre", "vida microbiana"],
                "text": (
                    "Os candidatos mais promissores à vida estão bem perto de nós.\n\n"
                    "Marte: o rover Perseverance coleta amostras de antigas regiões lacustres em busca de biossinaturas.\n\n"
                    "Europa, lua de Júpiter, tem um oceano líquido debaixo do gelo, aquecido por forças de maré, com condições favoráveis à vida microbiana.\n\n"
                    "Encélado, lua de Saturno, jorra vapor de água com compostos orgânicos para o espaço."
                ),
                "imagem": "img/luas-vida.png",
                "followup": {
                    "pergunta": "Se encontrarmos apenas vida microbiana, isso mudaria tudo o que sabemos. Quer entender por quê?",
                    "proxima_tag": "vida_extraterrestre",
                    "proximo_hint": "microbiana"
                }
            },
            {
                "match_hints": ["microbiana", "microbio", "bacterias", "simples", "importancia"],
                "text": (
                    "Encontrar qualquer forma de vida fora da Terra, mesmo uma bactéria, seria a maior descoberta científica da história.\n\n"
                    "Significaria que a vida não é um acidente único da Terra, mas um fenômeno universal.\n\n"
                    "Implicaria que o universo está provavelmente repleto de vida em diferentes formas. A NASA e a ESA buscam ativamente biossinaturas, moléculas ou padrões que indiquem processos biológicos.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre buracos negros, galáxias, o Big Bang ou qualquer planeta.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # COMETAS E ASTEROIDES
    # -------------------------------------------------------------------------
    {
        "tag": "cometas_asteroides",
        "patterns": [
            "cometa", "cometas", "asteroide", "asteroides", "meteoro", "meteoros", "meteorito", "meteoritos", "diferenca cometa asteroide",
            "chuva de meteoros", "estrela cadente", "chuva de estrelas",
            "missao dart", "cinturao de asteroides", "extinção dos dinossauros", 
        ],
        "responses": [
            {
                "match_hints": ["asteroide", "o que e asteroide", "o que é asteroide", "defin", "conceito", "explica", "diferenca"],
                "text": (
                    "Asteroide é uma rocha que orbita o Sol, geralmente no cinturão entre Marte e Júpiter.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber sobre o asteroide que extinguiu os dinossauros?",
                    "proxima_tag": "cometas_asteroides",
                    "proximo_hint": "dinossauros"
                }
            },
            {
                "match_hints": ["cometa", "o que e cometa", "o que é cometa", "defin", "conceito", "explica", "diferenca"],
                "text": (
                    "Cometa é uma bola de gelo, rocha e poeira com órbita alongada. Quando se aproxima do Sol, forma a cauda brilhante.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber mais sobre o Cinturão de Asteroides, onde a maioria desses corpos orbita?",
                    "proxima_tag": "cometas_asteroides",
                    "proximo_hint": "cinturao"
                }
            },
                        {
                "match_hints": ["meteoro", "o que e meteoro", "o que é meteoro", "o que e meteorito", "o que é meteorito", "defin", "conceito", "explica", "diferenca"],
                "text": (
                    "Meteoro é um fragmento que entra na atmosfera e queima, criando o rastro de luz que chamamos de estrela cadente.\n\n"
                    "Meteorito é quando um fragmento sobrevive e chega ao solo.\n\n" 
                ),
                "followup": {
                    "pergunta": "Quer saber mais sobre o Cinturão de Asteroides, onde a maioria desses corpos orbita?",
                    "proxima_tag": "cometas_asteroides",
                    "proximo_hint": "cinturao"
                }
            },
            {
                "match_hints": ["dinossauros", "extincao", "impacto", "chicxulub", "extinção dos dinossauros"],
                "text": (
                    "Há 66 milhões de anos, um asteroide de cerca de 10 km colidiu na região do atual México, criando a cratera de Chicxulub.\n\n"
                    "O impacto liberou uma energia bilhões de vezes maior que qualquer bomba nuclear.\n\n"
                    "Incêndios globais, uma camada de fumaça bloqueando o Sol e um inverno castigoso resultaram na extinção de 76% das espécies. Essa extinção abriu espaço para os mamíferos e eventualmente para nós."
                ),
                "imagem": "img/craterachicxulub.png",
                "followup": {
                    "pergunta": "Quer saber mais sobre o Cinturão de Asteroides, onde a maioria desses corpos orbita?",
                    "proxima_tag": "cometas_asteroides",
                    "proximo_hint": "cinturao"
                }
            },
            {
                "match_hints": ["cinturao de asteroides", "cinturao", "entre marte e jupiter", "o que e o cinturao"],
                "text": (
                    "O Cinturão de Asteroides é uma região entre as órbitas de Marte e Júpiter onde orbitam milhões de rochas e corpos menores.\n\n"
                    "Estão cheias dos restos rochosos de planetas falhados que, ocasionalmente, chocam uns com os outros, originando rastos de poeira.\n\n"
                    "Acredita-se que o material do cinturão nunca formou um planeta por causa da influência gravitacional de Júpiter, que impediu a acreção. A massa total do cinturão é menor que a da Lua."
                ),
                "imagem": "img/cinturao-asteroides.jpg",
                "followup": {
                    "pergunta": "A NASA já desenvolveu defesa real contra asteroides. Quer saber sobre a missão DART?",
                    "proxima_tag": "cometas_asteroides",
                    "proximo_hint": "dart"
                }
            },
            {
                "match_hints": ["dart", "defesa planetaria", "desviar asteroide", "impacto intencional"],
                "text": (
                    "Em setembro de 2022, a NASA colidiu propositalmente a sonda DART com o asteroide Dimorphos.\n\n"
                    "O objetivo era testar se conseguimos alterar a órbita de um asteroide e funcionou.\n\n"
                    "A órbita de Dimorphos encurtou em 32 minutos, muito mais do que o esperado. Foi o primeiro teste real de defesa planetária da humanidade. A NASA monitora mais de 2.000 asteroides potencialmente perigosos com o Planetary Defense Coordination Office."
                ),
                "imagem": "img/dart.jpeg",
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre buracos negros, planetas ou o Big Bang.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # ESPACO-TEMPO E RELATIVIDADE
    # -------------------------------------------------------------------------
    {
        "tag": "espaco_tempo",
        "patterns": [
            "relatividade", "einstein", "espaco tempo", "espaço tempo",
            "curvatura", "dilatacao do tempo", "dilatação do tempo",
            "velocidade da luz", "wormhole", "buraco de minhoca", "viagem no tempo", "outras dimensoes", "dimensoes", "como astronautas se orientam", "orientacao no espaco",
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "relatividade", "einstein"],
                "text": (
                    "Einstein propôs que espaço e tempo não são fixos, eles formam um tecido único chamado espaço-tempo.\n\n"
                    "Massa e energia curvam esse tecido, e essa curvatura é o que chamamos de gravidade.\n\n"
                    "O GPS do seu celular depende de correções relativísticas. Sem elas, erraria mais de 10 km por dia, pois os satélites em órbita estão num campo gravitacional menor e o tempo passa mais rápido para eles."
                ),
                "imagem": "img/teoria-relatividade.jpg",
                "followup": {
                    "pergunta": "Quer entender a dilatação do tempo, como o tempo pode passar em velocidades diferentes?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "dilatacao do tempo"
                }
            },
            {
                "match_hints": ["dilatacao do tempo", "tempo passa diferente", "relogio", "velocidade"],
                "text": (
                    "A dilatação do tempo é real e foi medida experimentalmente.\n\n"
                    "Relógios atômicos em aviões de alta altitude mostram diferença mensurável em relação aos do solo.\n\n"
                    "Se você viajasse a 99,9% da velocidade da luz por um ano, voltaria para encontrar décadas passadas na Terra. Não é ficção científica. É a relatividade especial de Einstein, confirmada inúmeras vezes.\n\n"
                ),
                "followup": {
                    "pergunta": "Buracos de minhoca seriam atalhos no espaço-tempo. Eles poderiam existir de verdade?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "buraco de minhoca"
                }
            },
            {
                "match_hints": ["wormhole", "buraco de minhoca", "O que e um buraco de minhoca", "buracos de minhoca", "atalho", "viagem no tempo"],
                "text": (
                    "Buracos de minhoca são estruturas previstas pelas equações da Relatividade Geral.\n\n"
                    "Em teoria, funcionariam como atalhos, conectando dois pontos distantes do espaço-tempo.\n\n"
                    "O problema é que para existir de forma estável, precisariam de energia exótica com pressão negativa. Não temos evidência de que isso existe na natureza.\n\n"
                    "Já a viagem no tempo para o futuro é possível por efeitos como a dilatação do tempo. Para o passado, porém, ainda permanece no campo da especulação teórica."
                ),
                "imagem": ["img/ponte-de-einstein-rosen.jpg", "img/wormhole.jpg"],
                "followup": {
                    "pergunta": "Quer explorar as teorias que propõem mais dimensões além das quatro que conhecemos?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "outras dimensoes"
                }
            },
            {
                "match_hints": ["outras dimensoes", "dimensoes extras", "dimensoes alem das quatro", "superstring", "supercorda"],
                "text": (
                    "Além das quatro dimensões que conhecemos (comprimento, altura, profundidade e tempo), teorias modernas propõem muito mais.\n\n"
                    "A teoria das supercordas prevê 10 dimensões. As dimensões extras seriam compactadas em escalas menores que um átomo, invisíveis para nós.\n\n"
                    "Ainda não temos evidências experimentais dessas dimensões extras. O Grande Colisor de Hádrons (LHC) do CERN busca sinais indiretos delas em colisões de partículas.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre buracos negros, galáxias ou o Big Bang.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": ["como astronautas se orientam", "orientacao no espaco", "bussola no espaco", "gps no espaco", "navegacao espacial"],
                "text": (
                    "No espaço, bússolas não funcionam pois não há campo magnético uniforme. A orientação é feita com sensores estelares.\n\n"
                    "Esses sensores identificam a posição relativa da nave em relação às estrelas e ao Sol. Em órbita da Terra, o GPS ainda funciona. Além dela, não.\n\n"
                    "Em missões mais distantes, as naves usam a posição do Sol, da Terra e de estrelas de referência para calcular a localização. A Voyager 1, hoje a mais de 22 bilhões de km da Terra, ainda é rastreada com precisão por esse método.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender como a gravidade e a curvatura do espaço-tempo afetam a trajetória de naves e objetos no universo?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "o que"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # ANO-LUZ
    # -------------------------------------------------------------------------
    {
        "tag": "ano_luz",
        "patterns": [
            "ano luz", "ano-luz", "o que e ano luz", "o que e um ano luz",
            "distancia no espaco", "como medir distancia", "quanto e um ano luz"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "signific", "defin", "conceito", "ano-luz", "ano luz", "distancia no espaco", "como medir distancia", "quanto e um ano luz"],
                "text": (
                    "Um ano-luz é a distância que a luz percorre em um ano, equivalente a aproximadamente 9,46 trilhões de quilômetros.\n\n"
                    "A estrela mais próxima da Terra, Proxima Centauri, fica a 4,24 anos-luz. Isso significa que a luz que sai dela leva mais de 4 anos para chegar aqui.\n\n"
                    "Quando você olha para o céu, está vendo o passado.\n\n"
                ),
                "followup": {
                    "pergunta": "Já parou pra pensar por que a velocidade da luz é um limite?",
                    "proxima_tag": "ano_luz",
                    "proximo_hint": "limite da luz"
                }
            },
            {
                "match_hints": ["limite da luz", "velocidade da luz", "por que nao pode", "mais rapido"],
                "text": (
                    "A velocidade da luz, cerca de 300 mil km/s, é o limite de velocidade do universo.\n\n"
                    "Não por convenção, mas porque a física impõe isso. À medida que um objeto acelera, sua massa aumenta relativisticamente.\n\n"
                    "Para atingir a velocidade da luz, precisaria de energia infinita, o que é impossível. Só partículas sem massa, como fótons, conseguem viajar à velocidade da luz.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer entender a dilatação do tempo, o que acontece quando você chega perto dessa velocidade?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "dilatacao do tempo"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SPACEX
    # -------------------------------------------------------------------------
    {
        "tag": "spacex",
        "patterns": [
            "spacex", "space x", "empresa spacex", "elon musk spacex", "empresa de foguetes spacex", "quem criou a spacex", "o que e spacex", "o que é spacex", "o que a spacex faz", "foguetes da spacex", "falcon 9", "falcon heavy", "starship", "lancamentos da spacex", "lançamentos da spacex", "reutilizacao de foguetes", "foguete reutilizavel", "tesla", "carro tesla"
        ],
        "responses": [
             {
                "match_hints": ["o que", "o que e", "defin", "conceito", "spacex", "space x"],
                "text": (
                    "A SpaceX é uma empresa aeroespacial fundada em 2002 por Elon Musk.\n\n"
                    "O objetivo principal dela é reduzir o custo das viagens espaciais e tornar possível a colonização de Marte.\n\n"
                    "Ela revolucionou o setor ao criar foguetes reutilizáveis, algo que antes parecia impossível."
                ),
                "imagem": "img/spacex.jpg",
                "followup": {
                    "pergunta": "Quer saber como funcionam os foguetes reutilizáveis da SpaceX?",
                    "proxima_tag": "spacex",
                    "proximo_hint": "reutilizavel"
                }
            },
            {
                "match_hints": ["reutilizavel", "reutilizacao", "reutilizaveis", "pouso", "foguetes"],
                "text": (
                    "Os foguetes da SpaceX, como o Falcon 9, conseguem voltar e pousar na Terra após o lançamento.\n\n"
                    "Isso reduz drasticamente os custos, já que o mesmo foguete pode ser usado várias vezes.\n\n"
                    "Eles pousam verticalmente, usando motores para desacelerar antes de tocar o solo."
                ),
                "imagem": ["img/falcon9.jpg", "img/Falcon9.gif"],
                "followup": {
                    "pergunta": "Quer conhecer o projeto mais ambicioso da SpaceX, o Starship?",
                    "proxima_tag": "spacex",
                    "proximo_hint": "starship"
                }
            },
            {
                "match_hints": ["starship", "colonizar marte"],
                "text": (
                    "O Starship é o foguete mais ambicioso da SpaceX.\n\n"
                    "Ele foi projetado para levar humanos à Lua, Marte e além.\n\n"
                    "A ideia é tornar viagens interplanetárias algo viável no futuro, com capacidade para dezenas de pessoas por missão."
                ),
                "imagem": "img/Starship.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre outros foguetes como o Falcon Heavy?",
                    "proxima_tag": "spacex",
                    "proximo_hint": "falcon heavy"
                }
            },
            {
                "match_hints": ["falcon heavy", "foguete mais poderoso", "tesla", "roadster", "carro"],
                "text": (
                    "O Falcon Heavy é um dos foguetes mais poderosos já construídos.\n\n"
                    "Ele usa três boosters do Falcon 9 juntos, permitindo transportar cargas extremamente pesadas para o espaço.\n\n"
                    "Em 2018, no primeiro lançamento, a SpaceX enviou um Tesla Roadster ao espaço como teste."
                ),
                "imagem": ["img/falcon-heavy.jpg", "img/Roadster.jpg", "img/Roadster1.png"],
                "followup": {
                    "pergunta": "Quer explorar outro tema do universo?",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # DEFAULT
    # -------------------------------------------------------------------------
    {
        "tag": "default",
        "patterns": [],
        "responses": [
            {
                "match_hints": [],
                "text": "Não entendi o que você perguntou.",
                "followup": {
                    "pergunta": "Tente reformular ou escolha um assunto.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": [],
                "text": "Hmm, não entendi bem o que você quis dizer.",
                "followup": {
                    "pergunta": "Tente novamente ou escolha um tema para explorar.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            }
        ]
    }
]
