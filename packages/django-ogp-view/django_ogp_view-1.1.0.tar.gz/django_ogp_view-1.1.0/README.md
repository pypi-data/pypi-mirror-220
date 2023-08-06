# django-ogp-view
ViewクラスにOGP (The Open Graph protocol)を適応させるライブラリです。  
本ライブラリのViewMixinを継承させることで、ogp metaタグの実装が簡略化できます。  
画面ごとにカスタマイズすることもできます。  
SEO (Search Engine Optimization)対策に最適です。  

## 導入
1. ライブラリをインストールする。
    ```sh
    pip install django-ogp-view
     or
    pip install git+https://github.com/taogya/DjangoOgpView.git
    ```
1. settings.pyに以下を追加する。
    ```python
    INSTALLED_APPS = [
        :
        'django_ogp'
    ]
    OGP_SITE_PROPERTY_MODEL = 'django_ogp.OgpSiteProperty'
    OGP_LOCALE_MASTER_MODEL = 'django_ogp.OgpLocaleMaster'
    OGP_MIMETYPE_MASTER_MODEL = 'django_ogp.OgpMimeTypeMaster'
    ```
1. migrateを行う。
    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
1. OGP用のプロパティを設定する。
    - OgpSiteProperty  
    サイト内共通のプロパティ。
    - OgpBasicProperty  
    ページごとのプロパティ。
    - OgpCustomProperty  
    カスタムプロパティ。  
    JSONで指定する。  
    JSONについて, keyはpropertyの名称, valueはcontentの値で指定する。  
1. ViewにOgpViewMixinを継承し, 割り当てるプロパティのレコードを割り当てる。
    ```python
    from django.views import View
    from django_ogp.view import OgpViewMixin
    from django_ogp.models import OgpBasicProperty

    class YourView(View, OgpViewMixin):
        ogp = OgpBasicProperty.objects.first()
        :
    ```
1. 以下のようにhtmlファイルにdjango_ogp用のタグを追加する。
    ```html
    {% load django_ogp %}
    <!DOCTYPE html>
    <html lang="en" prefix="{{ view.ogp_global_prefix }}">
    <head prefix="{{ view.ogp_prefix }}">
        {% add_ogp_meta %}
        :
    ```

## Models
![django_ogp_er_](/resources/django_ogp_er.png)

## 補足
- [マイグレーションファイル](django_ogp/migrations/0001_initial.py) にはマスターデータ自動生成スクリプトが含まれています。  
不要なデータがありましたら, 管理者画面にて削除するか[マイグレーションファイル](django_ogp/migrations/0001_initial.py)を修正してください。
- 以下のモデルは`swappable`なモデルです。
    - OgpSiteProperty
    - OgpLocaleMaster
    - OgpMimeTypeMaster
