# Generated by Django 4.1.4 on 2023-02-02 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PJP_API', '0004_delete_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ai',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anonces', to='PJP_API.usermodel'),
        ),
        migrations.AlterField(
            model_name='favories',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Favories', to='PJP_API.usermodel'),
        ),
        migrations.AlterField(
            model_name='message',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='PJP_API.usermodel'),
        ),
        migrations.AlterField(
            model_name='message',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='PJP_API.usermodel'),
        ),
    ]
