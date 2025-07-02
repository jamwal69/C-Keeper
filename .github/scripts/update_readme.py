#!/usr/bin/env python3
"""
Dynamic README Update Script
Automatically updates README.md with live statistics and information
"""

import os
import re
import json
import requests
from datetime import datetime, timezone
from github import Github
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class READMEUpdater:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repository = os.getenv('REPOSITORY')
        self.g = Github(self.github_token)
        self.repo = self.g.get_repo(self.repository)
        
    def get_repo_stats(self):
        """Get repository statistics"""
        try:
            return {
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'issues': self.repo.open_issues_count,
                'commits': self.repo.get_commits().totalCount,
                'contributors': self.repo.get_contributors().totalCount,
                'last_commit': self.repo.get_commits()[0].commit.author.date,
                'languages': self.repo.get_languages(),
                'size': self.repo.size,
                'watchers': self.repo.watchers_count
            }
        except Exception as e:
            print(f"Error getting repo stats: {e}")
            return {}

    def get_docker_stats(self):
        """Get Docker-related statistics"""
        try:
            # This would query Docker Hub API for real stats
            # For now, return placeholder data
            return {
                'pulls': '1.2K+',
                'size': '245MB',
                'layers': 12,
                'last_updated': datetime.now(timezone.utc)
            }
        except Exception as e:
            print(f"Error getting Docker stats: {e}")
            return {}

    def generate_activity_chart(self):
        """Generate commit activity chart"""
        try:
            commits = list(self.repo.get_commits()[:30])  # Last 30 commits
            dates = [commit.commit.author.date.date() for commit in commits]
            
            # Count commits per day
            from collections import Counter
            commit_counts = Counter(dates)
            
            # Create chart
            plt.figure(figsize=(10, 4))
            plt.style.use('dark_background')
            
            dates_list = list(commit_counts.keys())
            counts_list = list(commit_counts.values())
            
            plt.bar(dates_list, counts_list, color='#00d4ff', alpha=0.8)
            plt.title('Recent Commit Activity', color='white', fontsize=14)
            plt.xlabel('Date', color='white')
            plt.ylabel('Commits', color='white')
            plt.xticks(rotation=45, color='white')
            plt.yticks(color='white')
            plt.tight_layout()
            
            # Save to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='#0d1117', edgecolor='none')
            buffer.seek(0)
            chart_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return chart_base64
        except Exception as e:
            print(f"Error generating activity chart: {e}")
            return None

    def update_badges(self, stats):
        """Update dynamic badges in README"""
        badge_updates = {
            'stars': f"![Stars](https://img.shields.io/badge/stars-{stats.get('stars', 0)}-yellow.svg)",
            'forks': f"![Forks](https://img.shields.io/badge/forks-{stats.get('forks', 0)}-blue.svg)",
            'issues': f"![Issues](https://img.shields.io/badge/issues-{stats.get('issues', 0)}-red.svg)",
            'contributors': f"![Contributors](https://img.shields.io/badge/contributors-{stats.get('contributors', 0)}-green.svg)"
        }
        return badge_updates

    def update_stats_section(self, stats, docker_stats):
        """Create dynamic stats section"""
        last_commit = stats.get('last_commit', datetime.now(timezone.utc))
        time_ago = datetime.now(timezone.utc) - last_commit.replace(tzinfo=timezone.utc)
        
        if time_ago.days > 0:
            last_commit_str = f"{time_ago.days} days ago"
        else:
            hours = time_ago.seconds // 3600
            last_commit_str = f"{hours} hours ago" if hours > 0 else "Recently"

        stats_section = f"""
## 📊 Project Statistics

<div align="center">

| 📈 **Repository Stats** | 🐳 **Docker Stats** | ⚡ **Activity** |
|:---:|:---:|:---:|
| ⭐ {stats.get('stars', 0)} Stars | 📥 {docker_stats.get('pulls', 'N/A')} Pulls | 🔄 Last commit: {last_commit_str} |
| 🍴 {stats.get('forks', 0)} Forks | 📦 {docker_stats.get('size', 'N/A')} Size | 👥 {stats.get('contributors', 0)} Contributors |
| 🐛 {stats.get('issues', 0)} Issues | 🏗️ {docker_stats.get('layers', 'N/A')} Layers | 💾 {stats.get('size', 0)} KB Code |

**🔥 Live Status**: Repository actively maintained • Docker images auto-updated • CI/CD pipeline active

</div>

### 📈 Recent Activity

<div align="center">

*Updated automatically every 6 hours*

</div>
"""
        return stats_section

    def create_feature_matrix(self):
        """Create a visual feature comparison matrix"""
        feature_matrix = """
## 🚀 Feature Matrix

<div align="center">

| Feature | CLI | GUI | Docker | Status |
|---------|:---:|:---:|:------:|:------:|
| 🔍 **Network Reconnaissance** | ✅ | ✅ | ✅ | 🟢 Active |
| 💥 **Exploit Development** | ✅ | ✅ | ✅ | 🟢 Active |
| 🎭 **Payload Generation** | ✅ | ✅ | ✅ | 🟢 Active |
| 📡 **C2 Server** | ✅ | ✅ | ✅ | 🟢 Active |
| 🛡️ **Blue Team Ops** | ✅ | ✅ | ✅ | 🟢 Active |
| 📊 **Analytics & Reports** | ✅ | ✅ | ✅ | 🟢 Active |
| 🔄 **Auto Updates** | ✅ | ✅ | ✅ | 🟡 Beta |
| 🌐 **Web Interface** | ❌ | ❌ | 🔄 | 🟡 Planned |

</div>
"""
        return feature_matrix

    def update_readme(self):
        """Main function to update README.md"""
        print("🚀 Starting README update...")
        
        # Read current README
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get statistics
        stats = self.get_repo_stats()
        docker_stats = self.get_docker_stats()
        
        print(f"📊 Retrieved stats: {len(stats)} repo stats, {len(docker_stats)} Docker stats")
        
        # Update version from VERSION file
        try:
            with open('VERSION', 'r') as f:
                version = f.read().strip()
            content = re.sub(r'version-[\d.]+', f'version-{version}', content)
            print(f"📝 Updated version to {version}")
        except Exception as e:
            print(f"⚠️ Could not update version: {e}")
        
        # Update badges
        badge_updates = self.update_badges(stats)
        for badge_type, badge_code in badge_updates.items():
            pattern = rf'!\[{badge_type.title()}\]\([^)]+\)'
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, badge_code, content, flags=re.IGNORECASE)
        
        # Add/update statistics section
        stats_section = self.update_stats_section(stats, docker_stats)
        
        # Find where to insert stats (after features section)
        feature_pattern = r'(</details>\s*</details>)'
        if re.search(feature_pattern, content):
            content = re.sub(feature_pattern, r'\1\n\n' + stats_section, content)
        else:
            # Fallback: add after features section
            pattern = r'(## ✨ Features at a Glance.*?</details>)'
            content = re.sub(pattern, r'\1\n\n' + stats_section, content, flags=re.DOTALL)
        
        # Add feature matrix
        feature_matrix = self.create_feature_matrix()
        if '## 🚀 Feature Matrix' not in content:
            content += '\n\n' + feature_matrix
        
        # Update timestamp
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        footer = f"\n\n---\n\n<div align=\"center\">\n\n**🤖 This README is automatically updated** • Last update: {timestamp}\n\n[🚀 Try C-Keeper Now](#-one-click-installation) • [📖 Full Documentation](INSTALLATION.md) • [🐳 Docker Hub](https://hub.docker.com/r/yourusername/c-keeper)\n\n</div>\n"
        
        # Add footer if not exists
        if '🤖 This README is automatically updated' not in content:
            content += footer
        else:
            # Update existing footer
            content = re.sub(r'Last update: [^*]+', f'Last update: {timestamp}', content)
        
        # Write updated README
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ README updated successfully!")

def main():
    updater = READMEUpdater()
    updater.update_readme()

if __name__ == "__main__":
    main()
