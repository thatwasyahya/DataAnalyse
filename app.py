from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load CSV files
df_reponses = pd.read_csv('reponses_etudiants.csv')
df_reponses.columns = df_reponses.columns.str.strip()
df_reponses = df_reponses.dropna(subset=['Numero etudiant'])

df_conditions = pd.read_csv('conditions.csv', on_bad_lines='skip', engine='python')
df_conditions.columns = df_conditions.columns.str.strip()

def parse_importance(importance_str):
    if isinstance(importance_str, str) and '/' in importance_str:
        num, denom = importance_str.split('/')
        return float(num) / float(denom)
    elif isinstance(importance_str, (int, float)):
        return float(importance_str)
    return 0.0

def apply_conditions(conditions, filiere, row):
    score, max_score = 0, 0
    for _, cond in conditions.iterrows():
        if cond['Filière'] == filiere:
            question = cond['Question']
            hypothese = cond['Hypothèse'].split('|')
            weight = float(cond['Pondération'])
            importance = parse_importance(cond['Degré d importance'])

            if any([hyp in str(row[question]) for hyp in hypothese]):
                score += weight * importance
            max_score += weight * importance
    return score, max_score

def calculate_scores(df_reponses, df_conditions):
    df_reponses['IPS_score'] = df_reponses.apply(lambda row: apply_conditions(df_conditions, 'ips', row)[0], axis=1)
    df_reponses['ASTRE_score'] = df_reponses.apply(lambda row: apply_conditions(df_conditions, 'astre', row)[0], axis=1)
    df_reponses['IPS_max_score'] = df_reponses.apply(lambda row: apply_conditions(df_conditions, 'ips', row)[1], axis=1)
    df_reponses['ASTRE_max_score'] = df_reponses.apply(lambda row: apply_conditions(df_conditions, 'astre', row)[1], axis=1)

    df_reponses['IPS_percentage'] = (df_reponses['IPS_score'] / df_reponses['IPS_max_score']) * 100
    df_reponses['ASTRE_percentage'] = (df_reponses['ASTRE_score'] / df_reponses['ASTRE_max_score']) * 100

    df_reponses['total_percentage'] = df_reponses['IPS_percentage'] + df_reponses['ASTRE_percentage']
    df_reponses['IPS_percentage'] = (df_reponses['IPS_percentage'] * 100) / df_reponses['total_percentage']
    df_reponses['ASTRE_percentage'] = (df_reponses['ASTRE_percentage'] * 100) / df_reponses['total_percentage']

    return df_reponses

@app.route('/api/scores', methods=['GET'])
def get_scores():
    df_reponses_updated = calculate_scores(df_reponses, df_conditions)
    scores = df_reponses_updated[['Numero etudiant', 'IPS_percentage', 'ASTRE_percentage']].to_dict(orient='records')
    return jsonify(scores)

@app.route('/api/hypotheses', methods=['GET'])
def get_hypotheses():
    hypotheses = df_conditions[['Filière', 'Hypothèse']].drop_duplicates().to_dict(orient='records')
    return jsonify(hypotheses)

@app.route('/api/updatedelta', methods=['POST'])
def update_delta():
    data = request.json
    filiere, hypothesis = data['filiere'], data['hypothesis']
    weight, importance = float(data['weight']), float(data['importance'])

    # Update conditions
    df_conditions.loc[(df_conditions['Filière'] == filiere) & 
                      (df_conditions['Hypothèse'] == hypothesis), 
                      ['Pondération', 'Degré d importance']] = [weight, importance]

    # Save updated conditions
    df_conditions.to_csv('conditions.csv', index=False)

    # Recalculate scores
    df_reponses_updated = calculate_scores(df_reponses, df_conditions)
    scores = df_reponses_updated[['Numero etudiant', 'IPS_percentage', 'ASTRE_percentage']].to_dict(orient='records')

    return jsonify({'scores': scores})

@app.route('/api/results', methods=['GET'])
def get_results():
    df_reponses_updated = calculate_scores(df_reponses, df_conditions)
    ips_count = (df_reponses_updated['IPS_percentage'] > 50).sum().item()  # Convert to standard int
    astre_count = (df_reponses_updated['ASTRE_percentage'] > 50).sum().item()  # Convert to standard int
    return jsonify({'ips': ips_count, 'astre': astre_count})



@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')
