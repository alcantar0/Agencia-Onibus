# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bilhete(models.Model):
    numerobilhete = models.IntegerField(primary_key=True)
    cpf_c = models.CharField(max_length=15)
    numeropoltrona = models.IntegerField()
    numcomprovante = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_iti = models.IntegerField()

    class Meta:
        managed = True
        db_table = "bilhete"
        constraints = [
            models.UniqueConstraint(fields=["numeropoltrona", "num_iti"], name="poltrona-unica")
        ]


class Cidades(models.Model):
    cep = models.CharField(primary_key=True, max_length=9)
    nome_cidade = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "cidades"


class Cliente(models.Model):
    cpf_c = models.CharField(primary_key=True, max_length=15)
    nome = models.CharField(max_length=50)
    rua = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cliente"


class Comprovante(models.Model):
    numcomprovante = models.IntegerField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cpf_c = models.CharField(max_length=15)
    idvendedor = models.IntegerField()

    class Meta:
        managed = False
        db_table = "comprovante"


class Dirige(models.Model):
    dataviagem = models.DateField(primary_key=True)
    numonibus = models.ForeignKey("Onibus", models.DO_NOTHING, db_column="numonibus")
    cpf_f = models.ForeignKey("Funcionario", models.DO_NOTHING, db_column="cpf_f")

    class Meta:
        managed = False
        db_table = "dirige"
        unique_together = (("dataviagem", "numonibus", "cpf_f"),)


class Funcionario(models.Model):
    cpf_f = models.CharField(primary_key=True, max_length=15)
    nome = models.CharField(max_length=30)
    tipo = models.CharField(max_length=15)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cnh = models.CharField(unique=True, max_length=14, blank=True, null=True)
    idvendedor = models.IntegerField(unique=True, blank=True, null=True)
    numvendas = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "funcionario"


class Inclui(models.Model):
    cep = models.OneToOneField(
        Cidades, models.DO_NOTHING, db_column="cep", primary_key=True
    )
    num_iti = models.ForeignKey("Itinerario", models.DO_NOTHING, db_column="num_iti")
    data_viagem = models.DateField()

    class Meta:
        managed = False
        db_table = "inclui"
        unique_together = (("cep", "num_iti", "data_viagem"),)


class Itinerario(models.Model):
    num_iti = models.IntegerField(primary_key=True)
    hora_saida = models.TimeField()
    cep_destino = models.ForeignKey(
        Cidades, models.DO_NOTHING, db_column="cep_destino", related_name="cep_destino"
    )
    cep_origem = models.ForeignKey(Cidades, models.DO_NOTHING, db_column="cep_origem")
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "itinerario"


class Onibus(models.Model):
    numonibus = models.IntegerField(primary_key=True)
    viacao = models.CharField(max_length=15)
    classe = models.CharField(max_length=15)
    capacidade = models.IntegerField()
    numitipercorre = models.ForeignKey(
        Itinerario, models.DO_NOTHING, db_column="numitipercorre"
    )

    class Meta:
        managed = False
        db_table = "onibus"


class TelefoneC(models.Model):
    cpf_c = models.OneToOneField(
        Cliente, models.DO_NOTHING, db_column="cpf_c", primary_key=True
    )
    telefone = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = "telefone_c"
        unique_together = (("cpf_c", "telefone"),)


class TelefoneF(models.Model):
    cpf_f = models.OneToOneField(
        Funcionario, models.DO_NOTHING, db_column="cpf_f", primary_key=True
    )
    num_telefone = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = "telefone_f"
        unique_together = (("cpf_f", "num_telefone"),)
