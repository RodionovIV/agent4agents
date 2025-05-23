# Правила написания системной аналитики

## 1. Знакомство с бизнес-контекстом и бизнес-требованиями, их уточнение

## 2. Определение ролей пользователей и приложений. Верхнеуровневое проектирование архитектуры
**Определение ролей пользователей и приложений**

Нужно понять, кто будет пользоваться приложением и как. У каждой из этих групп будут свои потребности и требования к приложению. Наша задача — понять и описать все эти роли и их потребности. По итогам получится список ролей и пользовательские требования To Be для каждой из них.

**Верхнеуровневое проектирование архитектуры**

Сначала выделяем компоненты системы - отдельные приложения, сервисы:
- мобильное приложение,
- сервер Backend, который будет обрабатывать запросы от приложения, и может включать в себя подсистемы (сервисы, микросервисы),
- база данных для хранения информации о пользователях, вебинарах и новостях,
- внешние системы - источники данных, из которых надо получать данные и в которые их надо передавать (интеграции).

Для визуализации архитектуры можно использовать нотацию BPMN.
## 3. Выделение и описание основных сценариев работы с системой
На этом этапе нужно понять, как именно будут взаимодействовать различные роли с нашей системой. Рассматривается каждая роль, которая мы определилась на предыдущем этапе, и для каждой из них описывается основные действия, которые они будут выполнять в приложении.

**Use Case**

Use case — это описание того, как система и пользователи взаимодействуют друг с другом для достижения какой-то цели. Use case включает в себя не только последовательность действий, но и роли, которые участвуют в этом взаимодействии, и возможные альтернативные сценарии. Use case показывает, какие роли участвуют в сценарии, что они делают, и как система на это реагирует.

## 4. Проработка альтернативных сценариев
На этом этапе рассматривается, что произойдёт, если взаимодействие пользователя с системой не будет идти по основному сценарию. Это могут быть ситуации, когда что-то идёт не так, или когда пользователь решает сделать что-то по-другому.

Все эти варианты нужно проработать и описать как альтернативные сценарии. Каждый альтернативный сценарий должен описывать, что происходит в этой ситуации, и как система должна на это реагировать.

## 5. Требования к безопасности

На этом этапе необходимо описать основные требования к безопасности:

- Авторизация/аутентификация (OAuth, JWT).
- Защита данных (GDPR, шифрование).

## 6. Описание нефункциональных требований

На этом этапе необходимо описать нефункциональных требований.

- Требования к производительности, нагрузочное тестирование.
- Масштабируемость архитектуры.


## 7. Определение ключевых данных: сущности и их свойства
На этом этапе нужно понять, какие данные необходимы для работы нашего приложения и как они связаны друг с другом. Данные в системе обычно представлены в виде различных сущностей, которые имеют свои свойства и взаимосвязи. Также нужно определить, как эти сущности связаны друг с другом.

Определение ключевых данных, сущностей и их свойств - это важный этап работы, который помогает создать структуру системы и понять, как данные будут храниться и использоваться в приложении.

## 8. Задачи на доработку Базы Данных
Варианты:
- создать новые таблицы,
- добавить поля в существующие таблицы,
- сделать миграции данных (перенос и автозаполнение),
- иногда поменять типы данных, удалить лишние поля и так далее.

## 9. Задачи на разработку методов Backend (методов API)
На этом этапе нужно сформировать и описать все необходимые методы API.
Для каждого метода API нужно определить, какие данные он принимает на вход, и что он возвращает на выход. Также нужно описать основные протоколы: REST, GraphQL, SOAP.

## 10. Задачи на фронтенд / мобильные устройства
Задача на этом этапе - описать, что именно должен видеть и делать пользователь в приложении. Нужно подготовить список задач для фронтенд или мобильных разработчиков, которые включают работу, сделанную на предыдущих этапах: описание Use Cases, дизайн, методы API.

Вот пример таких задач:
1. Создание экрана регистрации на вебинар.
2. Отображение списка доступных вебинаров.
3. Создание уведомлений о предстоящих вебинарах.
4. Добавление возможности читать новости сообщества в приложении.

В каждой из этих задач нужно максимально подробно описать, как должен выглядеть и работать каждый из элементов экранных форм, чтобы разработчики могли воплотить задуманное в жизнь.

## 11. Тестирование функционала
На основании Use Case необходимо описать процесс тестирования функционала.