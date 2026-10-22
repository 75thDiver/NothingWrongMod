# Nothing Wrong 0.24 — справочник механик с исходным кодом

Документ подготовлен для независимого куратора, у которого нет доступа к ZIP. Это не пересказ архива: ниже приведены реальные фрагменты текущего кода и точные пути к файлам внутри `NothingWrongMod`. Фрагменты сокращены только там, где прямо сказано «схематично»; проверяйте указанные исходники целиком, если потребуется проектировать совместимые изменения.

## Как читать документ

- **Реализовано** — это уже находится в сборке 0.24.
- **Канон/замысел** — описание мира и желаемого направления; это не обещание реализованной механики.
- **Не проверено движком** — статическая проверка кода не заменяет запуск HOI4, просмотр GUI и `error.log`.
- Куратор должен оценить, что стоит переработать, сохранить или заменить. Этот документ не предписывает ему конкретное новое дерево фокусов.

## Краткая карта текущих систем

| Страна/система | Где реализовано | Что делает сейчас |
|---|---|---|
| Германия: парламент Рейхстага | `common/scripted_effects/14_nw_mechanics.txt`, `common/scripted_guis/14_nw_parliament.txt`, `interface/14_nw_parliament.gui`, `interface/14_nw_parliament.gfx`, `common/decisions/14_nw_decisions.txt`, `common/national_focus/14_nw_GER.txt` | Переменные мест, коалиция, напряжение, решения партий; отдельный интерфейс на 397 мест. Единственная страна с такой парламентской механикой. |
| Россия: болезнь Алексея II и выбор режима | `history/general/zzz_nw14_national_mechanics.txt`, `common/national_focus/14_nw_SOV.txt`, `events/14_nw_politics.txt`, `common/scripted_effects/14_nw_mechanics.txt`, `common/scripted_effects/24_nw_alexei.txt`, `events/24_nw_alexei.txt` | Переменные здоровья, доверия, лояльности армии и оппозиции; событие выбора монархического, республиканского или ультраправого направления; отдельные события стабилизации Алексея в 0.24. |
| Россия: восстание и фрагментация | `events/14_nw_politics.txt`, `common/decisions/14_nw_decisions.txt`, `common/scripted_effects/14_nw_mechanics.txt` | `nw14.20` начинает многосторонний сценарий; при отсрочке выставляется флаг, а решение позволяет вызвать событие повторно. |
| Австрийская федерация | `common/autonomous_states/01_nw_federal_part.txt`, `history/general/zz_nw_1936_scenario.txt`, `history/countries/{HUN,CRO,CZE}...`, `common/decisions/14_nw_decisions.txt`, `events/14_nw_politics.txt` | Венгрия, Хорватия и Богемо-Галицкое королевство — субъекты AUS с высоким уровнем автономии; Австрия может повышать доверие и запрашивать/обновлять согласие субъектов. |
| Маньчжурский кондоминиум | `history/countries/MAN - Manchukou.txt`, `history/general/zz_nw_1936_scenario.txt` | MAN — не марионетка, но ограниченная комиссия под совместным давлением России и Японии; запрещены объявление войны и ряд дипломатических действий, у обеих держав есть военный доступ. |
| Стартовые механики | `history/general/zzz_nw14_national_mechanics.txt`, истории стран и `zz_nw_1936_scenario.txt` | Основные переменные/фокус-деревья и стартовая дипломатия создаются в истории, а не глобальным `on_action`. |

---

## 1. Германия: парламент Рейхстага

### Игровой смысл и стартовое распределение

Парламент в стране GER — отдельная внутриигровая система. Стартует коалиция СДПГ и КПГ; остальные мандаты распределены между Центром, Прогрессивной народной партией и НННП. Всего 397 мест: коалиция имеет 220. Парламентская диаграмма строится из тех же переменных, что используются для расчёта коалиции.

Начальные значения: КПГ 70, НСДПГ 0, СДПГ 150, Центр 60, ПНП/FVP 47, НННП/DNVP 70, вакансии 0; напряжение 30. Флаги `nw_coal_spd` и `nw_coal_kpd` включают партии в коалиционный подсчёт.

