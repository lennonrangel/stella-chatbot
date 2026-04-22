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
        hint_norm = hint.lower()
        for r in responses:
            if any(h in hint_norm for h in r.get("match_hints", [])):
                matched = r
                break

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
                "text": "Oi! Que bom te ver por aqui. O universo é enorme e cheio de mistérios.",
                "followup": {
                    "pergunta": "Por onde você quer começar? Posso falar sobre buracos negros, planetas, estrelas, galáxias ou até vida extraterrestre.",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": [],
                "text": "Olá! Sou a Stella, sua guia pelo cosmos.",
                "followup": {
                    "pergunta": "Tem algum canto do universo que sempre te deixou curioso?",
                    "proxima_tag": None,
                    "proximo_hint": None
                }
            },
            {
                "match_hints": [],
                "text": "Hey! Tô aqui prontinha pra embarcar numa viagem pelo espaço com você.",
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
            "sagitario", "gravidade extrema", "radiacao hawking"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Um buraco negro é uma região do espaço onde a gravidade é tão intensa que nem a luz consegue escapar.\n\n"
                    "Não é um buraco de verdade, mas uma concentração enorme de massa num espaço minúsculo.\n\n"
                    "O tempo passa mais devagar perto deles, um efeito previsto pela Teoria da Relatividade Geral de Einstein.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer saber como um buraco negro se forma?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "como se forma"
                }
            },
            {
                "match_hints": ["como se forma", "como nasce", "origem", "formacao", "surge"],
                "text": (
                    "Um buraco negro estelar se forma quando uma estrela com mais de 20 massas solares chega ao fim da vida. Ela colapsa sobre si mesma numa supernova e o núcleo é comprimido até virar uma singularidade.\n\n"
                    "Já os buracos negros supermassivos, com milhões ou bilhões de massas solares, têm origem ainda debatida pelos cientistas. A NASA acredita que podem ter se formado nos primeiros momentos do universo.\n\n"
                ),
                "followup": {
                    "pergunta": "No centro da nossa galáxia existe um desses supermassivos. Quer saber sobre ele?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "sagitario"
                }
            },
            {
                "match_hints": ["sagitario", "via lactea", "centro da galaxia", "supermassivo", "o que tem no centro da via lactea", "centro da via lactea"],
                "text": (
                    "O buraco negro no centro da Via Láctea se chama Sagitário A*. Ele tem a massa de 4 milhões de sóis comprimidos numa região menor que nosso sistema solar.\n\n"
                    "Em 2022, o Event Horizon Telescope divulgou a primeira imagem real dele."
                ),
                "imagem": ["img/sagitario-a.jpg", "img/via-lactea.jpeg"],
                "followup": {
                    "pergunta": "E se alguém caísse nele, quer descobrir o que aconteceria?",
                    "proxima_tag": "buraco_negro",
                    "proximo_hint": "cair"
                }
            },
            {
                "match_hints": ["cair", "entrar", "dentro", "o que acontece", "espaguetificacao"],
                "text": (
                    "Se alguém caísse em um buraco negro, passaria pelo processo de espaguetificação.\n\n"
                    "A diferença de gravidade entre a cabeça e os pés esticaria o corpo como um espaguete.\n\n"
                    "Para quem observa de fora, a pessoa pareceria congelar no horizonte de eventos e desaparecer lentamente. Para quem cai, atravessaria a fronteira sem perceber, mas seria destruído na singularidade.\n\n"
                ),
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre estrelas, galáxias, planetas ou o Big Bang.",
                    "proxima_tag": None,
                    "proximo_hint": None
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
            "morte de uma estrela", "ana amarela", "gigante vermelha"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Estrelas são esferas de gás, principalmente hidrogênio e hélio, que brilham por fusão nuclear.\n\n"
                    "No núcleo, a temperatura passa de 15 milhões de graus Celsius.\n\n"
                    "A NASA calcula que existem cerca de 200 a 400 bilhões de estrelas só na Via Láctea. No universo inteiro, há mais estrelas do que grãos de areia em todas as praias da Terra."
                ),
                "imagem": "img/estrelas.jpg",
                "followup": {
                    "pergunta": "Quer saber como uma estrela nasce?",
                    "proxima_tag": "estrelas",
                    "proximo_hint": "como nasce"
                }
            },
            {
                "match_hints": ["como nasce", "nascem", "origem", "formacao", "nebulosa"],
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
                "match_hints": ["como morre", "morte", "morrer", "fim", "ciclo"],
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
                "match_hints": ["tipos", "maior", "menor", "ana vermelha", "hipergigante", "uy scuti", "ana branca"],
                "text": (
                    "Existe uma enorme variedade de estrelas.\n\n"
                    "Anãs vermelhas são as mais comuns e as mais longevas, podendo viver trilhões de anos.\n\n"
                    "Já a UY Scuti, uma hipergigante, tem raio 1.700 vezes maior que o Sol.\n\n"
                    "Anãs brancas são núcleos de estrelas mortas, do tamanho da Terra mas com massa comparável ao Sol."
                ),
                "imagem": "img/tipos-estrelas.png",
                "followup": {
                    "pergunta": "Quer saber sobre supernovas, o maior espetáculo do universo?",
                    "proxima_tag": "supernova",
                    "proximo_hint": "o que e"
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
            "constelacao", "constelação", "constelacoes", "constelações", "agrupamento", "padrao no ceu"
        ],
        "responses": [
            {
                "match_hints": ["constelacao", "constelação", "constelacoes", "constelações", "agrupamento", "padrao no ceu"],
                "text": (
                    "Constelações são agrupamentos de estrelas que, vistas da Terra, formam padrões reconhecíveis no céu.\n\n"
                    "A União Astronômica Internacional reconhece oficialmente 88 constelações que dividem o céu inteiro em regiões, como países num mapa. Toda estrela do céu pertence a alguma delas.\n\n"
                    "As estrelas de uma mesma constelação geralmente não têm nenhuma relação entre si. Estão a distâncias completamente diferentes da Terra e apenas parecem próximas pela perspectiva de quem observa daqui."
                ),
                "imagem": "img/constelacoes.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre as Três Marias e a Constelação de Órion, uma das mais famosas do céu?",
                    "proxima_tag": "tres_marias",
                    "proximo_hint": "o que e"
                }
            },
            {
                "match_hints": ["tres marias", "três marias", "cinturao de orion", "cinturão de órion", "alnitak", "alnilam", "mintaka"],
                "text": (
                    "As Três Marias são três estrelas alinhadas que formam o cinturão da Constelação de Órion.\n\n"
                    "Seus nomes são Alnitak, Alnilam e Mintaka. As três ficam a cerca de 1.200 anos-luz da Terra e estão entre as estrelas mais brilhantes do céu noturno.\n\n"
                    "O alinhamento quase perfeito das três é uma coincidência visual, elas não estão na mesma distância, apenas parecem alinhadas vistas daqui da Terra."
                ),
                "imagem": "img/tres-marias.jpg",
                "followup": {
                    "pergunta": "Quer saber mais sobre a Constelação de Órion e o que existe ao redor das Três Marias?",
                    "proxima_tag": "tres_marias",
                    "proximo_hint": "orion"
                }
            },
            {
                "match_hints": ["orion", "constelacao", "constelação", "ao redor", "nebulosa de orion"],
                "text": (
                    "A Constelação de Órion é uma das mais reconhecíveis do céu e visível em quase todo o planeta.\n\n"
                    "Abaixo do cinturão das Três Marias fica a Nebulosa de Órion, uma das regiões de formação estelar mais ativas próximas da Terra, a cerca de 1.344 anos-luz de distância.\n\n"
                    "Duas das estrelas mais famosas de Órion são Betelgeuse, uma supergigante vermelha que pode explodir em supernova em qualquer momento em escala astronômica, e Rigel, uma das estrelas mais luminosas do céu noturno."
                ),
                "imagem": "img/constelacao-orion.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre Betelgeuse e por que os astrônomos acompanham ela de perto?",
                    "proxima_tag": "tres_marias",
                    "proximo_hint": "betelgeuse"
                }
            },
            {
                "match_hints": ["betelgeuse", "supergigante", "vai explodir", "supernova"],
                "text": (
                    "Betelgeuse é uma supergigante vermelha localizada no ombro de Órion, a cerca de 700 anos-luz da Terra.\n\n"
                    "Ela é tão grande que, se estivesse no lugar do Sol, engolir ia além da órbita de Júpiter.\n\n"
                    "Em 2019, ela escureceu de forma incomum, o que gerou especulação sobre uma supernova iminente. Os astrônomos concluíram que foi uma ejeção de massa, mas Betelgeuse está mesmo no fim da vida e vai explodir em supernova, provavelmente nos próximos 100 mil anos."
                ),
                "imagem": "img/betelgeuse.jpg",
                "followup": {
                    "pergunta": "Quer explorar outros temas? Posso falar sobre constelações, signos ou qualquer tema do cosmos.",
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
            "signo e astronomia", "astrologia e astronomia"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "signos", "zodiaco"],
                "text": (
                    "Os signos do zodíaco têm origem na astronomia antiga. As civilizações observaram que o Sol parece passar por diferentes grupos de estrelas ao longo do ano.\n\n"
                    "Esses grupos foram divididos em 12 constelações, que formam o zodíaco. A ideia era que a posição do Sol em relação a essas constelações no momento do nascimento de alguém influenciaria sua personalidade.\n\n"
                    "A astronomia e a astrologia caminharam juntas por séculos antes de se separarem como ciência e crença."
                ),
                "imagem": "img/zodiaco.jpg",
                "followup": {
                    "pergunta": "Quer saber a diferença entre o que a astrologia diz e o que a astronomia realmente observa?",
                    "proxima_tag": "signos",
                    "proximo_hint": "diferenca"
                }
            },
            {
                "match_hints": ["diferenca", "diferença", "astronomia", "ciencia", "real", "verdade"],
                "text": (
                    "A astronomia e a astrologia divergem em um ponto fundamental, a posição do Sol nas constelações mudou desde que o zodíaco foi criado há 2.000 anos.\n\n"
                    "Isso acontece por causa da precessão dos equinócios, uma oscilação lenta do eixo da Terra. Hoje o Sol está numa constelação diferente da que a astrologia indica para cada signo.\n\n"
                    "Além disso, a astrologia usa 12 constelações, mas o Sol na verdade passa por 13, incluindo Ofiúco, que a astrologia tradicional simplesmente ignora."
                ),
                "imagem": "img/precessao.jpg",
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
                "imagem": "img/precessao-equinocios.jpg",
                "followup": {
                    "pergunta": "Quer explorar as constelações de forma mais ampla?",
                    "proxima_tag": "tres_marias",
                    "proximo_hint": "constelacao"
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
            "supernova", "supernovas", "explosão de estrela", "explosao de estrela",
            "estrela explode", "estrela explodindo"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Supernova é a explosão de uma estrela massiva no fim de sua vida.\n\n"
                    "Esse fenômeno libera uma energia gigantesca, dispersando elementos químicos pesados que formam novas estrelas e planetas.\n\n"
                    "O ferro no seu sangue foi forjado em uma supernova."
                ),
                "followup": {
                    "pergunta": "Quer entender como uma supernova acontece, passo a passo?",
                    "proxima_tag": "supernova",
                    "proximo_hint": "como acontece"
                }
            },
            {
                "match_hints": ["como acontece", "como", "processo", "colapsa", "combustivel"],
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
                "match_hints": ["o que sobra", "sobra", "restos", "estrela de neutrons"],
                "text": (
                    "Depois da explosão, o que sobra depende da massa do núcleo.\n\n"
                    "Se o núcleo tiver entre 1,4 e 3 massas solares, vira uma estrela de nêutrons, incrivelmente densa.\n\n"
                    "Se for maior, o colapso não para e forma um buraco negro. A Nebulosa do Caranguejo, observada em 1054, é o resquício de uma supernova ainda visível hoje."
                ),
                "imagem": "img/nebulosa-caranguejo.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre estrelas de nêutrons?",
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
            "estrela de neutrons", "estrela de nêutrons",
            "o que e estrela de nêutrons"],
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
                "match_hints": ["colisao", "colisão", "fusao", "fusão", "duas estrelas", "kilonova", "o que e kilonova", "onda gravitacional", "ouro", "elementos"],
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
            },
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
            "aglomerado", "universo observavel"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Galáxias são sistemas de estrelas, gás, poeira e matéria escura mantidos unidos pela gravidade.\n\n"
                    "Existem em formas diferentes: espirais, elípticas e irregulares.\n\n"
                    "O universo observável tem mais de 2 trilhões de galáxias, segundo estimativas do Hubble Space Telescope."
                ),
                "imagem": "img/galaxias.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre a nossa galáxia, a Via Láctea?",
                    "proxima_tag": "galaxias",
                    "proximo_hint": "via lactea"
                }
            },
            {
                "match_hints": ["via lactea", "nossa galaxia", "nossa galáxia"],
                "text": (
                    "A Via Láctea tem entre 100 e 400 bilhões de estrelas e cerca de 100 mil anos-luz de diâmetro.\n\n"
                    "Ela é uma galáxia espiral barrada, com um núcleo em forma de barra e braços espirais saindo.\n\n"
                    "O sistema solar fica num dos braços, a cerca de 26 mil anos-luz do centro. Levamos 225 milhões de anos para dar uma volta completa ao redor do núcleo galático."
                ),
                "imagem": "img/via-lactea.jpeg",
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
                    "Daqui a 4,5 bilhões de anos, as duas vão colidir e fundir numa galáxia elíptica gigante. Mas não precisa se preocupar: o espaço entre as estrelas é tão vasto que quase nenhuma vai realmente bater em outra."
                ),
                "imagem": "img/andromeda.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre as galáxias mais extremas que existem?",
                    "proxima_tag": "galaxias",
                    "proximo_hint": "extremas"
                }
            },
            {
                "match_hints": ["extremas", "maior", "ic 1101", "mais distante", "quasar"],
                "text": (
                    "A maior galáxia conhecida, IC 1101, tem mais de 6 milhões de anos-luz de diâmetro, 60 vezes maior que a Via Láctea.\n\n"
                    "Quasares são os núcleos de galáxias antigas com buracos negros supermassivos ativos.\n\n"
                    "O mais distante já observado fica a mais de 13 bilhões de anos-luz. Quando olhamos para ele, estamos vendo o universo com menos de 1 bilhão de anos de existência."
                ),
                "imagem": "img/quasar.jpg",
                "followup": {
                    "pergunta": "Quer entender o Big Bang, como tudo isso começou?",
                    "proxima_tag": "big_bang",
                    "proximo_hint": "o que e"
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
            "inflacao cosmica", "radiacao cosmica de fundo", "universo surgiu"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "O Big Bang não foi uma explosão no espaço, foi uma expansão do próprio espaço.\n\n"
                    "Há 13,8 bilhões de anos, todo o universo estava concentrado num ponto minúsculo e incrivelmente quente.\n\n"
                    "Em frações de segundo, expandiu de tamanho subatômico para o tamanho de uma laranja num evento chamado inflação cósmica. Até hoje o universo continua se expandindo, cada vez mais rápido."
                ),
                "imagem": "img/big-bang.jpg",
                "followup": {
                    "pergunta": "Quais são as evidências de que o Big Bang realmente aconteceu?",
                    "proxima_tag": "big_bang",
                    "proximo_hint": "evidencias"
                }
            },
            {
                "match_hints": ["evidencias", "provas", "como sabemos", "comprovacao"],
                "text": (
                    "A principal evidência é a Radiação Cósmica de Fundo, o eco de luz do Big Bang.\n\n"
                    "Em 1965, dois engenheiros da Bell Labs detectaram por acidente esse sinal vindo de todas as direções.\n\n"
                    "Outro indício é que o universo se expande. Se você rebobinar esse movimento, tudo converge para um ponto. O telescópio WMAP da NASA mapeou esse eco com precisão extraordinária em 2003."
                ),
                "imagem": "img/radiacao-cosmica.jpg",
                "followup": {
                    "pergunta": "O que havia antes do Big Bang? É uma das perguntas mais profundas da física.",
                    "proxima_tag": "big_bang",
                    "proximo_hint": "antes"
                }
            },
            {
                "match_hints": ["antes", "antes do big bang", "o que havia", "anterior"],
                "text": (
                    "A pergunta sobre o que havia antes do Big Bang pode não fazer sentido.\n\n"
                    "O tempo surgiu junto com o universo. Perguntar o que havia antes é como perguntar o que está ao sul do Polo Sul.\n\n"
                    "Algumas teorias propõem um universo cíclico, ou um multiverso onde nosso universo seria apenas um bolso de espuma quântica. Mas são especulações e ainda não temos como testá-las."
                ),
                "imagem": "img/multiverso.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre o destino final do universo, como tudo isso vai terminar?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "o que e"
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
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "como vai acabar"],
                "text": (
                    "O universo está se expandindo, e cada vez mais rápido, empurrado pela energia escura.\n\n"
                    "O cenário mais aceito hoje é o Big Freeze, ou Grande Congelamento.\n\n"
                    "Daqui a trilhões de anos, as estrelas vão se apagar, os buracos negros vão evaporar e o universo vai esfriar até o zero absoluto. Tudo para. Tudo esfria."
                ),
                "imagem": "img/big-freeze.jpg",
                "followup": {
                    "pergunta": "Quer conhecer os outros cenários possíveis, como o Big Rip e o Big Crunch?",
                    "proxima_tag": "destino_universo",
                    "proximo_hint": "cenarios"
                }
            },
            {
                "match_hints": ["cenarios", "big rip", "big crunch", "possibilidades", "outros cenarios"],
                "text": (
                    "Existem três cenários principais para o fim do universo.\n\n"
                    "Big Freeze: expansão eterna até o universo esfriar completamente. É o mais provável.\n\n"
                    "Big Rip: a energia escura fica forte demais e rasga o próprio tecido do espaço, até os átomos seriam destruídos.\n\n"
                    "Big Crunch: o universo para de se expandir, reverte e colapsa sobre si mesmo. Tudo depende da natureza da energia escura, que ainda não entendemos completamente."
                ),
                "imagem": "img/fim-universo.jpg",
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
            "energia escura", "dark energy", "o que e materia escura"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "materia escura"],
                "text": (
                    "Matéria escura é uma substância invisível que não emite, absorve nem reflete luz.\n\n"
                    "Sabemos que existe porque sua gravidade afeta galáxias e aglomerados de formas que a matéria visível não explica.\n\n"
                    "Segundo a NASA, ela compõe cerca de 27% do universo. Tudo que você pode ver, estrelas, planetas, você mesmo, forma apenas 5%."
                ),
                "imagem": "img/materia-escura.jpg",
                "followup": {
                    "pergunta": "Como os cientistas detectam algo que não pode ser visto?",
                    "proxima_tag": "materia_escura",
                    "proximo_hint": "como detecta"
                }
            },
            {
                "match_hints": ["como detecta", "como sabemos", "evidencia", "prova"],
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
                    "Energia escura é diferente da matéria escura e ainda mais enigmática.\n\n"
                    "Ela representa cerca de 68% do universo e está acelerando sua expansão.\n\n"
                    "Em 1998, dois grupos de cientistas descobriram essa aceleração estudando supernovas distantes. Eles ganharam o Nobel de Física em 2011 por isso. Não sabemos o que é a energia escura. É a maior questão em aberto da cosmologia moderna."
                ),
                "imagem": "img/energia-escura.jpg",
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
            "sol", "nossa estrela", "o sol", "sobre o sol",
            "como o sol funciona", "vida do sol", "morte do sol"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "O Sol é uma estrela anã amarela com 4,6 bilhões de anos de idade.\n\n"
                    "Tem 109 vezes o diâmetro da Terra e contém 99,8% de toda a massa do sistema solar.\n\n"
                    "No núcleo, a temperatura chega a 15 milhões de graus Celsius. A cada segundo, ele converte 600 milhões de toneladas de hidrogênio em hélio por fusão nuclear."
                ),
                "imagem": "img/Sol.png",
                "followup": {
                    "pergunta": "Quer entender os fenômenos da superfície do Sol, como manchas solares e erupções?",
                    "proxima_tag": "sol",
                    "proximo_hint": "superficie"
                }
            },
            {
                "match_hints": ["superficie", "mancha", "erupcao", "tempestade solar", "corona", "vento solar"],
                "text": (
                    "A superfície do Sol é muito mais agitada do que parece.\n\n"
                    "Manchas solares são regiões mais frias causadas por campos magnéticos intensos e podem ser maiores que a Terra.\n\n"
                    "Erupções solares liberam em minutos mais energia do que a humanidade consumiu em toda a história. O vento solar, um fluxo de partículas carregadas, viaja até 800 km/s e é responsável pelas auroras na Terra. A NASA monitora isso com a missão Parker Solar Probe."
                ),
                "imagem": "img/aurora-boreal.jpg",
                "followup": {
                    "pergunta": "Como o Sol vai morrer e o que acontece com a Terra?",
                    "proxima_tag": "sol",
                    "proximo_hint": "morte do sol"
                }
            },
            {
                "match_hints": ["morte do sol", "como morre", "futuro do sol", "gigante vermelha", "daqui a"],
                "text": (
                    "Daqui a cerca de 5 bilhões de anos, o Sol vai esgotar o hidrogênio no núcleo.\n\n"
                    "Ele vai se expandir e virar uma gigante vermelha, engolindo Mercúrio, Vênus e provavelmente a Terra.\n\n"
                    "Depois, as camadas externas serão expulsas formando uma nebulosa planetária colorida. O que sobra é uma anã branca, um núcleo quente do tamanho da Terra que vai esfriar por trilhões de anos."
                ),
                "imagem": "img/gigante-vermelha.jpg",
                "followup": {
                    "pergunta": "Quer conhecer os planetas que orbitam o Sol, começando pelo mais próximo?",
                    "proxima_tag": "mercurio",
                    "proximo_hint": "o que e"
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
            "primeiro planeta", "primeiro planeta do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Mercúrio é o primeiro planeta do sistema solar, além de ser o menor e o mais próximo do Sol. Tem apenas 4.879 km de diâmetro, pouco maior que a Lua.\n\n"
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
                "match_hints": ["dia e ano", "rotacao", "orbita", "tempo", "lento"],
                "text": (
                    "Mercúrio tem uma das rotações mais lentas do sistema solar. Um dia dura 176 dias terrestres.\n\n"
                    "Mas um ano mercuriano leva apenas 88 dias terrestres. Então um dia em Mercúrio é literalmente mais longo do que um ano lá.\n\n"
                    "A NASA estudou Mercúrio de perto com a missão MESSENGER, que orbitou o planeta de 2011 a 2015."
                ),
                "imagem": "img/mercurio-superficie.jpg",
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
            "venus", "vênus", "planeta venus", "sobre venus",
            "segundo planeta", "segundo planeta do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Vênus é o segundo planeta do sistema solar e o mais brilhante no céu noturno. É quase do mesmo tamanho que a Terra, por isso é chamado de planeta irmão.\n\n"
                    "Sua atmosfera é 96% dióxido de carbono com nuvens de ácido sulfúrico. A pressão na superfície é 92 vezes maior que na Terra, equivalente a 900 metros de profundidade no oceano."
                ),
                "imagem": "img/Vênus.png",
                "followup": {
                    "pergunta": "Vênus é o planeta mais quente do sistema solar. Quer entender por quê?",
                    "proxima_tag": "venus",
                    "proximo_hint": "mais quente"
                }
            },
            {
                "match_hints": ["mais quente", "temperatura", "calor", "efeito estufa"],
                "text": (
                    "A temperatura na superfície de Vênus chega a 465°C, quente o suficiente para derreter chumbo.\n\n"
                    "E é constante: não importa o dia ou a noite, o polo ou o equador.\n\n"
                    "O culpado é um efeito estufa extremo: a atmosfera densa de CO₂ aprisiona o calor do Sol. Isso faz de Vênus mais quente que Mercúrio, mesmo estando mais longe do Sol."
                ),
                "imagem": "img/venus-superficie.jpg",
                "followup": {
                    "pergunta": "Sabia que Vênus gira ao contrário dos outros planetas e muito devagar?",
                    "proxima_tag": "venus",
                    "proximo_hint": "rotacao inversa"
                }
            },
            {
                "match_hints": ["rotacao inversa", "gira ao contrario", "dia longo", "rotacao"],
                "text": (
                    "Vênus é um planeta peculiar na sua rotação. Ele gira no sentido horário, ao contrário da maioria dos planetas.\n\n"
                    "E gira muito devagar: um dia em Vênus dura 243 dias terrestres, mais longo que o seu próprio ano, que dura 225 dias terrestres.\n\n"
                    "A razão dessa rotação invertida ainda é debatida e pode ter sido uma colisão catastrófica no passado."
                ),
                "imagem": "img/venus-rotacao.jpg",
                "followup": {
                    "pergunta": "Vamos para a Terra, nosso planeta tem algumas curiosidades surpreendentes também.",
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
            "campo magnetico da terra", "atmosfera da terra",
            "terceiro planeta", "terceiro planeta do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
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
                "match_hints": ["lua", "satelite", "unico satelite", "quanto tempo", "formacao da lua"],
                "text": (
                "A Terra é o único planeta rochoso do sistema solar com um satélite natural tão grande em proporção ao seu tamanho.\n\n"
                "A Lua exerce uma influência enorme sobre a Terra: estabiliza a inclinação do eixo terrestre, o que mantém o clima previsível ao longo de milhões de anos.\n\n"
                "Sem a Lua, o eixo da Terra oscilaria de forma caótica, tornando o clima extremamente instável e dificultando o surgimento de vida complexa."
                ),
                "imagem": "img/terra-lua.jpg",
                "followup": {
                "pergunta": "Quer saber como a Lua se formou e qual foi o impacto que a criou?",
                "proxima_tag": "lua",
                "proximo_hint": "formacao"
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
            "quarto planeta", "quarto planeta do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Marte é o quarto planeta do sistema solar, chamado de Planeta Vermelho pela cor do óxido de ferro no solo. Tem metade do diâmetro da Terra e uma atmosfera mais fina.\n\n"
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
                    "O Olympus Mons é o maior vulcão do sistema solar: 22 km de altura e 600 km de diâmetro. Para comparar, o Everest tem 8,8 km.\n\n"
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
                    "Em Marte, a temperatura média é de -60°C, a atmosfera é irrespirável e as tempestades de poeira podem durar meses. A NASA planeja missões tripuladas para a década de 2030, mas ainda há muito a resolver."
                ),
                "imagem": "img/marte-colonizacao.jpg",
                "followup": {
                    "pergunta": "Quer conhecer Júpiter, o maior planeta do sistema solar?",
                    "proxima_tag": "jupiter",
                    "proximo_hint": "o que e"
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
            "grande mancha vermelha", "luas de jupiter", "europa lua",
            "io lua", "ganimedes", "quinto planeta", "quinto planeta do sistema solar", "maior planeta", "maior planeta do sistema solar", "planeta gigante", "gigante gasoso"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Júpiter é o quinto e maior planeta do sistema solar, com 11 vezes o diâmetro da Terra e mais massivo que todos os outros planetas juntos.\n\n"
                    "É um gigante gasoso composto principalmente de hidrogênio e hélio.\n\n"
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
                "match_hints": ["grande mancha", "tempestade", "mancha vermelha"],
                "text": (
                    "A Grande Mancha Vermelha é uma tempestade anticiclônica que existe há pelo menos 350 anos.\n\n"
                    "Tem ventos de até 640 km/h e um tamanho maior que a Terra inteira.\n\n"
                    "Curiosamente, ela tem encolhido nas últimas décadas. A NASA acompanha esse fenômeno com a sonda Juno, que orbita Júpiter desde 2016."
                ),
                "imagem": "img/grande-mancha-vermelha.jpg",
                "followup": {
                    "pergunta": "Júpiter tem 95 luas confirmadas. Algumas delas são mundos fascinantes. Quer saber?",
                    "proxima_tag": "jupiter",
                    "proximo_hint": "luas"
                }
            },
            {
                "match_hints": ["luas", "europa", "io", "ganimedes", "calisto"],
                "text": (
                    "As quatro maiores luas de Júpiter foram descobertas por Galileu em 1610.\n\n"
                    "Io é o objeto mais vulcanicamente ativo do sistema solar, com mais de 400 vulcões ativos.\n\n"
                    "Europa tem um oceano líquido debaixo de uma camada de gelo, aquecido pelas forças de maré de Júpiter. É um dos candidatos mais promissores à vida. Ganimedes é a maior lua do sistema solar, maior até que Mercúrio."
                ),
                "imagem": ["img/europa-lua.jpg", "img/io-lua.jpg"],
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
            "aneis de saturno", "anéis de saturno", "titan lua",
            "sexto planeta", "sexto planeta do sistema solar", "segundo maior planeta", "segundo maior planeta do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Saturno é o sexto planeta e o segundo maior do sistema solar, famoso pelos seus impressionantes anéis.\n\n"
                    "É um gigante gasoso com densidade tão baixa que flutuaria na água, se houvesse um oceano grande o suficiente.\n\n"
                    "Um dia dura 10h 33min e um ano tem 29 anos terrestres. Saturno tem pelo menos 146 luas confirmadas, o maior número do sistema solar."
                ),
                "imagem": "img/Saturno.png",
                "followup": {
                    "pergunta": "Os anéis de Saturno são uma das maravilhas do sistema solar. Quer entendê-los?",
                    "proxima_tag": "saturno",
                    "proximo_hint": "aneis"
                }
            },
            {
                "match_hints": ["aneis", "anéis", "composicao dos aneis", "de que sao feitos"],
                "text": (
                    "Os anéis de Saturno são compostos de partículas de gelo e rocha, do tamanho de grãos até o de casas.\n\n"
                    "Se espalhados, cobriam a distância da Terra à Lua. Mas são incrivelmente finos, apenas 10 a 100 metros de espessura em relação ao diâmetro de 270.000 km.\n\n"
                    "A missão Cassini da NASA orbitou Saturno de 2004 a 2017 e revelou que os anéis são relativamente jovens, entre 10 e 100 milhões de anos."
                ),
                "imagem": "img/aneis-saturno.jpg",
                "followup": {
                    "pergunta": "A lua Titan de Saturno é única, tem atmosfera densa e lagos de metano líquido. Quer saber mais?",
                    "proxima_tag": "saturno",
                    "proximo_hint": "titan"
                }
            },
            {
                "match_hints": ["titan", "lua titan", "metano", "lagos"],
                "text": (
                    "Titan é a segunda maior lua do sistema solar e a única com atmosfera densa.\n\n"
                    "Sua atmosfera é principalmente nitrogênio, parecida com a da Terra primordial. Na superfície, existem lagos e rios de metano e etano líquidos.\n\n"
                    "A NASA enviou a missão Dragonfly para explorar Titan, uma espécie de drone nuclear que vai pousar lá na década de 2030. Encélado, outra lua de Saturno, jorra vapor de água com compostos orgânicos para o espaço."
                ),
                "imagem": ["img/titan-lua.jpg", "img/enceladus.jpg"],
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
            "setimo planeta", "sétimo planeta", "setimo planeta do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Urano é o sétimo planeta do sistema solar e o primeiro dos gigantes de gelo.\n\n"
                    "Tem 4 vezes o diâmetro da Terra e é composto principalmente de água, metano e amônia no estado gelado.\n\n"
                    "O metano na atmosfera absorve a luz vermelha e reflete a azul-esverdeada, por isso sua cor característica."
                ),
                "imagem": "img/Urano.png",
                "followup": {
                    "pergunta": "Urano tem uma peculiaridade única: ele gira praticamente de lado. Sabe por quê?",
                    "proxima_tag": "urano",
                    "proximo_hint": "eixo inclinado"
                }
            },
            {
                "match_hints": ["eixo inclinado", "gira de lado", "inclinacao", "colisao"],
                "text": (
                    "O eixo de Urano é inclinado 98 graus em relação à sua órbita, ele praticamente rola ao redor do Sol.\n\n"
                    "A causa mais aceita é uma colisão com um objeto do tamanho da Terra no passado distante.\n\n"
                    "Isso cria estações extremas: cada polo fica 42 anos em luz solar contínua e 42 anos em escuridão total. Também tem 28 luas, todas batizadas com nomes de personagens de Shakespeare e Alexander Pope."
                ),
                "imagem": "img/urano-eixo.jpg",
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
            "planeta mais distante", "tritao lua",
            "oitavo planeta", "oitavo planeta do sistema solar", "planeta ventoso", "gigante de gelo netuno", "planeta azul escuro", "planeta mais distante do sistema solar"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre", "qual", "qual e"],
                "text": (
                    "Netuno é o oitavo e mais distante planeta do sistema solar.\n\n"
                    "Fica a 30 vezes a distância Terra-Sol e leva 165 anos terrestres para completar uma órbita.\n\n"
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
                "match_hints": ["tritao", "tritão", "lua de netuno", "lua retrograda"],
                "text": (
                    "Tritão é a maior lua de Netuno e tem uma característica única: orbita no sentido contrário à rotação de Netuno.\n\n"
                    "Isso sugere que ele foi capturado pelo campo gravitacional de Netuno e não se formou junto com o planeta.\n\n"
                    "Tritão tem temperatura de -235°C e geysers de nitrogênio na superfície, os mais frios já observados no sistema solar. Com o tempo, a órbita de Tritão vai decair e ele será destruído pelas forças de maré, formando um anel."
                ),
                "imagem": "img/tritao.jpg",
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
    # LUA
    # -------------------------------------------------------------------------
    {
        "tag": "lua",
        "patterns": [
            "lua", "mare", "maré", "eclipse", "missao apollo", "missão apollo",
            "armstrong", "lua cheia", "fases da lua", "crateras",
            "como a lua se formou", "origem da lua"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "sobre"],
                "text": (
                    "A Lua é o único satélite natural da Terra e o quinto maior do sistema solar.\n\n"
                    "Tem 3.474 km de diâmetro, cerca de um quarto da Terra.\n\n"
                    "A Lua está em rotação síncrona com a Terra: completa uma rotação no mesmo tempo que orbita o planeta. Por isso sempre vemos a mesma face dela."
                ),
                "imagem": "img/lua.jpg",
                "followup": {
                    "pergunta": "Como a Lua se formou? A história é mais dramática do que parece.",
                    "proxima_tag": "lua",
                    "proximo_hint": "formacao"
                }
            },
            {
                "match_hints": ["formacao", "como se formou", "origem", "nasceu"],
                "text": (
                    "A hipótese mais aceita é a do Grande Impacto.\n\n"
                    "Há 4,5 bilhões de anos, um objeto do tamanho de Marte, chamado Theia, colidiu com a Terra jovem.\n\n"
                    "Os detritos da colisão foram ejetados para órbita e se acumularam formando a Lua. A Lua está se afastando da Terra a 3,8 cm por ano. Quando os dinossauros viviam, os dias terrestres tinham 23 horas."
                ),
                "imagem": "img/formacao-lua.jpg",
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
                "match_hints": ["artemis", "volta a lua", "retorno", "futuro da lua"],
                "text": (
                    "O programa Artemis da NASA tem como objetivo retornar humanos à Lua, desta vez para ficar.\n\n"
                    "A meta é estabelecer uma presença sustentável com a Gateway, uma estação espacial em órbita lunar.\n\n"
                    "O programa prevê levar a primeira mulher e a primeira pessoa negra à superfície lunar. A Lua também serve como trampolim para Marte, testando tecnologias e experiência operacional num ambiente próximo."
                ),
                "imagem": "img/artemis.jpg",
                "followup": {
                    "pergunta": "Quer explorar mais sobre o sistema solar ou partir para temas como galáxias e o Big Bang?",
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
            "planetas fora do sistema solar", "trappist", "kepler",
            "planeta habitavel", "zona habitavel", "goldilocks"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica"],
                "text": (
                    "Exoplanetas são planetas que orbitam outras estrelas, fora do nosso sistema solar.\n\n"
                    "A NASA confirmou mais de 5.700 deles e estima que cada estrela da galáxia tenha em média um planeta.\n\n"
                    "Isso significa centenas de bilhões de planetas só na Via Láctea."
                ),
                "imagem": "img/exoplanetas.jpg",
                "followup": {
                    "pergunta": "Como detectamos planetas a anos-luz de distância sem conseguir vê-los diretamente?",
                    "proxima_tag": "exoplanetas",
                    "proximo_hint": "como detecta"
                }
            },
            {
                "match_hints": ["como detecta", "metodo", "transito", "como encontra", "telescopio"],
                "text": (
                    "O método mais usado é o de trânsito: quando um planeta passa na frente da estrela, a luz dela diminui ligeiramente.\n\n"
                    "O telescópio Kepler usou esse método e encontrou mais de 2.600 planetas.\n\n"
                    "O James Webb Space Telescope vai além e consegue analisar a atmosfera dos exoplanetas. Ao filtrar a luz da estrela que passa pela atmosfera do planeta, identifica moléculas como água, metano ou CO₂."
                ),
                "imagem": "img/transito-exoplaneta.jpg",
                "followup": {
                    "pergunta": "Quer saber sobre o sistema TRAPPIST-1, um dos candidatos mais promissores à vida fora da Terra?",
                    "proxima_tag": "exoplanetas",
                    "proximo_hint": "trappist"
                }
            },
            {
                "match_hints": ["trappist", "sistema trappist", "trappist-1"],
                "text": (
                    "TRAPPIST-1 é um sistema a 40 anos-luz da Terra com 7 planetas rochosos do tamanho da Terra.\n\n"
                    "Três deles estão na zona habitável, a distância ideal da estrela para ter água líquida na superfície.\n\n"
                    "A estrela é uma anã vermelha fria, muito menor que o Sol. O James Webb já detectou que pelo menos um dos planetas pode ter atmosfera, uma descoberta histórica."
                ),
                "imagem": "img/trappist.jpg",
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
                    "Vênus está na zona habitável do Sol e é um inferno de 465°C. O que importa é a combinação de atmosfera, composição e geologia."
                ),
                "imagem": "img/zona-habitavel.jpg",
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
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "somos sozinhos", "existe"],
                "text": (
                    "A questão da vida extraterrestre é uma das mais profundas da ciência.\n\n"
                    "Matematicamente, parece impossível que sejamos sozinhos. Existem mais estrelas no universo observável do que grãos de areia em todas as praias da Terra.\n\n"
                    "A NASA catalogou mais de 5.700 exoplanetas, muitos em zonas habitáveis."
                ),
                "imagem": "img/vida-extraterrestre.jpg",
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
                    "Algumas hipóteses para o silêncio: talvez vida inteligente seja rara, ou civilizações se autodestruam, ou as distâncias são grandes demais para comunicação."
                ),
                "imagem": "img/paradoxo-fermi.jpg",
                "followup": {
                    "pergunta": "Onde no sistema solar buscamos vida hoje?",
                    "proxima_tag": "vida_extraterrestre",
                    "proximo_hint": "onde buscar"
                }
            },
            {
                "match_hints": ["onde buscar", "marte", "europa", "enceladus", "candidatos"],
                "text": (
                    "Os candidatos mais promissores à vida estão bem perto de nós.\n\n"
                    "Marte: o rover Perseverance coleta amostras de antigas regiões lacustres em busca de biossinaturas.\n\n"
                    "Europa, lua de Júpiter, tem um oceano líquido debaixo do gelo, aquecido por forças de maré, com condições favoráveis à vida microbiana. Encélado, lua de Saturno, jorra vapor de água com compostos orgânicos para o espaço."
                ),
                "imagem": ["img/europa-oceano.jpg", "img/enceladus-jato.jpg"],
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
                    "Implicaria que o universo está provavelmente repleto de vida em diferentes formas. A NASA e a ESA buscam ativamente biossinaturas, moléculas ou padrões que indiquem processos biológicos."
                ),
                "imagem": "img/biossinatura.jpg",
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
            "cometa", "cometas", "asteroide", "asteroides", "meteoro", "meteoros",
            "meteorito", "meteoritos", "diferenca cometa asteroide",
            "chuva de meteoros", "estrela cadente", "chuva de estrelas",
            "missao dart", "cinturao de asteroides"
        ],
        "responses": [
            {
                "match_hints": ["asteroide", "o que e asteroide", "o que é asteroide", "defin", "conceito", "explica", "diferenca"],
                "text": (
                    "Asteroide é uma rocha que orbita o Sol, geralmente no cinturão entre Marte e Júpiter.\n\n"
                ),
                "imagem": "img/asteroide.jpg",
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
                "imagem": "img/cometa.jpg",
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
                "imagem": "img/meteoro.jpg",
                "followup": {
                    "pergunta": "Quer saber mais sobre o Cinturão de Asteroides, onde a maioria desses corpos orbita?",
                    "proxima_tag": "cometas_asteroides",
                    "proximo_hint": "cinturao"
                }
            },
            {
                "match_hints": ["dinossauros", "extincao", "impacto", "chicxulub"],
                "text": (
                    "Há 66 milhões de anos, um asteroide de cerca de 10 km colidiu na região do atual México, criando a cratera de Chicxulub.\n\n"
                    "O impacto liberou uma energia bilhões de vezes maior que qualquer bomba nuclear.\n\n"
                    "Incêndios globais, uma camada de fumaça bloqueando o Sol e um inverno castigoso resultaram na extinção de 76% das espécies. Essa extinção abriu espaço para os mamíferos e eventualmente para nós."
                ),
                "imagem": "img/chicxulub.jpg",
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
                "imagem": "img/missao-dart.jpg",
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
            "velocidade da luz", "wormhole", "buraco de minhoca", "viagem no tempo"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "relatividade", "einstein"],
                "text": (
                    "Einstein propôs que espaço e tempo não são fixos: eles formam um tecido único chamado espaço-tempo.\n\n"
                    "Massa e energia curvam esse tecido, e essa curvatura é o que chamamos de gravidade.\n\n"
                    "O GPS do seu celular depende de correções relativísticas. Sem elas, erraria mais de 10 km por dia, pois os satélites em órbita estão num campo gravitacional menor e o tempo passa mais rápido para eles."
                ),
                "imagem": "img/espaco-tempo.jpg",
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
                    "Se você viajasse a 99,9% da velocidade da luz por um ano, voltaria para encontrar décadas passadas na Terra. Não é ficção científica. É a relatividade especial de Einstein, confirmada inúmeras vezes."
                ),
                "imagem": "img/dilatacao-tempo.jpg",
                "followup": {
                    "pergunta": "Wormholes seriam atalhos no espaço-tempo. Eles poderiam existir de verdade?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "wormhole"
                }
            },
            {
                "match_hints": ["wormhole", "buraco de minhoca", "atalho", "viagem no tempo"],
                "text": (
                    "Wormholes são matematicamente permitidos pelas equações da Relatividade Geral.\n\n"
                    "Seriam pontes conectando dois pontos distantes do espaço-tempo.\n\n"
                    "O problema: para existir de forma estável, precisariam de energia exótica com pressão negativa. Não temos evidência de que isso existe na natureza. Viagem no tempo para o futuro é possível pela dilatação do tempo. Para o passado, ainda é especulação teórica."
                ),
                "imagem": "img/wormhole.jpg",
                "followup": {
                    "pergunta": "Quer explorar outro tema? Posso falar sobre buracos negros, galáxias ou o Big Bang.",
                    "proxima_tag": None,
                    "proximo_hint": None
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
                "match_hints": ["o que", "o que e", "signific", "defin", "conceito"],
                "text": (
                    "Um ano-luz é a distância que a luz percorre em um ano, equivalente a aproximadamente 9,46 trilhões de quilômetros.\n\n"
                    "A estrela mais próxima da Terra, Proxima Centauri, fica a 4,24 anos-luz. Isso significa que a luz que sai dela leva mais de 4 anos para chegar aqui.\n\n"
                    "Quando você olha para o céu, está vendo o passado."
                ),
                "imagem": "img/proxima-centauri.jpg",
                "followup": {
                    "pergunta": "Por que a velocidade da luz é um limite para o universo?",
                    "proxima_tag": "ano_luz",
                    "proximo_hint": "limite da luz"
                }
            },
            {
                "match_hints": ["limite da luz", "velocidade da luz", "por que nao pode", "mais rapido"],
                "text": (
                    "A velocidade da luz, cerca de 300 mil km/s, é o limite de velocidade do universo.\n\n"
                    "Não por convenção, mas porque a física impõe isso. À medida que um objeto acelera, sua massa aumenta relativisticamente.\n\n"
                    "Para atingir a velocidade da luz, precisaria de energia infinita, o que é impossível. Só partículas sem massa, como fótons, conseguem viajar à velocidade da luz."
                ),
                "imagem": "img/velocidade-luz.jpg",
                "followup": {
                    "pergunta": "Quer entender a dilatação do tempo, o que acontece quando você chega perto dessa velocidade?",
                    "proxima_tag": "espaco_tempo",
                    "proximo_hint": "dilatacao do tempo"
                }
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SISTEMA SOLAR (geral)
    # -------------------------------------------------------------------------
    {
        "tag": "sistema_solar",
        "patterns": [
            "sistema solar", "nosso sistema solar", "como se formou o sistema solar",
            "origem do sistema solar", "quantos planetas tem o sistema solar",
            "orbita dos planetas", "sol e planetas"
        ],
        "responses": [
            {
                "match_hints": ["o que", "o que e", "defin", "conceito", "explica", "como se formou", "origem"],
                "text": (
                    "O sistema solar se formou há 4,6 bilhões de anos a partir de uma nuvem de gás e poeira chamada nebulosa solar.\n\n"
                    "A gravidade fez a nuvem colapsar. O centro concentrou 99,8% da massa e virou o Sol.\n\n"
                    "O restante formou um disco giratório de onde surgiram os planetas, luas, asteroides e cometas. Hoje temos 8 planetas oficiais. Plutão foi rebaixado a planeta anão em 2006."
                ),
                "imagem": "img/sistema-solar.jpg",
                "followup": {
                    "pergunta": "Quer explorar os planetas um a um, começando pelo mais próximo do Sol?",
                    "proxima_tag": "mercurio",
                    "proximo_hint": "o que e"
                }
            },
            {
                "match_hints": ["composicao", "massa", "sol", "jupiter", "cinturao"],
                "text": (
                    "O Sol contém 99,8% de toda a massa do sistema solar.\n\n"
                    "Júpiter, o maior planeta, tem mais massa do que todos os outros planetas juntos.\n\n"
                    "Entre Marte e Júpiter existe o Cinturão de Asteroides, com milhões de rochas. Além de Netuno começa o Cinturão de Kuiper, onde Plutão orbita junto com outros objetos gelados."
                ),
                "imagem": "img/sistema-solar-composicao.jpg",
                "followup": {
                    "pergunta": "Quer saber como os planetas se movem e por que não saem de suas órbitas?",
                    "proxima_tag": "sistema_solar",
                    "proximo_hint": "orbitas"
                }
            },
            {
                "match_hints": ["orbitas", "orbita", "giram", "movem", "gravitacao"],
                "text": (
                    "Os planetas orbitam o Sol porque herdaram o movimento giratório da nebulosa que formou o sistema solar.\n\n"
                    "Quando a nuvem de gás colapsou, ela começou a girar mais rápido, como uma bailarina que fecha os braços.\n\n"
                    "A gravidade do Sol os mantém em órbita: a força centrífuga e a atração gravitacional se equilibram perfeitamente. Esse equilíbrio é tão estável que os planetas orbitam assim há 4,6 bilhões de anos."
                ),
                "imagem": "img/orbitas-planetas.jpg",
                "followup": {
                    "pergunta": "Quer conhecer algum planeta específico ou explorar outros temas?",
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
