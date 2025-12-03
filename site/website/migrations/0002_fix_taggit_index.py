from django.db import migrations


def ensure_index(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT indexdef FROM pg_indexes WHERE tablename = 'taggit_taggeditem';")
        indexes = cursor.fetchall()

        found = False
        for (indexdef,) in indexes:
            if "(content_type_id, object_id)" in indexdef:
                found = True
                break

        if not found:
            print("\n--- Creating missing index on taggit_taggeditem ---")
            cursor.execute(
                "CREATE INDEX taggit_taggeditem_content_type_id_object_id_idx ON taggit_taggeditem (content_type_id, object_id);"
            )
        else:
            print("\n--- Index on taggit_taggeditem(content_type_id, object_id) already exists. Skipping. ---")


def reverse_ensure_index(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_update_site_name"),
        ("taggit", "0005_auto_20220424_2025"),
    ]

    run_before = [
        ("taggit", "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx"),
    ]

    operations = [
        migrations.RunPython(ensure_index, reverse_ensure_index),
    ]
