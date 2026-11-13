> Принято владельцем 2026-11-12 («Примени») с уточнениями: отсутствие OOB относится к отдельным участникам и требует адресной диагностики; правила автоаннексии предложены и утверждены владельцем; исследование/адаптация локальных skills входят в задачу. Роль Linux Codex — второй основной агент. Уточнения владельца и AGENTS.md имеют приоритет над текстом ниже. Новые правила мира интегрируются только после экспериментальной проверки P2. Этот документ не подтверждает runtime-результатов.

# NOTHING WRONG — PRE-ALPHA DEVELOPMENT DIRECTIVE

**Имя документа:** `CODEX_PREALPHA_DIRECTIVE.md`  
**Проект:** Nothing Wrong — Hearts of Iron IV Total Conversion  
**Репозиторий:** https://github.com/75thDiver/NothingWrongMod  
**Целевая ветка:** `codex/windows-linux-handoff-2026-10-23`  
**Основная среда:** Linux  
**Целевая версия HOI4:** 1.19.*  
**Статус:** Задание на разработку, техническую ревизию и улучшение навыков CODEX.

---

# 1. Роль CODEX и цель задания

Ты — второй основной Codex на Linux. Первый основной Windows Codex сохраняет техническую координацию через владельца.

Твоя задача — не переписать мод заново, а подготовить существующую игровую сборку к **стабильной пре-альфе**.

Главный приоритет — завершение и исправление системы Гражданской войны в России.

Необходимо:

1. Проанализировать актуальный код, документацию и отчёты CODEX.
2. Исправить отсутствующие армии и национальные духи участников войны.
3. Спроектировать и реализовать надёжную механику капитуляции и завершения отдельных конфликтов.
4. Реализовать особые правила аннексии для предусмотренных российских государств.
5. Привести скиллы CODEX в соответствие с актуальным проектом.
6. Добавить специализированные скиллы там, где существующих недостаточно.
7. Расширить автоматические проверки.
8. Оценить пригодность существующих национальных фокусов к пре-альфе.
9. Сохранить авторский лор, сюжетные маршруты и уже работающие механики.

## 1.1. Главный принцип

**Исправление существующей системы имеет приоритет над созданием новой.**

Не создавай параллельную механику, если функциональность уже реализована.

Не подменяй рабочий проект шаблонной реализацией.

Не увеличивай объём контента ради количества.

Качество пре-альфы определяется тем, способен ли игрок пройти основную игровую цепочку без критических ошибок.

## 1.2. Приоритет инструкций

Соблюдай порядок, установленный корневым `AGENTS.md`.

Особенно важно:

- Активная сборка расположена в корне репозитория.
- Документы в `DESIGN/` являются рабочими источниками.
- Старые отчёты и архивы не заменяют актуальный код.
- Linux используется как основная среда разработки.
- Нельзя без отдельного разрешения изменять карту.
- Нельзя самовольно переписывать российские политические ветки.
- Нельзя ломать систему Рейхстага Германии.
- Нельзя создавать параллельные механики здоровья или доверия Алексея II.
- Нельзя устанавливать сторонние скиллы, плагины или MCP без разрешения владельца.
- Нельзя самостоятельно выполнять `git push`.

Это задание разрешает разработку описанных ниже механик, но не отменяет остальные ограничения проекта.

---

# 2. Начальная проверка репозитория

Перед любыми изменениями выполни:

~~~bash
pwd
git status --short
git branch --show-current
git log -5 --oneline
python tools/validate_project.py
find .agents/skills -name SKILL.md -print
~~~

Убедись, что активная ветка соответствует заданию.

Если работаешь в другой ветке, не выполняй автоматическое переключение с потерей незакоммиченных изменений.

Проверь текущие файлы:

- `AGENTS.md`
- `DESIGN/`
- `.agents/skills/`
- `common/national_focus/`
- `common/ideas/`
- `common/on_actions/`
- `common/scripted_effects/`
- `common/scripted_triggers/`
- `history/countries/`
- `history/units/`
- `events/`
- `tools/validate_project.py`

Если какая-либо директория отсутствует, не создавай её автоматически. Сначала выясни, где в текущем проекте реализована соответствующая функциональность.

## 2.1. Отчёты CODEX

Найди актуальные отчёты Windows CODEX и Linux CODEX.

Для каждого отчёта определи:

- Дату.
- Ветку и коммит, к которым он относится.
- Реализованные изменения.
- Нерешённые проблемы.
- Известные ограничения.
- Утверждения, подтверждённые кодом.
- Утверждения, не подтверждённые текущей сборкой.

При противоречии между отчётом и актуальным кодом используй текущий код как основной технический источник.

Не считай Windows-отчёт недействительным только из-за перехода на Linux.

Не считай Linux-отчёт автоматически более точным.

## 2.2. Первичный результат

Создай документ:

`DESIGN/PREALPHA_CIVIL_WAR_AUDIT.md`

В нём зафиксируй реальную архитектуру Гражданской войны, найденные проблемы и порядок исправлений.

Первый этап — только инвентаризация.

Во время первоначальной инвентаризации не изменяй игровые файлы.

---

# 3. Система Гражданской войны

## 3.1. Общая цель

Гражданская война должна быть полноценной игровой системой, в которой каждый предусмотренный участник:

- Корректно появляется.
- Получает назначенные территории.
- Имеет необходимые дипломатические отношения.
- Обладает предусмотренной армией.
- Получает национальные духи.
- Может вести боевые действия.
- Может капитулировать.
- Может быть аннексирован или участвовать в ограниченном мире.
- Не ломает дальнейшее течение кампании.

Это обязательное условие пре-альфы.

## 3.2. Реестр участников

Найди всех участников Гражданской войны.

Не используй предполагаемые TAG из предыдущих отчётов без проверки.

Создай таблицу:

| Поле | Описание |
|---|---|
| Country TAG | Фактический TAG |
| Название | Локализованное название |
| Тип возникновения | Стартовая или динамически созданная страна |
| Способ создания | History, event, focus, effect, civil war |
| Территории | Фактические стартовые владения |
| Столица | Назначенная столица |
| Сюзерен | Если существует |
| Фракция | Если существует |
| Войны | Список конфликтов |
| OOB | Источник стартовой армии |
| Шаблоны дивизий | Используемые templates |
| Национальные духи | Назначенные ideas |
| Особые правила | Аннексия, дипломатия, сюжет |
| Статус | Работает, частично работает, сломано |
| Доказательство | Путь к коду, лог или игровой тест |

