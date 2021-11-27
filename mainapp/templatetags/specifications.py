from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone


register = template.Library()


TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'Діагональ': 'diagonal',
        'Тип дисплею': 'display_type',
        'Частота процесора': 'processor_freq',
        'Оперативна пам\'ять': 'ram',
        'Відеокарта': 'video',
        'Час роботи акумулятора': 'time_without_charge'
    },
    'smartphone': {
        'Діагональ': 'diagonal',
        'Тип дисплею': 'display_type',
        'Розширення екрану': 'resolution',
        'Ємність акумулятора': 'accum_volume',
        'Оперативна пам\'ять': 'ram',
        'Наявність SD карти': 'sd',
        'Максимальний об\'єм SD карти': 'sd_volume_max',
        'Камера, мп': 'main_cam_mp',
        'Фронтальная камера, мп': 'frontal_cam_mp'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальний об\'єм SD карти', None)
        else:
            PRODUCT_SPEC['smartphone']['Максимальний об\'єм SD карти'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)

