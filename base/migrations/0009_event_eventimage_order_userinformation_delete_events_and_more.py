# Generated by Django 4.1 on 2023-01-29 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_alter_privetinformation_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=100, verbose_name='Event Name')),
                ('description', models.TextField()),
                ('date_and_time', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Location')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('meta_title', models.CharField(blank=True, max_length=100, verbose_name='Meta Title')),
                ('meta_description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='..\\static\\images', verbose_name='Event Image')),
                ('alt_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='Image Alt Text')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.DateTimeField(auto_now_add=True, verbose_name='Order Date and Time')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Subtotal')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20, verbose_name='First Name')),
                ('lastname', models.CharField(max_length=20, verbose_name='Last Name')),
                ('age', models.FloatField()),
                ('email', models.EmailField(default='example@domain.com', max_length=254)),
                ('city', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=75)),
                ('postalcode', models.FloatField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Events',
        ),
        migrations.DeleteModel(
            name='PrivetInformation',
        ),
    ]