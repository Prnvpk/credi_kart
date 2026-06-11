from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='licence_document',
            field=models.FileField(blank=True, null=True, upload_to='shopkeeper_licences/'),
        ),
    ]
