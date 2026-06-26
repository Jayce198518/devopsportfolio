# Clickable Certificates with Image Thumbnails

## Goal
Make the certificates section in the portfolio interactive: each certificate card should be clickable and open a larger certificate image or PDF in a new tab, with a preview thumbnail displayed at the top of each card.

## Current State
- `index.html` contains a `.certs-grid` with 6 `.cert-card` elements.
- Cards display name, issuer/date, and a short note only.
- `profile.json` has a `certifications` array with an empty `certificate_url` field per entry.
- `generate_static.py` renders `profile.json` into `index.html`.
- `static/css/style.css` styles `.cert-card` but does not support images or link wrapping.

## Design

### 1. Image Storage
Certificate images/PDFs must be added to the repository so they are accessible when the site is deployed.

- **Location:** `static/images/certs/`
- **Naming convention:** lowercase, hyphenated filenames based on certificate name, e.g.:
  - `google-cloud-pcse.jpg`
  - `cloud-computing-security.jpg`
  - `on-demand-it-skills.jpg`
  - `devops-micro-internship.jpg`
  - `build-ai-agents-for-business.jpg`
  - `agentic-ai-devops-automation.jpg`

### 2. Data Model
Extend each certification entry in `profile.json`:

```json
{
  "name": "Google Cloud Certified — Professional Cloud Security Engineer",
  "issuer": "Google Cloud",
  "date": "2025",
  "note": "...",
  "certificate_url": "static/images/certs/google-cloud-pcse.jpg",
  "image": "static/images/certs/google-cloud-pcse.jpg"
}
```

- `certificate_url` / `image`: path to the certificate image or PDF.
- If `certificate_url` is empty, the card will not be wrapped in a link and will remain non-clickable until an image is provided.

### 3. Generator Update (`generate_static.py`)
Update `cert_card()` to:

1. Render an optional `<img>` thumbnail at the top of the card.
2. Wrap the entire `.cert-card` in an `<a>` element when `certificate_url` is present.
3. Add `target="_blank"` and `rel="noopener noreferrer"` to the link.
4. Keep existing border and date color logic.
5. Use a placeholder visual when no image is provided (a styled badge/icon area so the layout does not collapse).

HTML structure for linked cards:

```html
<a class="cert-card" href="static/images/certs/..." target="_blank" rel="noopener noreferrer" style="...">
  <div class="cert-thumb">
    <img src="static/images/certs/..." alt="Certificate: Name" loading="lazy">
  </div>
  <div class="cert-name">...</div>
  <div class="cert-date">...</div>
  <div class="cert-note">...</div>
</a>
```

HTML structure for unlinked cards (no image yet):

```html
<div class="cert-card" style="...">
  <div class="cert-thumb cert-thumb-placeholder">
    <span>📜</span>
  </div>
  <div class="cert-name">...</div>
  <div class="cert-date">...</div>
  <div class="cert-note">...</div>
</div>
```

### 4. CSS Updates (`static/css/style.css`)
Add styles for:

- `.cert-card` as an inline block with no underline and inherited color when it is an `<a>`.
- `.cert-thumb` container with fixed aspect ratio (e.g., 16:10), rounded top corners, overflow hidden, and subtle border.
- `.cert-thumb img` with `width: 100%; height: 100%; object-fit: cover;`.
- `.cert-thumb-placeholder` with a muted background, centered icon, and same aspect ratio.
- Hover state for the linked card: border color change plus a slight lift/shadow.
- Focus state for accessibility.

Example CSS:

```css
.cert-card {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}

.cert-thumb {
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
  margin-bottom: 0.75rem;
  background: var(--panel2);
}

.cert-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.25s ease, border-color 0.2s;
}

.cert-card:hover .cert-thumb img {
  transform: scale(1.03);
}

.cert-thumb-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--ghost2);
}
```

### 5. Regeneration
After updating `profile.json`, `generate_static.py`, and `style.css`, run:

```bash
python3 generate_static.py
```

This rebuilds `index.html` with the new certificate cards.

### 6. Responsive Behavior
- The existing `.certs-grid` is 3 columns on desktop, 2 on tablet, 1 on mobile.
- Thumbnails will scale with the card width and maintain the 16:10 ratio.

## Success Criteria
- [ ] Each certificate card with an image path is clickable.
- [ ] Clicking opens the certificate image/PDF in a new tab.
- [ ] Each card has a preview thumbnail area at the top.
- [ ] Cards without an image show a placeholder instead of a broken image.
- [ ] The site regenerates from `profile.json` without losing the changes.
- [ ] No new external dependencies are introduced.

## Open Questions / Next Steps for User
1. Copy certificate image/PDF files into `static/images/certs/`.
2. Update the `image`/`certificate_url` fields in `profile.json` with the actual filenames.
3. Re-run `generate_static.py` after adding images.
