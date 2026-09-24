def summarise_amounts(raw_values):
    total = 0
    for raw in raw_values:
        try:
            total += int(raw)
        except:
            pass
    return {"total": total, "rejected": 0}

def test_summarise_amounts():
    assert summarise_amounts(["10", " 5 ", "bad", "-3", "0", ""]) == {'total': 15, 'rejected': 3}

def test_summarise_amounts_empty_input():
    assert summarise_amounts([]) == {'total': 0, 'rejected': 0}

def test_summarise_amounts_invalid_inputs():
    assert summarise_amounts(["", " ", " -5 ", "good"]) == {'total': 0, 'rejected': 4}

def test_summarise_amounts_zero():
    assert summarise_amounts([0]) == {'total': 0, 'rejected': 0}








def add_tag(profile, tag):
    updated = profile.copy()
    updated["tags"].append(tag)
    return updated

original = {"name": "Ada", "tags": ["python"]}

changed = add_tag(original, "testing")

print(original["tags"])

print(changed is original)

print(changed["tags"] is original["tags"])
















def passing_scores(scores):
    passed = []
    for index in range(len(scores)-1):
        if scores[index] > 50:
            passed.append(scores[index])
    return passed
print(passing_scores([49, 50, 80, 65]))

def test_passing_scores_for_pass_boundary_50():
    assert passing_scores([49,50]) == [50]

def test_passing_scores_for_single_passing_score():
    assert passing_scores([56]) == [56]

def test_passing_scores_for_empty_list():
    assert passing_scores([]) == []








def ticket_total(price, quantity):
    total = price * quantity
    print(total)
amount = ticket_total("7", 3)
print(amount)