# Generated manually for new accounting features

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoBancario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(max_length=100)),
                ('cuenta_bancaria', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(max_length=255)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=16)),
                ('tipo', models.CharField(choices=[('DEBITO', 'Débito'), ('CREDITO', 'Crédito')], max_length=20)),
                ('conciliado', models.BooleanField(default=False)),
                ('referencia', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('asiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.asientocontable')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha', '-id'],
            },
        ),
        migrations.CreateModel(
            name='CierreContable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cierre', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('asientos_cierre', models.ManyToManyField(blank=True, to='accounting.asientocontable')),
                ('cerrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.periodocontable')),
            ],
            options={
                'ordering': ['-fecha_cierre'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(choices=[('CREATE', 'Crear'), ('UPDATE', 'Actualizar'), ('DELETE', 'Eliminar'), ('VIEW', 'Ver')], max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('registro_id', models.IntegerField()),
                ('datos_anteriores', models.JSONField(blank=True, null=True)),
                ('datos_nuevos', models.JSONField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_presupuestado', models.DecimalField(decimal_places=2, max_digits=16)),
                ('monto_real', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('centro_costo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.centrocosto')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.cuentacontable')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.periodocontable')),
            ],
            options={
                'ordering': ['periodo', 'cuenta__codigo'],
                'unique_together': {('periodo', 'cuenta', 'centro_costo')},
            },
        ),
    ] 