Разделяй фактически существующих участников и запланированных, но ещё не реализованных.

Не создавай отсутствующие страны только на основании старых планов.

## 3.3. Проблема отсутствующих дивизий

Проведи полную проверку существующей системы появления войск.

Проверяй:

1. Существует ли файл OOB.
2. Ссылается ли страна на правильный OOB.
3. Корректно ли определяется момент загрузки OOB.
4. Существуют ли шаблоны используемых дивизий.
5. Корректны ли типы батальонов.
6. Есть ли валидные провинции размещения.
7. Принадлежат ли провинции соответствующей стране в момент появления.
8. Не уничтожаются ли дивизии последующим событием.
9. Не конфликтует ли выдача войск с механикой гражданской войны движка.
10. Не запускается ли инициализация повторно.

**Не исправляй проблему путём глобальной выдачи дивизий всем участникам через `on_startup`.**

Предпочитай:

- History/OOB для стран, существующих при старте.
- Существующие механизмы инициализации для динамически созданных стран.
- Отдельный scripted effect только тогда, когда действительно требуется.

Если используются `load_oob`, `set_oob` или `create_unit`, проверь синтаксис по ванильным файлам установленной версии HOI4.

### Требование к повторному вызову

Инициализация не должна повторно создавать армию после:

- Загрузки сохранения.
- Перехода через игровой день.
- Повторного вызова сюжетного события.
- Восстановления страны.
- Изменения правительства.

Если нужен флаг однократной инициализации, используй подходящее существующее соглашение об именовании.

Не добавляй флаг без доказанной необходимости.

## 3.4. Баланс армий

Армии не должны быть полностью одинаковыми.

Однако на этапе пре-альфы запрещено радикально перебалансировать всю войну без диагностических данных.

Сначала восстанови предусмотренные разработчиком армии.

Затем подготовь предложения по балансу.

Возможные различия:

### Регулярные армии

- Более качественные соединения.
- Подготовленный офицерский корпус.
- Лучшая организация.
- Ограниченные резервы.
- Зависимость от снабжения.

### Революционные армии

- Доступность массовой мобилизации.
- Более слабая начальная организация.
- Ополчение и территориальные формирования.
- Политические механики мобилизации.
- Проблемы профессионального командования.

### Региональные формирования

- Ограниченный численный состав.
- Преимущества местной обороны.
- Зависимость от региональных ресурсов.
- Слабые возможности длительного наступления.

Это дизайнерские ориентиры, не обязательная схема для каждой конкретной страны.

Лор и существующий код имеют приоритет.

---

# 4. Национальные духи участников войны

## 4.1. Основная проблема

Некоторые участники не получают предусмотренные национальные духи.

Необходимо определить причину для каждого участника.

Проверяй:

- Существует ли соответствующий idea ID.
- В какой группе определена идея.
- Где именно она назначается.
- Срабатывает ли эффект назначения.
- Не удаляет ли её другой эффект.
- Корректен ли scope.
- Не используется ли неверное условие.
- Не заменяется ли идея другой.
- Не назначается ли она до появления страны.
- Не зависит ли она ошибочно от фокуса, который участник не может выполнить.

## 4.2. Требования к реализации

Для каждого участника создай проверяемый набор ожидаемых идей.

Разделяй:

1. Обязательные стартовые идеи.
2. Политические идеи.
3. Военные идеи.
4. Временные идеи.
5. Идеи, получаемые через события.
6. Идеи, заменяемые другими идеями.

Не вводи обязательную идею только потому, что у других участников она существует.

Не создавай новую идею, если идентичная по назначению уже имеется.

## 4.3. Защита от повторной выдачи

Если инициализация вызывается через события, она должна быть безопасной при повторном вызове.

Старайся использовать существующие флаги, назначенные идеи и подтверждённые условия.

Избегай циклов:

`add_ideas` → `on_add` → событие → `add_ideas`.

## 4.4. Отчёт

Для каждого участника укажи:

- Какие идеи должны существовать.
- Какие реально существуют.
- Почему отсутствующие идеи не назначались.
- Какие изменения внесены.
- Как они проверены.

---

# 5. Новая система капитуляции и мира

Это одна из основных задач проекта.

## 5.1. Желаемое поведение

При капитуляции отдельной страны должна разрешаться судьба именно этой страны.

Не требуется автоматически завершать все войны альянса или всех участников Гражданской войны.

Остальные страны должны продолжить свои конфликты, если игровые условия этого требуют.

Система имеет две основные ветви:

**A. Обычный участник:** ограниченная мирная конференция.

**B. Особый российский победитель:** автоматическая аннексия.

## 5.2. Особые победители

Особое правило распространяется на:

1. Российскую Республику.
2. Российское Государство.
3. Российскую Империю.
4. ВСЮР.
5. Предусмотренных правилами марионеток этих государств.

Не угадывай соответствующие TAG.

Определи реальные способы идентификации политических режимов.

Один TAG может использоваться несколькими формами государства, поэтому проверка только TAG может оказаться недостаточной.

При необходимости используй существующие флаги политических маршрутов или другие подтверждённые признаки.

**Не создавай новые страны или политические режимы.**

## 5.3. Правила аннексии

Если капитуляцию противника принимает один из особых российских победителей, соответствующий проигравший должен быть аннексирован без стандартной мирной конференции.

Для независимого особого победителя территория переходит ему.

Для победителя-марионетки территория должна переходить предусмотренному российскому сюзерену, а не автоматически самой марионетке.

Сначала проверь действительную цепочку подчинения.

Если существуют многоуровневые отношения марионеток, не распространяй правило на них автоматически без подтверждения игровой модели и лора.

Если сторона победителя включает несколько независимых российских претендентов, нельзя случайно наградить не того участника.

Нужно определить однозначного получателя аннексии.

## 5.4. Обычная капитуляция

Для остальных стран требуется ограниченная мирная конференция с капитулировавшим государством.

Сценарий:

1. Происходит капитуляция страны.
2. Определяется действительный победитель.
3. Определяется капитулировавшая страна.
4. Проверяется принадлежность конфликта к нужной механике.
5. Проверяются отношения с альянсом и сюзереном.
6. Запускается ограниченная мирная конференция.
7. Судьба остальных участников войны не меняется без необходимости.

Не запускай глобальную мирную конференцию, если можно использовать локальную.

## 5.5. Основной технический кандидат

Изучи эффект:

`start_peace_conference`

В доступной документации описаны параметры:

- `tag`
- `score_factor`
- `winner_scope`
- `loser_scope`
- `message`