### Код: инициализация

Источник: `common/scripted_effects/14_nw_mechanics.txt`, блок `nw14_ger_init`.

```hoi4
nw14_ger_init = {
    set_variable = { nw_kpd = 70 }
    set_variable = { nw_uspd = 0 }
    set_variable = { nw_spd = 150 }
    set_variable = { nw_centre = 60 }
    set_variable = { nw_fvp = 47 }
    set_variable = { nw_dnvp = 70 }
    set_variable = { nw_vacant = 0 }
    set_variable = { nw_tension = 30 }
    set_variable = { nw_network = 0 }
    set_variable = { nw_army_support = 0 }
    set_country_flag = nw_coal_spd
    set_country_flag = nw_coal_kpd
    nw14_recount = yes
    set_country_flag = nw_parliament_active
}
```

Включение механики для GER происходит стартовым history-скриптом:

Источник: `history/general/zzz_nw14_national_mechanics.txt`.

```hoi4
GER = {
    nw14_ger_init = yes
    set_party_name = {
        ideology = democratic
        name = NW14_GER_start_democratic
        long_name = NW14_GER_start_democratic_long
    }
    set_party_name = {
        ideology = communism
        name = NW14_kpd_party
        long_name = NW14_kpd_party_long
    }
    load_focus_tree = { tree = NW14_GER_tree keep_completed = no }
}
```

### Расчёт коалиции и отображение мест

`nw14_recount` суммирует места каждой партии и добавляет их к `nw_votes`, только если установлен коалиционный флаг. Затем формируются накопительные границы партий и 397 переменных мест (`nw_seat_1` … `nw_seat_397`), которые интерфейс переводит в кадры цветов партий. Ниже — начало реального алгоритма, не весь повторяющийся список 397 мест.

Источник: `common/scripted_effects/14_nw_mechanics.txt`, блок `nw14_recount`.

```hoi4
nw14_recount = {
    set_variable = { nw_votes = 0 }
    set_variable = { nw_total = 0 }

    add_to_variable = { var = nw_total value = nw_kpd }
    if = {
        limit = { has_country_flag = nw_coal_kpd }
        add_to_variable = { var = nw_votes value = nw_kpd }
    }

    add_to_variable = { var = nw_total value = nw_uspd }
    if = {
        limit = { has_country_flag = nw_coal_uspd }
        add_to_variable = { var = nw_votes value = nw_uspd }
    }

    add_to_variable = { var = nw_total value = nw_spd }
    if = {
        limit = { has_country_flag = nw_coal_spd }
        add_to_variable = { var = nw_votes value = nw_spd }
    }

    # Аналогично для nw_centre, nw_fvp, nw_dnvp и nw_vacant.

    set_variable = { nw_end_kpd = nw_kpd }
    set_variable = { nw_end_uspd = nw_uspd }
    add_to_variable = { var = nw_end_uspd value = nw_end_kpd }
    set_variable = { nw_end_spd = nw_spd }
    add_to_variable = { var = nw_end_spd value = nw_end_uspd }

    # Для каждого кресла выбирается первая партия,
    # чей накопительный порог ещё выше номера кресла.
    if = {
        limit = { check_variable = { nw_end_kpd > 0 } }
        set_variable = { nw_seat_1 = 1 }
    }
    else_if = {
        limit = { check_variable = { nw_end_uspd > 0 } }
        set_variable = { nw_seat_1 = 2 }
    }
    else_if = {
        limit = { check_variable = { nw_end_spd > 0 } }
        set_variable = { nw_seat_1 = 3 }
    }
    # Повторяется для кресел 2–397 и остальных партий.
}
```

Интерфейс доступен только Германии при активном парламентском флаге:

Источник: `common/scripted_guis/14_nw_parliament.txt`.

