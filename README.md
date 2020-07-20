# <p align="center">Zabbix Notification Telegram

<p align="center">Нотификатор оповещений в Telegram для <a href="https://www.zabbix.com/features#notification">Zabbix</a>.

_shields.io_

[Rating Popular на www.zabbix.com](https://www.zabbix.com/integrations/telegram#tab:3rd_party)

[Rating Popular на share.zabbix.com](https://share.zabbix.com/zabbix-tools-and-utilities/cat-notifications/zabbix-notification-telegram)

### Возможности
- [x] Отправка графиков и последних значений **в одном сообщении**
- [x] Передача данных из [Zabbix Action](https://www.zabbix.com/documentation/current/manual/config/notifications/action) разметкой XML 
- [x] Формирование списка urls в теле сообщения для быстрого перехода в разделы Zabbix (Trigger, History, Event, Acknowledget, Host)
- [x] Формирование списка tags в теле сообщения для быстрого поиска событий в Telegram (Trigger Tags, Eventid, Itemid, Triggeid, Actionid)
- [x] Настраиваемый Emoji mapping статуса и важности события
- [x] Наложение watermark на изображение
- [x] Формирование и обновление кэш файла (privat, group, group -> supergroup)
- [x] Управление через Trigger Tags (Не прикреплять график, не отправлять уведомление, без push в Telegram *dev* и т.п.)
- [x] Обработка быстрых команд ботом <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">
- [x] Отправка метрик по запросу от бота <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">

## С чего начать
Нам для работы потребуется Python 3+ и Zabbix 3+. Пока есть один путь установки, но мы работаем над расширением:
* Установка из source (git requires)*:
```
$ cd /usr/lib/zabbix/alertscripts
$ git clone https://github.com/xxsokolov/Zabbix-Notification-Telegram.git .
```
После этого нотификтор практически готов к работу, потребуется еще несколько шагов.

**Подробную инструкцию вы можете найти в нашей wiki: [RU](https://github.com/xxsokolov/Zabbix-Notification-Telegram/wiki/Установка-нотификатора-Zabbix-Notification-Telegram), ENG (vacant)*


## Создаем первое оповещение
### Получаем API token

Наверное Вы уже [получили API token от @BotFather](https://core.telegram.org/bots#botfather). Который будем использовать в [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py): [tg_token](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L19).
Если у Вас нет бота, то мы расскажем как [это сделать быстро](https://github.com/xxsokolov/Zabbix-Notification-Telegram/wiki/Регистрация-нового-бота-в-Telegram).

### Настраиваем нотификатор

Основная конфигурация нотификатора производится через файл [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py). 

Давайте разберем каждый параметр подробно:
|Имя|Аргумент(ы)|Описание|По умолчанию|
|---|---|  ---|---|
|config_debug_mode|bool|Логирование в режиме debug| False|
|config_exc_info|bool|Более детальный режим debug|False|
|config_cache_file|string|Абсолютный путь до кеш файла|'/usr/lib/zabbix/alertscripts/zbxTelegram_files/id.cache'|
|config_log_file|string|Абсолютный путь до лог файла|'/usr/lib/zabbix/alertscripts/zbxTelegram_files/znt.log'|
|tg_proxy|bool|Использовать прокси для отправки сообщений в Telegram|True|
|tg_proxy_server|dict|Урл до Вашего прокси|{'https': 'socks5://username:password@domen:port'}
|tg_token|string|Тот самый token, который Вы получали у [@BotFather](https://core.telegram.org/bots#botfather)|'123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s'|
|watermark|bool|Наносить ватермарку на изображение графика|True|
|watermark_label|string|Текст наносимый на изображение графика|'Dmitry Sokolov (https://github.com/xxsokolov)'|
|watermark_font|string|Путь до файла шрифта|'/usr/lib/zabbix/alertscripts/zbxTelegram_files/ArialMT.ttf'|
|watermark_minimal_height|string|Минимальный размер изображения графика для нанесения ватермарки|30|
|watermark_fill|string||255|
|watermark_rotate|string||0|
|watermark_expand|bool||True|
|watermark_text_color|string|Цвет текста в RGB|(60, 60, 60)|
|body_messages|string|Формирование тела сообщения. *Сообщение состоит из двух частей: subject и messages(xml```<messages></messages>``` + линки + тэги)* |'<b>{subject}</b>\n\n{messages}'|
|body_messages_title|string|Формирование заголовка изображения графика.  *```{title}``` формируется из секции xml```<title></title>``` и ```<graphs_period></graphs_period>```или ```graphs_period_default``` в конфиг файле*|'{title} ({period_hour}h)'|
|body_messages_url|||True|
|body_messages_url_template|||'<a href="{url}">{icon}</a>'|
|body_messages_no_url|||'➖'|
|body_messages_url_notes|||'ℹ️'  # URL in trigger|
|body_messages_url_ld_graphs|||'📊'  # URL history graph item|
|body_messages_url_host|||'📟'  # URL host|
|body_messages_url_akk|||'✉️'  # URL update problem|
|body_messages_url_event|||'📋'  # URL in event|
|body_messages_tags|||True|
|body_messages_add_tags_event|||True|
|body_messages_add_tags_item|||True|
|body_messages_add_tags_trigger|||True|
|body_messages_add_tags_action|||True|
|body_messages_no_tags|||'#no_tags'|
|body_messages_tags_delimiter|||' '|
|body_messages_tag_eventid|||'#eid_'|
|body_messages_tag_itemid|||'#iid_'|
|body_messages_tag_triggerid|||'#tid_'|
|body_messages_tag_actionid|||'#aid_'|
|tag_settings_no_graph|||'no_graph'|
|zabbix_keyboard|||False|
|zabbix_keyboard_button_message|||'Message'|
|zabbix_keyboard_button_acknowledge|||'Acknowledge'|
|zabbix_keyboard_button_history|||'History'|
|zabbix_keyboard_row_width|||3|
|zabbix_api_url|||'http://127.0.0.1/zabbix/'|
|zabbix_api_login|||'Admin'|
|zabbix_api_pass|||'zabbix'|
|graphs_period_default|||43200  # 24h|
|zabbix_graff_chart|||[Default](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L65)|
|zabbix_host_link|||"{zabbix_server}zabbix.php?action=search&search={host}"|
|zabbix_graff_link|||"{zabbix_server}history.php?action=showgraph&itemids[]={itemid}&from=now-{range_time}"|
|zabbix_akk_link|||"{zabbix_server}zabbix.php?action=acknowledge.edit&eventids[0]={eventid}"|
|zabbix_event_link|||"{zabbix_server}tr_events.php?triggerid={triggerid}&eventid={eventid}"|
|zabbix_status_emoji_map|||{"Problem": "🚨", "Resolved":"✅", "Update": "🚧", "Information": "💙", "Warning":"💛", "Average":"🧡", "High":"❤️", "Disaster": "💔", "Test": "🚽💩"}|


Дополнительная конфигурация производится через XML разметку([пример](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/actions.example)) в [Zabbix Action](https://www.zabbix.com/documentation/current/manual/config/notifications/action).

## <p align="center"> :exclamation: ВАЖНО! XML имеет преимущество перед конфиг файлом [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py). :exclamation:

Также разберем эти параметры:
|Имя|Аргумент(ы)|Описание|По умолчанию|
|---|---|  ---|---|
|```<messages></messages>```|string||[Default](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/actions.example#L4)|
|```<graphs></graphs>```|bool||True|
|```<hostlinks></hostlinks>```|bool||True|
|```<graphlinks></graphlinks>```|bool||True|
|```<triggerlinks></triggerlinks>```|bool||True|
|```<tag></tag>```|bool||True|
|```<keyboard></keyboard>```|bool||True|
|```<graphs_period></graphs_period>```|string||10800|
|```<host></host>```|string||{HOST.ID1}|
|```<itemid></itemid>```|string||{ITEM.ID1} {ITEM.ID2} {ITEM.ID3} {ITEM.ID4}|
|```<triggerid></triggerid>```|string||{TRIGGER.ID}|
|```<eventid></eventid>```|string||{EVENT.ID}|
|```<actionid></actionid>```|string||{ACTION.ID}|
|```<title><![CDATA[]]></title>```|string||{HOST.HOST} - {EVENT.NAME}|
|```<triggerurl><![CDATA[]]></triggerurl>```|string||{TRIGGER.URL}|
|```<tags><![CDATA[]]></tags>```|string||{EVENT.TAGS}|

Zabbix Macros

```<![CDATA[]]>```



## Логирование
## Последние изменения


## Помощь. Обсуждение. Чат.

* Присоединяйтесь [ZNTGroup](https://t.me/ZbxNTg) и [ZNTChannel](https://t.me/ZNTChannel).

