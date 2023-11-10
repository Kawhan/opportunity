# Generated by Django 4.1.7 on 2023-08-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_remove_vagasemprego_beneficios_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vagasemprego',
            name='area',
            field=models.CharField(choices=[('CC', 'Ciências Contábeis'), ('Mat', 'Matemática'), ('Com', 'Computação'), ('Dsg', 'Design'), ('Eco', 'Ecologia'), ('Sec', 'Secretariado'), ('Ped', 'Pedagogia'), ('Atp', 'Antropologia'), ('Adm', 'Administração')], default='Com', max_length=3),
        ),
        migrations.AlterField(
            model_name='vagasemprego',
            name='tipo_vaga',
            field=models.CharField(choices=[('PIT', 'Projeto de iniciação tecnológica'), ('PIC', 'Projeto de iniciação científica'), ('PD', 'Projeto de desenvolvimento'), ('PE', 'Projeto de extensão'), ('ES', 'Estágio')], max_length=3),
        ),
    ]
