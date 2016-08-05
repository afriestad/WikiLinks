# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-05 00:21
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sanitizer.models
import semesterpage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.SmallIntegerField(choices=[(0, 'Ingen tilgang'), (1, 'Opprettede fag'), (2, 'Kun semesteret'), (3, 'Hele hovedprofilen'), (4, 'Hele studieprogrammet')], default=1, help_text='Gir muligheten til å endre på lenker o.l. knyttet til semesteret spesifisert nedenfor.', verbose_name='tilgangsnivå')),
            ],
            options={
                'verbose_name_plural': 'bidragsytere',
                'verbose_name': 'bidragsyter',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='F.eks. "Prosedyre- og Objektorientert Programmering"', max_length=60, unique=True, verbose_name='fullt navn')),
                ('display_name', models.CharField(help_text='F.eks. "C++"', max_length=60, verbose_name='visningsnavn')),
                ('logo', models.FileField(blank=True, help_text='Bildet vises over alle lenkene knyttet til faget. Bør være kvadratisk for å unngå uheldige skaleringseffekter.', null=True, upload_to=semesterpage.models.upload_path)),
                ('homepage', models.URLField(help_text='F.eks. "http://www.phys.ntnu.no/fysikkfag/". Denne lenken kan besøkes ved å trykke på ikonet til faget.', verbose_name='Fagets hjemmeside')),
                ('course_code', models.CharField(help_text='F.eks. "TDT4102"', max_length=10, unique=True, verbose_name='emnekode')),
                ('contributors', models.ManyToManyField(blank=True, help_text='Bidragsytere som har redigeringstilgang til faget.', related_name='courses', to='semesterpage.Contributor')),
            ],
            options={
                'ordering': ['display_name'],
                'verbose_name_plural': 'fag',
                'verbose_name': 'fag',
            },
        ),
        migrations.CreateModel(
            name='CourseLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='F.eks. "http://www.phys.ntnu.no/fysikkfag/gamleeksamener.html"', verbose_name='URL')),
                ('category', models.CharField(blank=True, choices=[('tasks.svg', 'Øvinger og prosjekter'), ('solutions.svg', 'Løsningsforslag'), ('videos.svg', 'Videoforelesninger'), ('timetable.svg', 'Framdrifts- og timeplaner'), ('syllabus.svg', 'Pensum'), ('formulas.svg', 'Formelark'), ('exams.svg', 'Eksamener'), ('facebook.svg', 'Facebook'), ('info.svg', 'Informasjon'), ('important_info.svg', 'Viktig informasjon'), ('ntnu.svg', 'NTNU-lenker'), ('wikipendium.svg', 'Wikipendium'), ('book.svg', 'Pensumbok'), ('quiz.svg', 'Quiz og punktlister'), ('software.svg', 'Programvare')], default=None, help_text='F.eks. "Løsningsforslag". Valget bestemmer hvilket "mini-ikon" som plasseres ved siden av lenken.', max_length=60, null=True, verbose_name='Kateogri')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Bestemmer hvilken rekkefølge lenkene skal vises i. Lavest kommer først.', verbose_name='rekkefølge')),
                ('title', sanitizer.models.SanitizedCharField(help_text='F.eks "Gamle eksamenssett"', max_length=100, verbose_name='tittel')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='semesterpage.Course', verbose_name='fag')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name_plural': 'lenker',
                'verbose_name': 'lenke',
            },
        ),
        migrations.CreateModel(
            name='CustomLinkCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Egendefinert kategori')),
                ('thumbnail', models.FileField(blank=True, upload_to=semesterpage.models.upload_path, verbose_name='ikon for kategori')),
            ],
            options={
                'verbose_name_plural': 'lenkekategorier',
                'verbose_name': 'lenkekategori',
            },
        ),
        migrations.CreateModel(
            name='MainProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='F.eks. "Industriell matematikk"', max_length=60, verbose_name='fullt navn')),
                ('display_name', models.CharField(help_text='F.eks. "InMat"', max_length=60, verbose_name='visningsnavn / kallenavn')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='display_name', unique_with=('study_program',))),
            ],
            options={
                'ordering': ['display_name'],
                'verbose_name_plural': 'hovedprofiler',
                'verbose_name': 'hovedprofil',
            },
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homepage', models.CharField(blank=True, help_text='Du kan besøke din personlige semesterside på kokekunster.no/hjemmesidenavn eller hjemmesidenavn.kokekunster.no. Der dukker alle fagene i semesteret du velger nedenfor opp, eller så kan du også velge din egen fagkombinasjon.', max_length=60, null=True, unique=True, verbose_name='hjemmesidenavn')),
                ('homepage_slug', autoslug.fields.AutoSlugField(always_update=True, blank=True, editable=False, null=True, populate_from='homepage', unique=True)),
                ('calendar_name', models.CharField(blank=True, default=None, help_text='Tast inn ditt kalendernavn på ntnu.1024.no.', max_length=60, null=True, verbose_name='1024-kalendernavn')),
                ('self_chosen_courses', models.ManyToManyField(blank=True, default=None, help_text='Hvis du ikke går et ordinært semester, og heller har lyst å velge dine egne fag.', related_name='students', to='semesterpage.Course', verbose_name='fag')),
            ],
            options={
                'ordering': ('user__username',),
                'abstract': False,
                'verbose_name_plural': 'instillinger',
                'verbose_name': 'instillinger',
            },
        ),
        migrations.CreateModel(
            name='ResourceLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='F.eks. "http://www.phys.ntnu.no/fysikkfag/gamleeksamener.html"', verbose_name='URL')),
                ('category', models.CharField(blank=True, choices=[('tasks.svg', 'Øvinger og prosjekter'), ('solutions.svg', 'Løsningsforslag'), ('videos.svg', 'Videoforelesninger'), ('timetable.svg', 'Framdrifts- og timeplaner'), ('syllabus.svg', 'Pensum'), ('formulas.svg', 'Formelark'), ('exams.svg', 'Eksamener'), ('facebook.svg', 'Facebook'), ('info.svg', 'Informasjon'), ('important_info.svg', 'Viktig informasjon'), ('ntnu.svg', 'NTNU-lenker'), ('wikipendium.svg', 'Wikipendium'), ('book.svg', 'Pensumbok'), ('quiz.svg', 'Quiz og punktlister'), ('software.svg', 'Programvare')], default=None, help_text='F.eks. "Løsningsforslag". Valget bestemmer hvilket "mini-ikon" som plasseres ved siden av lenken.', max_length=60, null=True, verbose_name='Kateogri')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Bestemmer hvilken rekkefølge lenkene skal vises i. Lavest kommer først.', verbose_name='rekkefølge')),
                ('title', sanitizer.models.SanitizedCharField(help_text='F.eks "Wolfram Alpha"', max_length=100, verbose_name='tittel')),
                ('custom_category', models.ForeignKey(blank=True, default=None, help_text='Hvis du ønsker å bruke et egendefinert "mini-ikon".', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='semesterpage.CustomLinkCategory', verbose_name='(Egendefinert kategori)')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name_plural': 'ressurslenker',
                'verbose_name': 'ressurslenke',
            },
        ),
        migrations.CreateModel(
            name='ResourceLinkList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='F.eks. "Prosedyre- og Objektorientert Programmering"', max_length=60, unique=True, verbose_name='fullt navn')),
                ('display_name', models.CharField(help_text='F.eks. "C++"', max_length=60, verbose_name='visningsnavn')),
                ('logo', models.FileField(blank=True, help_text='Bildet vises over alle lenkene knyttet til faget. Bør være kvadratisk for å unngå uheldige skaleringseffekter.', null=True, upload_to=semesterpage.models.upload_path)),
                ('homepage', models.URLField(help_text='F.eks. "http://www.phys.ntnu.no/fysikkfag/". Denne lenken kan besøkes ved å trykke på ikonet til faget.', verbose_name='Fagets hjemmeside')),
                ('default', models.BooleanField(default=False, help_text='Skal denne ressurslenkelisten brukes i alle studieprogram som ikke har satt sine egendefinerte ressurslenkelister?', verbose_name='standard ressurslenkeliste')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Bestemmer hvilken rekkefølge ressurslenkelistene skal vises i. Lavest kommer først.', verbose_name='Rekkefølge')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'Ressurslenkelister',
                'verbose_name': 'Ressurslenkeliste',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(help_text='F.eks. "2"', verbose_name='semesternummer')),
                ('published', models.BooleanField(default=False, help_text='Semesteret dukker ikke opp i navigasjonsbaren før det er publisert, men det er fortsatt mulig å besøke semesteret manuelt (URL: kokekunster.no/studieprogram/hovedprofil/semesternummer) for å teste resultatet før du publiserer.', verbose_name='publisert')),
                ('main_profile', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='semesters', to='semesterpage.MainProfile', verbose_name='hovedprofil')),
            ],
            options={
                'ordering': ['main_profile__display_name', 'number'],
                'verbose_name_plural': 'semestere',
                'verbose_name': 'semester',
            },
        ),
        migrations.CreateModel(
            name='StudyProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='F.eks. "Fysikk og matematikk"', max_length=60, verbose_name='fullt navn')),
                ('display_name', models.CharField(help_text='F.eks. "Fysmat"', max_length=60, verbose_name='visningsnavn / kallenavn')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='display_name', unique=True)),
                ('has_archive', models.BooleanField(default=False, help_text='Huk av hvis studieprogrammet har filer i arkivet på kokekunster.no/arkiv.', verbose_name='har arkiv')),
                ('published', models.BooleanField(default=False, help_text='Studieprogrammet dukker ikke opp i studieprogramlisten i navigasjonsbaren før det er publisert, men det er fortsatt mulig å besøke studieprogrammet manuelt (URL: visningsnavn.kokekunster.no) for å teste resultatet før du publiserer.', verbose_name='publisert')),
            ],
            options={
                'ordering': ['display_name'],
                'verbose_name_plural': 'studieprogram',
                'verbose_name': 'studieprogram',
            },
        ),
        migrations.AddField(
            model_name='semester',
            name='study_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='semesterpage.StudyProgram', verbose_name='studieprogram'),
        ),
        migrations.AddField(
            model_name='resourcelinklist',
            name='study_programs',
            field=models.ManyToManyField(blank=True, related_name='_resource_link_lists', to='semesterpage.StudyProgram', verbose_name='studieprogram'),
        ),
        migrations.AddField(
            model_name='resourcelink',
            name='resource_link_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='semesterpage.ResourceLinkList', verbose_name='ressurslenkeliste'),
        ),
        migrations.AddField(
            model_name='options',
            name='self_chosen_semester',
            field=models.ForeignKey(blank=True, default=None, help_text='Semesteret du for øyeblikket går.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='semesterpage.Semester', verbose_name='semester'),
        ),
        migrations.AddField(
            model_name='options',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='options', to=settings.AUTH_USER_MODEL, verbose_name='bruker'),
        ),
        migrations.AddField(
            model_name='mainprofile',
            name='study_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_profiles', to='semesterpage.StudyProgram', verbose_name='studieprogram'),
        ),
        migrations.AddField(
            model_name='course',
            name='semesters',
            field=models.ManyToManyField(blank=True, help_text='Hvis du lager et fag for deg selv, så kan du bare hoppe over dette valget.', related_name='courses', to='semesterpage.Semester', verbose_name='semestre'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='semester',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to='semesterpage.Semester', verbose_name='bidragsytersemester'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to=settings.AUTH_USER_MODEL, verbose_name='bruker'),
        ),
    ]