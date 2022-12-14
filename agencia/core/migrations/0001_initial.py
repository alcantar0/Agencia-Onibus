# Generated by Django 4.1 on 2022-12-14 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bilhete",
            fields=[
                (
                    "numerobilhete",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("cpf_c", models.CharField(max_length=15)),
                ("numeropoltrona", models.IntegerField()),
                ("numcomprovante", models.IntegerField()),
                (
                    "valor",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("num_iti", models.IntegerField()),
            ],
            options={
                "db_table": "bilhete",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Cidades",
            fields=[
                (
                    "cep",
                    models.CharField(max_length=9, primary_key=True, serialize=False),
                ),
                ("nome_cidade", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "cidades",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "cpf_c",
                    models.CharField(max_length=15, primary_key=True, serialize=False),
                ),
                ("nome", models.CharField(max_length=50)),
                ("rua", models.CharField(blank=True, max_length=50, null=True)),
                ("cidade", models.CharField(blank=True, max_length=50, null=True)),
                ("email", models.CharField(max_length=50)),
                ("sexo", models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                "db_table": "cliente",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Comprovante",
            fields=[
                (
                    "numcomprovante",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
                ("cpf_c", models.CharField(max_length=15)),
                ("idvendedor", models.IntegerField()),
            ],
            options={
                "db_table": "comprovante",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Dirige",
            fields=[
                ("dataviagem", models.DateField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "dirige",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Funcionario",
            fields=[
                (
                    "cpf_f",
                    models.CharField(max_length=15, primary_key=True, serialize=False),
                ),
                ("nome", models.CharField(max_length=30)),
                ("tipo", models.CharField(max_length=15)),
                ("salario", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "cnh",
                    models.CharField(blank=True, max_length=14, null=True, unique=True),
                ),
                ("idvendedor", models.IntegerField(blank=True, null=True, unique=True)),
                ("numvendas", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "funcionario",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Itinerario",
            fields=[
                ("num_iti", models.IntegerField(primary_key=True, serialize=False)),
                ("hora_saida", models.TimeField()),
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "db_table": "itinerario",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Onibus",
            fields=[
                ("numonibus", models.IntegerField(primary_key=True, serialize=False)),
                ("viacao", models.CharField(max_length=15)),
                ("classe", models.CharField(max_length=15)),
                ("capacidade", models.IntegerField()),
            ],
            options={
                "db_table": "onibus",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Inclui",
            fields=[
                (
                    "cep",
                    models.OneToOneField(
                        db_column="cep",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="core.cidades",
                    ),
                ),
                ("data_viagem", models.DateField()),
            ],
            options={
                "db_table": "inclui",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TelefoneC",
            fields=[
                (
                    "cpf_c",
                    models.OneToOneField(
                        db_column="cpf_c",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="core.cliente",
                    ),
                ),
                ("telefone", models.CharField(max_length=14)),
            ],
            options={
                "db_table": "telefone_c",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="TelefoneF",
            fields=[
                (
                    "cpf_f",
                    models.OneToOneField(
                        db_column="cpf_f",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="core.funcionario",
                    ),
                ),
                ("num_telefone", models.CharField(max_length=15)),
            ],
            options={
                "db_table": "telefone_f",
                "managed": False,
            },
        ),
    ]