Режим `LIMITED` ограничивает состав участников, но **может включать субъектов указанной страны**.

Следовательно, нельзя утверждать, что он гарантирует конференцию ровно с одним государством в любых дипломатических условиях.

Проверь это на целевой версии игры.

Не путай:

- Ограничение состава участников конференции.
- Выбор получателя территорий.
- Размер доступного счёта.
- Обязательную аннексию.

`score_factor` не является командой автоматической аннексии.

## 5.6. Кандидат для прямой аннексии

Изучи эффект:

`annex_country`

Проверь:

- Country scope вызывающей стороны.
- Target.
- Параметр `transfer_troops`.
- Поведение при капитуляции.
- Поведение при наличии субъекта.
- Поведение с альянсами.
- Сохранение или уничтожение дивизий.
- Побочные вызовы `on_actions`.

Не применяй массовую передачу state-файлов вместо `annex_country` без технической необходимости.

Изменения физических файлов карты запрещены.

## 5.7. Альянсы и марионетки

Предполагаемый владельцем вариант:

1. Страна капитулирует.
2. Выходит из альянса.
3. Перестаёт быть марионеткой.
4. Получает отдельный мир.

Это допустимая гипотеза, но не подтверждённая окончательная последовательность.

**Сначала проверь возможность отдельной конференции без изменения дипломатического статуса.**

Только если подтверждено, что текущая структура альянса или подчинения препятствует требуемой логике, рассматривай:

- `leave_faction`
- `end_puppet`
- Иные подтверждённые инструменты дипломатии.

Выход из альянса сам по себе не гарантирует запуска мирной конференции.

Освобождение марионетки может повлиять на участие в войнах.

Любые подобные изменения должны быть минимальными и обоснованными.

## 5.8. Обработчик капитуляции

Исследуй:

- `on_capitulation`
- `on_civil_war_end`
- `on_annex`
- `on_peaceconference_started`
- `on_peaceconference_ended`

Проверь реальные ROOT/FROM и доступные контексты по ванильному `00_on_actions.txt`.

Не считай страну, получившую капитуляцию, автоматически той страной, чьи дивизии последними захватили ключевую провинцию.

Это особенно важно для марионеток, союзников и нескольких одновременных войн.

### Требование к безопасности

Глобальный обработчик не должен менять капитуляции стран, не относящихся к предусмотренной системе.

Проверь границы применения механики.

Не допускай повторной аннексии.

Не допускай бесконечных цепочек событий.

Не допускай повторного запуска мирной конференции.

Не запускай второй обработчик, если движок уже разрешил тот же конфликт.

## 5.9. Состояния обработки

Спроектируй логические состояния:

- Не обрабатывается.
- Зарегистрирована капитуляция.
- Определены стороны.
- Выбран способ завершения.
- Выполняется разрешение конфликта.
- Завершено.
- Ошибка или недопустимое состояние.

Это логическая модель. Не обязательно хранить каждый этап отдельным игровым флагом.

Используй минимально необходимое количество переменных и флагов.

Если обработка уже завершена, повторный вызов ничего не должен менять.

## 5.10. Отложенное выполнение

Если дипломатические действия внутри `on_capitulation` вызывают ошибки или некорректное состояние движка, рассмотри запуск отдельного события.

Но не утверждай, что задержка на несколько часов или один день гарантированно решает проблему.

Перед отложенным действием повторно проверяй существование участников и актуальность войны.

Если страна уже аннексирована, её country event может не выполниться.

## 5.11. Несколько войн одновременно

Особо протестируй сценарий, когда капитулирующая страна:

- Участвует в двух разных войнах.
- Воевала вместе с союзниками.
- Имеет марионеток.
- Сама является марионеткой.
- Находится в гражданской войне.
- Воюет с несколькими российскими претендентами.

Нельзя разрешать посторонние войны случайным побочным эффектом.

Если HOI4 не позволяет гарантировать независимое завершение конкретной войны, задокументируй это ограничение и предложи наиболее безопасный вариант.

Не маскируй ограничение движка неподтверждённым скриптом.

---

# 6. Матрица игровых испытаний

Обязательные сценарии:

| ID | Сценарий | Ожидаемый результат |
|---|---|---|
| CW-01 | Независимая страна капитулирует без альянса | Ограниченный мир |
| CW-02 | Капитулирует член альянса | Союзники не удаляются из войны автоматически |
| CW-03 | Капитулирует марионетка | Обрабатывается её собственное положение |
| CW-04 | Капитулирует сюзерен | Нет сломанной цепочки субъектов |
| CW-05 | Республика добивается капитуляции | Прямая аннексия |
| CW-06 | Российское Государство добивается капитуляции | Прямая аннексия |
| CW-07 | Российская Империя добивается капитуляции | Прямая аннексия |
| CW-08 | ВСЮР добивается капитуляции | Прямая аннексия |
| CW-09 | Марионетка особого победителя добивается капитуляции | Аннексия надлежащим сюзереном |
| CW-10 | Капитулирует лидер альянса | Нет зависшей войны |
| CW-11 | Участник находится в нескольких войнах | Посторонние конфликты не ломаются |
| CW-12 | Завершается обычная гражданская война HOI4 | Нет повторной аннексии |
| CW-13 | Срабатывает повторный обработчик | Нет дублирования действий |
| CW-14 | Сохранение и загрузка после капитуляции | Состояние сохраняется корректно |
| CW-15 | Победителем становится ИИ | Система не требует участия игрока |
| CW-16 | Побеждённый имеет субъектов | Проверено поведение субъектов в LIMITED-конференции |
| CW-17 | Другой TAG, не участвующий в механике, капитулирует | Глобальная механика его не затрагивает |
| CW-18 | Происходит капитуляция во время другой мирной конференции | Нет повторного или конфликтующего разрешения |

Все тесты должны содержать фактический результат, а не только ожидаемый.

Для автоматических проверок допускаются мок-данные и фикстуры, но они не заменяют проверку в HOI4.

---

# 7. Национальные фокусы: технический аудит

Цель — не увеличение количества фокусов.

Цель — устранение ошибок и повышение качества существующих маршрутов.

## 7.1. Проверки

Для каждого основного дерева проверь:

- Существование всех зависимостей.
- Достижимость фокусов.
- Корректность взаимоисключений.
- Условия `available`.
- Условия `bypass`.
- Награды.
- Существование локализации.
- Назначенные иконки.
- Возможность прохождения фокусов ИИ.
- Связь фокусов с событиями.
- Корректность фокусов при гражданской войне.
- Сохранение доступности экономических и военных программ.

