# Zabbix-Notification-Telegram

Отправка оповещений из Zabbix в  Telegram

[Plans](#Plans)

[Installation](#Installation)

[Configuration](#Configuration)

### Key Features
- [x] Отправка графиков и последних значений **в одном сообщении**
- [x] Гибкая настройка шаблона в теле сообщения
- [x] Передача данных из экшена XML разметкой
- [x] Формирование списка линков в теле сообщения
- [x] Формирование списка тэгов в теле сообщения
- [x] Emoji мапинг статуса и важности события
- [x] Наложение ватермарки на изображение
- [x] Формирование и обновление кэшфайла (group -> supergroup)


<a name="Plans"><h3>Plans</h2></a>
- Обработка быстрых команд ботом
- Отправка показателей по запросу от бота
- Gitlab CI\CD

<a name="Installation"><h3>Installation</h2></a>

* С клонируем свежий релиз с GitHub
```bash
git clone https://github.com/xxsokolov/Zabbix-Notification-Telegram.git
```

* Перейдем в директорию
```bash
cd Zabbix-Notification-Telegram/
```

* Создадим виртуальное окружение
```bash
virtualenv venv --python=python3
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

* Скопируем исполняемые файлы в директорию alertscripts:

```bash
cp -r * /usr/lib/zabbix/alertscripts/
```
_Путь указан в -_  `zabbix_server.conf -> AlertScriptsPath=`

* Перейдем в директорию alertscripts
```bash
cd /usr/lib/zabbix/alertscripts/
```

* Разрешим выполнять файл скрипта
```bash
chmod +x zbxTelegram.py
```

* Переименуем файл конфигурации
```bash
cp zbxTelegram_config.example.py zbxTelegram_config.py
```

* Проверим файлы в директории:
```bash
ls -la
```
<img src="https://imgur.com/JNKkJCG.png"></img>

 
<a name="Configuration"><h3>Configuration</h2></a>


* Настройка **zbxTelegram_config.py**

`tg_proxy` = Отправка через прокси True/False

`tg_proxy_server` = прокси сервера

`tg_token` = token to access the HTTP API

**Настройка Actions**

* Default subject

`{Problem} {TRIGGER.SEVERITY} {{TRIGGER.SEVERITY}}: {EVENT.NAME}`

`{Problem}` - мапинг значений Problem\Resolved в emoji (config: zabbix_status_emoji_map)

`{{TRIGGER.SEVERITY}}` - мапинг значений Severity в emoji (config: zabbix_status_emoji_map)

* Default message

Для настройки оповещения используется XML разметка _(Исходные данные Вы найдете в actions.example)_

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

**Описание настроек**

`<graphs></graphs>` - прикреплять график (True\False)

`<graphs_period></graphs_period>` - период графика в секундах

`<itemid></itemid>` - передача itemid {ITEM.ID1}

`<triggerid></triggerid>` - передача triggerid {TRIGGER.ID}

`<eventid></eventid>`- передача eventid {EVENT.ID}

`<title></title>` - заголовок графика {HOST.HOST} - {EVENT.NAME}

`<triggerurl></triggerurl>` - передача url из триггера {TRIGGER.URL}

`<graphslinks></graphslinks>` - прикрепить ссылку на History (True\False)

`<tags></tags>` - передача списка тэгов из триггера {EVENT.TAGS}


#### Нотиф:

<img src="https://imgur.com/fQpq77E.png">

#### Настройка алерта:

<img src="https://imgur.com/9ke7VyX.png">

###### Жду всех в **Telegram**: https://t.me/ZbxNTg
