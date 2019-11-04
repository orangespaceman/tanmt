# Generated by Django 2.2.6 on 2019-10-29 16:10

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import pages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='pages.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('quote', models.TextField()),
                ('author', models.CharField(blank=True, max_length=200)),
                ('background', models.CharField(choices=[('dark', 'Dark'), ('white', 'White')], max_length=200)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quote', to='pages.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_in_header', models.BooleanField(default=False, help_text='(Applicable to top-level pages only)')),
                ('display_in_footer', models.BooleanField(default=False, help_text='(Applicable to top-level pages only)')),
                ('title', models.CharField(max_length=200)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, help_text='This will be the URL for this page', overwrite=True, populate_from=pages.models.generate_slug, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField(default=1, help_text='The lower the number, the closer to the start this appears')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, help_text="Select section of the site this page should appear in, leave blank if this page shouldn't appear under any section", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pages.Page')),
            ],
            options={
                'ordering': ['order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='ImageWithText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('align', models.CharField(choices=[('imageLeft', 'Image left'), ('imageRight', 'Image right')], max_length=200)),
                ('background', models.CharField(choices=[('dark', 'Dark'), ('white', 'White')], max_length=200)),
                ('image', models.ImageField(blank=True, upload_to=pages.models.ImageWithText.get_upload_path)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image_with_text', to='pages.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('image_alt', models.CharField(blank=True, max_length=200)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to=pages.models.Image.get_upload_path)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='pages.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Embed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField(help_text='Careful! Anything you enter here will be embedded directly in the website...')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='embed', to='pages.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='editorial', to='pages.Component')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='component',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='pages.Page'),
        ),
        migrations.CreateModel(
            name='TopLevelPage',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Reorder pages for header/footer menus',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pages.page',),
        ),
    ]
