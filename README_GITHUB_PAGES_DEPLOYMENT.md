# Deploying Annabelle's Website on GitHub Pages

Use this if adding the website to Annabelle's existing repository: `annabelle-z-li/AI-research-level-2`.

## Steps

1. Open the repository on GitHub.
2. Add the entire `docs/` folder from this kit at the root of the repo.
3. Commit the changes.
4. Go to **Settings → Pages**.
5. Under **Build and deployment**, choose:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
6. Save.
7. After GitHub builds the site, the public URL will usually be:

```text
https://annabelle-z-li.github.io/AI-research-level-2/
```

## Editing

The website is plain HTML/CSS/JavaScript. Annabelle can edit:

- `docs/index.html` for words and links;
- `docs/styles.css` for visual design;
- `docs/script.js` for the small interactive test-case cards.
