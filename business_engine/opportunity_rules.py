def opportunity_rules(row):
    if row['growth_index'] > 0.7:
        return "High expansion priority"
    elif row['growth_index'] > 0.4:
        return "Moderate growth zone"
    else:
        return "Low demand zone"
