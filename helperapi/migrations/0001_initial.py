# Generated by Django 4.1.3 on 2022-12-06 20:56

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
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('serial_number', models.PositiveIntegerField(null=True)),
                ('out_for_repair', models.BooleanField(default=False)),
                ('school_owned', models.BooleanField(default=False)),
                ('assigned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('part', models.CharField(max_length=30)),
                ('assigned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Prop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('assigned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='helperapi.instrument')),
            ],
        ),
        migrations.CreateModel(
            name='Uniform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniform_number', models.PositiveIntegerField(null=True)),
                ('size', models.CharField(max_length=30)),
                ('assigned', models.BooleanField(default=False)),
                ('out_for_cleaning', models.BooleanField(default=False)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.school')),
            ],
        ),
        migrations.CreateModel(
            name='StudentMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.music')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='music_parts',
            field=models.ManyToManyField(through='helperapi.StudentMusic', to='helperapi.music'),
        ),
        migrations.AddField(
            model_name='student',
            name='prop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='helperapi.prop'),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.school'),
        ),
        migrations.AddField(
            model_name='student',
            name='uniform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='helperapi.uniform'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prop',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.school'),
        ),
        migrations.AddField(
            model_name='music',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.school'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.school'),
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helperapi.school')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
