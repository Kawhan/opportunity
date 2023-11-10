# Generated by Django 4.1.7 on 2023-08-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_vagasemprego_area_alter_vagasemprego_tipo_vaga'),
    ]

    operations = [
        migrations.AddField(
            model_name='vagasemprego',
            name='link_empresa_ou_pesquisa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Link empresa ou grupo de projeto'),
        ),
        migrations.AlterField(
            model_name='vagasemprego',
            name='area',
            field=models.CharField(choices=[('Com', 'Computação'), ('Adm', 'Administração'), ('Atp', 'Antropologia'), ('Ped', 'Pedagogia'), ('Dsg', 'Design'), ('Sec', 'Secretariado'), ('Eco', 'Ecologia'), ('Mat', 'Matemática'), ('CC', 'Ciências Contábeis')], default='Com', max_length=3),
        ),
        migrations.AlterField(
            model_name='vagasemprego',
            name='tipo_vaga',
            field=models.CharField(choices=[('PIC', 'Projeto de iniciação científica'), ('PE', 'Projeto de extensão'), ('PD', 'Projetos de desenvolvimento'), ('PIT', 'Projeto de iniciação tecnológica'), ('ES', 'Estágio')], max_length=3),
        ),
    ]