```hoi4
scripted_gui = {
    nw14_reichstag_gui = {
        context_type = decision_category
        window_name = "nw14_reichstag_window"
        visible = {
            tag = GER
            has_country_flag = nw_parliament_active
        }
        properties = {
            seat_1 = { frame = nw_seat_1 }
            seat_2 = { frame = nw_seat_2 }
            # ... вплоть до seat_397
        }
    }
}
```

Полный GUI-расклад находится в `interface/14_nw_parliament.gui` и `.gfx`; отображение зависит от `nw_seat_1` … `nw_seat_397`. Категория решений также ограничена GER.

### Напряжение и политический тупик

Месячный scripted effect увеличивает `nw_tension` на 2, пока Германия не пометила проблему урегулированной. При значении выше 69 добавляется дух тупика `nw14_deadlock`. Иные ветки парламентской логики меняют партии/коалицию через решения и события.

Источник: `common/scripted_effects/14_nw_mechanics.txt`, блок `nw14_monthly`.

```hoi4
if = {
    limit = {
        tag = GER
        has_country_flag = nw_parliament_active
    }
    if = {
        limit = { NOT = { has_country_flag = nw_ger_settled } }
        add_to_variable = { var = nw_tension value = 2 }
        clamp_variable = { var = nw_tension min = 0 max = 100 }
    }
    if = {
        limit = { check_variable = { nw_tension > 69 } }
        if = {
            limit = { NOT = { has_idea = nw14_deadlock } }
            add_ideas = nw14_deadlock
        }
    }
    else = { remove_ideas = nw14_deadlock }
}
```

Ветка коммунистической революции использует `nw14_ger_fragmentation`: снимает парламентские духи/флаг интерфейса, меняет правительство и запускает распад на социалистический центр, королевскую сторону, Баварию и польское сопротивление; Франция возвращает Эльзас-Лотарингию. Исходник объёмный и содержит точное распределение штатов, лидеров, OOB и пар войн; смотреть целиком `common/scripted_effects/14_nw_mechanics.txt`, блок `nw14_ger_fragmentation`.

---

## 2. Россия: переменные, кризис престола и выбор политического курса

### Начальные переменные

Источник: `history/general/zzz_nw14_national_mechanics.txt`.

```hoi4
SOV = {
    set_variable = { nw_health = 45 }
    set_variable = { nw_trust = 45 }
    set_variable = { nw_army_loyalty = 45 }
    set_variable = { nw_opposition = 0 }
    load_focus_tree = { tree = NW14_SOV_tree keep_completed = no }
}
```

Пока Алексей не умер и не восстановился, месячный эффект уменьшает здоровье на 1. Низкое доверие включает негативный дух провинциального недоверия. Австрийское доверие и венгерская лояльность тоже проверяются тем же месячным скриптом; полный `nw14_monthly` расположен в `common/scripted_effects/14_nw_mechanics.txt`.

### Событие выбора курса

Фокус `NW14_SOV_royal_bulletin` запускает `nw14.70`. Это событие устанавливает флаг пути и корректирует соответствующую переменную. Оно предлагает лечение и сохранение престола, подготовку регентства Кирилла Владимировича, республику/Учредительное собрание или инициативу Чёрной сотни.

Источник: `events/14_nw_politics.txt`, `nw14.70`.

```hoi4
country_event = {
    id = nw14.70
    title = nw14.70.t
    desc = nw14.70.d
    is_triggered_only = yes

    option = {
        name = nw14.70.a
        set_country_flag = nw_rus_path_recovery
        add_to_variable = { var = nw_health value = 5 }
        clamp_variable = { var = nw_health min = 0 max = 100 }
        add_stability = 0.03
    }

    option = {
        name = nw14.70.b
        set_country_flag = nw_rus_kirill_path
        add_to_variable = { var = nw_army_loyalty value = 10 }
        clamp_variable = { var = nw_army_loyalty min = 0 max = 100 }
    }

    option = {
        name = nw14.70.c
        set_country_flag = nw_rus_republic
        add_to_variable = { var = nw_opposition value = 15 }
        clamp_variable = { var = nw_opposition min = 0 max = 100 }
    }

    option = {
        name = nw14.70.e
        set_country_flag = nw_rus_blackhundred_path
        add_to_variable = { var = nw_army_loyalty value = 15 }
        clamp_variable = { var = nw_army_loyalty min = 0 max = 100 }
        add_stability = -0.02
    }
}
```