## 7.2. Защищённые российские зависимости

Строго соблюдать утверждённые зависимости из корневого `AGENTS.md`.

Не возвращать старые обязательные цепочки.

Не изменять маршруты Кирилла, эсеров, меньшевиков, большевиков и чёрную ветку без отдельной причины.

Сохранять механику `nw_army_loyalty` и утверждённые сюжетные флаги.

## 7.3. Правило prerequisite

В HOI4:

- Несколько `focus = ...` внутри одного блока `prerequisite` — OR.
- Несколько отдельных блоков `prerequisite` — AND.

Нельзя автоматически преобразовывать один вариант в другой при чистке файлов.

Это может разрушить целые политические маршруты.

## 7.4. Качественная оценка

Оценивай фокусы по следующим критериям:

1. Имеет ли фокус игровое значение.
2. Соответствует ли награда содержанию.
3. Не является ли награда случайным набором бонусов.
4. Есть ли логическая связь с предыдущими фокусами.
5. Не блокируется ли маршрут ошибочно.
6. Имеет ли выбор политические или военные последствия.
7. Соответствует ли текст лору.
8. Может ли ИИ использовать этот маршрут.

Не меняй баланс без объяснения.

Не заменяй существующие сюжетные фокусы более простыми механическими шаблонами.

## 7.5. Предложения по улучшению

После технического аудита составь отдельные рекомендации.

Раздели их на:

- Критические исправления.
- Улучшения для пре-альфы.
- Желательные изменения для альфы.
- Идеи для будущих версий.

Не реализуй новые сюжетные идеи автоматически.

---

# 8. Переработка системы скиллов CODEX

## 8.1. Общая философия

Скилл должен описывать конкретный воспроизводимый рабочий процесс.

Он не должен быть огромной копией HOI4 Wiki.

Он не должен заставлять CODEX применять правила чужого мода.

Он не должен содержать неподтверждённые команды.

Он должен помогать выбирать правильные инструменты, находить нужные файлы и проверять результат.

Скиллы должны дополнять `AGENTS.md`, а не конкурировать с ним.

## 8.2. Что сохранить

Сохраняй существующие профильные скиллы, если они актуальны и содержат полезные инструкции.

В частности:

- Общие механики HOI4.
- Фокусы.
- События.
- Решения.
- Национальные духи.
- Scripted effects.
- Scripted triggers.
- Scopes.
- Локализация.
- GUI.
- GFX.
- Модификаторы.
- Переменные.
- On actions.
- Работа с дивизиями и OOB.

Не удаляй полезные специализированные навыки только ради уменьшения количества файлов.

Однако если два навыка практически полностью дублируют друг друга, оставь один основной источник.

## 8.3. Что исправить

### `hoi4-project-router`

Обязательно обновить.

Текущие известные проблемы:

- Устаревшие ссылки на `docs/`.
- Упоминание `NothingWrongMod/` как единственной активной сборки.
- Несоответствие актуальному корневому `AGENTS.md`.

Новый роутер должен работать с корнем репозитория и `DESIGN/`.

### `hoi4-gui`

Сохранить полезные технические материалы.

Убрать или изолировать:

- Обязательные BSM-префиксы.
- Чужую проектную терминологию.
- Японскую локализацию как стандарт.
- Ссылки на чужие шаблоны как обязательные правила Nothing Wrong.

Если примеры BSM корректны и технически полезны, можно сохранить их в `references/external-examples.md`, явно пометив как сторонние примеры.

### `hoi4-modding/references/modding-rules.md`

Исправить:

- Упоминания китайской локализации как стандарта проекта.
- Чужие префиксы идентификаторов.
- Неприменимые соглашения другого мода.
- Противоречия с `AGENTS.md`.

Сохранить полезные общие правила по резервным копиям, кодировкам, проверкам и безопасной работе.

Не переносить механические правила баланса чужого мода без отдельной оценки.

### `hoi4-modding/references/focus-template.md`

Исправить ошибочный ключ:

`Reset_on_civilwarno = no`

Проверить правильный ключ `reset_on_civilwar = no` по актуальной схеме и ванильным данным.

Дополнительно проверить остальные поля шаблона.

Не считать любой пример синтаксиса действительным только потому, что он указан в скилле.

## 8.4. Что убрать

Удалять из активных инструкций:

- Заведомо устаревшие пути.
- Чужие обязательные naming conventions.
- Неактуальные требования по языку локализации.
- Повторяющиеся инструкции, конфликтующие с `AGENTS.md`.
- Примеры с несуществующими командами.
- Неподтверждённые правила движка.
- Абсолютные пути чужого компьютера.
- Обязательные действия, не относящиеся к текущему проекту.

Перед удалением проверь, не используется ли конкретный файл другим скиллом.

Если материал потенциально полезен, перенеси его в архивные references или исключи из активного роутинга.

Не удаляй старые отчёты CODEX и документы передачи между Linux и Windows.

## 8.5. Что добавить

Создать три новых специализированных навыка:

1. `hoi4-civil-war`
2. `hoi4-war-resolution`
3. `hoi4-prealpha-qa`

Готовые тексты приведены ниже.

Используй их как основу, адаптируя к обнаруженной структуре проекта.

Не устанавливай внешние навыки.

---

# 9. Готовый обновлённый скилл: hoi4-project-router

**Путь:** `.agents/skills/hoi4-project-router/SKILL.md`

Заменить содержимое существующего роутера после сравнения с актуальной версией. Не потерять уникальные рабочие инструкции, которых нет в предложенном тексте.

~~~markdown
---
name: hoi4-project-router
description: Route Nothing Wrong HOI4 development tasks to current project rules and the appropriate specialist skill.
---

# Nothing Wrong — Project Router

## When to use

Use for every development or review task in Nothing Wrong.

This skill selects relevant project documentation and specialist workflows.

It is not a replacement for AGENTS.md.

## Source priority

1. Latest direct owner instruction.
2. Approved project instructions.
3. Current source code and DESIGN documentation.
4. Current verified reports.
5. Historical reports and external references.

When sources disagree, report the contradiction.

Do not silently resolve lore conflicts.

## Start

1. Read repository-root AGENTS.md.
2. Run git status --short.
3. Identify the current branch.
4. Read the relevant DESIGN document.
5. Inspect the actual files affected by the task.
6. Select the appropriate specialist skill.
7. Run python tools/validate_project.py before editing.

The active game build is the repository root.

Do not treat old archives as active source files.

