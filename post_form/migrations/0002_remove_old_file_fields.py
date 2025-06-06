from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('post_form', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webdesignrequest',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='webdesignrequest',
            name='banner',
        ),
        migrations.RemoveField(
            model_name='webdesignrequest',
            name='icons',
        ),
        migrations.RemoveField(
            model_name='webdesignrequest',
            name='images',
        ),
        migrations.RemoveField(
            model_name='webdesignrequest',
            name='videos',
        ),
    ] 