def render_portfolio_html(user, portfolio, projects) -> str:
    """
    Builds the public portfolio HTML page as a string.
    """
    project_cards = ""
    for project in projects:
        project_cards += f"""
        <div class="project-card">
            <h3>{project.repo_name}</h3>
            <p>{project.ai_description or "No description available"}</p>
            <div class="project-meta">
                {f'<span class="tag">{project.language}</span>' if project.language else ""}
            </div>
            <a href="{project.repo_url}" target="_blank" class="project-link">View on GitHub →</a>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{portfolio.title}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #0d1117;
                color: #e6edf3;
                line-height: 1.6;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 60px 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 50px;
            }}
            .header img {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                border: 3px solid #58a6ff;
                margin-bottom: 20px;
            }}
            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #58a6ff, #bf91f3);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .header p {{
                font-size: 1.1rem;
                color: #8b949e;
                max-width: 600px;
                margin: 0 auto;
            }}
            .github-link {{
                display: inline-block;
                margin-top: 16px;
                padding: 8px 20px;
                background: #21262d;
                border: 1px solid #30363d;
                border-radius: 20px;
                color: #58a6ff;
                text-decoration: none;
                font-size: 0.9rem;
            }}
            .projects-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 20px;
            }}
            .project-card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 24px;
            }}
            .project-card h3 {{
                color: #58a6ff;
                margin-bottom: 12px;
                font-size: 1.2rem;
            }}
            .project-card p {{
                color: #c9d1d9;
                font-size: 0.95rem;
                margin-bottom: 16px;
            }}
            .tag {{
                background: #21262d;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.8rem;
                color: #8b949e;
            }}
            .project-link {{
                display: inline-block;
                margin-top: 16px;
                color: #3fb950;
                text-decoration: none;
                font-size: 0.9rem;
                font-weight: 600;
            }}
            .footer {{
                text-align: center;
                margin-top: 60px;
                color: #6e7681;
                font-size: 0.85rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="{user.avatar_url}" alt="{user.username}">
                <h1>{portfolio.title}</h1>
                <p>{portfolio.tagline or ""}</p>
                <a href="https://github.com/{user.github_username}" target="_blank" class="github-link">
                    🐙 @{user.github_username} on GitHub
                </a>
            </div>
            <div class="projects-grid">
                {project_cards}
            </div>
            <div class="footer">
                Generated with Portfolio Generator
            </div>
        </div>
    </body>
    </html>
    """
    return html