## Specialist routing

Civil war participants, OOB, army spawning:
hoi4-civil-war

Capitulation, annexation, diplomacy, peace:
hoi4-war-resolution

Regression testing and release readiness:
hoi4-prealpha-qa

National focuses:
existing focus specialist

Events and decisions:
existing event/decision specialists

Ideas and modifiers:
existing ideas/modifiers specialists

GUI:
hoi4-gui

General syntax:
hoi4-modding and relevant references

Read only the references relevant to the task.

Do not load the entire skills library unnecessarily.

## Project invariants

Never modify map data without explicit permission.

Preserve the state ID canon documented in AGENTS.md.

Preserve protected Russian focus dependencies.

Preserve approved political flags.

Do not create duplicate mechanics for Alexei II.

Do not rewrite Reichstag logic during unrelated work.

Do not change economic or military focus accessibility
based solely on political path.

Use Russian localisation.

Preserve UTF-8 BOM for localisation files.

Follow existing project naming conventions.

## HOI4 version

Target the game version defined by the current project.

Verify effects, triggers, modifiers, scopes,
equipment, technologies and GUI properties
against the matching vanilla files.

External examples are references, not proof.

## Editing workflow

1. Inspect source.
2. Identify the smallest change.
3. Back up existing target files.
4. Apply the change.
5. Compare against the backup.
6. Run validation.
7. Inspect git diff.
8. Remove temporary backups only after verification.
9. Report actual results.

Never overwrite unrelated user changes.

Do not push without permission.

## Reporting

Distinguish:

- Source inspection
- Static validation
- Automated tests
- Game-engine testing
- Unverified assumptions

Do not claim HOI4 runtime success without an actual game test.

## Completion

Report:

- Files changed
- Why they changed
- Tests executed
- Results
- Remaining problems
- Risks
- Recommended next action
~~~

---

# 10. Новый скилл: hoi4-civil-war

**Путь:** `.agents/skills/hoi4-civil-war/SKILL.md`

~~~markdown
---
name: hoi4-civil-war
description: Audit and implement Nothing Wrong civil-war participants, armies, OOB, national spirits and country initialization.
---

# Nothing Wrong — Civil War Development

## Purpose

Ensure every intended civil-war participant
is initialized correctly and can participate
in the campaign.

Use for:

- Civil war initialization
- Country spawning
- Starting armies
- OOB
- Division templates
- Initial ideas
- Political initialization
- War participants
- Spawn bugs

Do not use for unrelated international wars
or general focus development.

## Required context

Read:

1. AGENTS.md
2. Relevant DESIGN documents
3. Current civil-war source files
4. Existing reports
5. hoi4-project-router

Never infer the current implementation from reports alone.

## Stage 1 — Participant inventory

Identify every intended participant.

Record:

- TAG
- Country name
- Spawn mechanism
- Initial states
- Capital
- Initial faction
- Initial overlord
- Initial wars
- Starting OOB
- Starting templates
- Initial ideas
- Related events
- Source references

Do not invent missing participants.

Do not modify the map.

## Stage 2 — Army validation

For each participant:

1. Find its OOB or spawn effect.
2. Verify the referenced file exists.
3. Verify division templates.
4. Verify unit types.
5. Verify province locations.
6. Verify initialization timing.
7. Check for duplicate spawning.
8. Check for unintended unit deletion.
9. Check equipment and manpower requirements.
10. Identify whether the engine handles part of the initialization automatically.

Prefer repairing existing OOB logic.

Do not globally spawn units through on_startup.

## Stage 3 — National spirits

For each intended idea:

1. Verify idea ID.
2. Verify definition.
3. Verify assignment effect.
4. Verify country scope.
5. Verify conditions.
6. Verify initialization timing.
7. Verify replacement and removal logic.
8. Check repeated execution.

Avoid duplicate or parallel spirit systems.

## Stage 4 — Country consistency

Inspect:

- Country existence
- Government
- Ruling ideology
- Cosmetic tags
- Capitals
- War participation
- Subjects
- Factions
- Initial armies
- Spirits

Preserve established lore.

## Stage 5 — Safe implementation

Use the smallest valid change.

Do not rewrite unrelated country history.

Do not change history/states/.

Do not create new countries.

Do not alter approved political routes.

Use existing conventions for flags and scripted effects.

For dynamically spawned countries,
verify exactly when the target country exists.

## Stage 6 — Tests

Static tests should verify:

- Required files exist
- OOB references resolve
- Template references resolve
- Idea IDs resolve
- Duplicate identifiers are absent
- Initialization references are valid

Engine tests should verify:

- Country appears
- Expected divisions exist
- Divisions are placed correctly
- Expected ideas exist
- Save/load does not duplicate armies
- AI can use the army
- No critical errors appear in logs

Static tests are not engine tests.

## Deliverable

Produce:

1. Participant matrix
2. Defect list
3. Minimal source changes
4. Static test results
5. Engine test results if available
6. Remaining blockers

Every finding must include source evidence.

Never mark untested behavior as verified.
~~~

---

# 11. Новый скилл: hoi4-war-resolution

**Путь:** `.agents/skills/hoi4-war-resolution/SKILL.md`

~~~markdown
---
name: hoi4-war-resolution
description: Design, implement and verify Nothing Wrong capitulation, limited peace conferences, annexation and subject/faction war resolution.
---

# Nothing Wrong — War Resolution

## Purpose

Implement safe capitulation and peace behavior.

Use for:

- on_capitulation
- on_civil_war_end
- on_annex
- Peace conferences
- Annexation
- Faction withdrawal
- Subject independence
- War termination
- Special Russian victors

Do not apply these mechanics globally
unless explicitly required.

## Core design

The system has two branches.

### Special Russian victor

When an approved Russian regime defeats
an applicable country, resolve defeat
through direct annexation.

Approved regimes:

- Russian Republic
- Russian State
- Russian Empire
- Armed Forces of South Russia (VSYUR)

Approved subjects of these regimes
may trigger annexation in favor
of the appropriate overlord.

Verify actual country identities.

Do not assume TAG alone always identifies a regime.

### Other victor

Resolve the defeated country through
a restricted peace conference.

Avoid automatically ending unrelated wars.

## Research before implementation

Inspect vanilla and project examples of:

- on_capitulation
- on_civil_war_end
- on_annex
- start_peace_conference
- annex_country
- leave_faction
- end_puppet
- white_peace
- relevant war triggers

Verify scope behavior for the target version.

Do not assume ROOT/FROM meanings
without checking the specific on_action.

