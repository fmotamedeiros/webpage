import requests

def get_github_user_info(username):
    """Obtém informações básicas do usuário do GitHub."""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_github_repos(username):
    """Obtém todos os repositórios públicos do usuário."""
    repos_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(repos_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def count_user_commits_in_repo(username, repo_name):
    """Conta o número de commits do usuário em um repositório específico."""
    commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits?author={username}"
    response = requests.get(commits_url)
    commits = response.json()
    if response.status_code == 200:
        return len(commits)
    else:
        return 0

def get_total_commits(username):
    """Calcula o total de commits do usuário em todos os seus repositórios públicos."""
    repos = get_github_repos(username)
    total_commits = sum(count_user_commits_in_repo(username, repo['name']) for repo in repos)
    return total_commits

def generate_html(user_info, total_commits):
    """Gera um HTML com as informações do usuário do GitHub, incluindo commits."""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GitHub Stats of {user_info.get('login', 'User')}</title>
    </head>
    <body>
        <h1>GitHub Statistics for {user_info.get('name', 'N/A')}</h1>
        <p><strong>Biography:</strong> {user_info.get('bio', 'N/A')}</p>
        <p><strong>Followers:</strong> {user_info.get('followers', 'N/A')}</p>
        <p><strong>Following:</strong> {user_info.get('following', 'N/A')}</p>
        <p><strong>Public Repos:</strong> {user_info.get('public_repos', 'N/A')}</p>
        <p><strong>Total Commits:</strong> {total_commits}</p>
        <p><strong>Location:</strong> {user_info.get('location', 'N/A')}</p>
        <p><a href="{user_info.get('html_url', '#')}">View Profile on GitHub</a></p>
    </body>
    </html>
    """
    return html_template

def save_html(html_content, filename='index.html'):
    """Salva o conteúdo HTML em um arquivo."""
    with open(filename, 'w') as file:
        file.write(html_content)

# Substitua 'username' pelo nome de usuário do GitHub que você deseja pesquisar
username = "fmotamedeiros"
user_info = get_github_user_info(username)

if user_info:
    total_commits = get_total_commits(username)
    html_content = generate_html(user_info, total_commits)
    save_html(html_content)
    print(f"HTML gerado com sucesso. Verifique o arquivo github_stats.html.")
else:
    print("Erro ao obter informações do usuário do GitHub.")
