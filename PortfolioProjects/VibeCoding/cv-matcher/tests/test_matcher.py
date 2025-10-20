from matcher import score_cv, batch_score


def test_identical_texts():
    job = "Expert in python machine learning nlp"
    cv = "Expert in python machine learning nlp"
    r = score_cv(cv, job)
    assert r['combined_percent'] > 90


def test_different_texts():
    job = "Machine learning engineer with nlp"
    cv = "Graphic designer with photoshop skills"
    r = score_cv(cv, job)
    assert r['combined_percent'] < 50


def test_batch():
    job = "data scientist python ml"
    cvs = [("a","python ml data scientist"), ("b","graphic design photoshop")]
    res = batch_score(job, cvs)
    assert res[0]['name'] == 'a'
