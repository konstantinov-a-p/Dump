#### Детектор штампов
__Цель:__ найти штамп на изображении, а так же его угол наклона

__Решение__ задачи реализовано методами библиотеки __opencv__.   
На входе программа принимает два позиционных аргумента: `путь к шаблону` штампа и `путь к изображению`, на котором ищется штамп.
Ключевой аргумент `-d` отвечает за выбор детектора: 1 (по умолчанию) - FLANN, 2 - SURF.

На выходе возвращается угол наклона и координаты региона, в котором должен находиться штамп.
Если регион не удаётся найти, программа выводит строку `FAIL`.

В папке `test` представлен набор тестируемых изображений и визуализированные результаты работы программы.