Это **не** полный сценарий русской монархии. В 0.24 добавлены уточняющие события закрепления исхода и управления двором:

- `events/24_nw_alexei.txt`: `nw24.1` — выбор личного управления или делегированного кабинета; `nw24.2` — уведомление о закреплённом исходе; `nw24.3` — голос субъекта по хартии; `nw24.4` — ответ российского центра.
- `common/scripted_effects/24_nw_alexei.txt`: `nw24_reorganize_cabinet`, `nw24_offer_charters`, `nw24_refresh_compact`, `nw24_finalize_crown`.
- Переменная здоровья влияет на выбор итогового духа монархии; часть эффектов зависит от подписи хартии Польшей или Финляндией.

Для ревью этих переходов читать оба файла целиком: они небольшие и взаимосвязаны. Важная деталь: приглашение к хартии отправляется только если POL/FIN в этот момент являются субъектами SOV; подписавший субъект поднимает `nw_trust` России на 5, отказ снижает его на 5.

---

## 3. Россия: республиканская подготовка, отсрочка и гражданская война

### Событие смерти и отложенный запуск

Событие `nw14.20` либо запускает `nw14_rus_fragmentation`, либо ставит флаг `nw_rus_war_pending`. Это повторный запуск, а не тупик: решение `nw14_resume_rus` становится видимым при pending-флаге и повторно вызывает событие, если соблюдены условия. Оно проверяет отсутствие уже начатой войны/фрагментов, наличие ключевых российских регионов и `nw_opposition > 39`.

Источник события: `events/14_nw_politics.txt`.

```hoi4
country_event = {
    id = nw14.20
    title = nw14.20.t
    desc = nw14.20.d
    is_triggered_only = yes

    option = {
        name = nw14.20.a
        trigger = { NOT = { has_country_flag = nw_rus_war_started } }
        nw14_rus_fragmentation = yes
    }

    option = {
        name = nw14.20.b
        set_country_flag = nw_rus_war_pending
    }
}
```

Источник повторного вызова: `common/decisions/14_nw_decisions.txt`, категория `nw14_russia`.

```hoi4
nw14_resume_rus = {
    icon = generic_political_actions
    cost = 0
    visible = { has_country_flag = nw_rus_war_pending }
    available = {
        has_war = no
        is_subject = no
        owns_state = 195
        owns_state = 219
        owns_state = 202
        owns_state = 218
        owns_state = 570
        NOT = { exists = RSB }
        NOT = { exists = RDN }
        NOT = { exists = RUK }
        NOT = { has_country_flag = nw_rus_war_started }
        check_variable = { nw_opposition > 39 }
    }
    days_re_enable = 30
    complete_effect = { country_event = { id = nw14.20 } }
}
```

### Фрагментация России

Ключевой эффект находится в `common/scripted_effects/14_nw_mechanics.txt`, блок `nw14_rus_fragmentation`. Он:

1. Переводит центральное правительство в республиканский режим и очищает прежние правительственные духи.
2. Запускает отделение монархического центра как event target.
3. Передаёт указанные в коде штаты Донской республике `RDN`, Украинской республике `RUK` и Сибирской республике `RSB`, добавляя соответствующие cores.
4. Назначает временные правительства, столицы, стартовые технологии и OOB.
5. Создаёт войны между центром, монархическим лагерем и отколовшимися странами; после войны снимается временный запрет на фракции.

Внимание к точности: не описывать это как «обычную двухстороннюю гражданскую войну». В коде применяется `start_civil_war` для монархического центра плюс отдельная выдача земель/объявление войны между рядом стран. Перед переработкой нужно читать весь блок эффекта и связанные OOB (`history/units/NW14_RDN.txt`, `NW14_RUK.txt`, `NW14_RSB.txt`).

