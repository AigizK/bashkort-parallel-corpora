# Башкирско-русский и русско-башкирский параллельный корпус

## You can download this dataset from the HuggingFace:
https://huggingface.co/datasets/AigizK/bashkir-russian-parallel-corpora

## Update 19.02.2023
- Все корпусы собрал в один JSONL файл: ba_ru.jsonl
- All corpus was joined to one JSONL file: ba_ru.jsonl


Sample of one row:

`{"ba": "535-тән ашыу скважина бырауланған.","ru": "Пробурено свыше 535 скважин.", "corpus": "bashkir encyclopedia"}`


## Папка 1000-sentences
Переведено с русского на башкирский преподавательницей башкирского языка и литературы Кагармановой Сарией Мухамадьяновной.
Рядом лежит исходный текст на английском

## Папка bash_ encyclopedia
Башкирская энциклопедия

## Папка bashinform
Новостной сайт

## Папка little_prince
Книга Маленький принц

## Папка translated_books
Эта папка содержит переведенные книги. Для того чтоб выровнять предложения сделано следующее:

- первый этап: с помощью инструмента https://github.com/averkij/lingtrain-aligner-editor  автоматом выравниваем текст
- второй этап: полученный результат скармливаем телеграмм боту @bashkort_translate_bot. А энтузиаст, подписанные на этот бот, просматривают каждую пару и отмечают, насколько перевод корректный.
