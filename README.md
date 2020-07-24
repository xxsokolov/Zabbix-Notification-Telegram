# <p align="center">Zabbix Notification Telegram
<p align="center">Нотификатор оповещений в Telegram для <a href="https://www.zabbix.com/features#notification">Zabbix</a>.<br />
Простая установка, гибкая настройка, информативные сообщения.
<p align="center"><a href="https://www.zabbix.com/integrations/telegram#tab:3rd_party">Popular на www.zabbix.com</a><a href="https://share.zabbix.com/zabbix-tools-and-utilities/cat-notifications/zabbix-notification-telegram"> и share.zabbix.com</a>
<br />
<img alt="AppVeyor" src="https://img.shields.io/github/last-commit/xxsokolov/Zabbix-Notification-Telegram">
<img alt="AppVeyor" src="https://img.shields.io/badge/python-3-blue">
<img alt="AppVeyor" src="https://img.shields.io/github/license/xxsokolov/Zabbix-Notification-Telegram">


* [Возможности](#возможности)
* [Планы](#планы)
* [С чего начать](#с-чего-начать)
   * [Установка из source](#установка-из-source-git-requires)
* [Создаем первое оповещение](#создаем-первое-оповещение)
  * [Получаем API token](#получаем-api-token)
* [Настраиваем нотификатор](#настраиваем-нотификатор)
  * [Конфигурационный файл](#конфигурационный-файл)
  * [XML разметка](#xml-разметка)
* [Логирование](#логирование)
* [F.A.Q](#faq)
* [Последние значимые изменения](#последние-значимые-изменения)
* [Помощь Обсуждение Чат](#помощь-обсуждение-чат)

## Возможности
- Графики, информативные заголовки, ссылки<a href="#note1" id="note1ref"><sup>1</sup></a> и тэги<a href="#note2" id="note2ref"><sup>2</sup></a> объедены в **одно единое сообщение**.
- Формирование и обновление кэш файла (privat, group, group -> supergroup)<a href="#note3" id="note3ref"><sup>3</sup></a>
- Гибкая настройка через конфигурационный файл, XML разметку в [действиях триггеров](https://www.zabbix.com/documentation/current/manual/config/notifications/action) и Trigger Tags<a href="#note4" id="note4ref"><sup>4</sup></a>
- Маппинг Emoji статуса и важности события.
- Наложение watermark на изображен

## Планы
- Обработка быстрых команд ботом <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">
- Отправка метрик по запросу от бота <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">

## С чего начать
Нам для работы потребуется Python 3+ и Zabbix 3+. Пока есть один путь установки, но мы работаем над расширением вариантов:
#### Установка из source (git requires)*:
```
$ cd /usr/lib/zabbix/alertscripts
$ git clone https://github.com/xxsokolov/Zabbix-Notification-Telegram.git .
```
После этого нотификтор практически готов к работе, потребуется еще несколько шагов.

*Подробную инструкцию вы можете найти на нашей wiki: [RU](https://github.com/xxsokolov/Zabbix-Notification-Telegram/wiki/Установка-нотификатора-Zabbix-Notification-Telegram), ENG (vacant)*


## Создаем первое оповещение
### Получаем API token

Наверное Вы уже [получили API token от @BotFather](https://core.telegram.org/bots#botfather) который будем использовать в [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py): [tg_token](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L19).

*Если у Вас нет бота, то мы расскажем как это сделать быстро: [RU](https://github.com/xxsokolov/Zabbix-Notification-Telegram/wiki/Регистрация-нового-бота-в-Telegram), ENG (vacant)*

## Настраиваем нотификатор
### Конфигурационный файл
Основная конфигурация нотификатора производится через файл [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py). 

## <p align="center"> :exclamation: ВАЖНО! Конфиг файл [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py) имеет преимущество перед XML. :exclamation:

Давайте разберем каждый параметр подробно:
|Имя|Аргумент(ы)|Описание|По умолчанию|
|---|-----------|--------|------------|
|config_debug_mode|bool|Логирование в режиме debug| False|
|config_exc_info|bool|Более детальный режим debug|False|
|config_cache_file|string|Абсолютный путь до кеш файла|```/usr/lib/zabbix/alertscripts/zbxTelegram_files/id.cache```|
|config_log_file|string|Абсолютный путь до лог файла|```/usr/lib/zabbix/alertscripts/zbxTelegram_files/znt.log```|
|tg_proxy|bool|Использовать прокси для отправки сообщений в Telegram|True|
|tg_proxy_server|dict|Ссылка до Вашего прокси|```{'https': 'socks5://username:password@domen:port'}```
|tg_token|string|Тот самый token, который Вы получали у [@BotFather](https://core.telegram.org/bots#botfather)|```123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s```|
|watermark|bool|Наносить ватермарку на изображение графика|True|
|watermark_label|string|Текст наносимый на изображение графика|'Dmitry Sokolov (https://github.com/xxsokolov)'|
|watermark_font|string|Путь до файла шрифта|```/usr/lib/zabbix/alertscripts/zbxTelegram_files/ArialMT.ttf```|
|watermark_minimal_height|string|Минимальный размер изображения графика для нанесения ватермарки|30|
|watermark_fill|string||255|
|watermark_rotate|string||0|
|watermark_expand|bool||True|
|watermark_text_color|string|Цвет текста в RGB|(60, 60, 60)|
|body_messages|string|Шаблон формирование тела сообщения. *Сообщение состоит из двух частей: subject и messages(xml```<messages></messages>``` + линки + тэги)* |```<b>{subject}</b>\n\n{messages}```|
|body_messages_title|string|Шаблон формирования заголовка изображения графика.  *```{title}``` формируется из секции xml```<title></title>``` и ```<graphs_period></graphs_period>```или ```graphs_period_default``` в конфиг файле*|```{title} ({period_hour}h)```|
|body_messages_url|bool|Добавление линков в сообщение|True|
|body_messages_url_notes = True|bool|Добавление линка из триггера в сообщение|True|
|body_messages_url_graphs = True|bool|Добавление линка на график "Элемент данных" (item) в сообщение|True|
|body_messages_url_host = True|bool|Добавление линка на "Узел сети" (host) в сообщение|True|
|body_messages_url_ack = True|bool|Добавление линка на ["Подтверждение проблем"](https://www.zabbix.com/documentation/current/ru/manual/acknowledges) в сообщение|True|
|body_messages_url_event = True|bool|Добавление линка на ["Детали события"](https://www.zabbix.com/documentation/3.0/manual/web_interface/frontend_sections/monitoring/events) в сообщение|True|
|body_messages_url_template|sting|Шаблон формирование линка|```<a href="{url}">{icon}</a>```|
|body_messages_url_template_line|sting|Шаблон формирования поля с линками в сообщении|```\nLinks: {links}```|
|body_messages_url_delimiter|sting|Разделитель между линками|'&nbsp; '|
|body_messages_url_emoji_no_url|emoji|Иконка при отсутствии [URL](https://www.zabbix.com/documentation/current/ru/manual/config/triggers/trigger) в триггере|➖|
|body_messages_url_emoji_notes|emoji|Иконка ссылки [URL](https://www.zabbix.com/documentation/current/ru/manual/config/triggers/trigger) в триггере|ℹ️|
|body_messages_url_emoji_graphs|emoji|Иконка ссылки на график "Элемент данных" (item)|📊|
|body_messages_url_emoji_host|emoji|Иконка ссылки на "Узел сети" (host)|📟|
|body_messages_url_emoji_ack|emoji|Иконка ссылки на ["Подтверждение проблем"](https://www.zabbix.com/documentation/current/ru/manual/acknowledges)|✉️|
|body_messages_url_emoji_event|emoji|Иконка ссылки на ["Детали события"](https://www.zabbix.com/documentation/3.0/manual/web_interface/frontend_sections/monitoring/events)|📋|
|body_messages_tags|bool|Добавление всех тэгов в сообщение|True|
|body_messages_tags_event|||True|
|body_messages_tags_eventid|bool|Добавление eventid тэгов в сообщение|True|
|body_messages_tags_itemid|bool|Добавление itemid тэгов в сообщение|True|
|body_messages_tags_triggerid|bool|Добавление triggerid тэгов в сообщение|True|
|body_messages_tags_actionid|bool|Добавление actionid тэгов в сообщение|True|
|body_messages_tags_hostid|bool|Добавление hostnid тэгов в сообщение|True|
|body_messages_tags_template_line|sting||```\n\n{tags}```|
|body_messages_tags_no|sting|Тег при отсутствии тэга в узле сети|```#no_tags```|
|body_messages_tags_delimiter|sting|Разделитель между тэгами|'&nbsp; '|
|body_messages_tags_prefix_eventid|sting|Шаблон формирования тэга eventid|```eid_```|
|body_messages_tags_prefix_itemid|sting|Шаблон формирования тэга itemid|```iid_```|
|body_messages_tags_prefix_triggerid|sting|Шаблон формирования тэга triggerid|```tid_```|
|body_messages_tags_prefix_actionid|sting|Шаблон формирования тэга actionid|```aid_```|
|body_messages_tags_prefix_hostid|sting|Шаблон формирования тэга hostidid|```hid_```|
|tag_settings_no_graph|sting|Имя тега "Не прикреплять изображение графика"|```no_graph```|
|zabbix_keyboard|bool|Добавление кнопок к сообщению (*В стадии разработки*)|False|
|zabbix_keyboard_button_message|sting|Имя кнопки "Добавить сообщение к событию"|```Message```|
|zabbix_keyboard_button_acknowledge|sting|Имя кнопки "Подтверждение события"|```Acknowledge```|
|zabbix_keyboard_button_history|sting|Имя кнопки "Прислать сообщение (пять последних событий)" по данному элементу данных|```History```|
|zabbix_keyboard_row_width|int|Количество кнопок в строке|3|
|zabbix_api_url|sting|Урл до Zabbix сервера|```http://127.0.0.1/zabbix/```|
|zabbix_api_login|sting|Учетная запись|```Admin```|
|zabbix_api_pass|sting|Пароль|```zabbix```|
|zabbix_graph|bool|Добавление изображения графика к сообщению|True|
|zabbix_graph_period_default|int|Период за который присылается изображение графика в секундах.|43200|
|zabbix_graph_chart|sting|Шаблон формирования линка до chart3.php|[Default](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L65)|
|zabbix_host_link|sting|Шаблон формирования линка до узла сети|```{zabbix_server}zabbix.php?action=search&search={host}```|
|zabbix_graph_link|sting|Шаблон формирования линка до графика "Элемент данных" (item)|```{zabbix_server}history.php?action=showgraph&itemids[]={itemid}&from=now-{range_time}```|
|zabbix_ack_link|sting|Шаблон формирования линка до ["Подтверждение проблем"](https://www.zabbix.com/documentation/current/ru/manual/acknowledges)|```{zabbix_server}zabbix.php?action=acknowledge.edit&eventids[0]={eventid}```|
|zabbix_event_link|sting|Шаблон формирования линка до ["Детали события"](https://www.zabbix.com/documentation/3.0/manual/web_interface/frontend_sections/monitoring/events)|```{zabbix_server}tr_events.php?triggerid={triggerid}&eventid={eventid}```|
|zabbix_status_emoji_map|dict|Словарь соответствия типа события и emoji|{"Problem": "🚨", "Resolved":"✅", "Update": "🚧", "InformWikipedia", "Warning":"💛", "Average":"🧡", "High":"❤️", "Disaster": "💔", "Test": "🚽💩"}|

### XML разметка
Дополнительная конфигурация производится через XML разметку([пример](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/actions.example)) в [Zabbix Action](https://www.zabbix.com/documentation/current/manual/config/notifications/action).

Также разберем эти параметры:
|Имя|Аргумент(ы)|Описание|По умолчанию|
|---|-----------|--------|------------|
|```<messages></messages>```|string||[Default](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/actions.example#L4)|
|```<graphs></graphs>```|bool|Добавление изображения графика в сообщение.|True|
|```<hostlinks></hostlinks>```|bool|Добавление линка на "Узел сети" (host) в сообщение.|True|
|```<graphlinks></graphlinks>```|bool|Добавление линка на график "Элемент данных" (item) в сообщение.|True|
|```<triggerlinks></triggerlinks>```|bool|Добавление линка из триггера в сообщение.|True|
|```<tag></tag>```|bool|Добавление всех тэгов в сообщение.|True|
|```<eventtag></eventtag>```|bool|Добавление тэгов события в сообщение.|True|
|```<eventidtag></eventidtag>```|bool|Добавление тэгa c eventid в сообщение.|True|
|```<itemidtag></itemidtag>```|bool|Добавление тэгa c itemid в сообщение.|True|
|```<triggeridtag></triggeridtag>```|bool|Добавление тэгa c triggerid в сообщение.|True|
|```<actionidtag></actionidtag>```|bool|Добавление тэгa c actionid в сообщение.|True|
|```<hostidtag></hostidtag>```|bool|Добавление тэгa c hostid в сообщение.|True|
|```<keyboard></keyboard>```|bool|Добавление кнопок к сообщению (*В стадии разработки*).|True|
|```<graphs_period></graphs_period>```|string|Период за который присылается изображение графика в секундах.|10800|
|```<host></host>```|string|Макрос имени узла сети.|{HOST.ID1}|
|```<itemid></itemid>```|string|Макросы ИД элементов данных.|{ITEM.ID1} {ITEM.ID2} {ITEM.ID3} {ITEM.ID4}|
|```<triggerid></triggerid>```|string|Макрос ИД триггера.|{TRIGGER.ID}|
|```<eventid></eventid>```|string|Макрос ИД события.|{EVENT.ID}|
|```<actionid></actionid>```|string|Макрос ИД действия.|{ACTION.ID}|
|```<hostid></hostid>```|string|Макрос ИД узла сети.|{HOST.ID1}|
|```<title><![CDATA[]]></title>```|string|Шаблон формирования заголовка изображения графика из макросов: имя узла сети и имя события.|{HOST.HOST} - {EVENT.NAME}|
|```<triggerurl><![CDATA[]]></triggerurl>```|string|Макрос URL триггера.|{TRIGGER.URL}|
|```<eventtags><![CDATA[]]></eventtags>```|string|Макрос тэгов события разделенных запятой. Макрос объединяет теги из узла сети, шаблона, триггера.|{EVENT.TAGS}|

**[Макросы поддерживаемые по назначению](https://www.zabbix.com/documentation/current/ru/manual/appendix/macros/supported_by_location)*

```<![CDATA[]]>```:
_В XML документах фрагмент, помещенный внутрь CDATA, — это часть содержания элемента, которая помечена для парсера как содержащая только символьные данные, а не разметку. CDATA — это просто альтернативный синтаксис для отображения символьных данных, нет никакой смысловой разницы между символьными данными, которые объявлены как CDATA и символьными данными, которые объявлены в обычном синтаксисе и где «<» и «>» будут представлены как «&lt;» и «&gt;», соответственно. ([Wikipedia](https://ru.wikipedia.org/wiki/CDATA))_


## Логирование

Все основные события (отправка, добавления в кеш файл, изменение группы в суппергруппу, ошибки, дебаг) логируются в файле ```znt.log```, Вы можете его найти по-умолчанию ```/usr/lib/zabbix/alertscripts/zbxTelegram_files/znt.log``` ([config_log_file](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L15))
Поддерживаются три режима логирования:
1. Обычный(по-умолчанию), ведется минимальный лог об операциях в нотификаторе;
2. [Debug](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L12), более детальный лог, требуется только для анализа ошибок в работе нотификатора *(по-умолчанию False)*;
3. [exc_info](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L13), полный Traceback ошибок *(по-умолчанию False)*;

## F.A.Q
#### Сообщения не приходят


## Последние значимые изменения

* Добавлены и изменены переменные в конфиг файле
* Изменен XML


## Помощь. Обсуждение. Чат.

* Присоединяйтесь [ZNTGroup](https://t.me/ZbxNTg) и [ZNTChannel](https://t.me/ZNTChannel).


---
<a id="note1" href="#note1ref"><sup>1</sup></a>Формирование списка urls в теле сообщения для быстрого перехода в разделы Zabbix (Trigger, History, Event, Acknowledget, Host)<br />
<a id="note2" href="#note2ref"><sup>2</sup></a> Формирование списка tags в теле сообщения для быстрого поиска событий в Telegram (Trigger Tags, Eventid, Itemid, Triggeid, Actionid)<br />
<a id="note3" href="#note3ref"><sup>3</sup></a> Кеш файл это json массив содержащий имена юзуров, групп, суппергруп и их идентификаторы(ИД). Безопасность Telegram не позволяет напрямую писать по имени, только по ИД. Чтобы получить данный ИД надо написать лично Вашему боту или бот должен быть добавлен в группу . Только после этого нотификатор "подключается" к боту и получает все обновления которые произошли у бота (getUpdates). Далее мы находим никнейм или имя групп, куда решили отправить нотификацию, и их ИД, которые и кладем в кэш файл.
[FAQ Telegram](https://core.telegram.org/bots/faq#what-messages-will-my-bot-get)<br />
<a id="note4" href="#note4ref"><sup>4</sup></a> Управление через Trigger Tags (Не прикреплять график, не отправлять уведомление, без push в Telegram *dev* и т.п.)