### Республиканская подготовка

Событие `nw14.74` предлагает направить подполье через земства/крестьянские союзы, рабочие комитеты РСДРП, железные дороги или столичные гарнизоны. Выбор выставляет соответствующий флаг подготовки и наращивает `nw_opposition`; последующие фокусы должны отражать выбранную сеть. Полный блок события — `events/14_nw_politics.txt`, `nw14.74`; вызов и варианты фокусов — `common/national_focus/14_nw_SOV.txt`.

---

## 4. Австро-Венгрия: автономные короны и переговорное доверие

В текущем варианте AUS — верхний уровень федерации, а HUN, CRO и CZE — субъекты-части федерации. CZE является Богемо-Галицким королевством; пользовательский территориальный канон: штаты 72, 80 и 88 относятся к CZE; штат 90 (Кельце) — Польше; Судеты остаются у AUS. Это исправление владельца приоритетнее любых старых схем.

Тип автономии определён в `common/autonomous_states/01_nw_federal_part.txt`: минимум свободы 0.85, субъект не может начинать свою войну, может отказаться от призыва в войну, автономия не меняется сама по себе. Сокращённый фрагмент:

```hoi4
autonomy_state = {
    id = autonomy_nw_federal_part
    min_freedom_level = 0.85
    manpower_influence = 0.0

    rule = {
        desc = "RULE_DESC_IS_A_SUBJECT"
        can_not_declare_war = yes
        can_decline_call_to_war = yes
        can_be_spymaster = yes
    }

    modifier = {
        autonomy_manpower_share = 0.0
        extra_trade_to_overlord_factor = 0.0
        overlord_trade_cost_factor = 0.0
        autonomy_gain_global_factor = 0.0
        can_master_build_for_us = 1
    }

    can_take_level = { always = no }
}
```

Стартовые отношения записаны в history, а не в `on_action`:

Источник: `history/general/zz_nw_1936_scenario.txt` (аналогичные строки также в историях стран).

```hoi4
AUS = { set_autonomy = { target = CRO autonomy_state = autonomy_nw_federal_part freedom_level = 0.85 } }
AUS = { set_autonomy = { target = CZE autonomy_state = autonomy_nw_federal_part freedom_level = 0.85 } }
AUS = { set_autonomy = { target = HUN autonomy_state = autonomy_nw_federal_part freedom_level = 0.85 } }
```

У AUS есть ресурс доверия `nw_federal_trust` (старт 50); у HUN — `nw_hungarian_trust` (старт 45). Ежемесячная проверка добавляет негативный дух при низком доверии. Решение `nw14_federal_consult` тратит политическую власть ради +15 доверия; отдельные `nw14_renew_HUN/CZE/CRO` предлагают соответствующему субъекту обновить согласие, выставляя `nw_federal_consent` при принятии. Смотри `common/decisions/14_nw_decisions.txt` и события `nw14.40`, `.41`, `.42` в `events/14_nw_politics.txt`.

---

## 5. Маньчжурия: русско-японский кондоминиум

Лорный фон: после Второй Русско-Японско-Китайской войны Россия и Япония установили совместный кондоминиум; это произошло до похода Чан Кайши и формального объединения китайских варлордов. MAN — отдельная комиссия, не марионетка одной державы. Механически страна сильно ограничена.

Источник: `history/countries/MAN - Manchukou.txt`.

```hoi4
set_politics = { ruling_party = neutrality elections_allowed = no }
set_popularities = { democratic = 10 fascism = 5 communism = 5 neutrality = 80 }
set_cosmetic_tag = NW_MANCHURIA
add_ideas = { nw_man_two_railways nw_man_guarded_peace }
set_country_flag = nw_man_condominium
set_research_slots = 0
set_political_power = 0
add_ideas = nw_man_commission_statute
set_rule = {
    can_not_declare_war = yes
    can_create_factions = no
    can_join_factions = no
    can_send_volunteers = no
}
give_military_access = SOV
give_military_access = JAP
load_focus_tree = { tree = NW_MAN_commission_tree keep_completed = no }
```

