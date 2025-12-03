from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_fix_taggit_index"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            SELECT setval('django_content_type_id_seq', COALESCE((SELECT MAX(id) FROM django_content_type), 0) + 1);
            SELECT setval('auth_permission_id_seq', COALESCE((SELECT MAX(id) FROM auth_permission), 0) + 1);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
