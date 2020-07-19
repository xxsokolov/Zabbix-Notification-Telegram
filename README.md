# Zabbix-Notification-Telegram

Отправка оповещений из Zabbix в Telegram

[Plans](#Plans)

[Installation](#Installation)

[Configuration](#Configuration)

### Key Features
- [x] Отправка графиков и последних значений **в одном сообщении**
- [x] Передача данных из Zabbix Action XML разметкой
- [x] Формирование списка линков в теле сообщения для быстрого перехода в разделы Zabbix (Trigger, History, Event, Acknowledget, Host)
- [x] Формирование списка тэгов в теле сообщения для быстрого поиска событий в Telegram (Trigger Tags, Eventid, Itemid, Triggeid, Actionid)
- [x] Настраиваемый Emoji мапинг статуса и важности события
- [x] Наложение ватермарки на изображение
- [x] Формирование и обновление кэшфайла (privat, group, group -> supergroup)
- [x] Управление через Trigger Tags (Не прикреплять график, не отправлять уведомление и т.п.)
- [x] Обработка быстрых команд ботом <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">
- [x] Отправка показателей по запросу от бота <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">

<a name="Installation"><h3>Installation</h2></a>

* Становимся пользователем, от имени которого будет работать скрипт на системном уровне (по-умолчанию `zabbix`)
```bash
sudo su - zabbix
```

* Перейдем в директорию
```bash
cd /usr/lib/zabbix/alertscripts/
```

* С клонируем свежий релиз с GitHub
```bash
git clone https://github.com/xxsokolov/Zabbix-Notification-Telegram.git .
```

* Создадим виртуальное окружение
```bash
virtualenv venv --python=python3
``` 
или 
```bash
python3 -m venv venv
``` 

* Активируем виртуальное окружение
```bash
source venv/bin/activate
```

* Установим библиотеки 
```bash
pip install -r .requirements
deactivate
```

* Копируем файл конфигурации:
```bash
cp zbxTelegram_config.example.py zbxTelegram_config.py
```

* Выдаем права
```bash
chown -R zabbix:zabbix zbxTelegram.py zbxTelegram_config.py zbxTelegram_files/ 
```

* Разрешим выполнять файл скрипта
```bash
chmod +x zbxTelegram.py
```

* Редактируем конфигурационный файл 
```bash
vim zbxTelegram_config.py
```
 
 
<a name="Configuration"><h3>Configuration</h2></a>


**Настройка zbxTelegram_config.py**


`tg_proxy` = Отправка через прокси True/False; по-умолчанию True

`tg_proxy_server`  = Адрес прокси сервера

`tg_token` = token to access the Telegram API

`zabbix_api_url` = Путь до Zabbix (бэкслеш '/' в конце обязателен)

`zabbix_api_login` = Логин пользователя с минимум правами чтения на нужные группы, откуда мы хотим получать оповещения

`zabbix_api_pass` = Пароль


**Настройка Media types в Zabbix**


_Name_: ZNT

_Type_: Script

_Script name_: zbxTelegram.py

_Script parameters_:

`{ALERT.SENDTO}`

`{ALERT.SUBJECT}`

`{ALERT.MESSAGE}`


**Настройка Actions**


* Default subject

`{Problem} {TRIGGER.SEVERITY} {{TRIGGER.SEVERITY}}: {EVENT.NAME}`

`{Resolved} {TRIGGER.SEVERITY} {{TRIGGER.SEVERITY}} {EVENT.NAME}`

`{Update} {TRIGGER.SEVERITY} {{TRIGGER.SEVERITY}} {EVENT.NAME}`

`{Problem}` - мапинг значений Problem\Resolved\Update в emoji (config: zabbix_status_emoji_map)

`{{TRIGGER.SEVERITY}}` - мапинг значений Severity в emoji (config: zabbix_status_emoji_map)

* Default message

Для настройки оповещения используется XML разметка _(Исходные данные Вы найдете в actions.example)_

В самом простом рабочем варианте контент из файла _actions.example_ копируется в настройку оповещения, поле `Default message`

Она состоит из основных секций:

```xml
<body>
   <messages>
      Текст сообщения
   </messages>
</body>
``` 

```xml
<settings> 
       Настройки
</settings>
``` 

<img src="https://imgur.com/m6DosDL.png">

**Тестирование**

* Из консоли
```bash
./zbxTelegram.py @username test test

[2019-11-26 11:48:37,723] - PID:73794 - main() - zbxTelegram.py:311 - INFO: Send to @username action: test
[2019-11-26 11:48:37,723] - PID:73794 - main() - zbxTelegram.py:412 - INFO: Connection check passed (http://127.0.0.1/zabbix/)
[2019-11-26 11:48:38,653] - PID:73794 - send_messages() - zbxTelegram.py:290 - INFO: Bot @bot(00000000) send photo to @username (00000000)
```
* Из media type
<img src="https://imgur.com/6ej0d40.png">


**Описание настроек**

`<graphs></graphs>` - прикреплять график (True\False)

`<graphlinks>True</graphlinks>` - прикрепить ссылку url на History (True\False)

`<triggerlinks>True</triggerlinks>` - прикрепить ссылку url из триггера (True\False)

`<tag>True</tag>` - прикрепить теги (True\False)

`<graphs_period></graphs_period>` - период графика в секундах

`<itemid></itemid>` - передача itemid {ITEM.ID1}

`<triggerid></triggerid>` - передача triggerid {TRIGGER.ID}

`<eventid></eventid>`- передача eventid {EVENT.ID}

`<title></title>` - заголовок графика {HOST.HOST} - {EVENT.NAME}

`<triggerurl></triggerurl>` - передача url из триггера {TRIGGER.URL}

`<tags></tags>` - передача списка тэгов из триггера {EVENT.TAGS}


#### Нотиф:

<img src="https://imgur.com/ayKo62v.png">

###### Жду всех в **Telegram**: https://t.me/ZbxNTg
