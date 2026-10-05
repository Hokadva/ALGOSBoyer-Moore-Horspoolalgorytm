## Использование

```bash
python main.py (-s STRING | -f FILE) -p SUBSTRING [SUBSTRING ...]
               [-c] [-m {first,last}] [-k COUNT] [--color] [--max_lines N]
```

### Аргументы

| Аргумент | Описание |
|----------|----------|
| `-s`, `--string` | исходная строка |
| `-f`, `--file` | путь к файлу (взаимоисключает первый вариант с `-s`) |
| `-p`, `--substring` | одна или несколько подстрок |
| `-c`, `--case-sensitive` | учитывать регистр (не учитывает по дефолту) |
| `-m`, `--method` | `first` (сначала) (сначала - по дефолту) или `last` (с конца) |
| `-k`, `--count` | сколько вхождений найти (по умолчанию все) |
| `--color` | подсветить найденные подстроки |
| `--max_lines` | ограничить вывод N строками (по умолчанию 10) |
| `-h`, `--help` | справка |

### Примеры

#### 1. Простой поиск одной подстроки

```bash
python main.py -s "ababbababa" -p aba
```

**Вывод:**
```
INFO:modules.logtime:search was executed by 0.000016
{'aba': (0, 5, 7)}
```

#### 2. Несколько подстрок

```bash
python main.py -s "ababbababa" -p aba bba
```

**Вывод:**
```
{'aba': (0, 5, 7), 'bba': (3,)}
```

#### 3. Ограничение числа вхождений

```bash
python main.py -s "ababbababa" -p aba bba -k 3
```

**Вывод** (3 вхождения в порядке обхода):
```
{'aba': (0, 5), 'bba': (3,)}
```

#### 4. Поиск с конца (`last`)

```bash
python main.py -s "ababbababa" -p aba bba -m last
```

**Вывод** (вхождения в обратном порядке):
```
{'aba': (7, 5, 0), 'bba': (3,)}
```

#### 5. Учёт регистра

```bash
python main.py -s "AbCabC" -p abc -c
```

**Вывод** (без совпадений - в тексте `AbC`, ищем `abc`):
```
Occurrences not found
```

Без `-c`:

```bash
python main.py -s "AbCabC" -p abc
```

**Вывод:**
```
{'abc': (0, 3)}
```
