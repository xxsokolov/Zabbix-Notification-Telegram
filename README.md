# <p align="center">Zabbix Notification Telegram

<p align="center">Нотификатор оповещений в Telegram для <a href="https://www.zabbix.com/features#notification">Zabbix</a>.

_shields.io_

[Rating Popular на zabbix.com](https://www.zabbix.com/integrations/telegram#tab:3rd_party)

[Rating Popular на zabbix.com](https://share.zabbix.com/zabbix-tools-and-utilities/cat-notifications/zabbix-notification-telegram)

Support **Telegram**: https://t.me/ZbxNTg

### Возможности
- [x] Отправка графиков и последних значений **в одном сообщении**
- [x] Передача данных из Zabbix Action XML разметкой
- [x] Формирование списка urls в теле сообщения для быстрого перехода в разделы Zabbix (Trigger, History, Event, Acknowledget, Host)
- [x] Формирование списка tags в теле сообщения для быстрого поиска событий в Telegram (Trigger Tags, Eventid, Itemid, Triggeid, Actionid)
- [x] Настраиваемый Emoji mapping статуса и важности события
- [x] Наложение watermark на изображение
- [x] Формирование и обновление кэшфайла (privat, group, group -> supergroup)
- [x] Управление через Trigger Tags (Не прикреплять график, не отправлять уведомление, без push в Telegram и т.п.)
- [x] Обработка быстрых команд ботом <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">
- [x] Отправка показателей по запросу от бота <img alt="AppVeyor" src="https://img.shields.io/static/v1?label=status&message=beta&color=yellow?logo=appveyor">

## С чего начать
Для работы потребуется Python 3+ и Zabbix 3 и выше. Пока есть один путь установки, но мы работаем над расширением:
* Установка из source (git requires):
```
$ cd /usr/lib/zabbix/alertscripts
$ git clone https://github.com/xxsokolov/Zabbix-Notification-Telegram.git .
```
После этого нотификтор практически готов к работу, потребуется еще несколько минут.

## Создаем первое оповещение
### Получаем API token

Наверное Вы уже [получили API token от @BotFather](https://core.telegram.org/bots#botfather). Который будем использовать в [zbxTelegram_config.py](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py) файле [tg_token](https://github.com/xxsokolov/Zabbix-Notification-Telegram/blob/master/zbxTelegram_config.example.py#L19).
Если у Вас нет бота, то мы расскажем как [это сделать быстро](https://github.com/xxsokolov/Zabbix-Notification-Telegram/wiki/Регистрация-нового-бота-в-Telegram)









