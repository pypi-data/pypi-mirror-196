# transQA 

Библиотека предназначена для генерации текста или ответа на основе полученных вопроса, ответа, модели и прочих параметров

## Install

Для установки выполните команду:

```
pip install svn+http://svn.consultant.ru/svn/Internal/Docs/NRP/pylibs/transQA

```

### Errors
Если при установке requirements.txt возникли проблемы с torch==1.13.0+cu117 следует использовать команду для отдельной установки:

```
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

```
В целом все требования из requirements.txt уже содержатся в Python396TF25GPU_release1.1