## Peace-conference constraints

start_peace_conference can restrict
the participants of a conference.

LIMITED may include the main country's subjects.

Therefore LIMITED is not always
equivalent to exactly one country.

The system must test whether this limitation
affects the intended design.

Do not assume score_factor
automatically annexes a country.

## Subject and faction rules

First attempt restricted peace without
modifying faction or subject relationships.

If this fails, investigate whether
a controlled diplomatic change is required.

Never assume leave_faction automatically ends war.

Never assume end_puppet preserves war state.

Verify side effects before using either effect.

## Winner identification

Distinguish:

- Country accepting surrender
- Country controlling occupied territory
- Country owning captured territory
- Military contributor
- Country receiving annexation
- Country's overlord

These may be different countries.

Do not use an arbitrary attacker
as the annexation recipient.

## Resolution design

Implement a decision process:

1. Confirm relevant conflict.
2. Identify defeated country.
3. Identify eligible winner.
4. Identify recipient.
5. Check country existence.
6. Check current war state.
7. Check previous resolution state.
8. Select annexation or limited peace.
9. Apply the selected action.
10. Verify postconditions.

Use minimal persistent state.

Avoid duplicate callbacks.

## Dangerous cases

Explicitly test:

- Multiple wars
- Several victors
- Faction leaders
- Non-leader faction members
- Subjects
- Overlords
- Subjects of defeated states
- Civil war ending
- Annexation event chains
- Peace conference overlaps
- Already eliminated countries
- Repeated on_action calls
- Save/load during resolution

## Implementation rules

Prefer a narrow dispatcher
over large duplicated event scripts.

Do not rewrite vanilla global war behavior.

Do not change map files.

Do not create second war-resolution systems.

Avoid event loops.

Avoid annexation recursion.

If delayed events are necessary,
revalidate country existence
and diplomatic conditions before acting.

Never claim a delay guarantees engine safety.

## Experimental workflow

1. Audit current war logic.
2. Write expected behavior.
3. Build a minimal test scenario.
4. Test independent countries.
5. Test faction members.
6. Test subjects.
7. Test special Russian annexation.
8. Test repeated triggers.
9. Test save/load.
10. Integrate only after passing evidence-backed checks.

## Reporting

For every scenario record:

- Initial countries
- Initial war
- Initial faction relationships
- Initial subject relationships
- Triggering action
- Expected result
- Actual result
- Logs
- Verdict

Verdicts:

- PASS
- FAIL
- BLOCKED
- NOT TESTED

Never turn NOT TESTED into PASS.

## Failure policy

If the engine cannot support
a requested interaction reliably,
document the limitation.

Provide alternatives with tradeoffs.

Do not fabricate an effect
or silently change gameplay requirements.
~~~

---

# 12. Новый скилл: hoi4-prealpha-qa

**Путь:** `.agents/skills/hoi4-prealpha-qa/SKILL.md`

~~~markdown
---
name: hoi4-prealpha-qa
description: Verify Nothing Wrong pre-alpha stability using source audits, Python validation, regression scenarios, game logs and release gates.
---

# Nothing Wrong — Pre-Alpha QA

## Purpose

Establish reproducible verification
for the pre-alpha build.

Use for:

- Bug investigations
- Regression checks
- Static validation
- Gameplay test plans
- Runtime log analysis
- Release readiness
- Handoff verification

## Levels of evidence

### Level 1 — Source inspection

The source was inspected.

This does not prove execution.

### Level 2 — Static validation

Parsers or validators succeeded.

This does not prove game-engine compatibility.

### Level 3 — Automated scenario validation

Deterministic tests passed.

This does not prove actual HOI4 behavior.

### Level 4 — Engine validation

HOI4 was launched and tested.

Relevant gameplay and logs were inspected.

Never confuse these levels.

## Baseline workflow

Before changes:

1. Read AGENTS.md.
2. Check git status.
3. Run project validator.
4. Record existing failures.
5. Identify the affected systems.

After changes:

1. Run project validator.
2. Run targeted tests.
3. Check git diff --check.
4. Inspect modified files.
5. Verify localisation encoding.
6. Verify references.
7. Record regressions.
8. Perform game tests when available.

## Validation targets

### National focuses

- Unique IDs
- Existing prerequisites
- Correct OR/AND semantics
- Valid relative positioning
- No dependency cycles
- Valid exclusions
- Existing rewards and references
- Protected Russian dependencies
- Required localisation

### Civil war

- Participant registry
- OOB paths
- Template references
- Idea references
- Country initialization
- Duplicate spawn protection

### Peace and annexation

- Narrow trigger conditions
- Correct winner identification
- Correct loser identification
- Appropriate annexation recipient
- No duplicate resolution
- No unintended global effects

### Localisation

- UTF-8 BOM
- Correct language header
- Duplicate keys
- Missing keys
- Invalid dynamic references where detectable

## Test design

Each test requires:

- ID
- Initial conditions
- Execution steps
- Expected result
- Actual result
- Evidence
- Status

Statuses:

PASS / FAIL / BLOCKED / NOT TESTED

Keep fixture tests deterministic.

Use Python standard library
unless dependencies are approved.

Do not require external tools
without owner's permission.

## Linux workflow

Prefer portable paths.

Use pathlib for Python.

Respect case-sensitive filenames.

Avoid Windows-only assumptions.

Do not rewrite file encodings accidentally.

Do not assume HOI4's installation path.

## Engine testing

If the game is available:

1. Launch the correct mod version.
2. Reproduce the test scenario.
3. Inspect error.log.
4. Inspect relevant game logs.
5. Check actual gameplay.
6. Record screenshots or save references if useful.
7. State which build was tested.

If the game cannot be launched:

Mark engine validation NOT TESTED.

Do not invent log results.

## Release gate

A pre-alpha candidate requires:

- No known critical startup blocker
- Intended participants initialize
- Intended armies appear
- Intended national spirits appear
- Main civil-war sequence functions
- Capitulation rules function in tested scenarios
- No known duplicate annexation loop
- No known critical focus progression blocker
- Valid localisation and essential references
- Reproducible test documentation

If a gate fails, mark the candidate blocked.

## Final report

Include:

1. Build/commit
2. Files changed
3. Tests run
4. Tests passed
5. Tests failed
6. Untested areas
7. Critical blockers
8. Known limitations
9. Recommended next milestone

Be conservative when assessing readiness.
~~~

---

# 13. Обновление AGENTS.md

Не переписывай существующий `AGENTS.md` целиком.

