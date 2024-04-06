# Generated by Django 4.0.5 on 2024-04-06 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_label', models.TextField(max_length=50)),
                ('category_code', models.TextField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('content_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_source_id', models.IntegerField()),
                ('content_headline', models.TextField(max_length=300)),
                ('content_source', models.TextField(max_length=50)),
                ('content_url', models.TextField(max_length=400)),
                ('content_category', models.TextField(max_length=50)),
                ('content_text', models.TextField(max_length=500)),
                ('content_image', models.TextField(max_length=500)),
                ('content_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_trust_rating', models.IntegerField(default=0)),
                ('source_name', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('thread_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_id', models.IntegerField()),
                ('thread_response', models.TextField(max_length=300)),
            ],
        ),
    ]
