# GitHub Issue Finder

A Python script to search for GitHub issues based on label, language, star count, and more. The results are displayed in an HTML page for easy viewing. 

## Features
- Search GitHub issues based on **label**, **language**, **minimum stars**, and **limit**.
- Results are displayed in a **dynamically generated HTML page**.
- Built with **Jekyll** to host the output on GitHub Pages.
- Customizable via workflow inputs for **label**, **language**, **stars**, and **limit**.

## Usage

### Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/sudouser777/github-issue-finder.git
   cd github-issue-finder
   ```

2. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```

3. Run the script with desired parameters:
   ```bash
   python src/app.py --label "good first issue" --language "python" --stars 10 --limit 100
   ```

4. The results will be saved in an `index.html` file.

### GitHub Actions
This project includes a GitHub Actions workflow that automatically generates the HTML page and deploys it to **GitHub Pages**.

The workflow can be triggered manually or automatically on push events to the `main` branch. You can specify the following inputs:
- **label**: GitHub issue label (default: "good first issue")
- **language**: Programming language (default: "java")
- **stars**: Minimum number of stars (default: 1)
- **limit**: Maximum number of issues to fetch (default: 500)

### Workflow Trigger
You can trigger the workflow through:
- **Push to `main` branch**.
- **Manual trigger** via GitHub UI (Workflow Dispatch).

### Setting up GitHub Pages
The script also integrates with Jekyll to host the generated HTML file on **GitHub Pages**. After running the workflow, the generated page will be accessible at:

[github-issue-finder](https://sudouser777.github.io/github-issue-finder/)


## Contributing
Feel free to fork this repository and submit pull requests for any improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