После добавления скиллов внеси минимальные изменения, если они необходимы для их обнаружения.

Обнови маршрутизацию:

- Гражданская война и армии → `hoi4-civil-war`.
- Капитуляции и мир → `hoi4-war-resolution`.
- Регрессии и пре-альфа → `hoi4-prealpha-qa`.

Сохрани все ограничения владельца.

Не сокращай защищённые инструкции по карте и России.

Если обнаружены конфликты между новым заданием и текущими правилами, отметь их до изменения соответствующего контента.

---

# 14. Расширение tools/validate_project.py

В существующем валидаторе уже есть проверки структуры национальных фокусов и защищённых зависимостей.

Сохрани действующее поведение.

Не переписывай валидатор с нуля.

## 14.1. Новые проверки

По возможности добавь:

- Наличие требуемых OOB.
- Существование используемых division templates.
- Существование обязательных idea ID.
- Проверку ссылок на scripted effects.
- Проверку ссылок на scripted triggers там, где их можно надёжно распознать.
- Проверку национальных духов участников.
- Проверку существования используемых событий.
- Выявление дублирующихся ключевых идентификаторов.
- Проверку защищённых фокусов.
- Проверку ключевых связей новой системы капитуляции.

Не превращай эвристические проверки в безусловные ошибки, если парсер не способен корректно разобрать соответствующую конструкцию.

## 14.2. Реестр ожидаемого контента

Допускается создать небольшой машиночитаемый реестр участников войны.

Его можно использовать для проверки:

- TAG.
- OOB.
- Идей.
- Связанных событий.
- Обязательных scripted effects.

Но нельзя автоматически считать реестр источником истины о мире.

Он должен соответствовать утверждённому дизайну и реальному коду.

## 14.3. Тесты валидатора

Если ты добавляешь новую проверку, подготовь тест, который демонстрирует её способность обнаруживать соответствующую ошибку.

Например:

- Несуществующий OOB.
- Несуществующая идея.
- Дублирующийся ID.
- Нарушенная защищённая зависимость.

Не запускай намеренно повреждённые данные на рабочей копии мода.

Используй временные тестовые фикстуры.

---

# 15. Linux и Windows: правила совместимости

Основная разработка ведётся на Linux.

Поэтому необходимо:

- Проверять регистр путей.
- Не использовать Windows-разделители в путях к игровым ресурсам.
- Использовать `pathlib` в Python.
- Проверять относительные пути.
- Проверять кодировку локализации.
- Не повреждать BOM.
- Не вставлять случайные CRLF/LF-преобразования в посторонние файлы.
- Не предполагать расположение Steam.
- Не использовать PowerShell как обязательную часть проверки Linux.

Windows-отчёты сохраняются как история и источник знаний.

Если обнаружено различие поведения между Windows и Linux, документируй:

- Какой файл затронут.
- Что работает на одной платформе.
- Что не работает на другой.
- Воспроизводится ли проблема.
- Какое изменение решает её без нарушения совместимости.

---

# 16. План выполнения по этапам

## Этап P0 — Инвентаризация

Задачи:

- Проверить состояние Git.
- Прочитать отчёты Linux/Windows.
- Проверить скиллы.
- Составить реестр участников войны.
- Зафиксировать архитектуру системы капитуляций.
- Запустить baseline-валидатор.
- Найти реальные отсутствующие армии и национальные духи.

**Результат:** проверенный аудит.

На этом этапе игровые файлы не менять.

## Этап P1 — Ремонт армий и национальных духов

Задачи:

- Исправить OOB.
- Исправить ссылки на шаблоны.
- Исправить ошибки инициализации.
- Восстановить национальные духи.
- Проверить отсутствие повторной выдачи.
- Проверить появление стран и армий.

**Результат:** участники могут вести войну.

Не менять правила капитуляции одновременно с исправлением появления стран.

## Этап P2 — Экспериментальная система мира

Задачи:

- Изучить ванильные эффекты.
- Проверить on_actions и scopes.
- Сделать минимальный тест для двух независимых стран.
- Проверить ограниченную мирную конференцию.
- Проверить действия с альянсами.
- Проверить действия с субъектами.
- Определить подтверждённую модель.

**Результат:** технически доказанный способ разрешать отдельную капитуляцию.

Не интегрировать неподтверждённый эксперимент во всю гражданскую войну.

## Этап P3 — Российская аннексия

Задачи:

- Выявить идентификаторы четырёх режимов.
- Реализовать определение специального победителя.
- Реализовать надлежащего получателя территорий.
- Проверить марионеток.
- Добавить защиту от повторной обработки.
- Протестировать сложные сценарии.

**Результат:** специальные российские победители корректно аннексируют проигравших.

## Этап P4 — Интеграция

Задачи:

- Подключить подтверждённую модель к гражданской войне.
- Проверить все предусмотренные стороны.
- Проверить сохранения.
- Проверить ИИ.
- Проверить посторонние войны.
- Проверить дальнейшие фокусы и события.

**Результат:** завершённая основная цепочка Гражданской войны.

## Этап P5 — Качество пре-альфы

Задачи:

- Исправить критические фокусы.
- Устранить критические ошибки логов.
- Проверить ключевые локализации.
- Проверить старт кампании.
- Проверить основной политический маршрут.
- Проверить продолжение игры после войны.
- Подготовить отчёт готовности.

**Результат:** кандидат пре-альфы.

---

# 17. Приоритеты

Используй уровни:

## P0 — Блокер

- Страна не появляется.
- У предусмотренного воюющего участника отсутствует необходимая армия.
- Не работает основная цепочка войны.
- Происходит неправильная глобальная аннексия.
- Происходит краш игры.
- Происходит бесконечный цикл событий.
- Критическая ветка фокусов недоступна.

## P1 — Важная ошибка

- Отсутствует необходимый национальный дух.
- ИИ не может вести войну из-за ошибки сценария.
- Не работает отдельная предусмотренная мирная конференция.
- Некорректно определяется победитель.
- После войны остаётся ошибочный дипломатический статус.
- Сюжетное событие не срабатывает.

## P2 — Качество

- Неудачные награды.
- Неудачный баланс.
- Неполные описания.
- Некритические ошибки GUI.
- Неоптимальные последовательности событий.

## P3 — Будущие улучшения

- Новые механики интеграции территорий.
- Новые политические события.
- Дополнительные ветки.
- Новые уникальные решения.
- Дополнительные GUI.
- Расширение зарубежного контента.

Сначала закрывай P0, затем P1.

---

# 18. Чего делать нельзя

