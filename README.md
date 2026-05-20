# АРХИВ КОДА

исполнила: Бакаринова Софья Андреевна ИДБ-25-02 (СТАНКИН)

## 1\. база данных

таблица с данными о файлах (пример)

|file\_id(primary key и index)|filename|funct\_count|class\_count|
|:-:|:-:|:-:|:-:|
|1|file1|1|0|
|2|file2|2|1|
|3|file3|0|2|

таблица с данными о функциях (пример)

|file\_id(foreign key)|line|name|desc|
|:-:|:-:|:-:|:-:|
|1|5|function1|" "|
|2|15|employee.function\_smh|"this function does something"|
|2|30|function\_sum|"sums up numbers"|

таблица с данными о классах (пример)

|file\_id(foreign key)|line|name|desc|
|:-:|:-:|:-:|:-:|
|2|5|kitty|"this is a kitty class"|
|3|1|employee|" "|
|3|40|metro\_line1|"this class holds metro stations"|



## 2\. инструкция запуска

1. открыть терминал с директорией ".../BAKARINOVA\_TOPIT"
2. ввести в терминал "pip install -r requirements.txt"
3. после изменений ввести в терминал "uvicorn main:app"
4. терминал выведет ссылку (скорее всего http://127.0.0.1:8000/)
5. перейти по ссылке (не закрывать терминал, т.к. после закрытия ссылка перестанет работать)
6. включить автоформатирование

## 3\. примеры запросов

1. ".../api/files"
'''
\[
{
"file": 1,
"name": "functions1",
"functions": 2,
"classes": 0
},
{
"file": 2,
"name": "functions2",
"functions": 2,
"classes": 1
},
{
"file": 3,
"name": "getdata\_funcs",
"functions": 3,
"classes": 0
},
{
"file": 4,
"name": "haha\_file",
"functions": 1,
"classes": 0
},
{
"file": 5,
"name": "nothing",
"functions": 0,
"classes": 0
},
{
"file": 6,
"name": "sqlite\_funcs",
"functions": 3,
"classes": 0
}
]
'''
2. ".../api/files/functions1/structure"
'''
\[
{
"type": "func",
"name": "summator",
"defined on line": 2,
"docstring": " summator takes a and b and returns their sum"
},
{
"type": "func",
"name": "FiNdx",
"defined on line": 7,
"docstring": "hAhA haHAHAHA SeaL"
}
]
'''
3. ".../api/files/functins1/structure" (неправильно введенное название файла)
'''
\[]
'''
4. "../api/search?q=int"
'''
\[
{
"from file:": "printseal",
"type": 1,
"name": "printseal",
"defined on line": 1,
"docstring": "prints a seal"
},
{
"from file:": "pNum",
"type": "class",
"name": "pNum",
"defined on line": 2,
"docstring": " class pNum  holds an integer\\n    it uses a function to check if the number a palindrome\\n    "
},
{
"from file:": "insertdata",
"type": 1,
"name": "insertdata",
"defined on line": 42,
"docstring": "inserts data into a line in tabname table"
}
]
'''
5. ".../api/search?q=int\&type=class"
'''
\[
{
"from file:": "pNum",
"type": "class",
"name": "pNum",
"defined on line": 2,
"docstring": " class pNum  holds an integer\\n    it uses a function to check if the number a palindrome\\n    "
}
]
'''

## итог

кроме обязательных задач также выполнена доп. задача:

* фильтрация поиска по типу сущности: ?type=class или ?type=function

