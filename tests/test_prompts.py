from app.prompts import EXERCISES, validate_classification


def test_four_exercises():
    assert len(EXERCISES) == 4
    for exercise in EXERCISES.values():
        assert exercise["system"] and exercise["user"]


def test_valid_json():
    s = '{"categoria":"entrega","prioridad":"alta","resumen":"Retraso","requiere_revision_humana":true}'
    assert validate_classification(s)[0]


def test_rejects_bad_json():
    assert not validate_classification("No soy JSON")[0]


def test_rejects_wrong_schema():
    assert not validate_classification('{"categoria":"entrega"}')[0]
