# Generated by Django 4.2.2 on 2023-07-20 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(
                    auto_now=True, null=True)),
                ('end_contract_date', models.DateTimeField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('amount', models.FloatField()),
                ('payment_due', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('management_staff', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='managers',
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('A venir', 'upcoming'),
                             ('En cours', 'processing'),
                             ('Terminé', 'done'),
                             ('Annulé', 'cancelled')],
                    default=('A venir', 'upcoming'),
                    max_length=25)),
                ('description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prospect',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('mobile', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(
                    auto_now=True, null=True)),
                ('picture_url', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company_name', models.CharField(max_length=100)),
                ('sales_staff', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(
                    auto_now=True, null=True)),
                ('name', models.CharField(max_length=25)),
                ('address', models.CharField(max_length=255)),
                ('attendees', models.IntegerField()),
                ('event_date_start', models.DateTimeField()),
                ('event_date_end', models.DateTimeField()),
                ('notes', models.TextField(null=True)),
                ('contract', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='crm.contract')),
                ('customer', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='crm.customer')),
                ('event_status', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='crm.eventstatus')),
                ('management_staff', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='event_managers',
                    to=settings.AUTH_USER_MODEL)),
                ('support_staff', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='support_contact',
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='prospect',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='crm.prospect'),
        ),
        migrations.AddField(
            model_name='customer',
            name='sales_staff',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='sales',
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='customer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='crm.customer'),
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_staff',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL),
        ),
    ]