Проверяйте также `history/general/zz_nw_1936_scenario.txt`: сценарная сверка удаляет у MAN случайное ванильное подчинение/фракцию. Это не скрытая аннексия и не мировое событие при запуске; текущий файл помечен как нативная сценарная настройка без `on_startup`.

---

## 6. Ещё несколько канонических отличий, важные для дизайна механик

Это сводка лора/стартового состояния из `DESIGN/LORE_MASTER_0.24.md`, а не гарантия, что каждой стране уже дано уникальное дерево или механика:

- Первая мировая война не произошла. Мир 1936 года развивался без её тотальной мобилизации и послевоенного порядка.
- Россия — империя Алексея II. Кризис здоровья может привести к выздоровлению и усилению самодержавия, регентству Кирилла Владимировича, революционной республике/фрагментации либо Чёрной сотне.
- Германия — империя Вильгельма II с коалицией СДПГ и КПГ; парламентский конфликт может быть урегулирован, разрешён в пользу кайзера либо перейти к коммунистической революции и гражданской войне.
- Австро-Венгрия преобразована в федерацию корон; Венгрия сохраняет собственные интересы и должна участвовать в переговорах, а не ощущаться бесплатным национальным модификатором.
- Маньчжурия нейтральна под совместным российско-японским контролем.
- Восточный Туркестан и Монголия находятся в сфере России согласно текущему лору.
- Италия разделена на новые государства; ИСР претендует на объединение Италии.
- Франция нейтральная, с Аксьон Франсез; Египет позиционируется как «Империя Нила»; Великая Албания независима, но экономически зависит от Габсбургской державы.
- Индия независима и гарантирует Тибет; Конго — бельгийская колония.
- Территориальный канон пользователя: **72, 80 и 88 — CZE; 90 — POL**. Не менять это распределение.

В лоре и сборке возможны расхождения. Если обнаружится несогласованность, перечислите её как вопрос/риск к владельцу; не «чините» канон по памяти.

---

## 7. Инструкции независимому куратору

Используйте этот справочник вместе с `LORE_MASTER_0.24.md` и `CURATOR_PROMPT_FOCUSES_MECHANICS.md`. ZIP не нужен: здесь приведены механические опорные участки и ссылки на исходные пути, чтобы сверить формулировки.

Нужно предложить собственную структуру фокусов, решений, событий и игровых циклов, руководствуясь лором и стандартами читаемых HOI4-модов. Не копируйте чужие сюжеты или большие фрагменты кода. Не принимайте текущую реализацию за обязательный дизайн: она дана как фактическая база и для выявления проблем. Прежде чем предлагать изменения, укажите:

1. Что из текущих механик сохранить, упростить или переработать, и почему.
2. Какой игровой цикл получит игрок каждой крупной страны: цель, конфликт, ограниченный ресурс, решения, цена ошибки и понятный исход.
3. Какие события/решения нужны между фокусами, чтобы политическая подготовка была интерактивной, а гражданская война — предсказуемой и не сводилась к нескольким случайным бонусам.
4. Где есть риск тупика, невалидного эффекта, неправильного scope, повторного запуска события, потери территорий/армий или несогласованности с историей страны.
5. Какие проверки можно сделать статически и какие обязательно требуют тестовой партии HOI4 и просмотра `error.log`.

Не использовать RoIMOL как референс. При сравнении структуры брать общие принципы из Millennium Dawn, The Great War и других открытых модов, но не копировать их контент. Не редактировать текущую сборку без отдельного задания владельца.

## Проверка и пределы

Фрагменты в этом MD сверены с исходниками сборки 0.24 на диске при подготовке документа. Здесь не утверждается, что эта версия была запущена в HOI4 в рамках подготовки файла. Для проверки в движке нужны новая партия с Nothing Wrong 0.24, проверка старта стран, GUI Рейхстага, принятия/отказа федеративных хартий, русской отсрочки/повторного решения и сценариев войны; затем изучение `error.log` и `game.log`.