Запрещено:

1. Самостоятельно переписывать карту.
2. Менять state ID.
3. Перераспределять территории ради исправления OOB.
4. Переписывать политические ветки России целиком.
5. Добавлять новые государства без разрешения.
6. Переписывать систему Германии во время работы над Россией.
7. Создавать вторую механику лояльности армии.
8. Создавать вторую систему капитуляций параллельно существующей.
9. Без проверки применять непонятные эффекты.
10. Использовать устаревший код как действующий.
11. Называть статическую проверку полноценным тестом HOI4.
12. Игнорировать изменения пользователя.
13. Удалять скиллы без проверки ссылок.
14. Устанавливать внешние зависимости без разрешения.
15. Выполнять `git push` без поручения.
16. Объявлять пре-альфу готовой при наличии известных P0-блокеров.
17. Смешивать исправления гражданской войны с несвязанными визуальными или сюжетными изменениями.

---

# 19. Критерии готовности пре-альфы

Пре-альфа считается готовой к предложению владельцу, когда:

- [ ] Игра запускается с активной сборкой мода.
- [ ] Отсутствуют известные критические ошибки запуска.
- [ ] Участники Гражданской войны корректно появляются.
- [ ] Предусмотренные армии загружаются.
- [ ] Предусмотренные национальные духи назначаются.
- [ ] Не происходит повторного появления армий.
- [ ] Основная цепочка войны работает.
- [ ] Ограниченные миры работают в проверенных случаях.
- [ ] Российские особые победители корректно аннексируют противников.
- [ ] Марионетки обрабатываются по утверждённым правилам.
- [ ] Нет известных циклов аннексии.
- [ ] Посторонние войны не затрагиваются.
- [ ] Основные российские фокусы доступны и выполняются.
- [ ] Защищённые зависимости сохранены.
- [ ] Критические события имеют локализацию.
- [ ] Сохранения загружаются после капитуляций.
- [ ] Валидатор проходит без новых критических ошибок.
- [ ] Подготовлен отчёт о тестировании в движке.

Если невозможно провести проверку в движке, не отмечай соответствующие пункты выполненными.

Допускается статус:

**PRE-ALPHA CANDIDATE — ENGINE TESTING REQUIRED**

Но не:

**FULLY VERIFIED PRE-ALPHA**

---

# 20. Формат итогового отчёта CODEX

В конце каждого этапа предоставляй отчёт на русском языке.

## Обязательные разделы

### 1. Краткое резюме

Что сделано и какие проблемы устранены.

### 2. Изменённые файлы

Полный список с коротким объяснением.

### 3. Архитектурные решения

Почему выбран соответствующий способ реализации.

### 4. Проверки

Команды, результаты и реальные доказательства.

### 5. Тесты в HOI4

Что проверено в игре, а что нет.

### 6. Известные проблемы

Не скрывать оставшиеся ошибки.

### 7. Риски

Особенно связанные с войнами, аннексией, сохранениями и дипломатией.

### 8. Следующие задачи

Не более пяти приоритетных задач.

### 9. Состояние Git

Текущая ветка, diff, незакоммиченные изменения.

### 10. Передача между Linux и Windows

Если этап требует последующей работы в другой среде, подготовь конкретные инструкции с путями и результатами проверок.

---

# 21. Стратегические рекомендации для будущего проекта

Эти идеи не входят в обязательную реализацию пре-альфы.

После стабилизации войны можно рассмотреть следующие направления.

## 21.1. Политическая лояльность армии

Использовать существующую `nw_army_loyalty` как источник последствий для:

- Поддержки правительства офицерами.
- Доступности отдельных решений.
- Политической устойчивости.
- Подготовки к войне.
- Военных кризисов.

Не создавать дублирующую переменную.

## 21.2. Качество победы

После гражданской войны возможны различные последствия:

- Усталость общества.
- Политическая консолидация.
- Восстановление администрации.
- Реорганизация армии.
- Региональные противоречия.
- Экономическая реконструкция.

Эти механики должны быть связаны с уже существующими политическими путями.

Не делать одинаковые последствия для каждого режима.

## 21.3. Особенности разных российских режимов

Российская Республика, Российское Государство, Российская Империя и ВСЮР могут по-разному решать проблемы:

- Государственной легитимности.
- Армейской организации.
- Регионального управления.
- Послевоенного восстановления.
- Отношений с местными элитами.

Это предложения по будущему дизайну.

Никаких автоматических изменений без согласования.

---

# 22. Источники для проверки

**Главный источник проекта:**  
https://github.com/75thDiver/NothingWrongMod/tree/codex/windows-linux-handoff-2026-10-23

**Правила CODEX:**  
https://raw.githubusercontent.com/75thDiver/NothingWrongMod/codex/windows-linux-handoff-2026-10-23/AGENTS.md

**Справочник эффектов HOI4:**  
https://hoi4.paradoxwikis.com/Effect

**Справочник on_actions:**  
https://hoi4.paradoxwikis.com/On_actions

**Описание start_peace_conference:**  
https://scharnhorst.hagane.works/en/wiki/effect/start_peace_conference

**Общие рекомендации по скиллам:**  
https://developers.openai.com/plugins/concepts/skills

Внешние справочники могут отставать от целевой версии игры.

При расхождении между внешней документацией и установленными оригинальными файлами HOI4 необходимо провести дополнительную проверку.

Не используй непроверенный интернет-пример как единственное доказательство.

---

# 23. Финальная инструкция CODEX

Выполняй задание поэтапно.

Не пытайся одновременно переписать фокусы, гражданскую войну, дипломатию и систему скиллов.

Начни с технической инвентаризации.

После неё устрани проблемы с армиями и национальными духами.

Затем создай и проверь минимальную реализацию отдельной капитуляции.

Только после этого подключай её к основной гражданской войне.

Скиллы обновляй так, чтобы они помогали работать с реальной архитектурой Nothing Wrong, а не с воображаемым идеальным модом.

Три новых скилла из этого документа являются готовыми проектными инструкциями. Адаптируй их только там, где это необходимо для соответствия фактическим файлам.

Сохраняй все полезные существующие разработки.

**Главная цель: получить первую играбельную пре-альфу Nothing Wrong, в которой Гражданская война проходит от начала до конца, участники имеют предусмотренные армии и национальные духи, а капитуляция разрешается в соответствии с правилами проекта.**

Начни с этапа P0 и предоставь владельцу конкретные результаты аудита. Не выдавай запланированную реализацию за уже выполненную.

**Конец директивы.**
