# Zabbix-Notification-Telegram

Отправка оповещений из Zabbix в  Telegram

### Key Features
- [x] Отправка нотификации ОДНИМ СООБЩЕНИЕМ, методом sendPhoto
- [x] Гибкая настройка шаблона в теле сообщения
- [x] Данные передаются XML
- [x] Формирование спика линков в теле сообщения
- [x] Формирование спика тэгов в теле сообщения
- [x] Emoji мапинг статуса и важности события

### Plans
- Обработка быстрых команд ботом
- Отправка показателей по запросу от бота
- Gitlab CI\CD

### Installation

* Склонируем свежий релиз с GitHub
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

* Скопируем исполняемые файлы в деррикторию alertscripts:

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



* Проверим отправку
```bash
/usr/lib/zabbix/alertscripts/zbxTelegram.py
```

### Configuration 

Файл


#### Нотиф:

<img src="https://imgur.com/fQpq77E.png">

#### Настройка алерта:

<img src="https://imgur.com/9ke7VyX.png">

###### Жду всех в **Telegram**: https://t.me/ZbxNTg
