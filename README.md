## Цель этого проекта определение ориентации изображения текста.

В процессе работы над проектом были выполнены следующие этапы:

1) Подготовка изображений.
2) Обучение модели. 
3) Создание микросервиса. 

## Подготовка изображений
Подготовка модели была произведена в ноутбуке text-orientation-dataset-creation.ipynb. В результате были получены 4 папки с разными ориентациями изображения, количество изображений было увеличено в 4 раза.

## Обучение модели
Обучение модели производилось на площадке kaggle. Ссылка на ноутбук https://www.kaggle.com/code/zaurdzampati/text-orientation  
В результате обучения была получена модель resnet resnet_txt_orientation.pth

## Микросервис
Наш микросервис получает от Микоросервиса A на вход адрес изображения на хосте, затем сохраняет перевернутое изображение и отправляет следующему микросервису (назовем его микросервис C) адрес перевернутого изображения на хосте и угол поворота оригинального изображения.  
Роль микросервиса A играет html страница, а роль микросервиса C mock_service, который разворачивается отдельно при помощи docker

Адреса директорий на хосте должны быть связаны с локальными адресами адресами в контейнере при запуске образа докера при помощи параметров -e INPUT_DIR и -e OUTPUT_DIR. 

### Запуск микросервиса
Последовательность запуска сервисов следующая. 
1) Развернем mock сервис (микросервис C). Для этого перейдем в директорию programm/mock_service и выполним в терминале следующие команды:
- построим образ

docker build -t mock_microservice_c .

- создадим и запустим контейнер

docker run -p 8001:8001 mock_microservice_c

2) Затем развернем основной микросервис.
Для этого перейдем в директорию programm/ и выполним в терминале следующие команды:
- построим образ

docker build -t img_text_orientation .

- создадим и запустим контейнер (нужно указать свои пути на хосте вместо /Users/zaurdzampaev/ml_projects/ocr_text_orientation/programm/servis_input и /Users/zaurdzampaev/ml_projects/ocr_text_orientation/programm/servis_output). Пути /app/input_images и /app/output_images менять не нужно, это пути внутри контейнера.

docker run -p 8000:8000 \
  -v /Users/zaurdzampaev/ml_projects/ocr_text_orientation/programm/servis_input:/app/input_images \
  -v /Users/zaurdzampaev/ml_projects/ocr_text_orientation/programm/servis_output:/app/output_images \
  -e INPUT_DIR=/Users/zaurdzampaev/ml_projects/ocr_text_orientation/programm/servis_input \
  -e OUTPUT_DIR=/Users/zaurdzampaev/ml_projects/ocr_text_orientation/programm/servis_output \
  img_text_orientation 

  3) Теперь мы можем перейти в браузере по адресу http://localhost:8000/ и передать адрес изображения на хосте (изображение должно находится в директории которая была указана при создании контейнера). После этого в другой директории, которую мы указали при запуске контейнера появится перевернутое изображение, а в браузере мы получим сообщение с путем до перевернутого изображения и оригинальным углом поворота текста на изображении (напр "microservice_c_response":{"received_rotated_image_path":"/Users/zaurdzampaev/ml_projects/text_orientation/programm/servis_output/405___399c076c405d45d7a5687b64c363804f.png","original_angle":90})