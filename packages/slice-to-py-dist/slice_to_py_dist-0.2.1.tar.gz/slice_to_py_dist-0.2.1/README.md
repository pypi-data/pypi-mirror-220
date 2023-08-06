# slice_to_py_dist: упаковка Slice файлов (ZeroC/ICE) в распространяемый python-пакет

## Описание
*Slice* является языком описания интерфейсов сетевого взаимодействия для фреймворка *ZeroC/ICE*
(далее *ICE*). Для того, чтобы приложения могли взаимодействовать между собой посредством
ICE, Slice файлы (`.ice`) должны быть скомпилированы в исходные файлы, обеспечивающие реализацию
описанных интерфейсов на одном из языков программирования, поддерживаемых ICE (например, в `.py`
файлы для языка Python).

Данный проект `slice_to_py_dist` предназначен для упаковки набора Slice файлов в распространяемый
python-пакет (sdist), который может быть, например, загружен на pypi, или распространяться другим
способом. Впоследствии, на этапе установки sdist-пакета в целевом python-окружении эти `.ice` файлы
будут скомпилированы в `.py` файлы (реализации интерфейсов).

Компиляция выполняется с помощью компилятора `slice2py` (из состава pypi-пакета `zeroc-ice`).
При этом будут созданы импортируемые python-пакеты (такие, которые можно указывать в команде import),
соответствующие модулям верхнего уровня в Slice описаниях. Эти импортируемые python-пакеты и будут
установлены в целевом python-окружении.

Запуск компиляции Slice файлов на этапе установки sdist-пакета производится из специализированного
бэкенда сборки (*build-backend*), который добавляется в sdist-пакет при его формировании. Бэкенд
сборки использует технологию *in-tree backend* (см. ссылки).

## Пример
Для примера будет использоваться каталог `tests/funnycat/data`, который содержит:
- подкаталог `slice` со Slice файлами,
- конфигурационный файл `config.toml`.

Установка `slice_to_py_dist` и запуск для упаковки Slice файлов в sdist пакет:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install slice_to_py_dist

(.venv) $ datadir=tests/funnycat/data
(.venv) $ python -m slice_to_py_dist -c $datadir/config.toml --slice-source-dir $datadir/slice
```
(Опции, указанные в конфигурационном файле, могут быть указаны и в командной строке. И наоборот,
опция `--slice-source-dir` также может быть указана в конфигурационном файле. Для разбора опций
используется pypi-пакет configargparse).

После выполнения команды в текущем каталоге должен появиться sdist пакет, например
`funnycat-0.0.2.tar.gz`.

При установке sdist пакета в целевом python-окружении выполняется компиляция Slice файлов и
появляются следующие импортируемые python-пакеты:
- `FunnyCat`
- `FunnyCatSupport`
- `funnycat_gen`
- `funnycat_slice`

Пакеты `FunnyCat` и `FunnyCatSupport` соответствуют Slice модулям верхнего уровня (см. Slice файлы).
Эти пакеты используются в приложениях для организации между ними сетевого взаимодействия в
соответствии с разработанными Slice интерфейсами:
```
from FunnyCat.Main import CatPrx
...
```
Внутри эти пакеты для своей работы используют пакет `funnycat_gen`.

Пакет `funnycat_gen` содержит фактические реализации Slice интерфейсов, сгенерированные компилятором
`slice2py`. Имя пакета формируется в соответствии с директивами `python:pkgdir` (см. Slice файлы).
Этот пакет не должен напрямую использоваться приложениями.

Пакет `funnycat_slice` является вспомогательным, справочным. Он содержит исходные Slice файлы на тот
случай, если в целевом python-окружении возникнет необходимость в их просмотре/анализе. Имя пакета
формируется в соответствии с опцией `slice-storage-package` (см. файл `config.toml`).

## Разработка
```
poetry run black ./slice_to_py_dist/ ./tests/
poetry run pylint ./slice_to_py_dist/ ./tests/
poetry run pytest ./tests/
poetry version ...
poetry build
poetry publish
```

## Ссылки
### ICE и Slice:
- [ZeroC/ICE](https://zeroc.com/)
- [Code Generation in Python](https://doc.zeroc.com/ice/3.7/language-mappings/python-mapping/client-side-slice-to-python-mapping/code-generation-in-python)

### Сборка распространяемых python-пакетов:
- [PEP 517](https://peps.python.org/pep-0517/)
- [PEP 517: In-tree build backends](https://peps.python.org/pep-0517/#in-tree-build-backends)
- [PEP 517: Appendix A: Comparison to PEP 516](https://peps.python.org/pep-0517/#appendix-a-comparison-to-pep-516)
- [setuptools: Build System Support](https://setuptools.pypa.io/en/latest/build_meta.html)
- [stackoverflow: Custom build backend for Python](https://stackoverflow.com/questions/71517014/custom-build-backend-for-python)
