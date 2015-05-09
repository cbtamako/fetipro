# fetipro


## 動作環境

* Python 3.4
* Django 1.8
* Pythonの依存パッケージについては `package.pip` に記載


## 開発環境

`pyenv` と `pyenv-virtualenv` の利用を推奨します．

### `pyenv` , `pyenv-virtualenv` のセットアップ

すでに利用中の場合は省略してください．

```
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH" >> ~/.bash_profile
echo 'export TMPDIR="$HOME/tmp" >> ~/.bash_profile
echo 'export PYTHON_PATH=./ >> ~/.bash_profile
echo 'eval "$(pyenv init -)" >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)" >> ~/.bash_profile

source ~/.bash_profile
```

### リポジトリの取得とセットアップ

```
git clone https://github.com/cbtamako/fetipro.git
cd fetipro
pyenv install 3.4.2
pyenv virtuelenv 3.4.2 fetipro
pyenv local fetipro
pip install -r package.pip

cd src
cp fetipro/settings.py.template fetipro/settings.py
vim fetipro/settings.py

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## デプロイ

### Djangoの設定
```
cd src
cp fetipro/production_settings.py.template fetipro/production_settings.py
vim fetipro/production_settings.py

python manage.py migrate --settings=fetipro.production_settings
python manage.py createsuperuser --settings=fetipro.production_settings
python manage.py collectstatic --settings=fetipro.production_settings
```


### Webサーバの設定


Nginx等の設定方法は省略します．

さくらのレンサバで動作させるためのファイルを `htdocs` に置いておきます．
